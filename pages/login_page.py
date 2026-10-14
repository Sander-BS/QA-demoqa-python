from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input: Locator = self.page.get_by_placeholder('UserName')
        self.password_input: Locator = self.page.get_by_placeholder('Password')
        self.login_button: Locator = self.page.get_by_role('button', name='login')
        self.error_message: Locator = self.page.locator('#name')

    def open(self) -> None:
        self.navigate('/login')

    def fill_username(self, username: str) -> None:
        self.username_input.fill(username)

    def fill_password(self, password: str) -> None:
        self.password_input.fill(password)

    def click_login_button(self) -> None:
        self.login_button.click()

    def login(self, username: str, password: str) -> None:
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_button()
