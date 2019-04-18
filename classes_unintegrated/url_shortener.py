
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
    while (True):
        shortLink = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        # print(x);
        # check if it is within the text file
        if (validateShortenedURL(shortLink)):
            f = open("test.txt", "a")
            f.write("\n" + shortLink + "\t" + longLink)  # write shortened and long url to test
            f.close()
            return 'www.membersonly.com/' + shortLink


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


# check if this hash is original (not in the db)
def validateShortenedURL(link):
	#link16 = link[:16]
	#print(link16)
	valid = True
	f = open("test.txt","r")
	for x in f:
		#print(x)
		link16 = x[:16]
		#print(link16)
		#print(link)
		#print("comparing " + link16 + " and " + link)
		if(link16 == link):
			valid = False
	f.close()
	return valid


# redirect a user clicking a long url to a shortened one
def get_long_url(sUrl):
    return Adapter.get_long_url(sUrl)

print(get_short_url("www.umass.edu"))
print(get_long_url('www.membersonly.com/fQCPeau1TeR643Ft'))
#print(validateShortenedURL('1234567812345679'))