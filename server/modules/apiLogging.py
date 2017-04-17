# coding=UTF-8
import logging, datetime
import logging.handlers

# logging.basicConfig(filename='/hanlp/log/apiRequest.log', filemode='w', level=logging.DEBUG)
handler = logging.handlers.RotatingFileHandler('/hanlp/log/apiRequest.log', maxBytes=50*1024*1024, backupCount=5)
logging.basicConfig( filemode='a', level=logging.DEBUG, handlers=[handler])

def inputMessage(message):
    if len(message):
        print('input: ', message)
        logging.info('input: ' + message)

def keyword(message):
    logging.info('keywordList: ' + message)

def info(message):
    logging.info(message)

def error(message):
    logging.error(message)