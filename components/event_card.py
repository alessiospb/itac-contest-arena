from playwright.async_api import Page

from components.base_component import BaseComponent
from elements.text import Text
from elements.link import Link


class EventCard(BaseComponent):
    def __init__(self, page: Page, root: str):
        super().__init__(page)

        self.card = Text(page, root, "Event card")
        self.title = Text(page, f"{root} >> h2", "Event title")
        self.category = Text(page, f"{root} >> h2 + div", "Event category")
        self.status = Text(page, f"{root} >> h2 + div + div", "Event status")
        self.lineup = Text(page, f"{root} >> h2 >> xpath=../following-sibling::p[1]", "Event lineup")
        self.venue = Text(page, f"{root} >> p:has(svg) >> nth=0", "Event venue")
        self.date = Text(page, f"{root} >> p:has(svg) >> nth=1", "Event date")
        self.price = Text(page, f"{root} >> p:has-text('From')", "Event price")
        self.seats_left = Text(page, f"{root} >> p:has-text('seats left')", "Event seats left")
        self.view_link = Link(page, f"{root} >> a", "View event")

    async def check_visible(self):
        await self.card.check_visible()

    async def check_title(self, title: str):
        await self.title.check_have_text(title)

    async def check_category(self, category: str):
        await self.category.check_have_text(category)

    async def check_status(self, status: str):
        await self.status.check_have_text(status)

    async def check_lineup(self, lineup: str):
        await self.lineup.check_have_text(lineup)

    async def check_venue(self, venue: str):
        await self.venue.check_have_text(venue)

    async def check_date(self, date: str):
        await self.date.check_have_text(date)

    async def check_price(self, price: str):
        await self.price.check_have_text(f"From {price}")

    async def check_seats_left(self, seats: int):
        await self.seats_left.check_have_text(f"{seats} seats left")

    async def open(self):
        await self.view_link.click()
