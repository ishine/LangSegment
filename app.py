import json
import re
import gradio as gr
import LangSegment

# 如何安装？ How to install
# pip3 install LangSegment

# =================================================================
# 这是本项目的webui，运行脚本后，它将会打开浏览器网页，即可体验。
# This is the webui of this project. After running the script, it will open the browser web page and you can experience it.
# =================================================================


# 显示版本，display version
print("LangSegment:",LangSegment.__version__)

# --------------------------------
# color label table
langdic = {
    "zh":["Chinese"  , "#F1F1F1"   ],
    "en":["English"  , "green"     ],
    "ja":["Japanese" , "yellow"    ],
    "ko":["Korean"   , "blue"      ],
    "no":["None"     , "red"       ],
}

# --------------------------------
# Chinese translation，Can comment
langdic["zh"][0] = "中文(zh)"
langdic["en"][0] = "英文(en)"
langdic["ja"][0] = "日文(ja)"
langdic["ko"][0] = "韩文(ko)"
langdic["no"][0] = "其它"

# --------------------------------
# Set language filters
LangSegment.setLangfilters(["zh", "en", "ja", "ko"])

# --------------------------------

def getLanglabel(lang):
    lang = lang if lang in langdic else "no"
    fullKey = langdic[lang][0]
    return fullKey

color_map = {}
for lang in langdic:
    data = langdic[lang]
    fullKey , color = data[0] , data[1]
    color_map[fullKey] = color
# print(color_map)

# 处理：
def parse_language(input_text):
    noneKey = getLanglabel("no")
    output = ""
    codes = []
    codes.append(("\n",noneKey))
    # （1）处理分词 processing participle
    langlist = LangSegment.getTexts(input_text)
    for data in langlist:
        output += f'{str(data)}\n'
        lang = data['lang']
        text = data['text']
        text = re.sub(r'\n+','\n',text)
        codes.append((text , getLanglabel(lang)))
    codes.append(("\n\n",noneKey))
    # （2）统计分词 Statistical participle
    label_text = "没有结果显示"
    langCounts = LangSegment.getCounts()
    if len(langCounts) > 0:
        lang , count = langCounts[0] 
        label_text = f"您输入的主要语言为：【{getLanglabel(lang)}】。参考依据：{str(langCounts)}"
    return output , codes , label_text

# Translated from Google：
#LangSegment Text-to-Speech TTS Multilingual Word Segmentation\ n\
# < b > Introduction: It is a powerful multi-lingual (97 languages) hybrid text automatic word segmentation tool. [China, Japan, UK and Korea: Tested] </b > < br >\
# Main use: It is well-suited for various TTS Text To Speech projects (e.g. vits), front-end inference for multilingual mixed text, and pre-processing back-end training. LICENSE is detailed in the root directory < br >\
# < b > Connect it to your vits project and install it on python: pip3 install LangSegment\ t (CN domestic image): pip3 install LangSegment -i https://pypi.mirrors.ustc.edu.cn/simple </b > < br >\
# If you encounter any problems, please go to github to provide feedback and make it easier to use: https://github.com/juntaosun/LangSegment < br >\

# Translated from Google：
#  Instructions for use: The default is automatic word segmentation. You can also manually add language tags to get more accurate word segmentation results: < br >
#     (1) Automatic word segmentation: If you encounter Chinese and Japanese, the recognition error is due to the overlap of Chinese characters, you can type a space to assist word segmentation (automatic context word segmentation). < br >
#     (2) Manual word segmentation: language tags\ < ja\ > Japanese </ja\ >,\ < ko \>언니\</ ko\ >,\ < zh\ > Hello\ </zh\ >,\ < en\ > Hello World\ </en\ > to assist word segmentation. < br >
#     (3) English capital abbreviations: such as USA, ChatGPT. The result is: U S A, ChatG P T. Text To Speech is often separated by spaces to allow letters to be pronounced alone.

lang_desc = """
    使用说明：默认为自动分词，您也可以手动添加语言标签，来获得更精准的分词结果：<br>
    （1）自动分词：若遇到中文与日语，因汉字重叠相连而识别错误，您可打上空格来辅助分词（自动上下文分词）。<br>
    （2）手动分词：语言标签 \<ja\>日本語\</ja\>、\<ko\>언니\</ko\>、\<zh\>你好\</zh\>、\<en\>Hello World\</en\> 来辅助分词。 <br>
    （3）英文大写缩略词：如USA、ChatGPT。结果为：U S A、ChatG P T。语音合成常用空格分隔，让字母单独发音。
"""

gr_css = """
.lang_button {
    height: 80px;
}
"""

with gr.Blocks(title="LangSegment WebUI" , css=gr_css) as app:
    gr.Markdown(
        value=f"# LangSegment 文本转语音专用，TTS混合语种分词 [v{LangSegment.__version__}]\n \
        <b>简介：它是一个强大的多语言（97种语言）的混合文本自动分词工具。[中日英韩：已测试]</b><br> \
        主要用途：它非常适合各种 TTS 语音合成项目（例如：vits），多语种混合文本的前端推理，和预处理后端训练。LICENSE详见根目录<br> \
        <b>将它接入您的vits项目，在python上安装：``` pip3 install LangSegment -i  https://pypi.org/simple ```</b><br> \
        若遇到问题，欢迎前往github提供反馈，一起让它变得更易用： https://github.com/juntaosun/LangSegment <br> \
        "
    )
    with gr.Group():
        with gr.Row():
            with gr.Column():
                # [Word input]: Multilingual mixed text content. Currently specially supported (Chinese, Japanese, English, Korean)
                input_text  = gr.TextArea(label=f"【分词输入】：多语种混合文本内容。目前仅专注（中文Chinese、日文Japanese、英文English、韩文Korean）", value="",lines=15)
                # [Word segmentation statistics]: According to the processing results, predict the main language you entered.
                label_text = gr.Text(label="【分词统计】：根据处理结果，推测您输入的主要语言。", value="")
                gr.Markdown(value=f"{lang_desc}")
                # TTS multilingual mixed text, click for word segmentation
                lang_button = gr.Button("TTS多语言混合文本 , 点击进行分词处理", variant="primary",elem_classes=["lang_button"])
            with gr.Column():
                with gr.Tabs():
                    # A: Toggle the result to highlight
                    with gr.TabItem("A：切换高亮结果显示"):
                        with gr.Column():
                            # [Word segmentation result]: Multi-language mixed highlighting: different languages correspond to different colors.
                            codes_text = gr.HighlightedText(
                                label="【分词结果】：多国语言混合高亮显示：不同语言对应不同的颜色。", 
                                scale=2,
                                show_label=True,
                                combine_adjacent=True,
                                show_legend=True,
                                color_map=color_map,
                            )
                    # B: Toggle the result code display
                    with gr.TabItem("B：切换代码结果显示"):
                        with gr.Column():
                            # [Word segmentation result]: Multiple languages have been separated (Chinese, Japanese, English, Korean), just enter TTS Text To Speech directly.
                            output_text = gr.TextArea(label="【分词结果】：多国语言已经分离完成（中zh、日ja、英en、韩ko），直接输入TTS语音合成处理即可。", value="",lines=15)
            
        
        lang_button.click(
            parse_language,
            [input_text],
            [output_text , codes_text ,label_text],
        )
        
app.queue(concurrency_count=511, max_size=1022).launch(
    server_name="0.0.0.0",
    inbrowser=True,
    share=False,
    server_port=6066,
    quiet=True,
)