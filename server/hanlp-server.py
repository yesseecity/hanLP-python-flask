# coding=UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import dicInitialize

from jpype import *
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_restful.representations.json import output_json
output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding': 'utf8'}


# Parameters 
innerConvertEnable = True


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

hanLPLibPath = '/hanlp/server/lib/hanlp-1.3.2/'
javaClassPath = hanLPLibPath+'hanlp-1.3.2.jar'+':'+hanLPLibPath

startJVM(getDefaultJVMPath(), '-Djava.class.path='+javaClassPath, '-Xms1g', '-Xmx1g')
HanLP = JClass('com.hankcs.hanlp.HanLP')

parser.add_argument('content', type=str, required=True, help='content無法解析, *必要欄位')
parser.add_argument('convertMode', type=str)
parser.add_argument('num', type=int)
parser.add_argument('mode', type=int)
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
    print 'initialize'
    LexiconUtility = JClass('com.hankcs.hanlp.utility.LexiconUtility')
    dicInitialize.dynamicDic(LexiconUtility)

## For router
class segment(Resource):
    def post(self):
        parser.add_argument('method', type=str, required=False)
        content = parser.parse_args()['content']
        # method = parser.parse_args()['method']

        # if method == 'NShort':
        #     NShortSegment = JClass('com.hankcs.hanlp.seg.NShort.NShortSegment')
        #     segemntTool = NShortSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)
        #     print segemntTool
        #     print segemntTool.__class__
        #     print segemntTool(content)
        # elif method == 'Viterbi':
        #     ViterbiSegment = JClass('com.hankcs.hanlp.seg.Viterbi.ViterbiSegment')
        #     segemntTool = ViterbiSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)
        # else:
        segemntTool = HanLP.segment

        if len(content)>0:
            segments = []
            for v in segemntTool(content):
                segments.append(str(v))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class tcSegment(Resource):
    def post(self):
        parser.add_argument('method', type=str, required=False)
        content = parser.parse_args()['content']

        if len(content)>0:
            segments = []
            tcTokenizer = JClass('com.hankcs.hanlp.tokenizer.TraditionalChineseTokenizer')
            for v in tcTokenizer.segment(content):
                segments.append(str(v))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class crfSegment(Resource):
    def post(self):
        parser.add_argument('method', type=str, required=False)
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            segments = []
            CRFSegment = JClass('com.hankcs.hanlp.seg.CRF.CRFSegment')
            segemntTool = CRFSegment().seg
            for v in segemntTool(innerConvert(content, '2sc')):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class jpNameRecognition(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
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

# class parseDependency(Resource):
#     def post(self):
#         content = parser.parse_args()['content']
#         if len(content)>0:
#             # segments = []
#             # for v in HanLP.parseDependency(content):
#             #     segments.append(str(v))
#             # return {'response': segments}
#             result = HanLP.parseDependency(content)
#             print result
#             # result2 = result.getWordArray()
#             # print result2
#             print type(result)
#             # return HanLP.parseDependency(content)
#         else:
#             return {'error': { 'content': '長度不得為零'}}

class keyword(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        num = parser.parse_args()['num']
        if len(content)>0:
            segments = []
            for v in HanLP.extractKeyword(innerConvert(content, '2sc'), int(num)):
                segments.append(innerConvert(str(v), convertMode))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零'}}
class nlpTokenizer(Resource):
    def post(self):
        content = parser.parse_args()['content']
        convertMode = parser.parse_args()['convertMode']
        if len(content)>0:
            NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
            segments = []
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
            URLTokenizer = JClass('com.hankcs.hanlp.tokenizer.URLTokenizer')
            sentence = []
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
            NotionalTokenizer = JClass('com.hankcs.hanlp.tokenizer.NotionalTokenizer')
            
            segments = []
            #去除停用词
            # print NotionalTokenizer.segment(content)
            #去除停用词+斷句
            # print NotionalTokenizer.seg2sentence(content)

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
            StandardTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
            StandardTokenizer.SEGMENT.enableNumberQuantifierRecognize(True)
            segments = []
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
            segemntTool = HanLP.newSegment().enableOrganizationRecognize(True)
            segments = []
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
            segemntTool = HanLP.newSegment().enablePlaceRecognize(True)
            segments = []
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
            segemntTool = HanLP.newSegment().enablePartOfSpeechTagging(True)
            segments = []
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

# class suggester(Resource):
#     def post(self):
#         content = parser.parse_args()['content']
#         mode = parser.parse_args()['mode']
#         if len(content)>0:
#             Suggester = JClass('com.hankcs.hanlp.suggest.Suggester')
#             return {'response': suggester.suggest(content, mode)}
#         else:
#             return {'error': { 'content': '長度不得為零'}}
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
        content = parser.parse_args()['content']
        if len(content)>0:
            parser.add_argument('comparedTo', type=str, required=True, action='append_const', help='comparedTo無法解析, 存放字串陣列 內含兩個要比對的字串, *必要欄位')
            comparedTo = parser.parse_args()['comparedTo']

            CoreSynonymDictionary = JClass('com.hankcs.hanlp.dictionary.CoreSynonymDictionary')

            distance = CoreSynonymDictionary.distance(innerConvert(comparedTo[0], '2sc'), innerConvert(comparedTo[1], '2sc'))
            similarity = CoreSynonymDictionary.similarity(innerConvert(comparedTo[0], '2sc'), innerConvert(comparedTo[1], '2sc'))
            return {'response': {
                'comparedTo': comparedTo,
                'distance': distance,
                'similarity': similarity
                }
            }
        else:
            return {'error': { 'content': '長度不得為零'}}

class convertToTraditionalChinese(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.convertToTraditionalChinese(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class convertToSimplifiedChinese(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.convertToSimplifiedChinese(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class tw2s(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.tw2s(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class s2tw(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.s2tw(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class hk2s(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.hk2s(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class s2hk(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.s2hk(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class hk2tw(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.hk2tw(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class tw2hk(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.tw2hk(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class t2tw(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.t2tw(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class t2hk(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.t2hk(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class tw2t(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
            result = HanLP.tw2t(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
class hk2t(Resource):
    def post(self):
        content = parser.parse_args()['content']
        if len(content)>0:
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

# api.add_resource(parseDependency, '/parseDependency')

# NLP 分詞
api.add_resource(nlpTokenizer, '/nlpTokenizer')

# 分析並回傳文章重點keyword
api.add_resource(keyword, '/keyword')


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
# api.add_resource(wordDistance, '/wordDistance')


# 文字轉換
api.add_resource(convertToTraditionalChinese, '/convert/2tc')
api.add_resource(convertToSimplifiedChinese, '/convert/2sc')
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

