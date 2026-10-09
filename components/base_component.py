from playwright.async_api import Page, expect
import logging



class BaseComponent:
    def __init__(self, page: Page):
        self.page = page
        self.logger_info = logging.getLogger("InfoLogger")
        self.logger_debug = logging.getLogger("DebugLogger")

