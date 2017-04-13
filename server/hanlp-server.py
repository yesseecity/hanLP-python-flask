# coding=UTF-8
import sys
sys.path.append('/hanlp/server/modules/')

import dictionaryService, apiLogging

from jpype import *
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_restful.representations.json import output_json


# Parameters 
innerConvertEnable = True


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

hanLPLibPath = '/hanlp/server/lib/hanlp-1.3.2/'
javaClassPath = hanLPLibPath+'hanlp-1.3.2.jar'+':'+hanLPLibPath

startJVM(getDefaultJVMPath(), '-Djava.class.path='+javaClassPath, '-Xms1g', '-Xmx1g')
HanLP = JClass('com.hankcs.hanlp.HanLP')
Config = JClass('com.hankcs.hanlp.HanLP$Config')

parser.add_argument('content', type=str, help='要分詞的內文')
parser.add_argument('convertMode', type=str, help='語言轉換模式')
parser.add_argument('num', type=int, help='回傳字詞陣列的長度')
parser.add_argument('compare', type=str, action='append_const', help='要比對的兩個詞所在的陣列')
parser.add_argument('enablePOSTagging', type=bool, help='顯示POS tag, default=true')
parser.add_argument('enableCustomDic', type=bool, help='啟用自定義詞庫, default=true')
parser.add_argument('keywords', type=str, action='append_const', help='新增keyword所傳入的陣列')

@api.representation('application/json; charset=utf-8')



def innerConvert(inputString, mode):
    if innerConvertEnable:
        if mode == '2tc':
            return HanLP.convertToTraditionalChinese(inputString)
        elif mode == '2sc':
            return HanLP.convertToSimplifiedChinese(inputString)
        elif mode == '2hk':
            return HanLP.s2hk(inputString)
        elif mode == '2tw':
            return HanLP.s2tw(inputString)
        else:
            return HanLP.s2tw(inputString)
    else:
        return inputString


def initialize():
    print('initialize')
    global ds
    ds = dictionaryService.active(JClass('com.hankcs.hanlp.dictionary.CustomDictionary'))
    ds.loadDictionary()

def generalProcess(input):
    apiLogging.inputMessage(input)

def generalSetting():
    enablePOSTagging =  parser.parse_args()['enablePOSTagging']
    if enablePOSTagging == False:
        Config.ShowTermNature = False
    else:
        Config.ShowTermNature = True

## For router
class segment(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        enableCustomDic = parser.parse_args()['enableCustomDic']

        StandardTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
        if enableCustomDic == False:
            StandardTokenizer.SEGMENT.enableCustomDictionary(False)
        else:
            StandardTokenizer.SEGMENT.enableCustomDictionary(True)

        segemntTool = HanLP.segment
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            segments = []
            for v in segemntTool(innerConvert(content, '2sc')):
                tempString = str(v).strip()
                segments.append(innerConvert(tempString, convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class tcSegment(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            segments = []
            tcTokenizer = JClass('com.hankcs.hanlp.tokenizer.TraditionalChineseTokenizer')
            for v in tcTokenizer.segment(content):
                segments.append(str(v))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class crfSegment(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            segments = []
            CRFSegment = JClass('com.hankcs.hanlp.seg.CRF.CRFSegment')
            segemntTool = CRFSegment().seg
            for v in segemntTool(innerConvert(content, '2sc')):
                tempString = str(v).strip()
                if len(tempString)>0:
                    segments.append(innerConvert(tempString, convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class jpNameRecognition(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            jpNameSegment = HanLP.newSegment().enableJapaneseNameRecognize(True)
            segments = []
            for v in jpNameSegment.seg(innerConvert(content, '2sc')):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class translatedNameRecognition(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            tranNameSegment = HanLP.newSegment().enableTranslatedNameRecognize(True)
            segments = []
            for v in tranNameSegment.seg(innerConvert(content, '2sc')):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class indexTokenizer(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            IndexTokenizer = JClass('com.hankcs.hanlp.tokenizer.IndexTokenizer')
            segments = []
            for v in IndexTokenizer.segment(innerConvert(content, '2sc')):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}

class keyword(Resource):
    '''
    # hanLP 原生 keyword
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        num = parser.parse_args()['num']
        if len(content)>0:
            generalProcess(content)
            segments = []
            for v in HanLP.extractKeyword(innerConvert(content, '2sc'), int(num)):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
    '''

    def getListByTag(self, segResult, tag):
        tempList = []
        tempDict = {}
        returnList = []

        for v in segResult:
            tempString = str(v).strip()
            if len(tempString)>0 and tempString.find('/'+tag)>1:
                tempList.append(tempString)

        tempSet = set(tempList)
        for item in tempSet:
            tempDict[item] = tempList.count(item)

        import operator, re
        sortedList = sorted(tempDict.items(), key=operator.itemgetter(1))
        sortedList.reverse()
        
        for v in sortedList:
            tempString = re.sub(r'(\/)\w+', '', v[0])
            # print('tempString: ', tempString ,', ', len(tempString), ', ', v[0])
            if len(tempString) >= 2:
                returnList.append( tempString )

        return returnList

    # 用StandardTokenizer 取出名詞並統計數量，取重複次數多的
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        num = parser.parse_args()['num']
        if not num:
            return {'error': { 'num': '必須輸入 num，為keyword數量'}}

        if len(content)>0:
            generalProcess(content)
            Config.ShowTermNature = True
            segments = []

            StandardTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
            StandardTokenizer.SEGMENT.enableNumberQuantifierRecognize(True)
            StandardTokenizer.SEGMENT.enableCustomDictionary(False)
            segemntTool = StandardTokenizer.segment

            segResult = segemntTool(innerConvert(content, '2sc'))

            keywordList = self.getListByTag(segResult, 'n')

            for i in range(0,num):
                if i < len(keywordList):
                    segments.append(innerConvert(keywordList[i], convertMode))
                else:
                    break

            tempList = []
            for v in list(segResult):
                tempList.append(str(v))
            apiLogging.keyword('segResult: ' + innerConvert(', '.join(tempList) ,convertMode))
            apiLogging.keyword('keywordList: ' + innerConvert(', '.join(keywordList) ,convertMode))
            if len(segments)==0:
                apiLogging.keyword('has no segments')
                
            return {'response': segments}
        else: 
            return {'error': { 'content': '長度不得為零'}}
class addKeyword(Resource):
    def post(self):
        keywords = parser.parse_args()['keywords']
        result = ds.addKeyword(keywords)
        if result == 'succes':
            return {'response': result}
        else:
            return {'error': result}

class nlpTokenizer(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            segments = []
            NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
            for v in NLPTokenizer.segment(innerConvert(content, '2sc')):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class urlTokenizer(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        num = parser.parse_args()['num']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            sentence = []
            URLTokenizer = JClass('com.hankcs.hanlp.tokenizer.URLTokenizer')
            for v in URLTokenizer.segment(innerConvert(content, '2sc')):
                sentence.append(innerConvert(str(v), convertMode))
            return {'response': sentence}
        else:
            return {'error': { 'content': '長度不得為零'}}
class notionalTokenizer(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            segments = []
            #去除停用词
            # print(NotionalTokenizer.segment(content))
            #去除停用词+斷句
            # print(NotionalTokenizer.seg2sentence(content))

            NotionalTokenizer = JClass('com.hankcs.hanlp.tokenizer.NotionalTokenizer')
            for v in NotionalTokenizer.segment(innerConvert(content, '2sc')):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class numberAndQuantifierRecognition(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            segments = []
            StandardTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
            StandardTokenizer.SEGMENT.enableNumberQuantifierRecognize(True)
            for v in StandardTokenizer.segment(innerConvert(content, '2sc')):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class organizationRecognition(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            segments = []
            segemntTool = HanLP.newSegment().enableOrganizationRecognize(True)
            for v in segemntTool.seg(innerConvert(content, '2sc')):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class phraseExtractor(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        num = parser.parse_args()['num']
        if len(content)>0:
            segments = []
            for v in HanLP.extractPhrase(innerConvert(content, '2sc'), num):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class placeRecognition(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            segments = []
            segemntTool = HanLP.newSegment().enablePlaceRecognize(True)
            for v in segemntTool.seg(innerConvert(content, '2sc')):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class posTagging(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            generalProcess(content)
            generalSetting()
            segments = []
            segemntTool = HanLP.newSegment().enablePartOfSpeechTagging(True)
            for v in segemntTool.seg(innerConvert(content, '2sc')):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}

class rewrite(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            CoreSynonymDictionary = JClass('com.hankcs.hanlp.dictionary.CoreSynonymDictionary')
            result = CoreSynonymDictionary.rewrite(innerConvert(content, '2sc'))
            return {'response': innerConvert(result, convertMode)}
        else:
            return {'error': { 'content': '長度不得為零'}}
'''
class suggester(Resource):
    def post(self):
        content = parser.parse_args()['content']
        mode = parser.parse_args()['mode']
        if len(content)>0:
            Suggester = JClass('com.hankcs.hanlp.suggest.Suggester')
            return {'response': suggester.suggest(content, mode)}
        else:
            return {'error': { 'content': '長度不得為零'}}
'''
class summary(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        num = parser.parse_args()['num']
        if len(content)>0:
            sentence = []
            for v in HanLP.extractSummary(innerConvert(content, '2sc'), 3):
                sentence.append(innerConvert(str(v), convertMode))
            return {'response': sentence}
        else:
            return {'error': { 'content': '長度不得為零'}}
class wordDistance(Resource):
    def post(self):
        compare = parser.parse_args()['compare']
        if compare:
            CoreSynonymDictionary = JClass('com.hankcs.hanlp.dictionary.CoreSynonymDictionary')

            distance = CoreSynonymDictionary.distance(innerConvert(compare[0], '2sc'), innerConvert(compare[1], '2sc'))
            similarity = CoreSynonymDictionary.similarity(innerConvert(compare[0], '2sc'), innerConvert(compare[1], '2sc'))
            return {'response': {
                'compare': compare,
                'distance': distance,
                'similarity': similarity
                }
            }
        else:
            return {'error': { 'compare': '存放字串陣列 內含兩個要比對的字串, *必要欄位'}}
class wordOccurrence(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            generalProcess(content)
            content = innerConvert(content, '2sc')

            Occurrence = JClass('com.hankcs.hanlp.corpus.occurrence.Occurrence')
            occurrence = Occurrence()
            occurrence.addAll(content)
            occurrence.compute()

            uniGramObj = {}
            uniGram = occurrence.getUniGram()
            for v in uniGram:
                key = innerConvert(v.getKey(), convertMode)
                uniGramObj[key] = v.getValue().toString().replace(v.getKey()+'=', '')

            return {'response': uniGramObj}
        else:
            return {'error': { 'content': '長度不得為零'}}

class toTC(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.convertToTraditionalChinese(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class toSC(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.convertToSimplifiedChinese(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class tw2s(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.tw2s(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class s2tw(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.s2tw(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class hk2s(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.hk2s(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class s2hk(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.s2hk(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class hk2tw(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.hk2tw(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class tw2hk(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.tw2hk(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class t2tw(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.t2tw(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class t2hk(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.t2hk(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class tw2t(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.tw2t(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class hk2t(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            generalProcess(content)
            result = HanLP.hk2t(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}



# 分詞工具
api.add_resource(segment, '/segment')
api.add_resource(tcSegment, '/tcSegment')
api.add_resource(crfSegment, '/crfSegment')
api.add_resource(jpNameRecognition, '/jpName')
api.add_resource(translatedNameRecognition, '/translatedName')
api.add_resource(indexTokenizer, '/indexTokenizer')


# NLP 分詞
api.add_resource(nlpTokenizer, '/nlpTokenizer')

# 分析並回傳文章重點keyword
api.add_resource(keyword, '/keyword')

# 新增keyword到自訂辭典
api.add_resource(addKeyword, '/addKeyword')

# 分詞優先分出url
api.add_resource(urlTokenizer, '/urlTokenizer')

# 去除停用詞 todo
# api.add_resource(notionalTokenizer, '/notionalTokenizer')

# 分詞優先分出量詞
api.add_resource(numberAndQuantifierRecognition, '/quantifier')

# 分詞優先分出組織
api.add_resource(organizationRecognition, '/org')

# 分詞優先分出地名
api.add_resource(placeRecognition, '/place')

# 分析並回傳片語
api.add_resource(phraseExtractor, '/phrase')

api.add_resource(posTagging, '/posTagging')

# 文章重寫
api.add_resource(rewrite, '/rewrite')

# api.add_resource(suggester, '/suggester')

# 文章總結
api.add_resource(summary, '/summary')

# 比對字串的相似性 todo
api.add_resource(wordDistance, '/wordDistance')

# 單詞出現次數
api.add_resource(wordOccurrence, '/wordOccurrence')


# 文字轉換
api.add_resource(toTC, '/convert/2tc')
api.add_resource(toSC, '/convert/2sc')
api.add_resource(tw2s, '/convert/tw2s')
api.add_resource(s2tw, '/convert/s2tw')
api.add_resource(hk2s, '/convert/hk2s')
api.add_resource(s2hk, '/convert/s2hk')
api.add_resource(hk2tw, '/convert/hk2tw')
api.add_resource(tw2hk, '/convert/tw2hk')
api.add_resource(t2tw, '/convert/t2tw')
api.add_resource(t2hk, '/convert/t2hk')
api.add_resource(tw2t, '/convert/tw2t')
api.add_resource(hk2t, '/convert/hk2t')

initialize()

if __name__ == '__main__':
    app.run('0.0.0.0', 5001, debug=False)

