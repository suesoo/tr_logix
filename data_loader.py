#-*- coding: utf-8 -*-

import mysql.connector
import pandas as pd


ret = raw_input(u'초기 자료 인가요? (Y/N)   ')


def insert_price(trade_date, brent=None, wti=None, dubai=None, vol=None ):
    conn = mysql.connector.connect(user='bunker', password='cost', database='OilPrice', host='130.1.12.38')
    cursor = conn.cursor(buffered=True)
    if brent is not None:
        query = "insert into Closings (trade_date,brent) values(%s, %s)"
        cursor.execute(query, (trade_date, brent))
    if wti is not None:
        query = "insert into Closings (trade_date,wti) values(%s, %s)"
        cursor.execute(query, (trade_date, brent))
    if dubai is not None:
        query = "insert into Closings (trade_date,dubai) values(%s, %s)"
        cursor.execute(query, (trade_date, brent))
    if vol is not None:
        query = "insert into Closings (trade_date,vol) values(%s, %s)"
        cursor.execute(query, (trade_date, brent))
    conn.commit()
    conn.close()


def update_price(trade_date, brent=None, wti=None, dubai=None, vol=None):
    conn = mysql.connector.connect(user='bunker', password='cost', database='OilPrice', host='130.1.12.38')
    cursor = conn.cursor(buffered=True)
    if brent is not None:
        query = "update Closings set brent = %s where  date_format(trade_date,'%Y-%m-%d') = %s"
        cursor.execute(query, (brent, trade_date))
    if wti is not None:
        query = "update Closings set wti = %s where  date_format(trade_date,'%Y-%m-%d') = %s"
        cursor.execute(query, (wti, trade_date))
    if dubai is not None:
        query = "update Closings set dubai = %s where  date_format(trade_date,'%Y-%m-%d') = %s"
        cursor.execute(query, (dubai, trade_date))
    if vol is not None:
        query = "update Closings set vol = %s where  date_format(trade_date,'%Y-%m-%d') = %s"
        cursor.execute(query, (vol, trade_date))
    conn.commit()
    conn.close()


if ret == 'Y':

    b_data = pd.read_table('c:\\ml_test\\oilpricedata_2.txt')

    query = "insert into Closings(trade_date,brent) values(%s, %s)"
    for date, price in zip(b_data.date, b_data.price):
        insert_price(date, price)

    conn = mysql.connector.connect(user='bunker', password='cost', database='OilPrice', host='130.1.12.38')
    query = "select * from Closings"
    db_data = pd.read_sql(query, conn)
    print db_data.head()

else:
    b_data = pd.read_table('c:\\ml_test\\new_data.txt')
    b_data['vol'] = b_data['vol_1'] + b_data['vol_2']

    conn = mysql.connector.connect(user='bunker', password='cost', database='OilPrice', host='130.1.12.38')
    query = "select * from Closings order by trade_date desc limit 1"
    db_data = pd.read_sql(query, conn)
    b_data['date'] = pd.to_datetime(b_data['date'])
    # print type(b_data.date.dtype)
    for row in b_data.iterrows():
        new_date = row[1].values[0].date()
        # print new_date, ' ', row[1].values[1]
        update_price(str(new_date).format('%Y-%m-%d'), vol=row[1].values[1])
    # last_db_date = db_data.head(1).iat[0, 0]
    # first_db_date = db_data.tail(1).iat[0, 0]
    #
    # for row in b_data.iterrows():
    #     # print row[1].values[0]
    #     new_date = row[1].values[0].date()
    #     if new_date > last_db_date:
    #         print row[1].values[1]
    #         insert_price(str(new_date).format('%Y-%m-%d'), vol=row[1].values[1])
    #         print '신규 거래일자 입니다.'
    #     elif new_date < first_db_date:
    #         print row[1].values[1]
    #         insert_price(str(new_date).format('%Y-%m-%d'), vol=row[1].values[1])
    #         print '이전 거래일자 입니다.'
    #     else:
    #         pass

        # if new_date > last_db_date:
        #     print row[1].values[1]
        #     insert_price(str(new_date).format('%Y-%m-%d'), brent=row[1].values[1])
        #     print '신규 거래일자 입니다.'
        # elif new_date < first_db_date:
        #     print row[1].values[1]
        #     insert_price(str(new_date).format('%Y-%m-%d'), brent=row[1].values[1])
        #     print '이전 거래일자 입니다.'
        # else:
        #     pass
conn.close()