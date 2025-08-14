import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestVerifyOTP:

    def test_verify_otp_success(self, api_client, create_user, create_otp):
        user = create_user()
        url = reverse('users:verify_code')
        otp_code = "123456"
        create_otp(user.email, otp_code, method="email")

        data = {
            "target": user.email,
            "method": "email",
            "code": otp_code
        }

        response = api_client.post(url, data)
        user.refresh_from_db()
        assert response.status_code == 200
        assert user.is_verified is True


