# stockupup

- 账户总收益 = 历史累计收益（含今日已结算收益） + 持仓收益

- 返回给前端，用户当前该股票的持仓成本、股数，前端根据此计算持仓收益、今日收益

- 定时任务
    - 计算 当日持仓总收益 = 当日清仓收益（数据库存储值） + 当日收盘持仓收益（通过券商接口获取）
    - 今日清仓收益 归0

- 前端计算 今日收益
    - 今日收益 = 今日持仓收益（ (现价-成本) * 股数） - 昨日收益 + 今日清仓收益



