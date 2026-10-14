from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_value: Locator = self.page.locator('#userName-value')
        self.logout_button: Locator = self.page.get_by_role('button', name='Logout')
        self.not_logged_in_label: Locator = self.page.locator('#notlogged-in-label')

    def open(self) -> None:
        self.navigate('/profile')

    def get_username_text(self) -> str:
        return self.username_value.inner_text()

    def get_book_link(self, title: str) -> Locator:
        return self.page.get_by_role('link', name=title)

    def delete_book(self, title: str) -> None:
        row = self.page.locator('tr', has_text=title)
        row.locator('span[id^="delete-record"]').click()
        self.page.locator('#closeSmallModal-ok').click()
