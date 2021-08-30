# -*- coding: utf-8 -*-
"""
# tom.li
# 2021/8/29
#
"""
import hashlib

from flask import Flask, jsonify, request
from bson.objectid import ObjectId
import datetime

from src.conf import MONGO_DATABASE, COLLECTION_STOCK, COLLECTION_STOCK_MARKET, COLLECTION_HOLDER
from src.lib.mongodb import get_mongo_client

app = Flask("stock")


@app.route('/api/v1/stock/update', methods=["POST"])
def stock_update():
    req_id = generate_id()
    params = request.json
    holder_id = params['holder_id']
    holder_name = params['holder_name']
    timestamp = params['timestamp']
    stock_code = str(params['stock_code'])
    stock_name = params['stock_name']
    cost = float(params['cost'])
    currency = params['currency']
    trans = int(params['trans'])
    h_stock_id = gen_id("so_", str(holder_id) + stock_code)
    create_stock_history(holder_id, stock_code, h_stock_id, currency)
    update_stock(holder_id, holder_name, stock_code, h_stock_id, stock_name, cost, currency, trans)
    return jsonify({'msg': "ok", "rid": req_id, "data": []})


def md5_encrypt(text):
    m5 = hashlib.md5()
    text = text.encode(encoding="utf-8")
    m5.update(text)
    value = m5.hexdigest()
    return str(value)


def date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def date_dt():
    return datetime.datetime.now().strftime("%Y%m%d")


def date_timestamp():
    return int(datetime.datetime.now().timestamp())


def gen_id(pix, unique):
    cid = pix + md5_encrypt(unique)[0:8]
    return cid


def query_holder(holder_id):
    client = get_mongo_client()
    db = client[MONGO_DATABASE][COLLECTION_HOLDER]
    query_filer = {}
    if holder_id:
        query_filer = {
            "_id": holder_id
        }

    result = db.find(query_filer)
    rets = [rs for rs in result]
    return rets


def add_holder(holder_name):
    client = get_mongo_client()
    db = client[MONGO_DATABASE][COLLECTION_HOLDER]
    holder_id = "hd_" + generate_id()[-8:]
    query_filer = {
        "_id": holder_id,
        "holder_id": holder_id,
        "holder_name": holder_name,
        "create_ts": date_timestamp(),
        "create_time": date_time()
    }

    db.insert_one(query_filer)
    return holder_id


def create_stock_history(holder_id, stock_code, stock_id, currency):
    client = get_mongo_client()
    stock_cc = client[MONGO_DATABASE][COLLECTION_STOCK]
    stock = stock_cc.find_one({"_id": stock_id})
    if not stock:
        new_stock = {
            "_id": stock_id,
            "stock_id": stock_id,
            "stock_code": str(stock_code),
            "holder_id": holder_id,
            "profit": 0,
            "currency": currency,
            "create_dt": date_dt(),
            "create_ts": date_timestamp(),
            "create_time": date_time()
        }
        stock_cc.insert_one(new_stock)

    client.close()


def update_stock(holder_id, holder_name, stock_code, stock_id, stock_name, cost, currency, trans):
    client = get_mongo_client()
    stock_cc = client[MONGO_DATABASE][COLLECTION_STOCK_MARKET]
    st_filter = {"stock_id": stock_id, "status": 1}
    stock = stock_cc.find_one(st_filter)
    if not stock:
        new_stock_market = {
            "date": date_dt(),
            "holder_id": holder_id,
            "holder_name": holder_name,
            "stock_id": stock_id,
            "stock_code": str(stock_code),
            "stock_name": stock_name,
            "profit": 0,
            "yesterday_profit": 0,
            "clearance_profit": 0,
            "total_profit": 0,
            "currency": currency,
            "cost": cost,
            "trans": trans,
            "create_dt": date_dt(),
            "create_ts": date_timestamp(),
            "create_time": date_time(),
            "modify_ts": date_timestamp(),
            "modify_time": date_time()
        }
        stock_cc.insert_one(new_stock_market)
        return
    update_info = {
        "cost": cost,
        "trans": trans,
        "modify_ts": date_timestamp(),
        "modify_time": date_time()
    }
    stock_cc.update_one(st_filter, {"$set": update_info})


@app.route('/api/v1/stock/clearance', methods=["POST"])
def stock_clearance():
    req_id = generate_id()
    return jsonify({'msg': "ok", "rid": req_id, "data": []})


@app.route('/api/v1/stock/query', methods=["GET"])
def query():
    req_id = generate_id()
    return jsonify({'msg': "ok", "rid": req_id, "data": []})


@app.route('/api/v1/holder/query', methods=["GET"])
def holder_query():
    req_id = generate_id()
    params = request.args
    holder_id = params.get("holder_id", None)
    rets = query_holder(holder_id)
    return jsonify({'msg': "ok", "rid": req_id, "data": rets})


@app.route('/api/v1/holder/add', methods=["POST"])
def holder_add():
    req_id = generate_id()
    params = request.json
    holder_name = params["holder_name"]
    holder_id = add_holder(holder_name)
    rets = query_holder(holder_id)
    return jsonify({'msg': "ok", "rid": req_id, "data": rets})


def generate_id() -> str:
    new_id = str(ObjectId())

    return new_id


if __name__ == '__main__':
    app.run(debug=False)
