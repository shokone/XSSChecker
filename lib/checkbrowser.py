import time
from selenium import webdriver
from seleniumrequests import Firefox, Chrome
from selenium.common.exceptions import NoAlertPresentException,InvalidCookieDomainException
from selenium.webdriver import firefox
from selenium.webdriver import chrome
from lib.log import logger

# open new window to test it
# params
# browser -> get the selected browser from arguments
# show    -> get from arguments if browser is displayed
# url     -> target url
# cookies -> (optional) cookies to send 
def open_browser(browser,show,url=None,cookies=None):
	logger.info("Opening %s browser..." %(browser))

	# add option to run on background
	if browser == "firefox":
		browser = _firefox(show)
	elif browser == "chrome":
		browser = _chrome(show)

	# if pass cookies
	# add this to browser
	if url and cookies is not None:
		cookie = browser_cookies(cookies)
		browser.get(url)
		try:
			for i in cookie:
				browser.add_cookie(i)
		except InvalidCookieDomainException as e:
			logger.debug(e)

	return browser


# configure webdriver with firefox
# params
# show -> get from arguments if browser is displayed
def _firefox(show):
	# declare options
	opt = firefox.options.Options()

	if show is False:
		opt.headless = True

	browser = Firefox(options=opt, executable_path= 'driver/linux/geckodriver',log_path="log/geckodriver.log")

	return browser


# configure webdriver with chrome
# params
# show -> get from arguments if browser is displayed
def _chrome(show):
	# declare options
	opt = chrome.options.Options()

	if show is False:
		# Runs Chrome in headless mode.
		opt.add_argument("--headless") 
		# Bypass OS security model
		opt.add_argument('--no-sandbox') 

	browser = Chrome(chrome_options=opt, executable_path= 'driver/linux/chromedriver')

	return browser


# split cookies into dict for webdriver
# params
# cookies -> cookies string
def browser_cookies(cookies):
	cookie = []
	if isinstance(cookies, str):
		ck = cookies.split(";")
		for i in ck:
			c = i.split("=")
			if c[0] and c[1]:
				cookie.append({'name': c[0].lstrip(), 'value': c[1].lstrip()})
	
	return cookie


# test if javascript alert is created
# params
# browser -> browser object
# url     -> url to test it
# rstr    -> random string to search on js alert
# rint    -> random integer to search on js alert
# cookies -> (optional) send cookies to used a user session
def test_browser(browser, wrapUrl, mtype, rstr, rint, cookies=None):
	result = None

	# get full params to build url
	params = ""
	name = None
	# get name on submit button
	for key in wrapUrl.kwargs[mtype]:
		if wrapUrl.kwargs[mtype][key] == "submit":
			name = key
		params += key + "=" + wrapUrl.kwargs[mtype][key] + "&"

	# remove last &
	params = params[:-1]
	
	# build url
	url = wrapUrl._url + "?" + params

	# check method used
	if wrapUrl.kwargs['method'] == "GET":
		browser.get(url)
		time.sleep(0.2)
	elif wrapUrl.kwargs['method'] == "POST":
		# if method is POST but exist a parameter called submit
		# fill form and send request to check XSS
		if name is not None:
			# call page by GET
			browser.get(url)
			# fill fields
			for key in wrapUrl.kwargs[mtype]:
				browser.find_element_by_name(key).send_keys(wrapUrl.kwargs[mtype][key])
			# and press submit button
			browser.find_element_by_name(name).click()
		else:
			browser.request('POST', wrapUrl._url, data=wrapUrl.kwargs[mtype])
		time.sleep(0.5)

	try:
		# check if random value exist on alert
		logger.debug("Alert detected:")
		logger.debug(browser.switch_to.alert.text)
		if rstr in browser.switch_to.alert.text or str(rint) in browser.switch_to.alert.text:
			result = True
		else:
			logger.debug("Alert detected but neither %s string nor number %s found" %(rstr, rint))

	except NoAlertPresentException:
		pass
	except UnexpectedAlertBehaviour:
		pass
	except UnexpectedAlertPresentException:
		pass
	except TimeoutException:
	    logger.error("Time exceed")
	except Exception as e:
		logger.debug(e)
	except KeyboardInterrupt:
		raise KeyboardInterrupt
	
	return result


# function to close browser
# params
# browser -> browser object
def close_browser(browser):
	try:
		# close browser
		logger.info("Closing browser...")
		browser.quit()
	except Exception as e:
		logger.debug("Error to close browser")
		logger.debug(e)
		pass