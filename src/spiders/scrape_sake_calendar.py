import scrapy
from scrapy.http import TextResponse, Response

from src.items import EventItem, OtherItem
from src.filter import get_id_from_url


class ScrapeSakeCalendarSpider(scrapy.Spider):
    name = "scrape_sake_calendar"
    allowed_domains = ["nihonshucalendar.com"]
    start_urls = ["https://nihonshucalendar.com"]

    def parse(self, response: Response):
        if not isinstance(response, TextResponse):
            self.logger.log(f"not TextResponse {response.url}")
            return

        event = self.__parse_event(response)
        if event is not None:
            yield event
        else:
            yield OtherItem(url=response.url)

        # follow all links
        for link in response.css("a::attr(href)").getall():
            yield response.follow(link, callback=self.parse)

    def __parse_event(self, response: TextResponse) -> EventItem | None:
        event_id = get_id_from_url(response.url)
        if event_id is None:
            return None
        events = response.css("section div.col-md-10")
        if len(events) == 0:
            return None
        event = events[0]
        title = event.css("h1::text").get()
        if title is None:
            return None

        return EventItem(
            event_id=event_id,
            url=response.url,
            title=title.strip(),
        )
