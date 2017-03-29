# coding=UTF-8
import logging, datetime
logging.basicConfig(filename='/hanlp/log/'+str(datetime.datetime.now())+'.log', filemode='w', level=logging.DEBUG)

def writeLog(input):
    if len(input):
        print('input: ', input)
        logging.info('input: ' + input)