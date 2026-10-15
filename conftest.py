import os
import allure
import pytest
import uuid
from dotenv import load_dotenv
from playwright.sync_api import Page, BrowserContext
from api.account_api import AccountAPI
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from api.bookstore_api import BookStoreAPI
from pages.bookstore_page import BookStorePage
from utils.telegram_notifier import send_telegram_notification

load_dotenv()


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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)


@pytest.fixture(scope='function', autouse=True)
def attach_artifacts_on_failure(request, page: Page, context: BrowserContext):
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield

    failed = (
        request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False
    )

    if failed:
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name=f'failed_screenshot_{request.node.name}',
            attachment_type=allure.attachment_type.PNG,
        )

        trace_path = f'allure-results/trace_{request.node.name}.zip'
        context.tracing.stop(path=trace_path)
        allure.attach.file(
            trace_path,
            name=f'playwright_trace_{request.node.name}',
            attachment_type='application/zip',
            extension='.zip',
        )
    else:
        context.tracing.stop()


def pytest_sessionfinish(session, exitstatus):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        print(
            '\n[INFO] Telegram notification skipped: TELEGRAM_BOT_TOKEN or'
            ' TELEGRAM_CHAT_ID not provided.'
        )
        return

    passed = session.testscollected - session.testsfailed
    failed = session.testsfailed

    status_icon = '✅' if failed == 0 else '❌'
    message = (
        f'<b>{status_icon} Результаты прогона автотестов DemoQA</b>\n\n'
        f'<b>Всего тестов:</b> {session.testscollected}\n'
        f'<b>Успешно:</b> {passed}\n'
        f'<b>Упало:</b> {failed}\n'
    )

    send_telegram_notification(token=token, chat_id=chat_id, message=message)
