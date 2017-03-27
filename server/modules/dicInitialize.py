# coding=UTF-8
import sys
import yaml
reload(sys)
sys.setdefaultencoding('utf-8')

def dynamicDic(CustomDictionary):
    with open('/hanlp/config/dictionaries.yaml', 'r') as stream:
        try:
            yamlFile = yaml.load(stream)

            for key, value in yamlFile['dictionaries'].iteritems():
                
                if len(value['parentPosTag']) > 0:
                    parentPosTag = ' '+value['parentPosTag']
                else:
                    parentPosTag = ''

                for dictionary in value['list']:
                    print '動態載入辭庫: ', dictionary
                    with open('/hanlp/server/dics/'+dictionary, 'r') as inputTxt:
                        for word in inputTxt.readlines():
                            word = word.replace('\n', '')
                            if len(word) > 0:
                                CustomDictionary.insert(word, key + ' 1' + parentPosTag);        
        except yaml.YAMLError as exc:
            print(exc)

