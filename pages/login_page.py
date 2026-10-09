import re

from playwright.async_api import Page, expect

from pages.base_page import BasePage
from elements.input import Input
from elements.button import Button
from helper.logger import log_message, LogLevel


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = Input(page, "[data-testid='login-email']", "Email")
        self.password_input = Input(page, "[data-testid='login-password']", "Password")
        self.submit_button = Button(page, "[data-testid='login-submit']", "Log in")

    async def login(self, email: str, password: str):
        async with log_message(self.logger_debug, f'Logging in as "{email}"', LogLevel.DEBUG, True, 0):
            await self.email_input.fill(email)
            await self.password_input.fill(password, mask=True)
            await self.submit_button.click()
            await expect(self.page).to_have_url(re.compile(r"/events"))
