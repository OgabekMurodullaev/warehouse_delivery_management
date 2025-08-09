from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer


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