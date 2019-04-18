
import random, string
import classes_unintegrated.adapter as Adapter


# user inputs url, see if it's in the database
def long_url_exists(lUrl):
    return Adapter.check_long_url(lUrl)


def find_short_url(longLink):
	errPage = "404.php" # edge case if short url doesn't exist
	f = open("test.txt","r")
	for x in f:
		sLink = x[:16]
		lLink = x[17:]
		if(lLink == longLink):
			f.close()
			return sLink
	f.close()
	return errPage

# generate random ascii string
def create_short_url(longLink):
    shortLink = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    # check if it is within the text file
    while Adapter.check_short_url(shortLink):
        shortLink = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    return shortLink


# retrieve short_url
def get_short_url(longLink):
    check = long_url_exists(longLink)
    if check:
        return Adapter.get_short_url(longLink)
    else:
        return create_short_url(longLink)


def find_by_line(num):
	with open("test.txt","r") as f:
		return f.read().split('\n')[num]


# redirect a user clicking a long url to a shortened one
def get_long_url(sUrl):
    return Adapter.get_long_url(sUrl)

print(get_short_url("www.umass.edu"))
print(get_long_url('www.membersonly.com/fQCPeau1TeR643Ft'))
#print(validateShortenedURL('1234567812345679'))