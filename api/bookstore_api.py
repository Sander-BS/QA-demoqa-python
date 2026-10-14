from requests import Response
from api.base_api import BaseAPI


class BookStoreAPI(BaseAPI):
    def get_books(self) -> Response:
        endpoint = '/BookStore/v1/Books'
        return self.get(endpoint)

    def add_book(self, user_id: str, isbn: str, token: str) -> Response:
        endpoint = '/BookStore/v1/Books'
        headers = {'Authorization': f'Bearer {token}'}
        payload = {'userId': user_id, 'collectionOfIsbns': [{'isbn': isbn}]}
        return self.post(endpoint, payload, headers)

    def delete_all_books(self, user_id: str, token: str) -> Response:
        endpoint = f'/BookStore/v1/Books?UserId={user_id}'
        headers = {'Authorization': f'Bearer {token}'}
        return self.delete(endpoint, headers)
