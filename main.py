from database import TweetDB
from loader import save_user_tweets, get_list

#purge the storage database before reload tweets
tweetdb = TweetDB()
engine = tweetdb.get_engine()
conn = engine.connect()
conn.execute('delete from tweets;')

#populate the "tweets" sqlite db table
news_list = get_list()
for member in news_list:
    save_user_tweets(screen_name=member,since='2019-01-01')
