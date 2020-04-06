import sys
import argparse
import logging
from lib.settings import VERSION,NAME
from lib.target import httpMethod
from lib.log import logger

# create arguments passed by cmd
def cmdArguments(argv=None):
	# check if argv isn't empty
	if not argv:
		argv = sys.argv

	parse = argparse.ArgumentParser()

	# basic options
	parse.add_argument("-V", "--version", dest="version", action="store_true", help="Show version number and exit.")
	parse.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Increase output verbosity")
	
	# target options
	target = parse.add_argument_group("Target", "It is mandatory to specify a target on which to carry out the testing")
	target.add_argument("-u", "--url", dest="url", help="Target URL. example: \"http://example.com/index.php\"")

	# request options
	request = parse.add_argument_group("Request", "Use this options to specify how to connect to the target")
	request.add_argument("-m", "--method", dest="method", help="Force usage of given HTTP method (GET, POST...). By default GET.")
	request.add_argument("-c", "--cookie", dest="cookie", help="Cookie header value.")
	request.add_argument("-p", "--parameter", dest="parameter", help="Type only one parameter name to check")
	request.add_argument("-d", "--data", dest="data", help="Data string to be sent. If you don't specify, the script will search for possible forms. Example: \"username=admin&pass=admin\"")
	request.add_argument("--user-agent", dest="useragent", help="User-Agent header value")

	# detection options
	detection = parse.add_argument_group("Detection", "Use this options to check if target is vulnerable to XSS")
	detection.add_argument("-l", "--level", dest="level", type=int, default=1, 
		help='''Level of tests to perform ( values 1-3, default 1 )
		Use only with default payloads.
		''')

	# injection options
	injection = parse.add_argument_group("Injection",
		"These parameters can be used to specify custom payloads or another specific parameters to test.")
	injection.add_argument("--payload", dest="payload", help="Custom payloads file. By default use data/payloads_lvl1.txt")

	# custom options
	customize = parse.add_argument_group("Customize", "Use this options to customize your testing")
	customize.add_argument("--show-browser", dest="showbrowser", action="store_true", help="By default browser is run in background. Add this option to show it.")
	customize.add_argument("--no-check-browser", dest="browser", action="store_true", help="By default use firefox to check XSS. Add this parameter to avoid it")
	customize.add_argument("--browser", dest="select_browser", help="Select browser to check XSS (firefox or chrome). By default use firefox.", default="firefox")

	
	# check if arguments are correct
	for i in range(len(argv)):
		if any(arg in argv for arg in ("-V", "--version")):
			print("%s Version: %s" %(NAME,VERSION))
			raise SystemExit

		elif not any(arg in argv for arg in ("-u", "--url")) and "-h" not in argv:
			errormsg = "Missing a mandatory option (-u, --url). Use -h for show help"
			parse.error(errormsg)

	try:
		if hasattr(parse, "parse_known_args"):
			(args, arg) = parse.parse_known_args(argv)
		else: 
			parse.parse_args(argv)
	except SystemExit:
		raise SystemExit(0)

	# enable verbose log level
	if args.verbose:
		logger.setLevel(logging.DEBUG)
		logger.debug("Verbose mode enabled")

	# check if method is loaded
	if args.method is None:
		args.method = httpMethod.GET.value
		logger.debug("Unspecified method. Use GET by default")

	# check if useragent is loaded
	if args.useragent is not None:
		args.useragent = {'User-Agent': args.useragent}
		logger.debug("Loaded user-agent %s" %(args.useragent))

	# check browser options
	# only one of these
	if args.browser and args.showbrowser:
		logger.error("Use only one of these options --show-browser or --no-check-browser")
		logger.info("Use -h for help")
		raise SystemExit(0)

	# check browser choosed
	if args.select_browser != "firefox" and args.select_browser != "chrome":
		logger.error("The selected browser must be firefox or chrome")
	else: 
		logger.info("Selected %s browser" %(args.select_browser))

	return args