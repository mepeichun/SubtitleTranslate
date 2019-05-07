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

