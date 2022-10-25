# 抓台股的每月營收
到TWSE [https://mops.twse.com.tw/] 抓營收
抓取csv檔以後，將資料儲存到sqlite中

## 套件版本
SQLAlchemy == 1.4.10
requests == 2.25.1

## 執行
上市公司
twse_monthly_revenue.py
上市公司101年以前
twse_monthly_revenue_101.py
上櫃公司
tpex_monthly_revenue.py
上櫃公司101年以前
tpex_monthly_revenue_101.py