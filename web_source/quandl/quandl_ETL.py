from utils.fetch_token import TokenFetcher
from utils.database_util import DatabaseUtil
import quandl

tf = TokenFetcher('token.json')
dbu = DatabaseUtil()

token = tf.fetch_token('quandl_cmhc')

cmhc = quandl.get("CMHC/HPPU50_ON", authtoken=token).reset_index()

conn = dbu.get_conn()

cmhc.to_sql('cmhc',con=conn,index=False, if_exists='replace')