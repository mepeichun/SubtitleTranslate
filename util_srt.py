import re
try:
    import jieba
except ImportError:
    print('If your target language is Chinese, please install third party library "jieba"')
    pass


class Splitter:
    def __init__(self):
        self.pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')

    def split(self, text):
        return self.pattern.split(text)


def triple_r(sub_list):
    """
    Remove the line break.
    Reconstruct plain text of the whole subtitle file.
    Record the index of each dialogue in the plain text.
    :param sub_list:
    :return: Plain text, dialog_idx
    """
    dialog_idx = []
    current_idx = 0
    plain_text = ''
    for sub in sub_list:
        sub.content = sub.content.replace('\n', ' ') + ' '  # remove line break
        current_idx += len(sub.content)
        dialog_idx.append(current_idx)  # record the position of dialogue in the plain text
        plain_text = plain_text + sub.content

    return plain_text[:-1], dialog_idx


def split_and_record(plain_text):
    """
    Split the plain text into sentences.
    Record the index of each sentence in the plain text.
    :param plain_text: Plain text output by triple_r(sub_list)
    :return: list of sentence, index of each sentence in the plain text
    """
    splitter = Splitter()
    sen_list = splitter.split(plain_text)
    sen_idx = [0]
    current_idx = 0
    for sen in sen_list:
        sen_len = len(sen) + 1
        current_idx += sen_len
        sen_idx.append(current_idx)
    return sen_list, sen_idx


def compute_mass_list(dialog_idx, sen_idx):
    """
    Most confusing step...

    dialog_idx = [41, 81, 134, ...]
        means the first dialogue of the subtitle is plain_text[0:41]
        the second dialogue of the subtitle is plain_text[41:81]
        the third dialogue of the subtitle is plain_text[81:134]

    sen_idx = [81, 204, ...]
        means the first sentence of the subtitle is plain_text[0:81]
        the second sentence of the subtitle is plain_text[81:204]

    Usually the len(dialog_idx) is larger than the len(sen_idx), because one sentence may so long
    that the video maker have to split it into multiple dialogues.

    What this function want to do is try to figure out each sentence belongs to which dialogues.

    For example:
        Sentence: Coding has been the bread and butter for developers since the dawn of computing.	[(5, 41), (6, 81)]
        means the "Coding has been the bread and butter for"(length equals to 41) is the 5th dialogue of the subtitle,
        "developers since the dawn of computing"(from position 41 to 81) is the 6th dialogue of the subtitle.

    mass_list = [[(1, a), (2, b)], [(3, c)], [(4, d), (5, e), (6, f)]]
    means a subtitle include 3 sentence (the length of the list record_each_sentence, len(record_each_sentence))
        In the first sentence: there are 2 dialogues, the first dialogue is first_sentence[0:a]
                                the second dialogue is first_sentence[a:b]
        In the second sentence: there are 1 dialogues, the third dialogue of the whole subtitle is second_sentence[0:c]


    :param dialog_idx:
    :param sen_idx:
    :return: record_each_sentence
    """
    i = 0
    j = 1
    mass_list = []
    one_sentence = []
    while i < len(dialog_idx):
        if dialog_idx[i] > sen_idx[j]:
            mass_list.append(one_sentence)
            one_sentence = []
            j += 1
        else:
            one_sentence.append((i + 1, dialog_idx[i] - sen_idx[j - 1]))
            i += 1
    mass_list.append(one_sentence)
    return mass_list


def get_the_nearest_space(sentence: str, current_idx: int):
    left_idx = sentence[:current_idx].rfind(' ')
    right_idx = sentence[current_idx:].find(' ')

    if current_idx - left_idx > right_idx:
        return right_idx + current_idx + 1
    else:
        return left_idx + 1


def get_the_nearest_split_sen_cn(sentence: str, current_idx: int, last_idx: int, scope=6):
    """
    Split Chinese sentence
    :param sentence: Chinese sentence
    :param current_idx:
    :param last_idx:
    :param scope:
    :return:
    """
    last_idx = last_idx if last_idx > current_idx - scope else current_idx - scope
    next_idx = current_idx + scope if current_idx + scope < len(sentence) else len(sentence)

    words = list(jieba.cut(sentence[last_idx:next_idx]))
    total_len = 0
    word_idx = 0
    target_idx = current_idx - last_idx
    for w in words:
        total_len += len(w)
        word_idx += 1
        if total_len >= target_idx:
            break
    if word_idx < len(words):
        if words[word_idx] == '\uff0c':
            total_len += len(words[word_idx])

    return total_len + last_idx


def sen_list2dialog_list(sen_list, mass_list, space=False, cn=False) -> list:
    """
    Convert the sentence list to dialogue list
    :param cn: is the target language is Chinese
    :param sen_list: sentence list (Translated)
    :param mass_list: mass_list compute by compute_mass_list(dialog_idx, sen_idx)
    :param space: is the vocabulary of target language split by space
    :return: dialog_list
    """
    dialog_num = mass_list[-1][-1][0]
    dialog_list = [''] * dialog_num
    for k in range(len(sen_list)):
        sentence = sen_list[k]
        record = mass_list[k]

        total_dialog_of_sentence = len(record)

        if total_dialog_of_sentence == 1:
            dialog_list[record[0][0]-1] += sentence[0:record[0][1]]

        else:
            origin_len = record[-1][1]
            translated_len = len(sentence)

            last_idx = 0
            for l in range(len(record) - 1):
                current_idx = int(translated_len * record[l][1] / origin_len)
                if space and not cn:
                    current_idx = get_the_nearest_space(sentence, current_idx)
                    dialog_list[record[l][0] - 1] += sentence[last_idx:current_idx]
                    last_idx = current_idx
                elif cn:
                    current_idx = get_the_nearest_split_sen_cn(sentence, current_idx, last_idx)

                    dialog_list[record[l][0] - 1] += sentence[last_idx:current_idx]
                    last_idx = current_idx
                else:
                    dialog_list[record[l][0] - 1] += sentence[last_idx:current_idx]
                    last_idx = current_idx

            dialog_list[record[-1][0]-1] += sentence[last_idx:]

    return dialog_list
