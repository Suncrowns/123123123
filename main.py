# Глобальные переменные

unions = [
    "и", "да", "или", "либо", "а", "но", "однако", "также", "тоже", "ежели", "если", "когда", "который", "что",
    "чтобы", "так как", "если бы", "так чтобы", "потому что", "что если", "как будто", "несмотря на то",
    "пока", "после того как", "до тех пор как", "с тех пор как", "чтобы не", "ведь", "например", "ибо",
    "даже если", "да не", "да и", "мало того", "то есть", "но зато", "так что", "при том что", "еще",
    "к тому же", "в то же время", "в то же самое время", "поэтому", "следовательно", "то есть", "иначе",
    "тогда", "после", "до", "при этом", "при этом", "где", "куда", "откуда", "куда бы", "ведь", "чем", "при", "будто",
    "хотя", "тем не менее", "один раз", "например", "итак", "следовательно", "однако", "при этом", "соответственно",
    "впрочем", "следом", "потому что", "так что", "иначе", "или", "либо", "или же", "чего бы ни было", "то ли"
]

special_characters = ["\0", "\a", "\b", "\t", "\n", "\v", "\f", "\r", "\xa0", "\"", "\'", "\\"
                                                                                          "\x00", "\x01", "\x02",
                      "\x03", "\x04", "\x05", "\x06", "\x07",
                      "\x08", "\x09", "\x0a", "\x0b", "\x0c", "\x0d", "\x0e", "\x0f", "\x10", "\x11", "\x12", "\x13",
                      "\x14", "\x15", "\x16", "\x17",
                      "\x18", "\x19", "\x1a", "\x1b", "\x1c", "\x1d", "\x1e", "\x1f",
                      "\u00A0", "\u200b", "\u2002", "\u2003", "\u2009", "\u2022", "\u2014"
                      ]  # список, содержащий в себе спеицльные символы пайтон, не существующие лингвистически

special_symbols_list = [
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=",
    "[", "]", "{", "}", "\\", "|", ";", ":", "'", "\"", ",", ".", "?", "/",
    "<", ">", "~", "`", "\n", "\t", " ", "\u00A0", "\u2013", "\u2014", "\u2026", "«", "»"
]  # еще один список с спец символами, но здесь большинство из них не относятся к спец символам строковых отображений,


# так же есть лингвистические


# функции редактирования текста для анализа текста


def remove_before_parenthesis(s):
    if '(' in s:
        return s
    else:
        index = s.find(')')
        if index != -1:
            return s[index + 1:]
        else:
            return s


def remove_numbers_before_symbols(sentence):
    c = 0
    while c < len(sentence) and sentence[c] in '0123456789':
        c += 1
    if c + 1 < len(sentence) and sentence[c] in '.)':
        return sentence[c + 1:len(sentence) + 1]
    return sentence


def define_chapter(sentence):
    c = 0
    for i in sentence:
        if i.isalpha() and i not in "IXVC":
            return True
    return False


def has_letters(s):
    for char in s:
        if char.isalpha():
            return True
    return False


def edit_sentence(s):
    # result = re.split(r'[.!?^-]', s)
    s = s.replace("?–", "–")
    s = s.replace("!–", "–")
    s = s.replace("?", "[]")
    s = s.replace("!", "[]")
    s = s.replace(".", "[]")
    result = s.split("[]")
    res = []
    for sentence in result:
        sentence = remove_numbers_before_symbols(sentence)
        sentence = remove_before_parenthesis(sentence)
        for i in special_symbols_list:
            sentence = sentence.replace(i, ' ')
        sentence = sentence.replace('  ', ' ')
        sentence = sentence.replace('  ', ' ')
        res.append(sentence.strip())
    return res


def edit_strings_for_analyzing(lst):
    result = []
    for i in lst:
        for j in special_characters:
            i = i.replace(j, "")
        if len(i) != 0 and has_letters(i) and define_chapter(i):
            result.append(i)
    return result


# Функции анализа текста


def define_medium_word_len(lst):
    word_count = 0
    letter_len = 0
    for sentence in lst:
        words = sentence.split()
        for word in words:
            word_count += 1
            letter_len += len(word)
    return letter_len / word_count


def define_count_of_words_and_frequency_of_union(lst):
    word_count = 0
    prepositions_count = 0
    for sentence in lst:
        words = sentence.split()
        for word in words:
            if word in unions:
                prepositions_count += 1
            word_count += 1
    return word_count, word_count / prepositions_count / 100


def define_count_of_unique_words_and_user_word_count(lst, user_word):
    lst_of_words = []
    user_word = user_word.lower()
    set_of_words = set()
    for sentences in lst:
        words = sentences.split()
        for word in words:
            lst_of_words.append(word.strip().lower())
            set_of_words.add(word.strip().lower())
    uniquie_words = set()
    for word in set_of_words:
        if lst_of_words.count(word) == 1:
            uniquie_words.add(word)
    return len(uniquie_words), lst_of_words.count(user_word)


def main(user_word):
    f = open('70299175.txt').readlines()
    lst_of_edited_sentences = []
    for i in edit_strings_for_analyzing(f):
        for sentence in edit_sentence(i):
            if len(sentence) != 0:
                lst_of_edited_sentences.append(sentence)
    unique_word_count, user_word_count = define_count_of_unique_words_and_user_word_count(lst_of_edited_sentences,
                                                                                          user_word)
    count_of_words, frequency_of_union = define_count_of_words_and_frequency_of_union(lst_of_edited_sentences)
    medium_word_len = define_medium_word_len(lst_of_edited_sentences)
    with open('results.txt', 'w+') as result_file:
        result_file.write(f"Количество уникальных слов в тексте: {unique_word_count}\n")
        result_file.write(f"Выбранное пользователем слово встречается столько раз: {user_word_count}\n")
        result_file.write(f"Общее количество слов в тексте: {count_of_words}\n")
        result_file.write(f"Средняя длина слова: {medium_word_len}\n")
        result_file.write(f"Частота встречи союзов: {frequency_of_union}\n")


user_word = str(input('Введите слово, которое хотели бы посчитать в тексте: '))
main(user_word)
