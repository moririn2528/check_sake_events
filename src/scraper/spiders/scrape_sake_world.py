import scrapy
from scrapy.http import TextResponse, Response
import gc

from items import EventItem
from utils.parse_url import get_id_from_world_url
from utils.firestore import Firestore
from utils.memory import gc_collect
from logging import getLogger


def get_item(dic: dict[str, str], keys: list[str], default_value: str = "") -> str:
    for key in keys:
        if key in dic:
            return dic[key]
    return default_value


class ScrapeSakeWorldSpider(scrapy.Spider):
    name = "scrape_sake_world"
    allowed_domains = ["sakeworld.jp"]
    start_urls = ["https://sakeworld.jp/event"]

    @gc_collect
    def parse(self, response: Response):
        logger = getLogger(__name__)
        logger.debug("parse: %s", response.url)
        if not isinstance(response, TextResponse):
            self.logger.log(f"not TextResponse {response.url}")
            return
        firestore = Firestore()

        for event in response.css("div.arccont_main article.arcsec_list_item"):
            url = event.css("a.arcsec_list_item_img::attr(href)").get()
            if url is None:
                continue
            event_id = get_id_from_world_url(url)
            if event_id in firestore.getAllIds():
                continue
            # logger.debug("follow: %s", url)
            yield response.follow(url, callback=self.parse_event, priority=10)

        next_page = response.css("div.arcsec_pager li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    @gc_collect
    def parse_event(self, response: Response):
        if not isinstance(response, TextResponse):
            self.logger.log(f"not TextResponse {response.url}")
            return

        event_id = get_id_from_world_url(response.url)
        article = response.css("div.artcont_main")
        info_article = article.css("div.cont_info_list")
        body = article.css("*::text").getall()
        info: dict[str, str] = {}
        for col in info_article.css("dl.cont_info_list_item"):
            key = col.css("dt.cont_info_list_item_ttl::text").get()
            value = col.css("dd.cont_info_list_item_desc::text").get()
            if key is None or value is None:
                continue
            info[key] = value
        head_title = response.css("div.pagehead_txt h1.pagehead_txt_ttl::text").get("")

        yield EventItem(
            event_id=event_id,
            url=response.url,
            title=get_item(info, ["名称", "イベント名"], head_title),
            body="\n".join(body),
            address=get_item(info, ["会場", "開催場所", "場所"]),
            links=article.css("div.cont_editor a::attr(href)").getall(),
        )
