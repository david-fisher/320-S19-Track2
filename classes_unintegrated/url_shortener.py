import hashlib
import random

import classes_unintegrated.adapter as db_adapter


class URLShortener:

    # user inputs url, see if it's in the database
    @staticmethod
    def long_url_exists(long_link):
        return db_adapter.check_long_url(long_link)


    # generate random ascii string
    @staticmethod
    def create_short_url():
        m = hashlib.shake_128()
        m.update(str(random.getrandbits(256)).encode('utf-8'))
        short_link = m.hexdigest(4)

        # check if it is within the db
        while db_adapter.check_short_url(short_link):
            m.update(str(random.getrandbits(256)).encode('utf-8'))
            short_link = m.hexdigest(4)

        return short_link


    # retrieve short_url
    @staticmethod
    def get_short_url(long_link):
        check = URLShortener.long_url_exists(long_link)
        if check:
            return db_adapter.get_short_url(long_link)
        else:
            return URLShortener.create_short_url()


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