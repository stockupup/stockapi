# -*- coding: utf-8 -*-
"""
# tom.li
# 2021/8/29
#
"""
import pymongo

from src.conf import MONGO_URL


def get_mongo_client():
    client = pymongo.MongoClient(MONGO_URL)
    return client
