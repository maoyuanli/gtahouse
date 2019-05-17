import os
import re
import sys

import pandas as pd
from sqlalchemy.types import NVARCHAR, INTEGER
from scrapy.cmdline import execute

from utils.database_util import DatabaseUtil

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

cur_path = os.path.dirname(__file__)

try:
    os.remove('listing.json')
except:
    print(Exception)
finally:
    execute(["scrapy", "crawl", "realmaster", "-o", "listing.json"])

DButil = DatabaseUtil()
conn = DButil.get_conn()
df = pd.read_json('./listing.json')


def sep_listID(raw: str):
    listID = raw.split('-')[-1]
    address = ' '.join(raw.split('-')[0:-1])
    return address, listID


def price_num(raw: str):
    num = re.findall(r'\d', raw)
    price_digit = int(''.join(num))
    return price_digit


df['address'] = df['location'].apply(lambda l: sep_listID(l)[0])

df['listID'] = df['location'].apply(lambda l: sep_listID(l)[1])

df['ask'] = df['price'].apply(lambda p: price_num(p))

new_df = df[['listID', 'address', 'ask', 'city', 'proptype']]

dtype_map = {
    'listID': NVARCHAR(100),
    'address': NVARCHAR(500),
    'ask': INTEGER,
    'city': NVARCHAR(100),
    'proptype': NVARCHAR(50)
}

try:
    new_df.to_sql(name='realmaster', con=conn, if_exists='replace', index=False, dtype=dtype_map)
except Exception:
    print(Exception)
