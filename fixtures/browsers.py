from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, Page
from _pytest.fixtures import SubRequest
import allure
from config import settings, Browser
from pages.login_page import LoginPage


@asynccontextmanager
async def open_browser_page(browser_type: str, test_name: str, storage_state=None):
    async with async_playwright() as playwright:
        browser = await playwright[browser_type].launch(headless=settings.headless)
        context = await browser.new_context(base_url=settings.get_base_url(),
                                  record_video_dir=settings.videos_dir,
                                  storage_state=storage_state)
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()

        yield page

        await context.tracing.stop(path=settings.tracing_dir.joinpath(f'{test_name}.zip'))
        await browser.close()

        allure.attach.file(settings.tracing_dir.joinpath(f'{test_name}.zip'), name='trace', extension='zip')
        allure.attach.file(await page.video.path(), name='video', attachment_type=allure.attachment_type.WEBM)


@pytest.fixture(params=settings.browsers)
async def browser_page(request: SubRequest) -> Page:
    async with open_browser_page(request.param, request.node.name) as page:
        yield page


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def initialize_browser_state():
    async with async_playwright() as playwright:
        browser = await playwright[Browser.CHROMIUM].launch(headless=settings.headless)
        context = await browser.new_context(base_url=settings.get_base_url())
        page = await context.new_page()

        login_page = LoginPage(page)
        await login_page.visit("/login")
        await login_page.login(settings.test_user.email, settings.test_user.password)

        await context.storage_state(path=settings.browser_state_file)
        await browser.close()


@pytest.fixture(params=settings.browsers)
async def browser_page_with_state(initialize_browser_state, request: SubRequest) -> Page:
    async with open_browser_page(request.param, request.node.name,
                                 storage_state=settings.browser_state_file) as page:
        yield page
