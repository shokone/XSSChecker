# _*_coding=utf-8_*_

###################
# XSSCHECKER      #
###################
# Version: 1.0.0
# Author: Shokone

# import libs
try:
	import sys
	from termcolor import colored
	try:
		# first check current python version
		pyversion    = sys.version.split()[0]
		splitversion = pyversion.split(".")
		if splitversion[0] < "3" and splitversion[1] < "7":
			raise Exception(colored(
				"[Error] Incompatible Python version detected %s."
				"\n[Error] To successfully run xsschecker you'll have to use version 3.7 or above."
				"\n[Error] Visit 'https://www.python.org/downloads/'" %(pyversion), "red")
				)
	except Exception as e:
		raise SystemExit(e)
	import traceback
	import threading
	import os
	import inspect
	from lib.banner import BANNER
	from lib.arguments import cmdArguments
	from lib.check import start
	from time import time
	from lib.log import logger
except KeyboardInterrupt:
	errormsg = "Aborted by user"
	raise SystemExit(errormsg)


## call banner
def banner():
	## print banner with author and version
	if not any(arg in sys.argv for arg in ("--version", "-V", "-h")):
		print(BANNER())
		logger.info("Starting xsschecker...")
		
# main function
def main():
	# get start time
	xssStart = time()
	
	# print banner
	banner()

	# check arguments
	args = cmdArguments()
	start(args)

	# get final time
	xssEnd = time()
							
	# calculate scan total time
	ctime = xssEnd - xssStart  
	logger.info("Duration: %s Seconds" %(ctime))


if __name__ == "__main__":
	try:
		main()
	except SystemExit as e:
		pass 
	except KeyboardInterrupt:
		pass
	except Exception as e:
		logger.critical(e)
		import traceback
		logger.critical(traceback.format_exc())
	except RuntimeError as e:
		logger.critical(e)
		import traceback
		logger.critical(traceback.format_exc())
	finally:
		# terminate a multi thread python program
		if threading.activeCount() > 1:
			os._exit(getattr(os, "_exitcode", 0))
		else:
			sys.exit(getattr(os, "_exitcode", 0))