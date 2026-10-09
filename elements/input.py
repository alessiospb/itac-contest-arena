from elements.base_element import BaseElement
from helper.logger import log_message, LogLevel


class Input(BaseElement):
    @property
    def type_of(self) -> str:
        return "input"

    async def fill(self, value: str, nth: int = 0, mask: bool = False, **kwargs):
        shown_value = "***" if mask else value
        async with log_message(self.logger_debug, f'Filling {self.type_of} "{self.name}" with value "{shown_value}"', LogLevel.DEBUG,
                         True,
                         0):
            locator = await self.get_locator(nth, **kwargs)
            await locator.fill(value)
