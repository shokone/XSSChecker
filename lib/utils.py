import random
import string
from urllib import parse


# return random integer value from a to b
# params
# a -> first
# b -> last
def _randomInt(a=11111, b=99999):
	randomInt = random.randint(a,b)
	return randomInt

# return random string value
# params
# length -> by default 5
# case   -> True is random, False if lower
def _randomStr(length=5, case=False):
	# check if lower or random case
	if case:
		randomStr = ''.join(random.choice(string.ascii_letters) for i in range(0, length))
	else:
		randomStr = ''.join(random.choice(string.ascii_lowercase) for i in range(0, length))
	
	return randomStr


# decode url characters
# params
# string -> string to decode
def urlDecode(string):
	# check if is a string
	if isinstance(string, str):
		decoded = parse.unquote_plus(string)
	else:
		raise TypeError

	return decoded

# encode url characters
# params
# string -> string to encode
def urlEncode(string):
	# check if is a string
	if isinstance(string, str):
		encode = parse.quote_plus(string)
	else:
		raise TypeError

	return encode

# split cookies str to dict
# params
# cookies -> cookies str to convert to dict
def splitCookies(cookies):
	cookie = dict()
	ck = cookies.split(";")
	for i in ck:
		c = i.split("=")
		if c[0] and c[1]:
			cookie[c[0].lstrip()] = c[1].lstrip()
	return cookie

# split each parameter
# params
# paramData -> params str to convert to dict
def splitParams(paramData):
	paramData = paramData.split("&")
	params = {}

	for i in paramData:
		d = i.split("=")
		params[d[0]] = d[1]

	return params

# extract params from url
# params
# wrapUrl -> url object to extract params
def extractUrlParams(wrapUrl):
	params = {}
	for key,val in wrapUrl.query:
		# call withParamOpt to test each param
		params[key] = val
		
	return params