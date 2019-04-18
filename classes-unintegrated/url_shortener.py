import random, string

# user inputs url, see if it's in the database
def long_url_exists(lUrl):
	f = open("test.txt","r")
	exists = 0
	lncnt = 0
	for x in f:
		# for each line in the file, check the long url
		cmp = x[17:]
		#print('comparing ' + cmp + " to " + lUrl)
		if(cmp == lUrl):
			exists = lncnt
		lncnt = lncnt + 1
	f.close()
	return exists

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
def gen_rand_url(longLink):
	check = long_url_exists(longLink)
	if(check == 0):
		while(True):
			shortLink = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
			# print(x);
			# check if it is within the text file
			if(validateShortenedURL(shortLink)):
				f = open("test.txt","a")
				f.write("\n" + shortLink + "\t" + longLink) # write shortened and long url to test
				f.close()
				return 'www.membersonly.com/' + shortLink
	shortLink = find_by_line(check)[:16] # find the short url corresponding to the long one
	return "www.membersonly.com/" + shortLink
	#return shortLink

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
def short_to_long(sUrl):
	default = '404.php' # if a user clicks on an invalid shortened url
	sLink = sUrl[20:] #www.membersonly.com/ spliced away
	f = open("test.txt","r")
	for x in f:
		link16 = x[:16]
		lUrl = x[17:]
		#print('comparing ' + link16 + " and " + sLink)
		if(link16 == sLink):
			return lUrl
	return default

print(gen_rand_url("www.umass.edu"))
#print(short_to_long('www.membersonly.com/SAgQoYRsvSKNVXwd'))
#print(validateShortenedURL('1234567812345679'))