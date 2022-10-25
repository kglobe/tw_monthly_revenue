import numpy as np
import datetime
import pandas as pd
import requests
from io import StringIO
import time
import get_data_sqlalchemy
from models import MonthlyRevenue
from dateutil.relativedelta import relativedelta

def getDataFrameData(convertType,df,key):
    getValue = None
    try:
        getValue = df[key].replace(',', '')
    except Exception:
        getValue = df[key]

    try:
        getValue = eval(convertType)(getValue)
    except Exception:
        getValue = str(getValue)

    if pd.isnull(df[key]):
        return None
    
    if isinstance(df[key], str):
        if df[key].strip() == '-':
            return None
        elif df[key].strip() == '---':
            return None
        elif df[key].strip() == '----':
            return None

    return getValue

def getLastMonth(thisMonth):
    dataDate = datetime.datetime.strptime(thisMonth, '%Y%m')
    lastMonthYear = dataDate.year
    lastMonth = dataDate.month - 1
    if lastMonth == 0:
        lastMonth = 12
        lastMonthYear = lastMonthYear - 1
    last = datetime.datetime.strptime(str(lastMonthYear)+str(lastMonth), '%Y%m')
    return last

def getYoYData(df):
    yoyDf = np.zeros(df.shape[0])
    for i in range(0,df.shape[0]):
        try:
            row = df.iloc[i]
            if float(row['累計營業收入-去年累計營收']) == 0:
                np.append(yoyDf,0)
            else:
                yoyComp = (row['累計營業收入-當月累計營收']-row['累計營業收入-去年累計營收'])/row['累計營業收入-去年累計營收']
                yoyDf[i] = yoyComp
        except Exception as e:
            print(str(e))
            np.append(yoyDf,0)
    
    return yoyDf

def monthly_report(year, month):
    # 假如是西元，轉成民國
    year_r = year
    if year > 1911:
        year_r -= 1911
    
    url = 'https://mops.twse.com.tw/server-java/FileDownLoad?step=9&functionName=show_file&filePath=%2Fhome%2Fhtml%2Fnas%2Ft21%2Fsii%2F&fileName=t21sc03_'+str(year_r)+'_'+str(month)+'.csv'
    
    # 偽瀏覽器
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    
    try:
        s = requests.Session()
        s.config = {'keep_alive': False}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'close',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        print('requests:',year,' ',month)
        r = requests.get(url, headers=headers,  timeout=5)
        r.encoding = 'UTF8'
        lines = r.text.replace('\r', '').split('\n')
        df = pd.read_csv(StringIO("\n".join(lines)), header=0)
    except Exception as e:
        print(str(year)+str(month)+' 抓資料有問題：'+str(e)+' , '+url)
    finally:
        s.close()
        print('Session closed!')
        # return
    
    # df['累積年增率'] = getYoYData(df)
    month = '{:02d}'.format(month)
    monthly_revenueList = []
    for i in range(0,df.shape[0]):
        monthlyRevenue = MonthlyRevenue()
        monthlyRevenue.revenueMonth = str(year)+str(month)
        monthlyRevenue.stock_id = getDataFrameData('str',df.iloc[i,:],'公司代號')
        monthlyRevenue.stock_name = getDataFrameData('str',df.iloc[i,:],'公司名稱')
        monthlyRevenue.thisMonthRevenue = getDataFrameData('float',df.iloc[i,:],'營業收入-當月營收')
        monthlyRevenue.lastMonthRevenue = getDataFrameData('float',df.iloc[i,:],'營業收入-上月營收')
        monthlyRevenue.lastYearRevenue = getDataFrameData('float',df.iloc[i,:],'營業收入-去年當月營收')
        monthlyRevenue.compLastMonth = getDataFrameData('float',df.iloc[i,:],'營業收入-上月比較增減(%)')
        monthlyRevenue.compLastYear = getDataFrameData('float',df.iloc[i,:],'營業收入-去年同月增減(%)')
        monthlyRevenue.thisMonthAccRevenue = getDataFrameData('float',df.iloc[i,:],'累計營業收入-當月累計營收')
        monthlyRevenue.lastYearAccRevenue = getDataFrameData('float',df.iloc[i,:],'累計營業收入-去年累計營收')
        monthlyRevenue.yoyAcc = getDataFrameData('float',df.iloc[i,:],'累計營業收入-前期比較增減(%)')
        monthlyRevenue.remarks = getDataFrameData('str',df.iloc[i,:],'備註')
        monthly_revenueList.append(monthlyRevenue)

    get_data_sqlalchemy.insertMonthlyRevenueList(monthly_revenueList)

if __name__ == '__main__':
    # years = [2012,2011]
    # months = [1,2,3,4,5,6,7,8,9,10,11,12]
    # for year in years:
    #     for month in months:
    #         monthly_revenue = monthly_report(year, month)
    #         time.sleep(5)
    
    run_date = datetime.datetime.now() - relativedelta(months=1)
    monthly_revenue = monthly_report(int(run_date.strftime('%Y')), int(run_date.strftime('%m')))