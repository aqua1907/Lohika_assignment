from utils import *


def run(sentences_tok, fruits, actions):
    sentences_dict = {}
    answers = []

    # loop all sentences
    for i, sentence in enumerate(sentences_tok):
        # Check first sentence that describes items on the table
        if i == 0:
            # Extract all fruits in sentence and corresponding quantity
            sentences_dict["sent_1"] = {"sentence": ' '.join([word for word in sentence]),
                                        "fruits": {}}
            for fruit in fruits:    # loop in all fruits and get corresponding index of fruit in sentence
                fruit_idx = sentence.index(fruit)
                fruit_qty = int(sentence[fruit_idx - 1])    # get quantity of fruit
                sentences_dict["sent_1"]["fruits"][fruit] = fruit_qty
            # sum all over quantities and get fruits_overall
            sentences_dict["sent_1"]["fruits_overall"] = sum(
                [x for x in sentences_dict["sent_1"]["fruits"].values()])

        # Check second sentence that describes boy's actions
        if i == 1:
            # Extract all fruits in sentence and corresponding quantity to corresponding action
            sentences_dict["sent_2"] = {"sentence": ' '.join([word for word in sentence])}
            # Loop in actions
            for action in actions:
                sentences_dict["sent_2"][action] = {}
                # get index of corresponding action and +1. This is for start looping from word that after action
                action_index = sentence.index(action) + 1
                # Looping from word that after action
                for word in sentence[action_index:]:
                    if word in actions:     # Break loop if
                        break
                    elif word.isalpha() and word in fruits:     # find fruit in sentence
                        fruit = word
                        fruit_idx = sentence.index(fruit)
                        fruit_qty = sentence[fruit_idx - 1]
                        # Add to corresponding action a fruit its and quantity
                        sentences_dict["sent_2"][action][fruit] = int(fruit_qty)

            sentences_dict["sent_2"]["fruits"] = {}
            # Loop all over fruits in dictionary of sentence to change quantity of fruits
            # for corresponding action
            for k, v in sentences_dict["sent_1"]["fruits"].items():
                for action in actions:
                    if k not in sentences_dict["sent_2"]:
                        sentences_dict["sent_2"]["fruits"][k] = v

                    if action == "з'їв" or action == "прибрав" or action == "забрав":
                        if k in sentences_dict["sent_2"][action]:
                            sentences_dict["sent_2"]["fruits"][k] = v - sentences_dict["sent_2"][action][k]

                    elif action == 'поклав' or action == "додав":
                        if k in sentences_dict["sent_2"][action]:
                            sentences_dict["sent_2"]["fruits"][k] = v + sentences_dict["sent_2"][action][k]

                # Summation all fruits after actions
                sentences_dict["sent_2"]["fruits_overall"] = sum(
                    [x for x in sentences_dict["sent_2"]["fruits"].values()])

        # Check all question sentence
        if i > 1:
            sentences_dict[f"q_{i - 1}"] = {"sentence": ' '.join([word for word in sentence])}
            # If in question about left fruits or all left fruits
            if "залишилось" in sentence:
                #  Get answer for question about all left fruits
                if "всього" in sentence or "фруктів" in sentence:
                    sentences_dict[f"q_{i - 1}"]["answer"] = "На столі залишилось {} фруктів".format(
                        sentences_dict["sent_2"]["fruits_overall"])

                # Get answer about each fruit that left on the table
                else:
                    sentences_dict[f"q_{i - 1}"]["answer"] = f"На столі залишилось"
                    for fruit in fruits:
                        if fruit in sentence:
                            sentences_dict[f"q_{i - 1}"]["answer"] += " {} {}".format(
                                sentences_dict["sent_2"]["fruits"][fruit], fruit)

            # If question about actions
            else:
                for action in actions:  # loop all over actions
                    # Check action if in sentence otherwise question sentence is incorrect
                    if action in sentence:
                        # Get answer about all fruits to corresponding action
                        if "всього" in sentence or "фруктів" in sentence:
                            all_fruits_action = sum(sentences_dict["sent_2"][action].values())
                            sentences_dict[f"q_{i - 1}"]["answer"] = \
                                "Хлопчик {} {} фруктів".format(action, all_fruits_action)

                        # Get answer for each fruit to corresponding action
                        else:
                            sentences_dict[f"q_{str(i - 1)}"]["answer"] = f"Хлопчик {action}"
                            for fruit in fruits:
                                # Check fruit if in sentence otherwise question sentence is incorrect
                                if fruit in sentence:
                                    sentences_dict[f"q_{i - 1}"]["answer"] += " {} {}".format(
                                        sentences_dict["sent_2"]["fruits"][fruit], fruit)
                                else:
                                    sentences_dict[f"q_{i - 1}"]["answer"] = f"Питання №{i - 1} " \
                                                                             f"описано в умові направильно"

            # If question starts with correct word "склільки" but has incorrect description
            # output message about it
            if "answer" not in sentences_dict[f"q_{i - 1}"]:
                sentences_dict[f"q_{i - 1}"]["answer"] = f"Питання №{i-1} описано в умові направильно"

            try:
                answers.append(sentences_dict[f"q_{i - 1}"]["answer"])
            except KeyError:
                print(f"Питання №{i - 1} описано в умові направильно\n", file=sys.stderr)

    return answers


def main(text, fruits, actions):
    # Load stopwords from .txt file
    stopwords = read_file("stopwords_uk.txt")

    # Preprocess and split sentence
    sentences = preprocess_split_sentences(text)

    # Use tokenazation and lemmatization on sentences
    sentences_tok = tokenize(sentences, stopwords=stopwords)
    sentences_tok = lemmatization(sentences_tok, fruits)

    # Check all tasks in the given example
    check_the_task(sentences_tok, fruits, actions)

    # Get answer
    answers = run(sentences_tok, fruits, actions)

    for i, answer in enumerate(answers):
        print(f"Відповідь №{i + 1}: {answer}")


if __name__ == "__main__":
    actions = ["поклав", "з'їв", "забрав"]
    fruits = ["апельсин", "яблуко", "мандарин", "груша"]

    ex1 = """На столі лежить 2 яблука, 3 апельсини, 1 груша та 3 мандарини. Хлопчик поклав на стіл 2 яблука, 
    і з'їв 1 мандарин і 1 грушу, при цьому він ще забрав 2 апельсини. Скільки всього фруктів з'їв хлопчик? Скільки 
    залишилось мандарин та апельсин на столі? Скільки фруктів поклав хлопчик на стіл? Скільки яблук залишилось? Скільки фруктів?"""

    main(ex1, fruits, actions)
