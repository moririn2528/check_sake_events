from scrapy.dupefilters import RFPDupeFilter
from scrapy.http.request import Request

from src.utils.parse_url import get_id_from_url


class DupeFilter(RFPDupeFilter):
    """同じサイトを参照しないようにする"""

    def request_fingerprint(self, request: Request) -> str:
        event_id = get_id_from_url(request.url)
        if event_id is not None:
            return event_id
        return super().request_fingerprint(request)
