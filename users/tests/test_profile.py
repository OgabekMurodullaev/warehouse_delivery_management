import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestProfile:
    def test_retrieve_profile(self, api_client, create_user):
        user = create_user()
        url = reverse('users:profile')
        api_client.force_authenticate(user)
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["data"]["user"]["is_verified"] == user.is_verified

    def test_update_profile(self, api_client, create_user):
        user = create_user()
        url = reverse('users:profile')
        api_client.force_authenticate(user)

        payload = {
            "first_name": "Ogabek"
        }

        response = api_client.patch(url, payload)
        assert response.status_code == 200
        assert response.data["data"]["first_name"] == "Ogabek"
