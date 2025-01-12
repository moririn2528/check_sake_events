from google.cloud import firestore
import os

from items import EventItem


class Firestore:
    _db: firestore.Client | None = None
    _ids: list[str] | None = None

    @property
    def db(self) -> firestore.Client:
        if Firestore._db is None:
            Firestore._db = firestore.Client(project=os.getenv("PROJECT_ID"))
        return Firestore._db

    def setItem(self, item: EventItem):
        doc = self.db.collection("events").document(item["event_id"])
        _ = doc.set(
            {
                "address": item["address"],
                "url": item["url"],
                "title": item["title"],
                "body": item["body"],
                "links": item["links"],
            }
        )

    def getAllIds(self):
        if self._ids is None:
            self._ids = [doc.id for doc in self.db.collection("events").get()]
        return self._ids
