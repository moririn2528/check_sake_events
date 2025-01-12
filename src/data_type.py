from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    event_id: str
    url: str
    title: str
    body: str
    links: list[str]
    address: str
