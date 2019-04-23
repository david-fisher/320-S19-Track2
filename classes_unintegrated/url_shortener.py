import hashlib
import random

import classes_unintegrated.adapter as db_adapter


# user inputs url, see if it's in the database
def long_url_exists(long_link):
    return db_adapter.check_long_url(long_link)


# generate random ascii string
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
def get_short_url(long_link):
    check = long_url_exists(long_link)
    if check:
        return db_adapter.get_short_url(long_link)
    else:
        return create_short_url()


# redirect a user clicking a long url to a shortened one
def get_long_url(short_link):
    if db_adapter.check_short_url(short_link):
        return db_adapter.get_long_url(short_link)
    else:
        return None

print(get_short_url("www.umass.edu"))
print(get_long_url('www.membersonly.com/fQCPeau1TeR643Ft'))
#print(validateShortenedURL('1234567812345679'))