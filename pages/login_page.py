import allure
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input: Locator = self.page.get_by_placeholder('UserName')
        self.password_input: Locator = self.page.get_by_placeholder('Password')
        self.login_button: Locator = self.page.get_by_role('button', name='login')
        self.error_message: Locator = self.page.locator('#name')

    @allure.step('Открыть страницу авторизации')
    def open(self) -> None:
        self.navigate('/login')

    @allure.step('ВВести имя пользователя: {username}')
    def fill_username(self, username: str) -> None:
        self.username_input.fill(username)

    @allure.step('Ввести пароль')
    def fill_password(self, password: str) -> None:
        self.password_input.fill(password)

    @allure.step('Нажать кнопку "Login"')
    def click_login_button(self) -> None:
        self.login_button.click()

    @allure.step('Выполнить авторизацию под пользователем: {username}')
    def login(self, username: str, password: str) -> None:
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_button()
