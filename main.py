# -*- coding: utf-8 -*-
"""
# tom.li
# 2021/8/29
#
"""
import hashlib
import re

import requests
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
    stock_code = str(params['stock_code'])
    stock_name = params['stock_name']
    cost = float(params['cost'])
    currency = params['currency']
    trans = int(params['trans'])
    h_stock_id = gen_id("so_", str(holder_id) + stock_code)
    create_stock_history(holder_id, stock_code, h_stock_id, currency)
    update_stock(holder_id, holder_name, stock_code, h_stock_id, stock_name, cost, currency, trans)
    rets = []
    return jsonify({'msg': "ok", "rid": req_id, "total_count": len(rets), "data": rets})


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


def date_ydt():
    return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")


def date_timestamp():
    return int(datetime.datetime.now().timestamp())


def gen_id(pix, unique):
    cid = pix + md5_encrypt(unique)[0:8]
    return cid


def query_holder(holder_id=None):
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


def get_yd_cost(stock_code):
    url = "http://49.7.37.132/?list={}".format(stock_code.lower())
    resp = requests.get(url)
    rets = re.findall(r'"([^"]*)"', resp.text)
    ret = rets[0]
    stock_info = ret.split(',')
    if len(stock_info) <= 30:
        return 0
    stock_dd = int(stock_info[30].replace('-', ''))
    now_dd = date_dt()
    if stock_dd <= int(now_dd):
        return format(stock_info[2])
    else:
        return 0


def update_yd_profit():
    client = get_mongo_client()
    stock_cc = client[MONGO_DATABASE][COLLECTION_STOCK_MARKET]
    query_ft = {"status": 1}
    stock = stock_cc.find(query_ft)
    for sk in stock:
        yd_cost = get_yd_cost(sk['stock_code'])
        cost = sk['cost']
        trans = sk['trans']
        clearance_profit = sk['clearance_profit']
        yd_profit = (yd_cost - cost) * trans + clearance_profit
        stock_cc.update_one({'_id': sk['_id']},
                            {"$set": {"yesterday_profit": yd_profit, "clearance_profit": 0, "yesterday": date_ydt()}})
    return True


def query_stock_by_holder(holder):
    client = get_mongo_client()
    stock_cc = client[MONGO_DATABASE][COLLECTION_STOCK_MARKET]
    query_ft = {"holder_id": holder["holder_id"], "status": 1}
    stock = stock_cc.find(query_ft)
    yesterday_profit = 0
    clearance_profit = 0
    total_profit = 0
    currency = "CNY"
    profit = 0
    stocks = []
    for sk in stock:
        profit += sk['profit']
        total_profit += sk['total_profit']
        yesterday_profit += sk['yesterday_profit']
        clearance_profit += sk['clearance_profit']
        currency = sk['currency']
        stocks.append(sk)
    return {
        "holder_id": holder["holder_id"],
        "holder_name": holder["holder_name"],
        "profit": profit,
        "yesterday_profit": yesterday_profit,
        "clearance_profit": clearance_profit,
        "total_profit": total_profit,
        "currency": currency,
        "stocks": stocks
    }


def update_stock(holder_id, holder_name, stock_code, stock_id, stock_name, cost, currency, trans):
    client = get_mongo_client()
    stock_cc = client[MONGO_DATABASE][COLLECTION_STOCK_MARKET]
    st_filter = {"stock_id": stock_id, "status": 1}
    stock = stock_cc.find_one(st_filter)
    if not stock:
        new_stock_market = {
            "_id": generate_id(),
            "date": date_dt(),
            "status": 1,
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
            "yd_cost": get_yd_cost(stock_code),
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
        "yd_cost": get_yd_cost(stock_code),
        "trans": trans,
        "modify_ts": date_timestamp(),
        "modify_time": date_time()
    }
    stock_cc.update_one(st_filter, {"$set": update_info})


@app.route('/api/v1/stock/clearance', methods=["POST"])
def stock_clearance():
    req_id = generate_id()
    rets = []
    return jsonify({'msg': "ok", "rid": req_id, "total_count": len(rets), "data": rets})


@app.route('/api/v1/stock/query', methods=["GET"])
def query():
    req_id = generate_id()
    params = request.args
    holder_id = params.get("holder_id", None)
    if holder_id == '0':
        holder_id = None
    holders = query_holder(holder_id)
    hd_stocks = []
    for hd in holders:
        hd_stocks.append(query_stock_by_holder(hd))

    total_count = len(hd_stocks)
    return jsonify({'msg': "ok", "rid": req_id, "total_count": total_count, "data": hd_stocks})


@app.route('/api/v1/stock/ydp', methods=["GET"])
def yd_profit():
    req_id = generate_id()
    update_yd_profit()
    return jsonify({'msg': "ok", "rid": req_id, "total_count": 0, "data": []})


@app.route('/api/v1/holder/query', methods=["GET"])
def holder_query():
    req_id = generate_id()
    params = request.args
    holder_id = params.get("holder_id", None)
    if holder_id == '0':
        holder_id = None
    rets = query_holder(holder_id)
    return jsonify({'msg': "ok", "rid": req_id, "total_count": len(rets), "data": rets})


@app.route('/api/v1/holder/add', methods=["POST"])
def holder_add():
    req_id = generate_id()
    params = request.json
    holder_name = params["holder_name"]
    holder_id = add_holder(holder_name)
    rets = query_holder(holder_id)
    return jsonify({'msg': "ok", "rid": req_id, "total_count": len(rets), "data": rets})


def generate_id() -> str:
    new_id = str(ObjectId())

    return new_id


if __name__ == '__main__':
    app.run(debug=False)
