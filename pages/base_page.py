from playwright.async_api import Page
from helper.logger import log_message, LogLevel
import logging
class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger_debug = logging.getLogger("DebugLogger")
        self.logger_info = logging.getLogger("InfoLogger")
        self.logger = {"info": self.logger_info, "debug": self.logger_debug}

    async def visit(self, url: str):
        async with log_message(self.logger_debug,f'Opening the url "{url}"', LogLevel.DEBUG,True,0):
            await self.page.goto(url, wait_until='networkidle')