import LangSegment


if __name__ == "__main__":
    
    
    # 输入示例：（包含日文，中文，韩语，英文）
    text = "你的名字叫<ja>佐々木？<ja>吗？韩语中的안녕 오빠读什么呢？あなたの体育の先生は誰ですか? 此次发布会带来了四款iPhone 15系列机型和三款Apple Watch等一系列新品，这次的iPad Air采用了LCD屏幕" 
    
    
    # 进行分词：（接入TTS项目仅需一行代码调用）
    langlist = LangSegment.getTexts(text)
    print("\n\n===================【打印结果】===================")
    for line in langlist:
        print(line)
    print("==================================================\n")
    
    
    # 分词输出：lang=语言，text=内容
    # ===================【打印结果】===================
    # {'lang': 'zh', 'text': '你的名字叫'}
    # {'lang': 'ja', 'text': '佐々木？'}
    # {'lang': 'zh', 'text': '吗？韩语中的'}
    # {'lang': 'ko', 'text': '안녕 오빠'}
    # {'lang': 'zh', 'text': '读什么呢？'}
    # {'lang': 'ja', 'text': 'あなたの体育の先生は誰ですか?'}
    # {'lang': 'zh', 'text': ' 此次发布会带来了四款'}
    # {'lang': 'en', 'text': 'i Phone '}
    # {'lang': 'zh', 'text': '15系列机型和三款'}
    # {'lang': 'en', 'text': 'Apple Watch'}
    # {'lang': 'zh', 'text': '等一系列新品，这次的'}
    # {'lang': 'en', 'text': 'i Pad Air'}
    # {'lang': 'zh', 'text': '采用了'}
    # {'lang': 'en', 'text': 'L C D'}
    # {'lang': 'zh', 'text': '屏幕'}
    # ===================【语种统计】===================
    
    # 功能二，语种统计:
    print("\n===================【语种统计】===================")
    # 获取所有语种数组结果，根据内容字数降序排列
    langCounts = LangSegment.getCounts()
    print(langCounts , "\n")
    
    # 根据结果获取内容的主要语种 (语言，字数含标点)
    lang , count = langCounts[0] 
    print(f"输入内容的主要语言为 = {lang} ，字数 = {count}")
    print("==================================================\n")

    # ===================【语种统计】===================
    # [('zh', 51), ('en', 33), ('ja', 19), ('ko', 5)]

    # 输入内容的主要语言为 = zh ，字数 = 51
    # ==================================================