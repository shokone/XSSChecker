
from urllib.parse import urlparse, urlunparse, parse_qs, parse_qsl, urlsplit
from enum import Enum

# class to get method
class httpMethod(Enum):
	POST = "POST"
	GET = "GET"


# class to generate wrapped url
class wrapUrl(object):
	# init class
	def __init__(self, url, **kwargs):
		self._url = url
		self._request = wrapRequest(**kwargs)
		self._parseUrl = urlparse(url)
	
	# declare method __str__
	def __str__(self):
		return "(%s %s)" %(self.__class__, self._url) 
	
	# declare properties
	@property
	def url(self):
		url = self._parseUrl.scheme + "://" + self._parseUrl.netloc + self._parseUrl.path
		self._url = url
		return self._url
	
	@property
	def port(self):
		if self._parseUrl.port is None:
			if self._parseUrl.scheme == "http":
				port = 80
			elif self._parseUrl.scheme == "https":
				port = 443
		else:
			port = self._parseUrl.port
		return port

	@property
	def method(self):
		return self._request.method
	
	@property
	def headers(self):
		return self._request.headers

	@property
	def parameters(self):
		return self._parseUrl.params
	
	@property
	def post_data(self):
		return self._request.post_data
	
	@property
	def cookies(self):
		return self._request.cookies
	
	@property
	def kwargs(self):
		return self._request.kwargs

	@property
	def query(self):
		return parse_qsl(self._parseUrl.query)
	
	@property
	def scheme(self):
		return self._parseUrl.scheme

	@property
	def json(self):
		return self._request.json
	
	# declare setter of properties
	@url.setter
	def url(self,url):
		self._url = url

	@method.setter
	def method(self,method):
		self._request.method = method

	@headers.setter
	def headers(self,headers):
		self._request.headers = headers

	@post_data.setter
	def post_data(self,post_data):
		self._request.post_data = post_data

	@kwargs.setter
	def kwargs(self,kwargs):
		self._request.kwargs = kwargs


# class to define wrapped request 
class wrapRequest(object):

	def __init__(self, method=httpMethod.GET.value, params=None, data='', json=None, headers={}, cookies=None, files=None, auth=None, timeout=None, allow_redirects=False, proxies=None, verify=False, stream=None, cert=None, **kwargs):
		kwargs = dict(kwargs)

		kwargs['method'] = method

		if params:
			kwargs['params'] = params
		if data:
			kwargs['data'] = data
		if json:
			kwargs['json'] = json

		kwargs['headers'] = headers

		if cookies:
			kwargs['cookies'] = cookies
		if files:
			kwargs['files'] = dict(files)
		if auth:
			kwargs['auth'] = auth
		if timeout:
			kwargs['timeout'] = timeout

		kwargs['allow_redirects'] = allow_redirects

		if proxies:
			kwargs['proxies'] = proxies
		if verify:
			kwargs['verify'] = verify
		if stream:
			kwargs['stream'] = stream
		if cert:
			kwargs['cert'] = cert
		
		self._kwargs = kwargs

	# declare method __str__
	def __str__(self):
		return "(%s %s)" %(self.__class__, self.method) 

	# declare properties
	@property
	def method(self):
		return self._kwargs['method']

	@property
	def headers(self):
		return self._kwargs['headers']

	@property
	def cookies(self):
		return self._kwargs['cookies']

	@property
	def post_data(self):
		return self._kwargs['data']

	@property
	def kwargs(self):
		return self._kwargs
	@property
	def json(self):
		return self._kwargs.get('json')

	# declare setters
	@method.setter
	def method(self,method):
		self._kwargs['method'] = method

	@headers.setter
	def headers(self,headers):
		self._kwargs['headers'] = headers

	@cookies.setter
	def cookies(self,cookies):
		self._kwargs['cookies'] = cookies

	@post_data.setter
	def post_data(self,post_data):
		self._kwargs['data'] = post_data

	@kwargs.setter
	def kwargs(self,kwargs):
		self._kwargs = kwargs



