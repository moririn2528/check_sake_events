from typing import TypedDict, Optional
from dataclasses import dataclass


class Event(TypedDict):
    name: str
    address: Optional[str]
    datetime: str
    price: str


@dataclass(frozen=True)
class EventItem:
    event_id: str
    url: str
    title: str
    body: str
    address: str
    links: list[str]
