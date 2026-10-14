from pages.bookstore_page import BookStorePage
from playwright.sync_api import expect


def test_search_book(bookstore_page: BookStorePage):
    book_title = 'Git Pocket Guide'
    bookstore_page.open()
    bookstore_page.search_book(book_title)

    expect(bookstore_page.get_book_link(book_title)).to_be_visible()
