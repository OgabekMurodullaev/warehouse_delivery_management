import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestAuth:
    def test_register_success(self, api_client):
        url = reverse('users:register')
        payload = {
            'email': 'newuser@gmail.com',
            'password': 'pass1223'
        }

        response = api_client.post(url, payload)
        assert response.status_code == 201

    def test_login_success(self, api_client, create_user):
        user = create_user()
        url = reverse('users:login')
        payload = {
            "email": user.email,
            "password": "Bek31040"
        }

        response = api_client.post(url, payload)
        assert "access" in response.data
        assert response.status_code == 200

    def test_verify_otp_success(self, api_client, create_user):
        # Bunda testdan oldin OTP code yaratish kerak bo‘ladi
        user = create_user(is_verified=False)
        # OTP yaratish mantiqini fixture orqali qo‘shamiz
        pass  # keyin to‘ldiramiz

    def test_send_otp_throttle(self, api_client, create_user):
        user = create_user()
        url = reverse('users:send_code')
        api_client.force_authenticate(user)
        payload = {
            "email": user.email
        }

        response1 = api_client.post(url, payload)
        response2 = api_client.post(url, payload)
        assert response2.status_code == 429