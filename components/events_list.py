import json
import re

from playwright.async_api import Page, expect

from components.base_component import BaseComponent
from components.event_card import EventCard
from elements.text import Text
from elements.button import Button
from helper.logger import log_message, LogLevel
from helper.events_api import is_events_list_response


class EventsList(BaseComponent):
    CARD = "[data-testid='event-card']"

    def __init__(self, page: Page):
        super().__init__(page)

        self.list = Text(page, "[data-testid='events-list']", "Events list")
        self.event_card = Text(page, self.CARD, "Event card")
        self.event_title = Text(page, f"{self.CARD} h2", "Event title")
        self.event_price = Text(page, f"{self.CARD} p:has-text('From')", "Event price")

        self.pagination_info = Text(page, "[data-testid='pagination-info']", "Pagination info")
        self.prev_button = Button(page, "[data-testid='pagination-prev']", "Previous page")
        self.next_button = Button(page, "[data-testid='pagination-next']", "Next page")

    def card(self, nth: int = 0) -> EventCard:
        return EventCard(self.page, f"{self.CARD} >> nth={nth}")

    def card_by_title(self, title: str) -> EventCard:
        return EventCard(self.page, f"{self.CARD}:has(h2:text-is({json.dumps(title)}))")

    async def check_visible(self):
        await self.list.check_visible()

    async def check_events_count(self, count: int):
        await self.event_card.check_count(count)

    async def next_page(self):
        start, end, total = await self.get_pagination_range()
        async with self.page.expect_response(is_events_list_response):
            await self.next_button.click()
        pagination_locator = await self.pagination_info.get_locator()
        await expect(pagination_locator).to_contain_text(f"Showing {end + 1}")
        await self.event_card.check_visible()

    async def go_to_last_page(self):
        async with log_message(self.logger_debug, 'Going to the last page', LogLevel.DEBUG, True, 0):
            await self.event_card.check_visible()
            start, end, total = await self.get_pagination_range()
            while end < total:
                await self.next_page()
                start, end, total = await self.get_pagination_range()

    async def check_cards_match_pagination(self):
        start, end, total = await self.get_pagination_range()
        await self.check_events_count(end - start + 1)

    async def prev_page(self):
        await self.prev_button.click()

    async def get_prices_on_page(self) -> list[float]:
        texts = await self.event_price.get_all_texts()
        return [float(re.search(r"[\d,]+\.?\d*", text).group().replace(",", "")) for text in texts]

    async def get_pagination_range(self) -> tuple[int, int, int]:
        text = await self.pagination_info.get_text()
        start, end, total = map(int, re.findall(r"\d+", text))
        return start, end, total

    async def get_events_on_page(self) -> list[tuple[str, str]]:
        ids = await self.event_card.get_all_attributes("data-event-id")
        titles = await self.event_title.get_all_texts()
        return list(zip(ids, titles))

    async def collect_from_all_pages(self, get_on_page) -> list:
        await self.event_card.check_visible()
        items = await get_on_page()
        start, end, total = await self.get_pagination_range()
        while end < total:
            await self.next_page()
            items += await get_on_page()
            start, end, total = await self.get_pagination_range()
        return items

    async def get_all_prices(self) -> list[float]:
        async with log_message(self.logger_debug, 'Collecting prices from all pages', LogLevel.DEBUG, True, 0):
            return await self.collect_from_all_pages(self.get_prices_on_page)

    async def get_all_events(self) -> list[tuple[str, str]]:
        async with log_message(self.logger_debug, 'Collecting events from all pages', LogLevel.DEBUG, True, 0):
            return await self.collect_from_all_pages(self.get_events_on_page)
