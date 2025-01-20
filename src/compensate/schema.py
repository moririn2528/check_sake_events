from typing import TypedDict, Optional
from dataclasses import dataclass
from datetime import datetime


class EventInfo(TypedDict):
    name: str
    address: Optional[str]
    datetime: str
    price: str


class Location(EventInfo):
    start: datetime


@dataclass(frozen=True)
class EventItem:
    event_id: str
    url: str
    title: str
    body: str
    address: str
    links: list[str]
