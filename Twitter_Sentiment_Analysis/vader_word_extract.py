def vader_word_extract(vadertext: str, library: str, new_library: str):

    """
    This function takes in the vader lexicon file and a
    library with financial context words and returns
    the overlap.  

    :param vadertext: The vader lexicon file
    :param library: The library to intersect with the vader lexicon file
    :param new_library: The intersected library
    :return:
    """
    with open(vadertext, 'r') as vader:
        vader = vader.readlines()
    with open(library, 'r') as lib:
        lib = lib.read().split()
    written = open(new_library, "w")
    for line in vader:
        for word in lib:
            if line.startswith(word):
                written.write(line)

    return written