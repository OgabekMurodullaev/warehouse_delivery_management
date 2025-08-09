import random
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from users.models import VerificationCode


def _generate_code(length=6):
    start = 10 ** (length-1)
    end = (10**length)-1
    return str(random.randint(start, end))

def create_verification_code(target: str, method: str, user=None):
    length = settings.VERIFICATION.get('CODE_LENGTH', 6)
    exp_minutes = settings.VERIFICATION.get('EXPIRATION_MINUTES', 5)
    max_attempts = settings.VERIFICATION.get('MAX_ATTEMPTS', 5)

    code = _generate_code(length)
    vc = VerificationCode.objects.create(
        user=user,
        target=target,
        method=method,
        code=code,
        expires_at=timezone.now() + timedelta(minutes=exp_minutes),
        max_attempts=max_attempts
    )
    return vc

def send_verification_email(to_email: str, code: str):
    subject = "Tasdiqlash kodi"
    message = f"Sizning tasdiqlash kodingiz: {code}. Kod {settings.VERIFICATION.get('EXPIRATION_MINUTES', 5)} daqiqa amal qiladi"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
