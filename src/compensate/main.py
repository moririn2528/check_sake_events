import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import requests
from html2text import html2text
from urllib.parse import urlparse
from datetime import datetime
from typing import TypedDict, Annotated, Optional

from .schema import Location, EventItem, EventInfo
from .firestore import Firestore

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
low_model = genai.GenerativeModel("gemini-1.5-flash-8b")


class APILimitError(Exception):
    pass


def extract_info(item: EventItem) -> list[EventInfo]:
    details: list[str] = []
    for link in item.links:
        try:
            result = urlparse(link)
            if not all([result.scheme, result.netloc]):
                continue
        except Exception:
            continue
        response = requests.get(link)
        if 300 <= response.status_code:
            continue
        body = html2text(response.text)
        details.append(body)

    bodies = [item.body]
    for i, detail in enumerate(details):
        bodies.append(f"詳細ページ情報{i+1}: {detail}")
    body = "\n-----\n".join(bodies)
    print(item.title, item.url)
    try:
        res = model.generate_content(
            f"""日本酒に関するイベント情報が与えられる。
{'加えて、その詳細ページと思われる情報も与えられる。' if len(details)>0 else ''}
これらの情報からイベント名、開催場所の住所、開催日時、料金形態を抽出してください。記載されていない場合は出力しないでください。
イベント情報:
{body}""",
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=list[EventInfo]
            ),
        )
        return res.text
    except Exception as e:
        print("Error:", e)
        return []


class StartDate(TypedDict):
    start_datetime: str


def extract_start_date(duration: str) -> datetime:
    try:
        res = low_model.generate_content(
            f"""イベントの開催期間が与えられるので、そのイベントの開催開始日時を出力してください。
時間までわかる場合は yyyy-mm-ddTHH:MM の形式で、時間がわからないときは　yyyy-mm-dd で出力してください。
{duration}""",
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=StartDate
            ),
        )
        output = StartDate(**json.loads(res.text))
        return datetime.fromisoformat(output["start_datetime"])
    except Exception as e:
        print("Error:", e)
        return []


def extract_location(item: EventItem):
    info = extract_info(item)
    locations: list[Location] = []
    for e in info:
        locations.append(
            Location(
                name=e["name"],
                address=e["address"],
                start=extract_start_date(e["datetime"]),
                duration=e["datetime"],
                price=e["price"],
            )
        )
    return locations


def main():
    fs = Firestore()
    stream = fs.stream()
    try:
        for item in stream:
            locs = extract_location(item)
            fs.compensate(item.event_id, locs)
    except APILimitError:  # TODO: API LIMIT ERROR を raise するようにする
        print(
            "WARNING: API LIMIT EXCEEDED: you may execute this function after few minites"
        )


# サーバーのスタートや関数フローの開始
if __name__ == "__main__":
    # テスト用入力
    res = extract_start_date("2024年10月26日（土）10：00～15：00")
    print("result: ", res)
