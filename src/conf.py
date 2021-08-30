# -*- coding: utf-8 -*-
"""
# tom.li
# 2021/8/29
#
"""

# Mongo 相关: 使用内网
MONGO_HOST = "127.0.0.1"
MONGO_PORT = "27017"
MONGO_DATABASE = "stock"
MONGO_URL = "mongodb://{}:{}".format(MONGO_HOST, MONGO_PORT)

COLLECTION_STOCK = "stock"
COLLECTION_STOCK_MARKET = "stock_market"
COLLECTION_HOLDER = "holder"

