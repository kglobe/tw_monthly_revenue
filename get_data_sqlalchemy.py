from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

db_url = 'sqlite:///stock.db'

def insertMonthlyRevenueList(monthlyRevenueList):
    try:
        engine = create_engine(db_url,poolclass=NullPool)
        DB_Session = sessionmaker(bind=engine)
        session = DB_Session()
        for monthlyRevenue in monthlyRevenueList:
            session.merge(monthlyRevenue)
        # session.add_all(monthlyRevenueList)
        session.commit()
    except Exception as e:
        print('insertMonthlyRevenueList error:',e)
    finally:
        session.close()
