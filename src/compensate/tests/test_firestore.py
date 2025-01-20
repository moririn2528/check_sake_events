# 以下のコマンドを必ず打つこと
# gcloud beta emulators firestore start --host-port=localhost:8596
import os
from google.cloud import firestore
import pytest
from datetime import datetime

from ..firestore import Firestore
from ..schema import Location


@pytest.fixture(scope="module", autouse=True)
def setup_firestore():
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8596"
    Firestore._db = firestore.Client()


def test_firestore():
    fs = Firestore()
    db = fs.db
    ref = db.collection("events").document("dummy")
    ref.set(
        {
            "address": "address_value",
            "url": "url_value",
            "title": "title_value",
            "body": "body_value",
            "links": ["link1", "link2"],
            "status": "SCRAPED",
        }
    )

    items = [item for item in fs.stream()]
    assert len(items) == 1
    for item in items:
        assert item.event_id == "dummy"
        assert item.url == "url_value"
        assert item.title == "title_value"
        assert item.body == "body_value"
        assert item.address == "address_value"
        assert item.links == ["link1", "link2"]

    fs.compensate(
        "dummy",
        [
            {
                "name": "name",
                "address": "address1",
                "start": datetime(2024, 10, 26, 10, 0, 0),
                "duration": "2024年10月26日（土）10：00～15：00",
                "price": "price",
            },
            {
                "name": "name",
                "address": "address2",
                "start": datetime(2024, 10, 27, 11, 0, 0),
                "duration": "2024年10月27日（日）11：00～15：00",
                "price": "price",
            },
        ],
    )
