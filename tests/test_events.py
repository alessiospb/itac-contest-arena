import re

import pytest
from playwright.async_api import expect

from pages.events_page import EventsPage


async def test_events_page_displayed(events_page: EventsPage):
    await events_page.visit("/events")
    await events_page.title.check_have_text("Events")
    await events_page.events_list.check_visible()
    await events_page.events_list.check_events_count(5)


async def test_search_event_by_name(events_page: EventsPage):
    await events_page.visit("/events")
    await events_page.filters.search("Kickoff Night")
    await events_page.events_list.check_events_count(1)
    await events_page.events_list.card(0).check_title("Kickoff Night")


async def test_event_card_details(events_page: EventsPage):
    await events_page.visit("/events")
    card = events_page.events_list.card_by_title("Kickoff Night")
    await card.check_visible()
    await card.check_category("concert")
    await card.check_status("Ended")
    await card.check_lineup("The Flaky Tests")
    await card.check_venue("BDO Arena · Tel Aviv")
    await card.check_date("16/09/2026 20:30")
    await card.check_price("₪80.00")
    await card.seats_left.check_visible()


@pytest.mark.parametrize("order", ["asc", "desc"])
async def test_sort_by_price(events_page: EventsPage, order: str):
    await events_page.visit("/events")
    await events_page.filters.sort_by("price", order)
    await expect(events_page.page).to_have_url(re.compile(r"sort=price"))

    prices = await events_page.events_list.get_all_prices()

    expected = sorted(prices, reverse=(order == "desc"))
    assert prices == expected, f"Prices are not sorted {order}: {prices}"


async def test_last_page_pagination(events_page: EventsPage):
    await events_page.visit("/events")
    await events_page.events_list.go_to_last_page()
    await events_page.events_list.check_cards_match_pagination()


async def test_no_duplicate_events_between_pages(events_page: EventsPage):
    await events_page.visit("/events")
    events = await events_page.events_list.get_all_events()

    ids = [event_id for event_id, title in events]
    duplicates = sorted({title for event_id, title in events if ids.count(event_id) > 1})
    assert not duplicates, f"Events shown on more than one page: {duplicates}"


async def test_open_event(events_page: EventsPage):
    await events_page.visit("/events")
    await events_page.events_list.card(0).open()
    await expect(events_page.page).to_have_url(re.compile(r"/events/[\w-]+"))
