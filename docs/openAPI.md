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
  "timestamp": 1630156207,
  // 10位秒级时间戳
  "holder_name": "豆豆",
  "stock_id": 111101,
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
  "timestamp": 1630156207,
  // 10位秒级时间戳
  "holder_name": "豆豆",
  "stock_id": 111101,
  "stock_code": "002415",
  "stock_name": "海康威视",
  "cost": 53.27,
  "currency": "CNY",
  "trans": 100
  //为0 时就是清仓
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
      "profit": -2000,
      "yesterday_profit": -12000,
      "clearance_profit": 0,
       "total_profit": -2000,
      "currency": "CNY",
      "stocks": [
        {
          "date": 20210828,
          "holder_id": 1,
          "stock_id": 111101,
          "stock_code": "002415",
          "stock_name": "海康威视",
          "profit": -1000,
          "yesterday_profit": -6000,
          "clearance_profit": 0,
          "total_profit": -1000,
          "currency": "CNY",
          "cost": 80.01,
          "trans": 400
        },
        {
          "date": 20210828,
          "holder_id": 1,
          "stock_id": 111102,
          "stock_code": "002415",
          "stock_name": "五粮液",
          "profit": 0,
          "yesterday_profit": -200,
          "clearance_profit": -20000,
          "total_profit": -1000,
          "currency": "CNY",
          "cost": 0,
          "trans": 0
        }
      ]
    }
  ]
}
```