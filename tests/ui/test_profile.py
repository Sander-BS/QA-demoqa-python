from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from playwright.sync_api import expect


def test_added_book_visible_in_profile(
    login_page: LoginPage, profile_page: ProfilePage, user_with_book: dict
):
    login_page.open()
    login_page.login(user_with_book['username'], user_with_book['password'])

    expect(profile_page.logout_button).to_be_visible()

    book_link = profile_page.get_book_link(user_with_book['book_title'])
    expect(book_link).to_be_visible()


def test_delete_book_from_profile(
    login_page: LoginPage, profile_page: ProfilePage, user_with_book: dict
):
    login_page.open()
    login_page.login(user_with_book['username'], user_with_book['password'])

    expect(profile_page.logout_button).to_be_visible()

    profile_page.delete_book(user_with_book['book_title'])

    book_link = profile_page.get_book_link(user_with_book['book_title'])
    expect(book_link).not_to_be_visible()
