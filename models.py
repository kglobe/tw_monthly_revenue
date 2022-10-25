from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Float, Text
Base = declarative_base()

class MonthlyRevenue(Base): #每月營收
    __tablename__ = 'monthly_revenue'
    revenueMonth = Column(Text, primary_key=True)
    stock_id = Column(Text, primary_key=True) #股票代碼
    stock_name = Column(Text) #股票名稱
    thisMonthRevenue = Column(Float) #當月營收
    lastMonthRevenue = Column(Float) #上個月營收
    lastYearRevenue = Column(Float) #去年同月營收
    compLastMonth = Column(Float) #當月月增
    compLastYear = Column(Float) #當月年增
    thisMonthAccRevenue = Column(Float) #當月累積
    lastYearAccRevenue = Column(Float) #去年同月累積
    yoyAcc = Column(Float) #累積年增
    remarks = Column(Text) #備註
