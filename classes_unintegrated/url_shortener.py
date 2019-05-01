import random

import classes_unintegrated.adapter as db_adapter


class URLShortener:

    # user inputs url, see if it's in the database
    @staticmethod
    def long_url_exists(long_link):
        return db_adapter.check_long_url(long_link)

    # generate random ascii string
    @staticmethod
    def create_short_url(long_link):
        token = str(hex(random.getrandbits(32)))[2:]

        # check if it is within the db
        while db_adapter.check_short_url(token):
            token = str(hex(random.getrandbits(32)))[2:]
            db_adapter.store_short_url(token)
            db_adapter.store_long_url(long_link)
        return token

    # retrieve short_url
    @staticmethod
    def get_short_url(long_link):
        check = URLShortener.long_url_exists(long_link)
        if check:
            return db_adapter.get_short_url(long_link)
        else:
            return URLShortener.create_short_url(long_link)


    # redirect a user clicking a long url to a shortened one
    @staticmethod
    def get_long_url(short_link):
        if db_adapter.check_short_url(short_link):
            return db_adapter.get_long_url(short_link)
        else:
            return None

print(URLShortener.get_short_url("www.umass.edu"))
print(URLShortener.get_long_url('www.membersonly.com/fQCPeau1TeR643Ft'))
#print(validateShortenedURL('1234567812345679'))