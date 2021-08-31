import json
import re
import random

def get_stories(filename):
    stories = []
    answers = []
    story_lines = []
    with open(filename, "r") as f:
        for line in f:
            if re.search("^1 ", line):
                story_lines = []
            first_space_index = line.index(" ")
            line = line[first_space_index:]
            if "." in line:
                period_index = line.index(".")
                line = line[:period_index + 1]
                story_lines.append(line)
            elif "?" in line:
                question_index = line.index("?")
                answer = line[question_index + 2:-3]
                line = line[:question_index + 1]
                story_lines.append(line)
                story = "".join(story_lines)
                story = story[1:]
                stories.append(story)
                answers.append(answer)
    stories_answers = list(set(zip(stories, answers)))
    random.shuffle(stories_answers)
    return stories_answers[:6500]

def get_definition(split):
    if split == 1:
        definition = "Given a story, answer the question about the story. The question is the last sentence in the input. The story has one of the three following scenarios: the first is when the individual's belief matches reality, the second is when the individual's belief does not match reality, and the third is when an individual has a false belief about another individual's beliefs. The question will ask about the location of an object in the story with respect to either none or one of the three scenarios."
    elif split == 2:
        definition = "Given a story, answer the question about the story. The question is the last sentence in the input. The story has one of the three following scenarios: the first is when the individual's belief matches reality, the second is when the individual's belief does not match reality, and the third is when an individual has a false belief about another individual's beliefs. The question will ask about the location of an object in the story with respect to either none or one of the three scenarios. Note that there are distractor sentences in each story that are unrelated to the question and are designed to confuse the reader."
    elif split == 3:
        definition = "Given a story, answer the question about the story. The question is the last sentence in the input. These stories can be difficult due to their length and how each story has at least one of the three following scenarios: the first is when the individual's belief matches reality, the second is when the individual's belief does not match reality, and the third is when an individual has a false belief about another individual's beliefs. The question will ask about the location of an object in the story with respect to either none or one of the three scenarios."
    else:
        definition = "Given a story, answer the question about the story. The question is the last sentence in the input. These stories can be difficult due to their length and how each story has at least one of the three following scenarios: the first is when the individual's belief matches reality, the second is when the individual's belief does not match reality, and the third is when an individual has a false belief about another individual's beliefs. The question will ask about the location of an object in the story with respect to either none or one of the three scenarios. Note that there are distractor sentences in each story that are unrelated to the question and are designed to confuse the reader."
    return definition

def get_positive_examples(split):
    if split == 1:
        positives = [{"input": "Isabella entered the hall. Olivia entered the hall. The apple is in the blue_treasure_chest. Olivia exited the hall. Isabella moved the apple to the green_basket. Where does Isabella think that Olivia searches for the apple?", "output" : "blue_treasure_chest", "explanation" : "Since Olivia was no longer in the hall, she last remembers the apple being in the blue_treasure_chest even though Isabella moved it to the green_basket. Since Isabella was in the hall the entire time, she knows where Olivia will look for it."}, \
                     {"input": "Ethan entered the bedroom. Liam entered the bedroom. The eggplant is in the green_cupboard. Liam exited the bedroom. Ethan moved the eggplant to the green_basket. Where is the eggplant really?", "output" : "green_basket", "explanation" : "Ethan last moved the eggplant to the green_basket, which is where it really is."}, \
                     {"input": "Abigail entered the TV_room. Oliver entered the TV_room. The cucumber is in the blue_envelope. Oliver exited the TV_room. Abigail moved the cucumber to the red_suitcase. Where was the cucumber at the beginning?", "output" : "blue_envelope", "explanation" : "The cucumber was first in the blue_envelope before it was moved to the red_suitcase."}]
    elif split == 2:
        positives = [{"input": "Isabella entered the hall. Olivia entered the hall. Phone rang. The apple is in the blue_treasure_chest. Olivia exited the hall. Isabella moved the apple to the green_basket. Where does Isabella think that Olivia searches for the apple?", "output" : "blue_treasure_chest", "explanation" : "Since Olivia was no longer in the hall, she last remembers the apple being in the blue_treasure_chest even though Isabella moved it to the green_basket. Since Isabella was in the hall the entire time, she knows where Olivia will look for it."}, \
                     {"input": "Ethan entered the bedroom. Liam entered the bedroom. Phone rang. The eggplant is in the green_cupboard. Liam exited the bedroom. Ethan moved the eggplant to the green_basket. Where is the eggplant really?", "output" : "green_basket", "explanation" : "Ethan last moved the eggplant to the green_basket, which is where it really is."}, \
                     {"input": "Abigail entered the TV_room. Oliver entered the TV_room. The cucumber is in the blue_envelope. Phone rang. Oliver exited the TV_room. Abigail moved the cucumber to the red_suitcase. Where was the cucumber at the beginning?", "output" : "blue_envelope", "explanation" : "The cucumber was first in the blue_envelope before it was moved to the red_suitcase."}]
    elif split == 3:
        positives = [{"input": "Jacob entered the dining_room. William entered the dining_room. The tomato is in the green_drawer. William exited the dining_room. Jacob moved the tomato to the blue_cupboard. Jacob is in the dining_room. Olivia entered the dining_room. The cucumber is in the blue_cupboard. Olivia exited the dining_room. Jacob moved the cucumber to the green_drawer. William entered the pantry. Jacob entered the pantry. The asparagus is in the red_cupboard. Jacob exited the pantry. William moved the asparagus to the green_pantry. Abigail entered the hall. William entered the hall. The persimmon is in the blue_pantry. William exited the hall. Abigail moved the persimmon to the blue_envelope. Where does Abigail think that William searches for the persimmon?", "output" : "blue_pantry", "explanation" : "The persimmon was last in the blue_pantry before William exited the hall. After William exited the hall, Abigail moved the persimmon to the blue_envelope, so she knows where William will look for it."}, \
                     {"input": "James entered the cellar. Owen entered the cellar. The asparagus is in the blue_suitcase. James moved the asparagus to the green_drawer. James entered the sunroom. Ella entered the sunroom. The turnip is in the red_box. James moved the turnip to the red_drawer. Ella entered the office. Jacob entered the office. The pumpkin is in the green_suitcase. Ella moved the pumpkin to the blue_treasure_chest. Ella is in the office. Jacob is in the office. The potato is in the blue_treasure_chest. Ella moved the potato to the green_suitcase. Where will Jacob look for the potato?", "output" : "green_suitcase", "explanation" : "Jacob is in the same room as Ella and sees that Ella moved the potato from the blue_treasure_chest to the green_suitcase."}, \
                     {"input": "Jacob entered the dining_room. Avery entered the dining_room. The persimmon is in the green_box. Avery exited the dining_room. Jacob moved the persimmon to the red_drawer. Avery entered the master_bedroom. Jacob entered the master_bedroom. The orange is in the red_bottle. Jacob exited the master_bedroom. Avery moved the orange to the blue_pantry. Avery is in the master_bedroom. Jackson entered the master_bedroom. The orange is in the blue_pantry. Jackson exited the master_bedroom. Avery moved the orange to the red_bottle. Avery entered the hall. Jackson entered the hall. The cucumber is in the blue_treasure_chest. Jackson exited the hall. Avery moved the cucumber to the blue_box. Where was the cucumber at the beginning?", "output" : "blue_treasure_chest", "explanation" : "The cucumber was first in the blue_treasure_chest before Avery moved it to the blue_box."}]
    else:
        positives = [{"input": "Jacob entered the dining_room. William entered the dining_room. The tomato is in the green_drawer. William exited the dining_room. Jacob moved the tomato to the blue_cupboard. Jacob is in the dining_room. Olivia entered the dining_room. The cucumber is in the blue_cupboard. Olivia exited the dining_room. Jacob moved the cucumber to the green_drawer. William entered the pantry. Jacob entered the pantry. The asparagus is in the red_cupboard. Jacob exited the pantry. Phone rang. William moved the asparagus to the green_pantry. Abigail entered the hall. William entered the hall. The persimmon is in the blue_pantry. William exited the hall. Abigail moved the persimmon to the blue_envelope. Where does Abigail think that William searches for the persimmon?", "output" : "blue_pantry", "explanation" : "The persimmon was last in the blue_pantry before William exited the hall. After William exited the hall, Abigail moved the persimmon to the blue_envelope, so she knows where William will look for it."}, \
                     {"input": "James entered the cellar. Owen entered the cellar. The asparagus is in the blue_suitcase. Phone rang. James moved the asparagus to the green_drawer. James entered the sunroom. Ella entered the sunroom. The turnip is in the red_box. Phone rang. James moved the turnip to the red_drawer. Ella entered the office. Jacob entered the office. The pumpkin is in the green_suitcase. Ella moved the pumpkin to the blue_treasure_chest. Ella is in the office. Jacob is in the office. The potato is in the blue_treasure_chest. Ella moved the potato to the green_suitcase. Where will Jacob look for the potato?", "output" : "green_suitcase", "explanation" : "Jacob is in the same room as Ella and sees that Ella moved the potato from the blue_treasure_chest to the green_suitcase."}, \
                     {"input": "Jacob entered the dining_room. Avery entered the dining_room. The persimmon is in the green_box. Avery exited the dining_room. Jacob moved the persimmon to the red_drawer. Avery entered the master_bedroom. Jacob entered the master_bedroom. The orange is in the red_bottle. Jacob exited the master_bedroom. Avery moved the orange to the blue_pantry. Phone rang. Avery is in the master_bedroom. Jackson entered the master_bedroom. The orange is in the blue_pantry. Phone rang. Jackson exited the master_bedroom. Avery moved the orange to the red_bottle. Avery entered the hall. Jackson entered the hall. The cucumber is in the blue_treasure_chest. Phone rang. Jackson exited the hall. Avery moved the cucumber to the blue_box. Where was the cucumber at the beginning?", "output" : "blue_treasure_chest", "explanation" : "The cucumber was first in the blue_treasure_chest before Avery moved it to the blue_box."}]
    return positives

def get_negative_examples(split):
    if split == 1:
        negatives = [{"input": "Isabella entered the hall. Olivia entered the hall. The apple is in the blue_treasure_chest. Olivia exited the hall. Isabella moved the apple to the green_basket. Where does Isabella think that Olivia searches for the apple?", "output" : "green_basket", "explanation" : "Olivia will search for the apple in the blue_treasure_chest because that is where she last saw it. Isabella knows she moved the apple to the green_basket after Olivia left, so she won't think that Olivia will look for it there."}, \
                     {"input": "Ethan entered the bedroom. Liam entered the bedroom. The eggplant is in the green_cupboard. Liam exited the bedroom. Ethan moved the eggplant to the green_basket. Where is the eggplant really?", "output" : "green_cupboard", "explanation" : "The eggplant is really in the green_basket because that is where Ethan moved it to at the end."}]
    elif split == 2:
        negatives = [{"input": "Isabella entered the hall. Olivia entered the hall. Phone rang. The apple is in the blue_treasure_chest. Olivia exited the hall. Isabella moved the apple to the green_basket. Where does Isabella think that Olivia searches for the apple?", "output" : "green_basket", "explanation" : "Olivia will search for the apple in the blue_treasure_chest because that is where she last saw it. Isabella knows she moved the apple to the green_basket after Olivia left, so she won't think that Olivia will look for it there."}, \
                     {"input": "Ethan entered the bedroom. Liam entered the bedroom. Phone rang. The eggplant is in the green_cupboard. Liam exited the bedroom. Ethan moved the eggplant to the green_basket. Where is the eggplant really?", "output" : "green_cupboard", "explanation" : "The eggplant is really in the green_basket because that is where Ethan moved it to at the end."}]
    elif split == 3:
        negatives = [{"input": "Jacob entered the dining_room. William entered the dining_room. The tomato is in the green_drawer. William exited the dining_room. Jacob moved the tomato to the blue_cupboard. Jacob is in the dining_room. Olivia entered the dining_room. The cucumber is in the blue_cupboard. Olivia exited the dining_room. Jacob moved the cucumber to the green_drawer. William entered the pantry. Jacob entered the pantry. The asparagus is in the red_cupboard. Jacob exited the pantry. William moved the asparagus to the green_pantry. Abigail entered the hall. William entered the hall. The persimmon is in the blue_pantry. William exited the hall. Abigail moved the persimmon to the blue_envelope. Where does Abigail think that William searches for the persimmon?", "output" : "blue_envelope", "explanation" : "Abigail moved the persimmon to the blue_envelope after William exited the hall. William does not know where the persimmon is if she moved it after he left."}, \
                     {"input": "James entered the cellar. Owen entered the cellar. The asparagus is in the blue_suitcase. James moved the asparagus to the green_drawer. James entered the sunroom. Ella entered the sunroom. The turnip is in the red_box. James moved the turnip to the red_drawer. Ella entered the office. Jacob entered the office. The pumpkin is in the green_suitcase. Ella moved the pumpkin to the blue_treasure_chest. Ella is in the office. Jacob is in the office. The potato is in the blue_treasure_chest. Ella moved the potato to the green_suitcase. Where will Jacob look for the potato?", "output" : "blue_treasure_chest", "explanation" : "Jacob is in the same room as Ella, so he saw her move the potato to the green_suitcase, which is where he will look for it."}]
    else:
        negatives = [{"input": "Jacob entered the dining_room. William entered the dining_room. The tomato is in the green_drawer. William exited the dining_room. Jacob moved the tomato to the blue_cupboard. Jacob is in the dining_room. Olivia entered the dining_room. The cucumber is in the blue_cupboard. Olivia exited the dining_room. Jacob moved the cucumber to the green_drawer. William entered the pantry. Jacob entered the pantry. The asparagus is in the red_cupboard. Jacob exited the pantry. Phone rang. William moved the asparagus to the green_pantry. Abigail entered the hall. William entered the hall. The persimmon is in the blue_pantry. William exited the hall. Abigail moved the persimmon to the blue_envelope. Where does Abigail think that William searches for the persimmon?", "output" : "blue_envelope", "explanation" : "Abigail moved the persimmon to the blue_envelope after William exited the hall. William does not know where the persimmon is if she moved it after he left."}, \
                     {"input": "James entered the cellar. Owen entered the cellar. The asparagus is in the blue_suitcase. Phone rang. James moved the asparagus to the green_drawer. James entered the sunroom. Ella entered the sunroom. The turnip is in the red_box. Phone rang. James moved the turnip to the red_drawer. Ella entered the office. Jacob entered the office. The pumpkin is in the green_suitcase. Ella moved the pumpkin to the blue_treasure_chest. Ella is in the office. Jacob is in the office. The potato is in the blue_treasure_chest. Ella moved the potato to the green_suitcase. Where will Jacob look for the potato?", "output" : "blue_treasure_chest", "explanation" : "Jacob is in the same room as Ella, so he saw her move the potato to the green_suitcase, which is where he will look for it."}]
    return negatives

def get_instances(stories_answers):
    instances = []
    for story, answer in stories_answers:
        instance = {"input" : story, "output" : [answer]}
        instances.append(instance)
    print(len(instances))
    return instances

def create_json(stories_answers, json_filename, split):
    json_file = {}
    json_file["Contributors"] = ["Eshaan Pathak"]
    json_file["Source"] = ["tomqa (https://github.com/kayburns/tom-qa-dataset)"]
    json_file["Categories"] = ["Answer Generation"]
    json_file["Definition"] = get_definition(split)
    json_file["Positive Examples"] = get_positive_examples(split)
    json_file["Negative Examples"] = get_negative_examples(split)
    json_file["Instances"] = get_instances(stories_answers)
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(json_file, f, indent=4)


if __name__ == "__main__":
    tomeasy_clean_filename = "tom_easy/world_large_nex_1000_0/all.txt"
    stories_answers = get_stories(tomeasy_clean_filename)
    json_filename = "task151_tomqa_find_location_easy_clean.json"
    create_json(stories_answers, json_filename, 1)

    tomeasy_noise_filename = "tom_easy/world_large_nex_1000_10/all.txt"
    stories_answers = get_stories(tomeasy_noise_filename)
    json_filename = "task152_tomqa_find_location_easy_noise.json"
    create_json(stories_answers, json_filename, 2)

    tom_clean_filename = "tom/world_large_nex_1000_0/all.txt"
    stories_answers = get_stories(tom_clean_filename)
    json_filename = "task153_tomqa_find_location_hard_clean.json"
    create_json(stories_answers, json_filename, 3)

    tom_noise_filename = "tom/world_large_nex_1000_10/all.txt"
    stories_answers = get_stories(tom_noise_filename)
    json_filename = "task154_tomqa_find_location_hard_noise.json"
    create_json(stories_answers, json_filename, 4)
