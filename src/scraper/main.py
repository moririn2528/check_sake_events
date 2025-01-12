from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from logging.config import fileConfig
import functions_framework
from flask import Request
from multiprocessing import Queue, Process
from logging import getLogger

from spiders.scrape_sake_world import ScrapeSakeWorldSpider
from const import ROOT_DIR


def crawl():
    settings = get_project_settings()
    getLogger().info(settings["CLOSESPIDER_PAGECOUNT"])
    process = CrawlerProcess(settings=settings)
    process.crawl(ScrapeSakeWorldSpider)
    process.start()


def crawlInFunction(queue: Queue):
    try:
        fileConfig(ROOT_DIR.joinpath("settings/logging.conf"))
        load_dotenv(dotenv_path=ROOT_DIR.joinpath("settings/.env"))
        crawl()
        queue.put(None)
    except Exception as e:
        queue.put(e)


@functions_framework.http
def crawlSakeEvents(_: Request):
    """HTTP Cloud Function.
    crawl して、Firestore にデータを保存する
    """
    queue = Queue()
    process = Process(target=crawlInFunction, args=(queue,))
    process.start()
    process.join()
    result = queue.get()
    if result is not None:
        raise result
    return "Done"


if __name__ == "__main__":
    fileConfig(ROOT_DIR.joinpath("settings/logging_local.conf"))
    load_dotenv(dotenv_path=ROOT_DIR.joinpath("settings/local.env"))
    crawl()
