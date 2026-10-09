from elements.base_element import BaseElement
from helper.logger import log_message, LogLevel


class Button(BaseElement):
    @property
    def type_of(self) -> str:
        return "button"

    async def click(self, nth: int = 0, **kwargs):
        async with log_message(self.logger_debug, f'Clicking {self.type_of} "{self.name}"', LogLevel.DEBUG,
                         True,
                         0):
            locator = await self.get_locator(nth, **kwargs)
            await locator.click()
