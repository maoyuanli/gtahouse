from twitter_source.database import DatabaseUtil
from twitter_source.tweets_ETL import save_newstweets, get_list, save_searchtweets


def purge_table(table_name):
    tweetdb = DatabaseUtil()
    engine = tweetdb.get_engine()
    conn = engine.connect()
    query = 'delete from {0};'.format(table_name)
    conn.execute(query)

def populate_table(switch):
    if switch == 'newstweets':
        purge_table(switch)
        news_list = get_list()
        for member in news_list:
            save_newstweets(screen_name=member)
    elif switch == 'searchtweets':
        purge_table(switch)
        save_searchtweets()
    else:
        purge_table('newstweets')
        purge_table('searchtweets')
        news_list = get_list()
        for member in news_list:
            save_newstweets(screen_name=member)
        save_searchtweets()


populate_table('searchtweets')