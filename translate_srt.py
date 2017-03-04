'''
This is a script that translate the English *.srt file
 into Chinese&English *.srt file

Translate by Google!

Before using this script, make sure that you have been install "pyexecjs",
Otherwise, you can use pip install to install.

 pip install pyexecjs

'''
from __future__ import division
import re
import execjs
import urllib.request
import os


class Py4Js:
    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;

        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";

        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


def open_url(url, content):
    postdata = {
        'q': content
    }
    data = urllib.parse.urlencode(postdata).encode(encoding='utf-8')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, data=data, headers=headers)
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8')


def translate(subtitle):
    js = Py4Js()
    tk = js.getTk(subtitle)
    content = urllib.parse.quote(subtitle)
    url = "http://translate.google.cn/translate_a/single?client=t" \
          "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
          "&srcrom=0&ssel=0&tsel=0&kc=1&tk="+tk

    result = open_url(url, subtitle)
    p = re.compile(r'\["(.*?)(?:\\n)')
    return p.findall(result)


def getPosition(sentence_list):
    length_quene = []
    index_quene = []

    length_list = []
    index_list = []

    full_sentence_list = []

    pattern = re.compile(r".*(\.|\?|!)")
    index = 0

    full_sentence = ''
    for x in sentence_list:
        element_match = pattern.search(x)
        if element_match is not None:
            length_quene.append(element_match.end())
            index_quene.append(index)

            length_list.append(length_quene)
            index_list.append(index_quene)
            length_quene = []
            index_quene = []

            length_quene.append(len(x) - element_match.end() - 1)
            index_quene.append(index)

            full_sentence += x[0:element_match.end()]
            full_sentence_list.append(full_sentence)

            full_sentence = x[element_match.end()+1:]

        else:
            index_quene.append(index)
            length_quene.append(len(x))
            full_sentence += x
        index += 1
    # for i in range(len(full_sentence_list)):
    #     print(full_sentence_list[i])
    #     print(index_list[i])
    #     print(length_list[i])
    return full_sentence_list, index_list, length_list


def String_Recovery(after_translate, index_list, length_list):
    index = 0
    string_list = ['']
    for i in range(len(length_list)):
        after_translate[i] = re.sub(r'(",".*",,,3],\[")', '', after_translate[i])
        chinese_length = len(after_translate[i])
        english_length = sum(length_list[i])
        begin = 0
        end = 0
        length_sum = 0
        for j in range(len(index_list[i])):
            if index_list[i][j] == index:
                length_sum += length_list[i][j]
                end += int(chinese_length*length_sum/english_length)
                string_list[index] += after_translate[i][begin:end]
                begin = end
            else:
                index += 1
                string_list.append('')
                length_sum += length_list[i][j]
                end += int(chinese_length*length_sum / english_length)
                string_list[index] += after_translate[i][begin:end]
                begin = end
    return string_list


def translate_file(root, name):
    new_srt = os.path.join(root, name)
    backup_srt = os.path.join(root, 'backup'+name)
    os.rename(new_srt, backup_srt)

    f = open(backup_srt)
    fsrt = open(new_srt, "w", encoding='utf-8')
    content = f.read()
    result = re.findall(r'\d+\n(?:\d\d:){2}(?:\d\d),(?:\d){3} --> (?:\d\d:){2}(?:\d\d),(?:\d){3}', content)
    sentence = re.split(r'\d+(?:\d\d:){2}(?:\d\d),(?:\d){3} --> (?:\d\d:){2}(?:\d\d),(?:\d){3}', re.sub(r'\n','', content))
    sentence.pop(0)
    full_sentence_list, index_list, length_list = getPosition(sentence)

    sum_length = 0
    tmp_index = 0
    after_translate = []

    for i in range(len(full_sentence_list)):
        sum_length += len(full_sentence_list[i])
        if sum_length > 4500:
            tmp_list = translate('\n'.join(full_sentence_list[tmp_index:i]) + '\n' + 'end')
            tmp_list.pop()
            after_translate.extend(tmp_list)
            tmp_index = i
            sum_length = 0
            i -= 1

    tmp_list = translate('\n'.join(full_sentence_list[tmp_index:]) + '\n' + 'end')
    tmp_list.pop()
    after_translate.extend(tmp_list)
    # for i in range(len(full_sentence_list)):
    #     print("===================")
    #     print(full_sentence_list[i])
    #     print(after_translate[i])
    Chinese = String_Recovery(after_translate, index_list, length_list)
    for i in range(len(sentence)):
        fsrt.write(result[i] + '\n' + sentence[i] + '\n' + Chinese[i] + '\n\n')
    print("Translate subtitle file '" + new_srt + "' successfully!")


def translate_file_in_path(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            # print(name)
            # os.rename(os.path.join(path, file), os.path.join(path, newname))
            if re.search(r'.*\.srt', name, re.I) is not None:
                translate_file(root, name)


def main():
    # 修改path即可
    # path文件夹及其子文件夹下的所有srt文件将被翻译
    # 并且将原始的srt文件命名为“backup+原始名字.srt”
    path = 'F:\\015_Algorithms Design and Analysis Part 1\\'
    translate_file_in_path(path)


if __name__ == "__main__":
    main()


