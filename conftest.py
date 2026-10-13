import pytest
import uuid
from api.account_api import AccountAPI


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
def account_api():
    return AccountAPI('https://demoqa.com')


@pytest.fixture(scope='function')
def api_user(account_api: AccountAPI):
    username = f'qa_user_{uuid.uuid4().hex[:8]}'
    password = 'Password123!'

    create_res = account_api.create_user(username, password)
    assert create_res.status_code == 201
    user_id = create_res.json()['userID']

    token_res = account_api.generate_token(username, password)
    assert token_res.status_code == 200
    token = token_res.json()['token']

    user_data = {
        'user_id': user_id,
        'username': username,
        'password': password,
        'token': token,
    }

    yield user_data

    account_api.delete_user(user_id, token)
