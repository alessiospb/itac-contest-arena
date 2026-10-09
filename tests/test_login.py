import re

from playwright.async_api import Page, expect

from config import settings
from pages.login_page import LoginPage


async def test_login(login_page: LoginPage):
    await login_page.visit("/login")
    await login_page.login(settings.test_user.email, settings.test_user.password)


async def test_events_open_for_logged_in_user(browser_page_with_state: Page):
    await browser_page_with_state.goto("/events")
    await expect(browser_page_with_state).to_have_url(re.compile(r"/events"))
