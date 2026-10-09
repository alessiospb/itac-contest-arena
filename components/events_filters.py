from playwright.async_api import Page

from components.base_component import BaseComponent
from elements.input import Input
from elements.select import Select
from helper.logger import log_message, LogLevel
from helper.events_api import is_events_list_response


class EventsFilters(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.search_input = Input(page, "[data-testid='events-search']", "Search events")
        self.category_select = Select(page, "#filter-category", "Category")
        self.city_select = Select(page, "#filter-city", "City")
        self.date_from_input = Input(page, "#filter-from", "Date from")
        self.date_to_input = Input(page, "#filter-to", "Date to")
        self.sort_select = Select(page, "[data-testid='events-sort']", "Sort")
        self.order_select = Select(page, "[data-testid='events-order']", "Order")

    async def search(self, text: str):
        await self.search_input.fill(text)

    async def filter_by(self, category: str = None, city: str = None, date_from: str = None, date_to: str = None):
        async with log_message(self.logger_debug, 'Applying events filters', LogLevel.DEBUG, True, 0):
            if category is not None:
                await self.category_select.select_option(category)
            if city is not None:
                await self.city_select.select_option(city)
            if date_from is not None:
                await self.date_from_input.fill(date_from)
            if date_to is not None:
                await self.date_to_input.fill(date_to)

    async def sort_by(self, field: str, order: str = "asc"):
        async with log_message(self.logger_debug, f'Sorting events by "{field}" "{order}"', LogLevel.DEBUG, True, 0):
            current_field = await (await self.sort_select.get_locator()).input_value()
            current_order = await (await self.order_select.get_locator()).input_value()
            if (current_field, current_order) == (field, order):
                return

            async with self.page.expect_response(
                    lambda response: is_events_list_response(response, sort=field, order=order)):
                await self.sort_select.select_option(field)
                await self.order_select.select_option(order)
