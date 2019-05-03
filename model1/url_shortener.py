import random

from model1.adapter import DBAdapter as dbAdapter


class URLShortener:

    # user inputs url, see if it's in the database
    @staticmethod
    def long_url_exists(long_link):
        return dbAdapter.check_long_url(long_link)

    # generate random ascii string
    @staticmethod
    def create_short_url(long_link):
        token = str(hex(random.getrandbits(32)))[2:]

        # check if it is within the db
        while dbAdapter.check_short_url(token):
            token = str(hex(random.getrandbits(32)))[2:]

        dbAdapter.store_url(token, long_link)
        return token

    # retrieve short_url
    @staticmethod
    def get_short_url(long_link):
        check = URLShortener.long_url_exists(long_link)
        if check:
            return dbAdapter.get_short_url(long_link)
        else:
            return URLShortener.create_short_url(long_link)


    # redirect a user clicking a long url to a shortened one
    @staticmethod
    def get_long_url(short_link):
        if dbAdapter.check_short_url(short_link):
            return dbAdapter.get_long_url(short_link)
        else:
            return None
