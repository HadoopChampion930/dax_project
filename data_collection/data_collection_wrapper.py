import sys

def main(args):
    try:
        twitter_collection.main(args)
    except Exception as e:
        print(e)
    try:
        historical_scraper.main(args)
    except Exception as e:
        print(e)
    try:
        ticker_data.main(args)
    except Exception as e:
        print(e)
    try:
        bloomberg_scraper.main(args)
    except Exception as e:
        print(e)
    try:
        news_collection_orbis.main(args)
    except Exception as e:
        print(e)
    try:
        news_collection_zephyr.main(args)
    except Exception as e:
        print(e)
    try:
        reuters_scraper.main(args)
    except Exception as e:
        print(e)
    try:
        yahoo_finance.main(args)
    except Exception as e:
        print(e)
    try:
        stocktwits.main(args)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('python_path', help='The connection string')
    parser.add_argument('google_key_path', help='The path of the Google key')
    parser.add_argument('param_connection_string', help='The connection string')
    parser.add_argument('environment', help='production or test')
    args = parser.parse_args()
    sys.path.insert(0, args.python_path)
    from data_collection.twitter import twitter_collection as twitter_collection
    from data_collection.financial import historical_scraper as historical_scraper
    from data_collection.financial import ticker_data as ticker_data
    from data_collection.news import bloomberg_scraper as bloomberg_scraper
    from data_collection.news import news_collection_orbis as news_collection_orbis
    from data_collection.news import news_collection_zephyr as news_collection_zephyr
    from data_collection.news import reuters_scraper as reuters_scraper
    from data_collection.rss_feeds import yahoo_finance as yahoo_finance
    from data_collection.stocktwits_collection import stocktwits as stocktwits
    main(args)