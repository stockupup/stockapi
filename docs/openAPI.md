API文档
=========================

总则
---------------------------

* 协议: HTTP
* 方法: GET * POST(读数据使用GET， 写数据使用POST)
* 数据格式: JSON
* 国家化参数lang：放在url参数中, 或者header中, 否则默认出中文

update 更新持仓数据
--------------------------

* 请求方式: post
* 接口路径: ```/api/v1/stock/update```
* 请求参数:

```json
{
  "holder_id": 1,
  "holder_name": "豆豆",
  "stock_code": "002415",
  "stock_name": "海康威视",
  "cost": 53.27,
  // 0 清仓
  "currency": "CNY",
  "trans": 100
  //为0 时就是清仓
}
```

clearance 清仓
--------------------------

* 请求方式: post
* 接口路径: ```/api/v1/stock/clearance```
* 请求参数:

```json
{
  "holder_id": 1,
  "holder_name": "豆豆",
  "stock_id": 111101,
  "stock_code": "002415",
  "stock_name": "海康威视",
  "profit": 53.27
}
```

新增 holder
--------------------------

* 请求方式: post
* 接口路径: ```/api/v1/holder/add```
* 请求参数:

```json
{
  "holder_name": "豆豆"
}
```

* response

```json
{
  "data": [
    {
      "_id": "hd_83682a00",
      "create_time": "2021-08-30 12:23:56",
      "create_ts": 1630297436,
      "holder_id": "hd_83682a00",
      "holder_name": "豆豆"
    }
  ],
  "msg": "ok",
  "rid": "612c5d5cb59112c3836829fe"
}
```


查询 holder
--------------------------

* 请求方式: GET
* 接口路径: ```/api/v1/holder/query```
* 请求参数:

* response

```json
{
    "data": [
        {
            "_id": "hd_83682a06",
            "create_time": "2021-08-30 12:28:32",
            "create_ts": 1630297712,
            "holder_id": "hd_83682a06",
            "holder_name": "豆豆"
        },
        {
            "_id": "hd_83682a0a",
            "create_time": "2021-08-30 12:28:44",
            "create_ts": 1630297724,
            "holder_id": "hd_83682a0a",
            "holder_name": "强哥"
        }
    ],
    "msg": "ok",
    "rid": "612c5e87b59112c383682a0c"
}
```

持仓情况
--------------------------

* 请求方式: get
* 接口路径: ```/api/v1/stock/query```
* 请求参数:

    - holder_id  :为0的时候查所有人的持仓数据， 为1的时候查豆豆的持仓数据

```json
{
    "data": [
        {
            "clearance_profit": 0,
            "currency": "CNY",
            "holder_id": "hd_83682a06",
            "holder_name": "豆豆",
            "profit": 0,
            "stocks": [
                {
                    "_id": "612d85502fed8186d9e62329",
                    "clearance_profit": 0,
                    "cost": 54.461,
                    "create_dt": "20210831",
                    "create_time": "2021-08-31 09:26:40",
                    "create_ts": 1630373200,
                    "currency": "CNY",
                    "date": "20210831",
                    "holder_id": "hd_83682a06",
                    "holder_name": "豆豆",
                    "modify_time": "2021-08-31 09:26:40",
                    "modify_ts": 1630373200,
                    "profit": 0,
                    "status": 1,
                    "stock_code": "SZ002415",
                    "stock_id": "so_6a74097d",
                    "stock_name": "海康威视",
                    "total_profit": 0,
                    "trans": 500,
                    "yd_cost": 0,
                    "yesterday_profit": 0
                },
                {
                    "_id": "612d85542fed8186d9e6232d",
                    "clearance_profit": 0,
                    "cost": 54.461,
                    "create_dt": "20210831",
                    "create_time": "2021-08-31 09:26:45",
                    "create_ts": 1630373205,
                    "currency": "CNY",
                    "date": "20210831",
                    "holder_id": "hd_83682a06",
                    "holder_name": "豆豆",
                    "modify_time": "2021-08-31 09:26:45",
                    "modify_ts": 1630373205,
                    "profit": 0,
                    "status": 1,
                    "stock_code": "SH0600711",
                    "stock_id": "so_868fa29e",
                    "stock_name": "盛屯矿业",
                    "total_profit": 0,
                    "trans": 500,
                    "yd_cost": 0,
                    "yesterday_profit": 0
                }
            ],
            "total_profit": 0,
            "yesterday_profit": 0
        },
        {
            "clearance_profit": 0,
            "currency": "CNY",
            "holder_id": "hd_83682a0a",
            "holder_name": "强哥",
            "profit": 0,
            "stocks": [],
            "total_profit": 0,
            "yesterday_profit": 0
        }
    ],
    "msg": "ok",
    "rid": "612d85592fed8186d9e6232e",
    "total_count": 2
}
```