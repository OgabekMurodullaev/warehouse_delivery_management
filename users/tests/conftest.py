import pytest
from rest_framework.test import APIClient

from users.models import CustomUser, VerificationCode


@pytest.fixture()
def api_client():
    return APIClient()

@pytest.fixture()
def create_user(db):
    def make_user(**kwargs):
        data = {
            "email": "ogabek@mail.ru",
            "phone_number": "+998973172306",
            "password": "Bek31040",
            "is_verified": False
        }

        data.update(**kwargs)
        return CustomUser.objects.create_user(**data)
    return make_user

@pytest.fixture()
def create_otp(db):
    def make_otp(user, target, code="123456", **kwargs):
        defaults = {
            "user": user,
            "target": target,
            "code": code,
            "is_used": False
        }

        defaults.update(**kwargs)
        return VerificationCode.objects.create(**defaults)
    return make_otp