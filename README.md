# LangSegment
**<font size=3 color='#00FFFF'>简介：它是一个多语言（97种语言）的混合文本内容自动识别和拆分工具。[中日英韩：已测试]</font>**   
**<font size=3 color='#00FFFF'>主要用途：各种 TTS 语音合成项目的前端，多语种文本混合预处理（训练和推理）。</font>**   

它基于 py3langid 的扩展实现（>=python3.6）。  
``LangSegment`` It is a multi-lingual (97 languages) text content automatic recognition and segmentation tool.  
The main purposes are: front-end for various TTS (Text-to-Speech) synthesis projects, preprocessing of multilingual text mixing for both training and inference.  

>Implementation based on py3langid，See LICENSE file for more info.  
https://github.com/adbar/py3langid  


---    

功能：将文章或句子里的例如（中/英/日/韩），按不同语言自动识别并拆分，适合AI处理。    
本代码专为各种 TTS 项目的前端文本多语种混合标注区分，多语言混合训练和推理而编写。  

---    

（1）自动识别：“韩语中的오빠读什么呢？あなたの体育の先生は誰ですか? 此次带来了四款iPhone 15系列机型”  
（2）手动标注：“你的名字叫\<ja\>佐々木？\<ja\>吗？”  


>语言标签：它和html类似，它需要成对出现 \<zh\>内容\<zh\>  或者  \<zh\>内容\</zh\>。    
本处理结果主要针对（中文=zh , 日文=ja , 英文=en , 韩语=ko）, 实际上可支持多达 97 种不同的语言混合处理。    

---     

安装方法：Install  
```bash
pip3 install LangSegment

# 或者，国内推荐使用镜像安装：  
pip3 install LangSegment -i https://pypi.mirrors.ustc.edu.cn/simple
```
使用示例：Example Input  
>示例中的句子，同时包含中日英韩4种语言，接下来将对它们分语种进行拆分，以方便TTS项目进行语音合成。  
```python

    # pip3 install LangSegment
    import LangSegment

    # input text example 示例：
    text = "你的名字叫<ja>佐々木？<ja>吗？韩语中的오빠读什么呢？あなたの体育の先生は\
    誰ですか? 此次发布会带来了四款iPhone 15系列机型\
    和三款Apple Watch等一系列新品，这次的iPad Air采用了LCD屏幕" 

    # example
    langlist = LangSegment.getTexts(text)

    # output list : {'lang': 'zh', 'text': '...'}
    print("=================================")
    for line in langlist:
        print(line)
    print("=================================")
```
处理结果：Example Output  
```python
    # output 输出列表行：lang=语言，text=内容
    # ===========================================================================
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
    # ===========================================================================
    # 其中英文缩写字母如“LCD”，英文标准发音为“L-C-D”，
    # 而在语音合成TTS项目中，一般用空格隔开字母来单独发音：“L C D”
```

上述代码对text的输入进行自动分词，针对中日汉字重叠问题，解决方案如下：  
（1）方案1：在中文与日文句子之间，打上空格来辅助区分。  
（2）方案2：您可手动添加语言标签\<ja\>,\<ko\>,\<zh\>,\<en\>等来辅助处理以进行强制区分。  
以下是语言标签详细示例：   
```python
    # 手动标签的应用示例，例如针对中日汉字有重叠，而需要在 TTS 中混合发音的情况：
    # 标签内的文本将识别成日文ja内容，也可以写成<ja>内容</ja>
    text = "你的名字叫<ja>佐々木？<ja>"  
    # 或者：
    text = "你的名字叫<ja>佐々木？</ja>"  
    # 以上均能正确输出：
    # 处理成中文-- {'lang': 'zh', 'text': '你的名字叫'}
    # 处理成日文-- {'lang': 'ja', 'text': '佐々木？'}
```
它支持高达97种语言的识别和折分，目前主要针对中文(zh)/日文(ja)/英文(en)/韩文(ko)。以下是输出结果：  
它特别适合各种 TTS 前端文本多语种内容的混合标注（自动/手动），训练和推理使用。  

```python
    # 手动标签规范：<语言标签>文本内容</语言标签>
    # ===========================================================================
    # 如需手动标注，标签需要成对出现，如：“<ja>佐々木<ja>”  或者  “<ja>佐々木</ja>”
    # 错误示范：“你的名字叫<ja>佐々木。” 此句子中出现的单个<ja>标签将被忽略，不会处理。
    # ===========================================================================
```  

---
---
> 备注：语音合成测试内容，目前主要针对中日英韩4种。  
其它语种未作具体测试，如有Bug和优化建议，欢迎提出或指正，感谢~。  
Note: The speech synthesis test content is currently mainly for four categories: Chinese, Japanese, English and Korean.     
Other languages have not been specifically tested. If there are any bugs or optimization suggestions, please feel free to raise them or correct them. Thank you~  
Special thanks to the following projects: [py3langid](https://github.com/adbar/py3langid)
---
---