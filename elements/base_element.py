from playwright.async_api import Page, Locator, expect
from helper.logger import log_message, LogLevel
import logging
import json

class BaseElement:
    def __init__(self, page: Page, locator: str, name: str):
        self.page = page
        self.name = name
        self.locator = locator
        self.logger_debug = logging.getLogger("DebugLogger")

    @property
    def type_of(self) -> str:
        return "base element"

    async def get_locator(self, nth: int = 0, **kwargs) -> Locator:
        locator = self.locator.format(**kwargs)
        async with log_message(self.logger_debug,f'Getting locator with "{locator}" at index "{nth}"', LogLevel.DEBUG,True,0):
            return self.page.locator(locator).nth(nth)


    async def check_have_text(self, text: str, nth: int = 0, **kwargs):
        async with log_message(self.logger_debug, f'Checking that {self.type_of} "{self.name}" has text "{text}"', LogLevel.DEBUG,
                         True,
                         0):
            locator = await self.get_locator(nth, **kwargs)
            await expect(locator).to_have_text(text)

    async def get_text(self, nth: int = 0, **kwargs) -> str:
        async with log_message(self.logger_debug, f'Getting text of {self.type_of} "{self.name}"', LogLevel.DEBUG,
                         True,
                         0):
            locator = await self.get_locator(nth, **kwargs)
            return await locator.inner_text()

    async def get_all_texts(self, **kwargs) -> list[str]:
        async with log_message(self.logger_debug, f'Getting texts of all {self.type_of} "{self.name}"', LogLevel.DEBUG,
                         True,
                         0):
            locator = self.page.locator(self.locator.format(**kwargs))
            return await locator.all_inner_texts()

    async def get_all_attributes(self, attribute: str, **kwargs) -> list[str]:
        async with log_message(self.logger_debug, f'Getting "{attribute}" of all {self.type_of} "{self.name}"', LogLevel.DEBUG,
                         True,
                         0):
            locator = self.page.locator(self.locator.format(**kwargs))
            return await locator.evaluate_all(f"elements => elements.map(e => e.getAttribute({json.dumps(attribute)}))")

    async def check_visible(self, nth: int = 0, **kwargs):
        async with log_message(self.logger_debug, f'Checking that {self.type_of} "{self.name}" is visible', LogLevel.DEBUG,
                         True,
                         0):
            locator = await self.get_locator(nth, **kwargs)
            await expect(locator).to_be_visible()

    async def check_count(self, count: int, **kwargs):
        async with log_message(self.logger_debug, f'Checking that {self.type_of} "{self.name}" count is "{count}"', LogLevel.DEBUG,
                         True,
                         0):
            locator = self.page.locator(self.locator.format(**kwargs))
            await expect(locator).to_have_count(count)


