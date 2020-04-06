import requests
import copy
from lib.payloads import payloads
from lib.log import logger
from termcolor import colored
from bs4 import BeautifulSoup
from lib.target import wrapUrl
from urllib.parse import urljoin
from lib.request import new_request, get_forms_request
from lib.checkbrowser import open_browser, test_browser, close_browser
from lib.utils import _randomStr, _randomInt, splitParams, extractUrlParams

# start xss attack
# params
# args -> arguments passed by cmd
def start(args):
	kwargs = dict()
	kwargs['method'] = args.method.upper()
	kwargs['headers'] = args.useragent
	kwargs['cookies'] = args.cookie
	kwargs['data'] = args.data
	kwargs['payload'] = args.payload
	kwargs['params'] = args.parameter
	kwargs['browser'] = args.browser
	kwargs['showbrowser'] = args.showbrowser
	kwargs['select_browser'] = args.select_browser
	kwargs['level'] = args.level
	
	new = checkXSS(wrapUrl(args.url, **kwargs), **kwargs)
	new._do_attack()


# class to define how to make xss checks
class checkXSS(object):

	# init function
	# params
	# wrapUrl -> object
	# kwargs  -> dict
	def __init__(self,wrapUrl, **kwargs):
		self._wrapUrl = wrapUrl
		self.xss_flag = False
		self._browser = kwargs['browser']
		self._open_browser = None
		self._showbrowser = kwargs['showbrowser']
		self.randStr = _randomStr()
		self.randInt = _randomInt()
		self._select_browser = kwargs['select_browser']
		self.payloads = payloads(kwargs['payload'],self.randStr,self.randInt,kwargs['level'])
		

	# get inputs automatically to check XSS
	# params
	# input_type -> element to search, by default form
	def get_inputs(self, input_type="form"):
		try:
			request = get_forms_request(self._wrapUrl)
			#request = requests.get(self._wrapUrl._url)
		except Exception as e:
			logger.debug(e)
			pass

		bs = BeautifulSoup(request.content, "html.parser")
		
		inputs = []
		# add inputs 
		for i in bs.find_all(input_type):
			inputs.append(i)

		return inputs

	# This function extracts all possible useful information about an HTML form
	# params
	# form -> form to get data
	def get_form_data(self, form):
		# declare vars
		data = {}
		inputs = []

		# get textareas
		for itag in form.find_all("textarea"):
			# if empty type, use text by default
			itype = itag.attrs.get("type", "textarea")
			iname = itag.attrs.get("name")
			inputs.append({"type": itype, "name": iname})

		# get inputs
		for itag in form.find_all("input"):
			# if empty type, use text by default
			itype = itag.attrs.get("type", "text")
			iname = itag.attrs.get("name")
			inputs.append({"type": itype, "name": iname})

		# get inputs
		for itag in form.find_all("button"):
			# if empty type, use text by default
			itype = itag.attrs.get("type", "submit")
			iname = itag.attrs.get("name")
			inputs.append({"type": itype, "name": iname})

		# save fields
		data["action"] = form.attrs.get("action").lower()

		# if empty method, use get by default
		data["method"] = form.attrs.get("method", "get").upper()
		data["inputs"] = inputs
		
		data = self.parse_form_data(data)
		
		return data

	# parse inputs form
	# params
	# form_data -> form data
	def parse_form_data(self, form_data):
		# construct the full URL (if the url provided in action is relative)
		self._wrapUrl._url = urljoin(self._wrapUrl._url, form_data["action"])
		
		# get the inputs
		inputs = form_data["inputs"]
		data = {}
		iname = ""
		ivalue = ""
		itypes = ["text", "search", "textarea", "password", "submit"]

		# get each input
		for input in inputs:
			
			# replace all text and search values with `value`
			if input["type"] in itypes:
				iname = input.get("name")
				if input["type"] == "submit":
					ivalue = "submit"
				else:
					ivalue = "a"
			
			# if input name and value are not None, 
			# then add them to the data of form submission
			if iname and ivalue:
				data[iname] = ivalue

		form_data["inputs"] = data

		return form_data

	# submit a form 
	# params
	# form_data -> form data
	def submit_form(self, form_data):

		# check form method
		if form_data["method"] == "post":
			self._wrapUrl.kwargs['data'] = form_data['inputs']
		else:
			self._wrapUrl.kwargs['params'] = form_data['inputs']
		
		return new_request(self._wrapUrl)

	# basic check
	# it is not necessary to indicate a parameter
	# params 
	# method -> if post is data, if get is params
	def _do_basic_attack(self, method):	
		logger.info("Finding forms in the page..")
		forms = self.get_inputs()

		# check if exist forms 
		if len(forms) == 0:
			logger.warn("There aren't forms to check.")
			logger.warn("Please, add more info to find anything.")
			return

		logger.info("Detected %s forms." %(len(forms)))

		try: 
			# scan each form
			for f in forms:
				logger.info("Checking XSS on form...")
				data = self.get_form_data(f)
				inputs = data['inputs']
				if not inputs:  
					logger.warn("The form has no fields to check")
					continue
				
				self._wrapUrl.kwargs[method] = data['inputs']
				self._send_payload(inputs,method)
		except Exception as e:
			logger.debug(e)



	# check if data or parameters have been specified 
	# params 
	# method -> if post is data, if get is params
	def check_params(self, method):
		# declare param var
		param = None

		if "data" in self._wrapUrl.kwargs:
			param = self._wrapUrl.kwargs["data"]
			if isinstance(param, str):
				param = splitParams(param)
		elif "params" in self._wrapUrl.kwargs:
			param = self._wrapUrl.kwargs["params"]
			if isinstance(param, str):
				if "=" in param: 
					param = splitParams(param)
				else:
					param = {param: ""}
		elif self._wrapUrl.query:
			param = extractUrlParams(self._wrapUrl)

		# save data
		if param:
			self._wrapUrl.kwargs[method] = param
			return 1

	# function to send payloads
	# params
	# params -> parameters to check
	# method -> if post is data, if get is params
	def _send_payload(self, params, method):
				
		p = list()
		self._wrapUrl.kwargs[method] = dict()

		if isinstance(params, list):
			for i in params:
				self._wrapUrl.kwargs[method][i] = ""
		elif isinstance(params, dict):
			for key,value in params.items():
				p.append(key)
				self._wrapUrl.kwargs[method][key] = value

		logger.info("%s params detected." %(len(params)))

		# check each param
		for param in p:
			logger.info("Checking parameter %s..." %(param))
			# check payloads on each param
			try:
				for payload in self.payloads:
				#try:
					# save original data
					original = self._wrapUrl.kwargs[method][param]
					self._wrapUrl.kwargs[method][param] = payload
					logger.debug("Sending payload %s..." %(payload))
					# do request					
					req = new_request(self._wrapUrl)
					
					if req is None:
						break

					# check if payload exist on response
					if self.randStr in str(req.content,"utf-8") or str(self.randInt) in str(req.content,"utf-8"):
						if self._check_browser(self._wrapUrl, method) is not None or self._browser is True:
							# close browser
							if not self._browser:
								self._force_close_browser(self._open_browser)
							self.xss_flag = True
							# print data
							logger.success("FOUND -> Payload: %s" %(payload))
							logger.success("Vulnerable URL  -> %s" %(self._wrapUrl._url))
							logger.success("Vulnerable Input -> %s" %(param))
							
							return 1 
					else:
						self._wrapUrl.kwargs[method][param] = original

				if not self.xss_flag:
					# close browser
					if not self._browser:
						self._force_close_browser(self._open_browser)
					logger.warn("Parameter name %s might not be injectable" %(param))
			except Exception as e:
				logger.debug(e)
			except KeyboardInterrupt:
				raise KeyboardInterrupt	
			


	# xss attack
	def _do_attack(self):
		logger.info("Checking XSS on url %s..." %(self._wrapUrl._url))

		# get value depends on method used
		# check method
		if self._wrapUrl.kwargs["method"] == "POST":
			result = "data"
		else:
			result = "params"

		# if no parameter or data is entered
		# run basic scan
		try:
			if not self.check_params(result):
				self._do_basic_attack(result)
			else:
				self._send_payload(self._wrapUrl.kwargs[result],result)

			if not self.xss_flag:
				logger.warn("Input form might not be injectable")

		except KeyboardInterrupt:
			raise KeyboardInterrupt


	# function to call browser to check XSS
	# params
	# wrapUrl -> wrapUrl object
	# method  -> if post is data, if get is params
	# string  -> random string to search
	def _check_browser(self, wrapUrl, method):
		# check if option is specified
		if not self._browser:
			if self._open_browser is None:
				cookies = None
				if "cookies" in wrapUrl.kwargs:
					cookies = wrapUrl.kwargs['cookies']
				self._open_browser = open_browser(self._select_browser,self._showbrowser,wrapUrl._url,cookies)
		
			result = None
			result = test_browser(self._open_browser, wrapUrl, method, self.randStr, self.randInt)

			return result

	# when checked is complete call it to close browser
	# params
	# browser -> browser object
	def _force_close_browser(self,browser):
		close_browser(browser)
