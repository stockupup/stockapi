API文档
=========================

总则
---------------------------

* 协议: HTTP
* 方法: GET * POST(读数据使用GET， 写数据使用POST)
* 数据格式: JSON
* 国家化参数lang：放在url参数中, 或者header中, 否则默认出中文

scale up 加仓
--------------------------

* 请求方式: post
* 接口路径: ```/api/v1/stock/scale```
* 请求参数:

```json
{
  "holder_id": 1,
  "holder_name": "豆豆",
  "stock_id": 111101,
  "stock_code": "002415",
  "stock_name": "海康威视",
  "price": 53.27,
  "currency": "CNY",
  "trans": 100
}
```

reduce 减仓
--------------------------

* 请求方式: post
* 接口路径: ```/api/v1/stock/reduce```
* 请求参数:

```json
{
  "holder_id": 1,
  "holder_name": "豆豆",
  "stock_id": 111101,
  "stock_code": "002415",
  "stock_name": "海康威视",
  "currency": "CNY",
  "price": 53.27,
  "trans": 100
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
  "code": 1,
  "msg": "ok",
  "total_count": 1,
  "data": [
    {
      "holder_id": 1,
      "holder_name": "豆豆",
      "profit": -1000,
      "market_value": 3000,
      "currency": "CNY",
      "stocks": [
        {
          "holder_id": 1,
          "holder_name": "豆豆",
          "stock_id": 111101,
          "stock_code": "002415",
          "stock_name": "海康威视",
          "market_value": 3000,
          "profit": -1000,
          "currency": "CNY",
          "price": 53.27,
          "cost": 80.01,
          "trans": 400
        }
      ]
    }
  ]
}
```