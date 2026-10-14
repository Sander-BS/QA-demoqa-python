from pages.base_page import BasePage
from playwright.sync_api import Page, Locator


class BookStorePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_box: Locator = page.locator('#searchBox')

    def open(self) -> None:
        self.navigate('/books')

    def search_book(self, title: str) -> None:
        self.search_box.fill(title)

    def get_book_link(self, title: str) -> Locator:
        return self.page.get_by_role('link', name=title)
