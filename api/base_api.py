import requests


class BaseAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _get_full_url(self, endpoint: str) -> str:
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def post(
        self, endpoint: str, payload: dict = None, headers: dict = None
    ) -> requests.Response:
        url = self._get_full_url(endpoint)
        return self.session.post(url, json=payload, headers=headers)

    def get(
        self, endpoint: str, params: dict = None, headers: dict = None
    ) -> requests.Response:
        url = self._get_full_url(endpoint)
        return self.session.get(url, params=params, headers=headers)

    def delete(self, endpoint: str, headers: dict = None) -> requests.Response:
        url = self._get_full_url(endpoint)
        return self.session.delete(url, headers=headers)
