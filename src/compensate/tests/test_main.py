import pytest
import json

from ..schema import EventItem
from ..main import search_info, extract_start_date


def test_extract_info():
    with open("output.json", "r", encoding="utf-8") as f:
        inputs = json.load(f)
    events: list[EventItem] = []
    for event in inputs:
        events.append(EventItem(**event))
    results = search_info(events[2])
    assert len(results) > 0
    print("Results:", results)
    # Results: [{"address": "京都市伏見区紙子屋町554-1", "datetime": "2024年10月26日（土）10：00～15：00", "name": "キンシ正宗 秋の蔵開き", "price": "入場無料・予約不要（試飲等には別途料金要）"}, {"address": "京都市伏見区舞台町16", "datetime": "2024年10月26日（土）10：00～15：00", "name": "招德蔵開き", "price": "入場無料・予約不要（試飲等には別途料金要）"}, {"address": "京都市伏見区村上町370-6", "datetime": "2024年10月26日（土）10：00～15：00", "name": "北川本家 富翁 新酒祭", "price": "入場無料・予約不要（試飲等には別途料金要）、きき酒券 4枚綴り 1000円"}, {"address": "京都市伏見区横大路三栖山城屋敷町105", "datetime": "2024年10月26日（土）10：00～15：00", "name": "英勲 蔵開き2024 秋", "price": "入場無料・予約不要（試飲等には別途料金要）"}]


def test_extract_date():
    res = extract_start_date("2024年10月26日（土）10：00～15：00")
    assert res.isoformat() == "2024-10-26T10:00:00"
