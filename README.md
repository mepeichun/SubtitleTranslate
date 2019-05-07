# SubtitleTranslate
Translate English subtilte into other language.
Only support \*.srt file currently.
(Please forgive me for my poor English T_T)

## Prerequisite

    pip install pyexecjs
    pip install srt

if you are from China, please install jieba

    pip install jieba

## How do it works
* parse \*.srt file into subtitle by *third party library srt* 
* split subtitle into sentences.
* translate sentences by Google Translate.
* split sentences into dialogues.
* merge original subtitle and translated subtitle

## How to use
clone or download *util_trans.py*, *util_srt.py*, *utils.py* into your working dictionary.

```python
from utils import translate_and_compose

input_file = "sample.en.srt"

# Translate the subtitle into Chinese, save both English and Chinese to the output srt file
# translate_and_compose(input_file, output_file, src_lang, target_lang, encoding='UTF-8', mode='split', both=True, space=False)
translate_and_compose(input_file, 'sample_en_cn_both.srt', 'en', 'zh-CN')
# translate_and_compose(input_file, 'sample_en_cn_both.srt', 'en', 'zh-CN', encoding='UTF-8-sig')


# Translate the subtitle into Chinese, save only Chinese subtitle to the output srt file
translate_and_compose(input_file, 'sample_cn_only.srt', 'en', 'zh-CN', both=False)

# Translate the subtitle into German, save both English and German to the output srt file
# In German language, each words separated by space, so space=True
translate_and_compose(input_file, 'sample_en_de_both.srt', 'en', 'de', space=True)

# Translate the subtitle into Japanese, save both English and Japanese to the output srt file
# In Japanese(Chinese, Korean), words are characters which are NOT separated by space, so space=False (default)
translate_and_compose(input_file, 'sample_en_ja_both.srt', 'en', 'ja')
```

## More

Original subtitle:

    1
    00:00:00,000 --> 00:00:02,430
    Coding has been
    the bread and butter for
    2
    00:00:02,430 --> 00:00:04,290
    developers since
    the dawn of computing.

Translate into Chinese:

    1
    00:00:00,000 --> 00:00:02,430
    自计算机开始以来，编码
    Coding has been the bread and butter for 
    2
    00:00:02,430 --> 00:00:04,290
    一直是开发人员的必需品。
    developers since the dawn of computing. 
 
 Translate into Japanese:
 
     1
    00:00:00,000 --> 00:00:02,430
    コーディングは、コンピューティングの夜
    Coding has been the bread and butter for 
    2
    00:00:02,430 --> 00:00:04,290
    明け以来、開発者にとって重要な要素です。
    developers since the dawn of computing. 
 
 ## Adavance
 
 ### If you meet some problem in *srt.parse()*
 
 Try another encoding method, like encoding='UTF-8-sig'
 
    translate_and_compose(input_file, 'sample_en_cn_both.srt', 'en', 'zh-CN', encoding='UTF-8-sig')
 
 ### There two tanslation mode. 
 
 If your srt file is well-splitted like:
 
    1
    00:00:00,000 --> 00:00:04,290
    Coding has been the bread and butter for developers since the dawn of computing.

 Well-splitted means each line is a sentence.
 
 So, you should use:
 
 ```python
from utils import translate_and_compose

input_file = "sample.en.srt"

# Translate the subtitle into Chinese, save both English and Chinese to the output srt file
# translate_and_compose(input_file, output_file, src_lang, target_lang, encoding='UTF-8', mode='split', both=True, space=False)
translate_and_compose(input_file, 'sample_en_cn_both.srt', 'en', 'zh-CN', mode='naive')
```
If one sentence may be splitted into multiple lines in the srt file. Please use *mode='split'*

### about the target language

Explore more google translate supported language please visit: https://cloud.google.com/translate/docs/languages

        Afrikaans	af      Albanian	sq      Amharic	am      Arabic	ar      Armenian	hy      Azerbaijani	az
        Basque	eu          Belarusian	be      Bengali	bn      Bosnian	bs      Bulgarian	bg      Catalan	ca
        Cebuano	ceb         Chinese(Simplified)	zh-CN           Chinese (Traditional)	zh-TW
        Corsican	co      Croatian	hr      Czech	cs      Danish	da      Dutch	nl          English	en
        Esperanto	eo      Estonian	et      Finnish	fi      French	fr      Frisian	fy          Galician	gl
        Georgian	ka      German	de          Greek	el      Gujarati	gu  Haitian Creole	ht  Hausa	ha
        Hawaiian	haw     Hebrew	he          Hindi	hi      Hmong	hmn     Hungarian	hu      Icelandic	is
        Igbo	ig          Indonesian	id      Irish	ga      Italian	it      Japanese	ja      Javanese	jw
        ...
    English, French, German ... are the language that split each word in a sentence by space
    Chinese, Japanese are NOT the language that split each word in a sentence by space

# README in Chinese

## 
字幕翻译，目前仅支持\*.srt 文件

## Python第三方库

    pip install pyexecjs
    pip install srt

同时请安装中文分词库“结巴”

    pip install jieba
    
    
## 工作原理
* 利用谷歌翻译实现，使用前请安装*pyexecjs*库，使用*pip install pyexecjs*进行安装即可
* 根据英文字幕的句号、感叹号、问号进行断句，再切割翻译得来的中文
* 若文件太大，则将文件切割成若干部分进行翻译（谷歌翻译限制字数）


## 使用方法
下载 *util_trans.py*, *util_srt.py*, *utils.py* 到你的工作路径
```python
from utils import translate_and_compose

input_file = "sample.en.srt"

# 把英文字幕翻译为 中英双语字幕
# translate_and_compose(input_file, output_file, src_lang, target_lang, encoding='UTF-8', mode='split', both=True, space=False)
translate_and_compose(input_file, 'sample_en_cn_both.srt', 'en', 'zh-CN')
# translate_and_compose(input_file, 'sample_en_cn_both.srt', 'en', 'zh-CN', encoding='UTF-8-sig')
```


