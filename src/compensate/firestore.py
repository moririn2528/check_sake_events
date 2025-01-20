from google.cloud import firestore
import os

from .schema import EventItem, Location


class Firestore:
    _db: firestore.Client | None = None
    _ids: list[str] | None = None

    @property
    def db(self) -> firestore.Client:
        if Firestore._db is None:
            Firestore._db = firestore.Client(project=os.getenv("PROJECT_ID"))
        return Firestore._db

    def stream(self):
        q = self.db.collection("events").where("status", "==", "SCRAPED")
        for snap in q.stream():
            data: dict = snap.to_dict()
            yield EventItem(
                event_id=snap.id,
                url=data["url"],
                title=data["title"],
                body=data["body"],
                address=data["address"],
                links=data["links"],
            )

    def compensate(self, id: str, info: list[Location]):
        event_doc = self.db.collection("events").document(id)
        col: firestore.CollectionReference = event_doc.collection("location")
        for loc in info:
            col.add(loc)
        event_doc.update({"state": "FULFILLED"})
