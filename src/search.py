from typing import Dict, List
from uuid import UUID
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders import SpiderLoader
from langchain_core.messages import HumanMessage, SystemMessage
from dataclasses import dataclass
import requests
from html2text import html2text
from langchain_core.callbacks import StdOutCallbackHandler, BaseCallbackHandler
import json
from dotenv import load_dotenv
from logging import FileHandler, getLogger, Formatter
from typing import Any

from const import ROOT_DIR


@dataclass(frozen=True)
class EventItem:
    event_id: str
    url: str
    title: str
    body: str
    links: list[str]


class Event(BaseModel):
    """出力されるイベント情報"""

    name: str | None = Field(
        description="イベント名", example="岐阜の地酒に酔う2024in大阪"
    )
    address: str | None = Field(
        description="開催場所の住所", example="大阪市中央区本町橋2番5号"
    )
    datetime: str | None = Field(description="開催日時", example="2024/8/10(土)")
    fee: str | None = Field(description="料金", example="3500円")


class FileLogHandler(BaseCallbackHandler):
    def __init__(self):
        self.logger = getLogger(__name__)

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any,
    ):
        self.logger.info(f"Starting LLM with prompts: {prompts}")

    def on_llm_end(
        self,
        outputs: List[str],
        **kwargs: Any,
    ):
        self.logger.info(f"LLM outputs: {outputs}")


def extract_titles(event: EventItem):
    log_handler = FileLogHandler()
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        timeout=None,
        max_retries=2,
        callbacks=[log_handler],
    )

    details: list[str] = []
    for link in event.links:
        response = requests.get(link)
        if 300 <= response.status_code:
            continue
        body = html2text(response.text)
        details.append(body)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "日本酒に関するイベント情報が与えられる。{}これらの情報からイベント名、開催場所の住所、開催日時、料金形態を抽出してください。記載されていない場合は出力しないでください。".format(
                    "加えて、その詳細ページと思われる情報も与えられる。"
                    if len(details) > 0
                    else ""
                ),
            ),
            ("human", "情報: {body}"),
        ]
    )
    bodies = [event.body]
    for i, detail in enumerate(details):
        bodies.append(f"詳細ページ情報{i+1}: {detail}")

    runnable = prompt | llm.with_structured_output(schema=Event)
    data: Event = runnable.invoke({"body": "\n-----\n".join(bodies)})
    print(event.title, event.url)
    print(data)


def embody_events():
    with open(ROOT_DIR.joinpath("output.json"), "r", encoding="utf8") as f:
        inputs = json.load(f)
    events: list[EventItem] = []
    for event in inputs:
        if "event_id" not in event:
            continue
        events.append(EventItem(**event))

    extract_titles(events[0])
    # for event in events:
    #     extract_titles(event)


if __name__ == "__main__":
    load_dotenv()
    embody_events()
