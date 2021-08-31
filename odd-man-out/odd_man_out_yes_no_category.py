import pandas as pd
import json
import random

def get_words(filename):
    puzzles = []
    with open(filename, "r") as f:
        for line in f:
            puzzle = line.split("\t")
            puzzle[-1] = puzzle[-1][:-1]
            category = puzzle[0]
            odd_man = puzzle[1]
            words = tuple(puzzle[1:])
            sep_puzzle = (category, odd_man, words)
            puzzles.append(sep_puzzle)
    puzzles = list(set(puzzles))
    random.shuffle(puzzles)
    new_puzzles = []
    for puzzle in puzzles[:6500]:
        words = list(puzzle[2])
        random.shuffle(words)
        new_puzzles.append([puzzle[0], puzzle[1], words])
    return new_puzzles

def get_definition(category):
    if category:
        definition = "Given a category and a set of five words, generate the word from the set that does not belong (i.e. is the least relevant) with the other words in the category. Words are separated by commas."
    else:
        definition = "Given a set of five words, generate the word from the set that does not belong (i.e. is the least relevant) with the other words. Words are separated by commas."
    return definition

def get_positive_examples(category):
    if category:
        positives = [{"input": "Category: construction\n\n Words: excavator, crane, pelican, hoist, upraise", "output" : "pelican", "explanation" : "A pelican is not related to construction because it is a type of bird."}, \
                     {"input": "Category: emotional status\n\n Words: annoyed, fine, ok, jail time, calm", "output" : "jail time", "explanation" : "The word 'jail time' is not an emotion that a person feels and is the time one must serve in jail after being convicted guilty of a crime."}, \
                     {"input": "Category: animals\n\n Words: cat, push, sheep, duck, lion", "output" : "push", "explanation" : "The word 'push' is not an animal and is an act of exerting force."}]
    else:
        positives = [{"input": "excavator, crane, pelican, hoist, upraise", "output" : "pelican", "explanation" : "The common category here are words related to construction. A pelican is not related to construction because it is a type of bird."}, \
                     {"input": "annoyed, fine, ok, jail time, calm", "output" : "jail time", "explanation" : "The common category here is 'emotional states'. The word 'jail time' is not an emotion that a person feels and is the time one must serve in jail after being convicted guilty of crime. "}, \
                     {"input": "cat, push, sheep, duck, lion", "output" : "push", "explanation" : "The common category here is 'animals'. The word 'push' is not an animal and is an act of exerting force."}]
    return positives

def get_negative_examples(category):
    if category:
        negatives = [{"input": "Category: boxing terminology\n\n Words: jab, punch, corner, joker, deck", "output" : "punch", "explanation" : "The word 'punch' is a boxing term that means to strike with a fist. The correct answer is 'joker', which is a different word for a comedian."}, \
                     {"input": "Category: card games\n\n Words: bridge, gin, canasta, vodka, uno", "output" : "canasta", "explanation" : "Canasta is a card game of the rummy family. The correct answer is 'vodka', which is an alcoholic beverage."}]
    else:
        negatives = [{"input": "jab, punch, corner, joker, deck", "output" : "punch", "explanation" : "The common category here is 'boxing terminology'. The word 'punch' is a boxing term that means to strike with a fist. The correct answer is 'joker', which is a different word for a comedian."}, \
                     {"input": "bridge, gin, canasta, vodka, uno", "output" : "canasta", "explanation" : "The common category here is 'card games'. Canasta is a card game of the rummy family. The correct answer is 'vodka', which is an alcoholic beverage."}]
    return negatives

def get_instances(puzzles, category):
    instances = []
    for puzzle in puzzles:
        puzzle_category = puzzle[0]
        odd_man = puzzle[1]
        words = puzzle[2]
        if category:
            input_instance = "Category: {}\n\n Words: {}, {}, {}, {}, {}".format(puzzle_category, words[0], words[1], words[2], words[3], words[4])
        else:
            input_instance = "{}, {}, {}, {}, {}".format(words[0], words[1], words[2], words[3], words[4])
        instance = {"input" : input_instance, "output" : [odd_man]}
        instances.append(instance)
    return instances


def create_json(puzzles, json_filename, category):
    json_file = {}
    json_file["Contributors"] = ["Eshaan Pathak"]
    json_file["Source"] = ["odd-man-out (https://github.com/gabrielStanovsky/odd-man-out)"]
    json_file["Categories"] = ["Classification"]
    json_file["Definition"] = get_definition(category)
    json_file["Positive Examples"] = get_positive_examples(category)
    json_file["Negative Examples"] = get_negative_examples(category)
    json_file["Instances"] = get_instances(puzzles, category)
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(json_file, f, indent=4)


if __name__ == "__main__":
    filename = "data/crowdsourced.tsv"
    puzzles = get_words(filename)
    create_json(puzzles, "task141_odd-man-out_classification_category.json", True)
    create_json(puzzles, "task142_odd-man-out_classification_no_category.json", False)
