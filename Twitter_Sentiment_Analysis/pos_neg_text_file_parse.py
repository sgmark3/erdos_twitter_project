def pos_neg_text_file_parse(pos, neg):
    """
    This function takes in two text files, positive and negative
    words associated with a text library, and returns the words 
    in a list.
    """
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
    del pos_words, neg_words #Free up memory
    return [pos_words_list, neg_words_list]
