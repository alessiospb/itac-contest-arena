from playwright.async_api import expect

from elements.base_element import BaseElement
from helper.logger import log_message, LogLevel


class Select(BaseElement):
    @property
    def type_of(self) -> str:
        return "select"

    async def select_option(self, value: str, nth: int = 0, **kwargs):
        async with log_message(self.logger_debug, f'Selecting option "{value}" in {self.type_of} "{self.name}"', LogLevel.DEBUG,
                         True,
                         0):
            locator = await self.get_locator(nth, **kwargs)
            await locator.select_option(value)

    async def check_have_value(self, value: str, nth: int = 0, **kwargs):
        async with log_message(self.logger_debug, f'Checking that {self.type_of} "{self.name}" has value "{value}"', LogLevel.DEBUG,
                         True,
                         0):
            locator = await self.get_locator(nth, **kwargs)
            await expect(locator).to_have_value(value)
