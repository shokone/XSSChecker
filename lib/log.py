
import logging
from termcolor import colored

# create class to declare custom formatter
class CustomFormatter(logging.Formatter):
	# Logging Formatter to add colors and default format

	# add new level
	logging.SUCCESS = 25
	logging.addLevelName(logging.SUCCESS, "SUCCESS")

	def success(self, msg, *args, **kws):
		if self.isEnabledFor(logging.SUCCESS):
			self._log(logging.SUCCESS, msg, args, **kws)

	def logToRoot(message, *args, **kwargs):
		logging.log(logging.SUCCESS, message, *args, **kwargs)

	logging.Logger.success = success
	setattr(logging, "SUCCESS", logging.SUCCESS)
	setattr(logging.getLoggerClass(), "success", success)
	setattr(logging, "success", logToRoot)
	format = "\r[%(asctime)s] [%(levelname)s] %(message)s"

	FORMATS = {
		logging.DEBUG: colored(format, "white"),
		logging.INFO: colored(format, "white"),
		logging.SUCCESS: colored(format, "green"),
		logging.WARNING: colored(format, "yellow"),
		logging.ERROR: colored(format, "red"),
		logging.CRITICAL: colored(format, "red")
	}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt, "%H:%M:%S")
		return formatter.format(record)

# create logger
logger = logging.getLogger('xsscheckerlog')

# by default set log level to info
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()

# add formatter to ch
ch.setFormatter(CustomFormatter())

# add ch to logger
logger.addHandler(ch)

