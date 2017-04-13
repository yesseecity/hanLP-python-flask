# coding=UTF-8
import yaml
class active:

    def __init__(self, CustomDictionary):
        self.CustomDictionary = CustomDictionary

    def loadDictionary(self):
        with open('/hanlp/config/dictionaries.yaml', 'r') as stream:
            try:
                yamlFile = yaml.load(stream)

                for key, value in yamlFile['dictionaries'].items():
                    
                    if len(value['parentPosTag']) > 0:
                        parentPosTag = ' '+value['parentPosTag']
                    else:
                        parentPosTag = ''

                    for dictionary in value['list']:
                        print('動態載入辭庫: ', dictionary)
                        with open('/hanlp/server/dics/'+dictionary, 'r') as inputTxt:
                            for word in inputTxt.readlines():
                                word = word.replace('\n', '')
                                if len(word) > 0:
                                    self.CustomDictionary.insert(word, key + ' 1' + parentPosTag);
            except yaml.YAMLError as exc:
                print(exc)

    def addKeyword(self, words):
        try:
            f = open('/hanlp/server/dics/keyword-from-api.txt', 'r+')
            for word in words:
                self.CustomDictionary.insert(word, 'keyword 1');
                f.seek(0, 2)
                f.write(word+'\n')

            f.close()
            return 'succes'
        except ValueError:
            print('Add keyword failed!')
            return ValueError
        