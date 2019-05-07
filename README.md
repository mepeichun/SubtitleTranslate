# SubtitleTranslate
Translate English subtilte into other language.
Only support \*.srt file currently.

## 翻译效果
    00:00:00,025 --> 00:00:03,403
    Hi, my name's Tim Roughgarden. I'm a professor here at Stanford University
    嗨，我叫Tim Roughgarden。我是斯坦福大学的教授嗨，我叫Tim，斯坦

    00:00:03,403 --> 00:00:06,283
    And I'd like to welcome you to this first course on the
    福大学的一名教授我想你欢迎来到第一次的算法设计和分析课程。

## 工作原理
* 利用谷歌翻译实现，使用前请安装*pyexecjs*库，使用*pip install pyexecjs*进行安装即可
* 根据英文字幕的句号、感叹号、问号进行断句，再切割翻译得来的中文
* 若文件太大，则将文件切割成若干部分进行翻译（谷歌翻译限制字数）
* 实际工作效果一般，因为课程字幕常常出现大量的专业词汇


## 使用方法
```python
def main():
    # 修改path即可
    # path文件夹及其子文件夹下的所有srt文件将被翻译
    # 并且将原始的srt文件命名为“backup+原始名字.srt”
    path = 'F:\\015_Algorithms Design and Analysis Part 1\\algo-004\\10_X._GRAPH_SEARCH_AND_CONNECTIVITY_Week_4'
    translate_file_in_path(path)
```

## 已知BUG
* 目前发现有些文件无法翻译
