from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from playwright.sync_api import expect


def test_successful_login(
    login_page: LoginPage, profile_page: ProfilePage, api_user: dict
):
    login_page.open()
    login_page.login(api_user['username'], api_user['password'])
    expect(profile_page.logout_button).to_be_visible()
    expect(profile_page.username_value).to_have_text(api_user['username'])


def test_login_invalid_password(login_page: LoginPage):
    login_page.open()
    login_page.login('non_existent_qa_user', 'WrongPassword123!')

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text('Invalid username or password!')
