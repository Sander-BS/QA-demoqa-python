import pytest
import uuid

from playwright.sync_api import Page

from api.account_api import AccountAPI
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from api.bookstore_api import BookStoreAPI
from pages.bookstore_page import BookStorePage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
    }


@pytest.fixture(scope="session")
def account_api(base_url: str):
    return AccountAPI(base_url)


@pytest.fixture(scope='function')
def api_user(account_api: AccountAPI):
    username = f'qa_user_{uuid.uuid4().hex[:8]}'
    password = 'Password123!'

    create_res = account_api.create_user(username, password)
    assert create_res.status_code == 201, f"Failed to create user: {create_res.text}"
    user_id = create_res.json()['userID']

    token_res = account_api.generate_token(username, password)
    assert token_res.status_code == 200, f"Failed to generate token: {token_res.text}"
    token = token_res.json()['token']

    user_data = {
        'user_id': user_id,
        'username': username,
        'password': password,
        'token': token,
    }

    yield user_data

    account_api.delete_user(user_id, token)


@pytest.fixture(scope='function')
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope='function')
def profile_page(page: Page) -> ProfilePage:
    return ProfilePage(page)


@pytest.fixture(scope='session')
def bookstore_api(base_url: str) -> BookStoreAPI:
    return BookStoreAPI(base_url)


@pytest.fixture(scope='function')
def bookstore_page(page: Page) -> BookStorePage:
    return BookStorePage(page)


@pytest.fixture(scope='function')
def user_with_book(api_user: dict, bookstore_api: BookStoreAPI) -> dict:
    response = bookstore_api.get_books()
    assert response.status_code == 200, f'Failed to fetch books: {response.text}'

    books = response.json()['books']
    first_book = books[0]
    isbn = first_book['isbn']
    title = first_book['title']

    add_res = bookstore_api.add_book(
        user_id=api_user['user_id'], isbn=isbn, token=api_user['token']
    )
    assert add_res.status_code == 201, f"Failed to add book: {add_res.text}"

    user_data = {**api_user, "isbn": isbn, "book_title": title}

    yield user_data

    bookstore_api.delete_all_books(api_user['user_id'], api_user['token'])
