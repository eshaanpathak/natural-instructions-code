import pandas as pd
import json
import random

def get_words(filename):
    puzzles = []
    categories = set()
    with open(filename, "r") as f:
        for line in f:
            puzzle = line.split("\t")
            puzzle[-1] = puzzle[-1][:-1]
            category = puzzle[0]
            words = tuple(puzzle[2:])
            if len(words) != 4:
                continue
            sep_puzzle = (category, words)
            puzzles.append(sep_puzzle)
    puzzles = list(set(puzzles))
    random.shuffle(puzzles)
    new_puzzles = []
    for puzzle in puzzles:
        if len(new_puzzles) == 6500:
            break
        words = list(puzzle[1])
        random.shuffle(words)
        if [puzzle[0], words] not in new_puzzles:
            new_puzzles.append([puzzle[0], words])
    return new_puzzles

def get_definition():
    definition = "Given a set of four words, generate the category that the words belong to. Words are separated by commas. The possible categories are social gathering, accomodation, physical property, measurement unit, corporate, nutritional value, boats, police punishment, location (proximity), card games, outdoor sport activity, military rank, baby animals, weather, consumer product, animals, boxing terminology, food, chocolate food, bird, type of sandwich, date status, body part, ocean, employment activity, moral characteristic, elements, poker, computers, construction, guitar part, shady activities, physical activity, kitchenware, temperature, type of rigidity, emotional status, season, mode of transportation, window material, activity, emotional display, geographical property, fried food, store status, widespread, aesthetic characteristic, alcoholic drinks, secretary duty, direction, personal characteristic, and animal."
    return definition

def get_positive_examples():
    positives = [{"input": "excavator, crane, hoist, upraise", "output" : "construction", "explanation" : "These four words are all construction equipment, such as 'excavator', 'crane', and 'hoist', or describe a common activity used in construction, such as 'upraise'."}, \
                 {"input": "annoyed, fine, ok, calm", "output" : "emotional status", "explanation" : "These are all emotions that people feel or use to describe how they feel."}, \
                 {"input": "cat, sheep, duck, lion", "output" : "animals", "explanation" : "These words are types of animals. All of these are mammals except for 'duck' which is a type of bird."}]
    return positives

def get_negative_examples():
    negatives = [{"input": "jab, punch, corner, deck", "output" : "physical activity", "explanation" : "Though this set of words is representative of physical activity, they are more related to boxing moves. The correct answer is 'boxing terminology'."}, \
                 {"input": "bridge, gin, canasta, uno", "output" : "games", "explanation" : "The word 'games' is not in the given list of possible categories. The correct answer is 'card games'."}]
    return negatives

def get_instances(puzzles):
    instances = []
    for puzzle in puzzles:
        puzzle_category = puzzle[0]
        words = puzzle[1]
        input_instance = "{}, {}, {}, {}".format(words[0], words[1], words[2], words[3])
        instance = {"input" : input_instance, "output" : [puzzle_category]}
        instances.append(instance)
    return instances


def create_json(puzzles, json_filename):
    json_file = {}
    json_file["Contributors"] = ["Eshaan Pathak"]
    json_file["Source"] = ["odd-man-out (https://github.com/gabrielStanovsky/odd-man-out)"]
    json_file["Categories"] = ["Classification"]
    json_file["Definition"] = get_definition()
    json_file["Positive Examples"] = get_positive_examples()
    json_file["Negative Examples"] = get_negative_examples()
    json_file["Instances"] = get_instances(puzzles)
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(json_file, f, indent=4)


if __name__ == "__main__":
    filename = "data/crowdsourced.tsv"
    puzzles = get_words(filename)
    create_json(puzzles, "task143_odd-man-out_classification_generate_category.json")
