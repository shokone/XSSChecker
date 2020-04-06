from lib.utils import _randomInt, _randomStr, urlEncode
from lib.log import logger

# default payloads
# params
# file  -> check if payloads file is passed as argument
# rstr  -> random string to search on js alert
# rint  -> random integer to search on js alert
# level -> level choosed
def payloads(file,rstr,rint,level):
	# declare list to save payloads
	plist = list()

	# check if specified file exist
	if file is None:
		logger.debug("The payload file does not specify. Loading default payloads")
		logger.info("Generating payloads for level %s..." %(level))
		plist = _open_file("data/basic.txt", plist, rstr, rint)

		if level == 2 or level == 3:
			plist = _open_file("data/body.txt", plist, rstr, rint)
			plist = _open_file("data/img.txt", plist, rstr, rint)
			plist = _open_file("data/div.txt", plist, rstr, rint)

		if level == 3:
			plist = _open_file("data/svg.txt", plist, rstr, rint)
			plist = _open_file("data/polyglot.txt", plist, rstr, rint)

	else:
		logger.info("Generating payloads for file %s..." %(file))
		plist = _open_file(file, plist, rstr, rint)
		
	logger.info("%s payloads have been generated" %(len(plist)))
	
	return plist  
    

# function to open files
# params
# file  -> check if payloads file is passed as argument
# plist -> list to save payloads
# rstr  -> random string to search on js alert
# rint  -> random integer to search on js alert
def _open_file(file, plist, rstr, rint):
	try:
		with open(file, "r") as f:
			payloads = f.read().splitlines()
			plist = _main_generate_payloads(payloads, plist, rstr, rint)
	
	except Exception as e:
		logger.error("File %s doesn't exist" %(file))
		raise SystemExit(0)

	return plist


# payloads on current file
# params
# payloads -> list of payloads on the current file
# plist    -> list to save payloads
# rstr     -> random string to search on js alert
# rint     -> random integer to search on js alert
def _main_generate_payloads(payloads, plist, rstr, rint):
	# generate payloads with random string and integer
	for i in payloads:
		istr = (i.replace("INJECTHERE", "\'"+rstr+"\'"))
		estr = urlEncode(istr)
		iint = i.replace("INJECTHERE", str(rint))
		eint = urlEncode(iint)
		plist.append(istr)
		plist.append(estr)
		plist.append(iint)
		plist.append(eint)
	
	return plist




		
