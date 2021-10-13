from typing import List


def pos_neg_text_file_parse(pos, neg):
    if not isinstance(pos, str) or not isinstance(neg, str):
        print('File names must be in string format.')
        return
    try:
        with open(pos) as pos_file:
            pos_words = pos_file.read()
        with open(neg) as neg_file:
            neg_words = neg_file.read()
    except:
        print('Positive or negative words text files are not in your current directory.')

    pos_words_list = pos_words.split()
    neg_words_list = neg_words.split()
    return [pos_words_list, neg_words_list]