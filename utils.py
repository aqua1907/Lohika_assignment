import re
import difflib
import sys


def read_file(path):
    """
    Read txt file with stopwords
    :param path: path to the file
    :return: list of stopwords
    """
    with open(path, 'r', encoding="utf-8") as f_obj:
        stopwords = [line for line in f_obj.read().splitlines()]
    f_obj.close()

    return stopwords


def preprocess_split_sentences(string):
    """
    Remove punctuation in sentences and split sentences by "."
    :param string: input text
    :return: list of sentences split by "."
    """
    sentences = re.sub(r"\n", " ", string)
    sentences = re.sub(r"\s*([.!?])\s*", ".", sentences)
    sentences = re.sub(r"[\-,:+*/_]", ' ', sentences).lower()
    sentences = sentences.split(".")
    del sentences[-1]

    return sentences


def check_the_task(sentences, fruits, actions):
    """
    Check all conditions in the given task if it is not correct
    :param actions: list of actions in the given task
    :param fruits: list of fruits in the given task
    :param sentences: list of sentences of the task
    :return: print errors
    """
    if not fruits:
        print("Масив в якомуу задається перелік фруктів — пустий")
        sys.exit(0)
    if not actions:
        print("Масив в якомуу задається перелік дій хлопчика — пустий")
        sys.exit(0)

    for i, sentence in enumerate(sentences):
        if i == 0:
            if "стіл" not in sentence and "столі" not in sentence:
                print(f"Помилка в умові задачі({i+1} речення): задані речі "
                      f"в умові повинні бути на столі.", file=sys.stderr)
                sys.exit(0)

            for fruit in fruits:
                try:
                    sentence.index(fruit)
                except ValueError:
                    print(f"Помилка в умові задачі({i+1} речення): задані фрутки в масиві не "
                          "відповідають заданим фруктам в умові задачі. "
                          "В масиві вказано більше фруктів, ніж в умові", file=sys.stderr)
                    sys.exit(0)

        if i == 1:
            if "хлопчик" not in sentence:
                print(f"Помилка в умові задачі({i+1} речення): хлопчик повинен фігурувати в умові "
                      "задачі(той хто маніпуляє з речами на столі)", file=sys.stderr)
                sys.exit(0)
            for action in actions:
                try:
                    sentence.index(action)
                except ValueError:
                    print(f"Помилка в умові задачі({i+1} речення): задані дії хлопчика в масиві "
                          "не відповідають заданим діям в умові задачі.", file=sys.stderr)
                    sys.exit(0)
        if i > 1:
            if sentence[0] != "скільки":
                print(f"Помилка в умові задачі({i+1} речення): питання задачі "
                      f"повинні обов'язково починатися зі слова 'Скільки'", file=sys.stderr)
                sys.exit(0)


def tokenize(sentences, stopwords=None):
    """
    Tokenize each sentence and create sequence of sentences, also remove stopwords if not None
    :param sentences: input list of sentences
    :param stopwords: input list of stopwords
    :return: tokenized sequences of sentences
    """
    sentences_tok = []

    if stopwords is not None:
        for sentence in sentences:
            words = []
            for word in sentence.split():
                if word not in stopwords:
                    words.append(word)
            sentences_tok.append(words)
    else:
        for sentence in sentences:
            words = []
            for word in sentence.split():
                words.append(word)
            sentences_tok.append(words)

    return sentences_tok


def lemmatization(sentences_tok, fruits):
    """
    Process fruit words to put them in normal form according to given lis of fruits
    :param sentences_tok: tokenized sequences of sentences
    :param fruits: list of given fruits in the normal form
    :return: tokenized sequences of sentences with fruits in normal form
    """
    for i, sentence in enumerate(sentences_tok):
        for j, word in enumerate(sentence):
            for fruit in fruits:
                similarity = difflib.SequenceMatcher(None, word, fruit).ratio()
                if similarity >= 0.8:
                    sentences_tok[i][j] = fruit

    return sentences_tok
