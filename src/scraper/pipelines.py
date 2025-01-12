# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from items import EventItem
from const import ROOT_DIR

from utils.firestore import Firestore
from utils.memory import gc_collect


class FirestorePipeline:
    @gc_collect
    def process_item(self, item: EventItem, spider):
        firestore = Firestore()
        firestore.setItem(item)
        return item
