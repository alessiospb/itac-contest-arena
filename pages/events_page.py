from playwright.async_api import Page

from pages.base_page import BasePage
from components.events_filters import EventsFilters
from components.events_list import EventsList
from elements.text import Text


class EventsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.title = Text(page, "h1", "Page title")
        self.filters = EventsFilters(page)
        self.events_list = EventsList(page)
