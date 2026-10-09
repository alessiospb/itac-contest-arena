import pytest
from pages.login_page import LoginPage
from pages.events_page import EventsPage
from playwright.async_api import Page

@pytest.fixture
async def login_page(browser_page: Page) -> LoginPage:
    return LoginPage(page=browser_page)

@pytest.fixture
async def events_page(browser_page_with_state: Page) -> EventsPage:
    return EventsPage(page=browser_page_with_state)
