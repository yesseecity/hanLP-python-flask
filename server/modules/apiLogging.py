# coding=UTF-8
import logging, datetime
import logging.handlers
from termcolor import cprint

# logging.basicConfig(filename='/hanlp/log/apiRequest.log', filemode='w', level=logging.DEBUG)
handler = logging.handlers.RotatingFileHandler('/hanlp/log/apiRequest.log', maxBytes=50*1024*1024, backupCount=5)
logging.basicConfig( filemode='a', level=logging.DEBUG, handlers=[handler])

def inputMessage(message):
    if len(message):
        cprint('input: '+ message, 'white')
        logging.info('input: ' + message)

def keyword(message):
    cprint('keywordList: '+ message, 'blue')
    logging.info('keywordList: ' + message)

def info(message):
    cprint('info: '+ message, 'blue')
    logging.info(message)

def error(message):
    cprint('error: '+ message, 'red')
    logging.error(message)