
import random
import string

import classes_unintegrated.adapter as DBAdapter


# user inputs url, see if it's in the database
def long_url_exists(lUrl):
    return DBAdapter.check_long_url(lUrl)


# generate random ascii string
def create_short_url(longLink):
    shortLink = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    # check if it is within the text file
    while DBAdapter.check_short_url(shortLink):
        shortLink = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    return shortLink


# retrieve short_url
def get_short_url(longLink):
    check = long_url_exists(longLink)
    if check:
        return DBAdapter.get_short_url(longLink)
    else:
        return create_short_url(longLink)


# redirect a user clicking a long url to a shortened one
def get_long_url(sUrl):
    return DBAdapter.get_long_url(sUrl)

print(get_short_url("www.umass.edu"))
print(get_long_url('www.membersonly.com/fQCPeau1TeR643Ft'))
#print(validateShortenedURL('1234567812345679'))