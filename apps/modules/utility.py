'''Should contain printdebug and logging functionality '''
import logging

# utility globals
DEBUG_MODE = False
LOGGING_MODE = False


logging.basicConfig(filename="logs.log",
                    format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()

# set the threshold to debug
logger.setLevel(logging.INFO)

logger.debug("Logger Initialized")


def print_debug(string):
    '''This prints in console and logs based on preset variables in util'''
    if DEBUG_MODE:
        print(string)
    if LOGGING_MODE:
        logger.info(string)


def print_log(string):
    '''This prints in .log file based on preset variables in util'''
    if LOGGING_MODE:
        logger.info(string)


def map_range(value, in_min, in_max, out_min, out_max):
    '''This maps a value from one range to another'''
    return out_min + (((value - in_min) / (in_max - in_min)) * (out_max - out_min))
