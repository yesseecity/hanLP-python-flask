# coding=UTF-8
import logging, datetime
# logging.basicConfig(filename='/hanlp/log/'+str(datetime.datetime.now())+'.log', filemode='w', level=logging.DEBUG)
logging.basicConfig(filename='/hanlp/log/apiRequest.log', filemode='w', level=logging.DEBUG)

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