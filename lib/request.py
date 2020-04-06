import copy
import requests
import time
from lib.target import wrapUrl
from lib.settings import DEFAULT_TIMEOUT, USERAGENT_TEST
from lib.utils import splitCookies
from lib.log import logger

# define parameters to the new request
# params
# wrapUrl -> wrapUrl object
# timeout -> request timeout
def new_request(wrapUrl, timeout=None):
	# create dict to save request data
	kwargs = dict(wrapUrl.kwargs)
	method = kwargs['method']
	
	# check if exist timeout, else use default value
	if timeout is not None:
		kwargs['timeout'] = timeout
	else:
		kwargs['timeout'] = DEFAULT_TIMEOUT

	kwargs = define_request(wrapUrl._url, **kwargs)
	
	try:
		session = requests.Session()
		request = session.request(method, wrapUrl._url, **kwargs)
		
	except Exception as e:
		logger.debug(e)
	finally:
		if request is not None:
			if request.status_code != 200:
				logger.error("%s (%s)" %(request.reason, request.status_code))
			else:
				return request

# function to send cookies if exist
# params
# wrapUrl -> wrapUrl object
def get_forms_request(wrapUrl):
	# create dict to save request data
	kwargs = dict(wrapUrl.kwargs)
	kwargs = define_request(wrapUrl._url, **kwargs)
	
	# now check if cookies exist
	if "cookies" in kwargs:
		# do get request
		request = requests.get(wrapUrl._url, **kwargs)
	else:
		request = requests.get(wrapUrl._url)

	return request

# define some data of request
# params
# url    -> target url
# kwargs -> dict with extra data
def define_request(url, **kwargs):
	method = kwargs['method']

	# define possibly headers based on requests lib documentation
	headers = [
		"params", 
		"data", 
		"json", 
		"headers", 
		"cookies", 
		"files", 
		"auth", 
		"timeout",
		"allow_redirects",
		"proxies",
		"verify",
		"stream",
		"cert"
		]

	# create vars to test values
	user_args = dict(kwargs)
	copy_user_args = copy.deepcopy(user_args)
	
	# check if key exist in headers
	for key in list(user_args):
		# if key not exists, delete it
		if key not in headers:
			user_args.pop(key)
	
	kwargs = user_args
	
	if method == "POST":
		if "params" in kwargs:
			kwargs.pop("params")
	else:
		if "data" in kwargs:
			kwargs.pop("data")
	
	# if not exist user-agent
	# add default
	if not "headers" in kwargs or kwargs["headers"] is None:
		kwargs["headers"] = dict(USERAGENT_TEST)

	# check if https
	if not url.startswith('https'):
		kwargs['verify'] = False

	# now check if cookies exist
	if "cookies" in kwargs:
		if not isinstance(kwargs["cookies"], dict):
			kwargs["cookies"] = splitCookies(kwargs["cookies"])
	
	# return kwargs data
	return kwargs









