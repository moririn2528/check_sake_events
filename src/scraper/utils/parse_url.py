from urllib.parse import urlparse, parse_qs, ParseResult
from logging import getLogger


def get_id_from_calendar_url(url: str) -> str | None:
    parsed_url: ParseResult = urlparse(url)
    if "show_event" not in parsed_url.path:
        return None
    query_params = parse_qs(parsed_url.query)
    if "id" not in query_params or len(query_params["id"]) == 0:
        return None
    event_id = query_params["id"][0]
    index = event_id.find("_")
    if index != -1:
        event_id = event_id[:index]
    return event_id


def get_id_from_world_url(url: str) -> str | None:
    parsed_url: ParseResult = urlparse(url)
    path_comp = parsed_url.path.split("/")
    if path_comp[-1] == "":
        path_comp.pop()
    return path_comp[-1]
