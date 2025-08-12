from django.conf import settings
from ipware import get_client_ip
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser, VerificationCode
from users.rate_limit import increment_global_day, check_and_increment_ip, check_and_increment_target
from users.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, SendCodeSerializer, VerifyCodeSerializer
from users.utils import create_verification_code, send_verification_email


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Ro'yxatdan o'tish muvaqqiyatli",
                "data": serializer.data
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SendCodeSerializer

    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        phone = serializer.validated_data.get('phone_number')

        # get client IP (fallback to request.META)
        client_ip, is_routable = get_client_ip(request)
        client_ip = client_ip or request.META.get('REMOTE_ADDR', 'unknown')

        # Global daily limit
        day_count = increment_global_day()
        if settings.VERIFICATION.get('GLOBAL_DAILY_LIMIT') and day_count > settings.VERIFICATION['GLOBAL_DAILY_LIMIT']:
            return Response({"detail": "Global daily limit reached"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # IP rate-limit
        ok, reason = check_and_increment_ip(client_ip)
        if not ok:
            return Response({"detail": "Too many requests from this IP. Try later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)


        if email:
            target = email.lower()
            ok, reason = check_and_increment_target(target)
            if not ok:
                if reason == "CooldownActive":
                    return Response({"detail": f"Please wait {settings.VERIFICATION.get('RESEND_COOLDOWN_SECONDS')} seconds before resending"},
                                    status=status.HTTP_429_TOO_MANY_REQUESTS)
                return Response({"detail": "Hourly limit for this email reached."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            user = CustomUser.objects.filter(email=target).first()
            # Invalidate previous active codes for this target (optional)
            VerificationCode.objects.filter(target=target, is_used=False).update(is_used=True)

            vc = VerificationCode.objects.create(target=target, method=VerificationCode.Methods.EMAIL, user=user)
            try:
                send_verification_email(target, vc.code)
            except Exception as e:
                return Response({"detail": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"detail": "Verification code sent to email"}, status=status.HTTP_200_OK)

        if phone:
            user = None
            try:
                user = CustomUser.objects.get(phone_number=phone)
            except user.DoesNotExist:
                user = None

            vc = create_verification_code(target=phone, method=VerificationCode.Methods.PHONE, user=user)
            send_verification_email(user.email, vc.code)
            return Response({"detail": "Tasdiqlash kodi emailingizga yuborildi"}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target = serializer.validated_data.get('target')
        method = serializer.validated_data.get('method')
        code = serializer.validated_data.get('code')

        try:
            vc = VerificationCode.objects.filter(target=target, method=method, is_used=False).latest('created_at')
        except VerificationCode.DoesNotExist:
            return Response({"detail": "Kod topilmadi yoki allaqachon ishlatilgan"}, status=status.HTTP_400_BAD_REQUEST)

        if vc.is_expired():
            return Response({"detail": "Kod muddati tugagan"}, status=status.HTTP_400_BAD_REQUEST)

        if vc.attempts > vc.max_attempts:
            return Response({"detail": "Urinishlar soni tugadi"}, status=status.HTTP_400_BAD_REQUEST)

        if code != vc.code:
            vc.attempts += 1
            vc.save(update_fields=['attempts'])
            return Response({"detail": "Kiritilgan kod xato qaytadan urining"}, status=status.HTTP_400_BAD_REQUEST)

        # success
        vc.mark_used()
        if vc.user:
            vc.user.is_verified = True
            vc.user.save(update_fields=['is_verified'])
            return Response({"detail": "Tasdiqlandi. Foydalanuvchi tasdiqlandi"}, status=status.HTTP_200_OK)
        return Response({"detail": "Kod tasdiqlandi"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if not user.is_verified:
                return Response({
                    "message": "Sms kod orqali hisobingiz tasdiqlanmagan"},
                    status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            data = {"message": "Login amalga oshirildi",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)}
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        data = {
            "message": "Profil ma'lumotlaringiz",
            "data": serializer.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = ProfileSerializer(instance=request.user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Profil ma'lumotlaringiz yangilandi",
                "data": serializer.data
            }
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)