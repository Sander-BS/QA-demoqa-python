from api.base_api import BaseAPI
from requests import Response


class AccountAPI(BaseAPI):
    def create_user(self, username: str, password: str) -> Response:
        endpoint = 'Account/v1/User'
        payload = {'userName': username, 'password': password}
        return self.post(endpoint, payload=payload)

    def generate_token(self, username: str, password: str) -> Response:
        endpoint = 'Account/v1/GenerateToken'
        payload = {'userName': username, 'password': password}
        return self.post(endpoint, payload=payload)

    def delete_user(self, user_id: str, token: str) -> Response:
        endpoint = f'Account/v1/User/{user_id}'
        headers = {'Authorization': f'Bearer {token}'}
        return self.delete(endpoint, headers=headers)
