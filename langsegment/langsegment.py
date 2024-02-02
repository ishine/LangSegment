"""
This file bundles language identification functions.

Modifications (fork): Copyright (c) 2021, Adrien Barbaresi.

Original code: Copyright (c) 2011 Marco Lui <saffsd@gmail.com>.
Based on research by Marco Lui and Tim Baldwin.

See LICENSE file for more info.
https://github.com/adbar/py3langid

Projects:
https://github.com/juntaosun/LangSegment
"""

import re
# import langid
import py3langid as langid
# pip install py3langid==0.2.2


# ===========================================================================================================
# 分词功能：将文章或句子里的例如（中/英/日/韩），按不同语言自动识别并拆分，让它更适合AI处理。
# 本代码专为各种 TTS 项目的前端文本多语种混合标注区分，多语言混合训练和推理而编写。
# ===========================================================================================================
# （1）自动分词：“韩语中<ja>的오빠读什么呢？あなたの体育の先生は誰ですか? 此次发布会带来了四款iPhone 15系列机型”
# （2）手动分词：“你的名字叫<ja>佐々木？<ja>吗？”
# 本处理结果主要针对（中文=zh , 日文=ja , 英文=en , 韩语=ko）, 实际上可支持多达 97 种不同的语言混合处理。
# ===========================================================================================================


# 手动分词标签规范：<语言标签>文本内容</语言标签>
# ===========================================================================================================
# 如需手动分词，标签需要成对出现，如：“<ja>佐々木<ja>”  或者  “<ja>佐々木</ja>”
# 错误示范：“你的名字叫<ja>佐々木。” 此句子中出现的单个<ja>标签将被忽略，不会处理。
# ===========================================================================================================

class LangSegment():
    
    _text_cache = {}
    
    # 可自定义语言匹配标签：
    # <zh>你好<zh> , <ja>佐々木</ja> , <en>OK<en> , <ko>오빠</ko> 这些写法均支持
    SYMBOLS_PATTERN = r'(<([a-zA-Z|-]*)>(.*?)<\/*[a-zA-Z|-]*>)'
    
    @staticmethod
    def _is_english_word(word):
        return bool(re.match(r'^[a-zA-Z]+$', word))

    @staticmethod
    def _is_chinese(text):
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
    
    @staticmethod
    def _insert_english_uppercase(text):
        modified_text = re.sub(r'(?<!\b)([A-Z])', r' \1', text)
        return modified_text.strip('-')

    @staticmethod
    def _addwords(words,language,text,newline=False):
        if text is None:return True
        if language is None:language = ""
        language = language.lower()
        if language == 'en':
            text = LangSegment._insert_english_uppercase(text)
        if newline == False:
            preResult = None
            if len(words) > 0:
                preResult = words[-1]
            if preResult and (preResult["lang"] == language or not text.strip()):
                text = preResult["text"] + text
                preResult["text"] = text
                return True
        words.append({"lang":language,"text": text})
        return False
    
    @staticmethod
    def _split_sentence(sentence):
        words = []
        segments = re.split(r'([a-zA-Z]+)', sentence)
        for segment in segments:
            if LangSegment._is_english_word(segment):
                language = "en"
                LangSegment._addwords(words,language,segment)
            else:
                korean_pattern = re.compile('([\uac00-\ud7a3]+)')
                split_words = re.split(korean_pattern,segment)
                for segment in split_words:
                    language = 'zh'
                    regex_pattern = re.compile(r'(\s+|[^\w\s]+)')
                    lines = regex_pattern.split(segment)
                    lines_max = len(lines)
                    passlist = {}
                    for index, text in enumerate(lines):
                        if index in passlist:continue
                        nextId = index + 1
                        nextText = lines[nextId] if index < (lines_max - 1) else None
                        ispunc = re.sub(regex_pattern,'',text) == ""
                        if ispunc == True or text == "" or (len(text) == 1 and regex_pattern.match(text)):
                            if nextText is not None:
                                lines[nextId] = f'{text}{nextText}'
                            elif len(words) > 0:
                                data = words[-1]
                                data['text'] += text
                            continue
                        if nextText is not None and len(nextText) == 1 and regex_pattern.match(nextText):
                            text += nextText
                            passlist[nextId] = True
                            pass
                        check_text = re.sub(regex_pattern, '', text) 
                        language, _ = langid.classify(check_text)
                        if len(check_text) <= 2 and LangSegment._is_chinese(check_text):language = "zh" 
                        LangSegment._addwords(words,language,text)
                        pass
        return words
    
    @staticmethod
    def _parse_symbols(text):
        pattern = re.compile(LangSegment.SYMBOLS_PATTERN)
        matches = pattern.findall(text)
        LangSegment._text_cache = {}
        for i , match in enumerate(matches):
            key = f"[{i:06d}]"
            text = re.sub(pattern , key , text , count=1)
            LangSegment._text_cache[key] = match
        pattern = LangSegment.SYMBOLS_PATTERN.replace('(.*?)',"|")
        text = re.sub(pattern , '' , text)
        pattern = re.compile(r'(\[[\d]{6,}\]+)')
        segments = re.split(pattern, text)
        words = []
        text_cache = LangSegment._text_cache
        for line in segments:
            if line in text_cache:
                match = text_cache[line]
                language = match[1]
                text = match[2]
                LangSegment._addwords(words,language,text,True)
                pass
            else:
                result = LangSegment._split_sentence(line)
                words += result
                pass
        return words
    
    @staticmethod
    def getTexts(text:str):
        if text is None or len(text.strip()) == 0:return []
        text = LangSegment._parse_symbols(text)
        return text
    
    @staticmethod
    def classify(text:str):
        return LangSegment.getTexts(text)
    
    

def getTexts(text:str):
    return LangSegment.getTexts(text)


def classify(text:str):
    return LangSegment.classify(text)
    
    
if __name__ == "__main__":
    
    # 分词示例：
    text = "你的名字叫<ja>佐々木？<ja>吗？韩语中的오빠读什么呢？あなたの体育の先生は誰ですか? 此次发布会带来了四款iPhone 15系列机型和三款Apple Watch等一系列新品，这次的iPad Air采用了LCD屏幕" 
    langlist = LangSegment.getTexts(text)
    print("=================================")
    for line in langlist:
        print(line)
    print("=================================")
    
    # 分词输出：lang=语言，text=内容
    # =================================
    # {'lang': 'zh', 'text': '你的名字叫'}
    # {'lang': 'ja', 'text': '佐々木？'}
    # {'lang': 'zh', 'text': '吗？韩语中的'}
    # {'lang': 'ko', 'text': '오빠'}
    # {'lang': 'zh', 'text': '读什么呢？'}
    # {'lang': 'ja', 'text': 'あなたの体育の先生は誰ですか?'}
    # {'lang': 'zh', 'text': ' 此次发布会带来了四款'}
    # {'lang': 'en', 'text': 'i Phone'}
    # {'lang': 'zh', 'text': ' 15系列机型和三款'}
    # {'lang': 'en', 'text': 'Apple Watch'}
    # {'lang': 'zh', 'text': '等一系列新品，这次的'}
    # {'lang': 'en', 'text': 'i Pad Air'}
    # {'lang': 'zh', 'text': '采用了'}
    # {'lang': 'en', 'text': 'L C D'}
    # {'lang': 'zh', 'text': '屏幕'}
    # =================================