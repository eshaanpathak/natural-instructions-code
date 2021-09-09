import random
import json
import re

def get_questions(filename):
    prompt_completions = []
    with open(filename, "r") as f:
        for line in f:
            line_lst = line.split("\t")
            line_lst[-1] = line_lst[-1][:-1]
            prompt = line_lst[1]
            completions = line_lst[2:-1]
            answer = "Completion " + chr(ord("A") + int(line_lst[-1]))
            instance_input = "Prompt: {}\n\n Completion A: {}\n\n Completion B: {}\n\n Completion C: {}\n\n Completion D: {}".format(prompt, completions[0], completions[1], completions[2], completions[3])
            prompt_completions.append((instance_input, answer))
    random.shuffle(prompt_completions)
    return prompt_completions[:6500]

def get_definition():
    definition = "Given a prompt and four completions, select the completion that is the most plausible in continuing or answering the prompt. This task is designed to test common sense and has various categories ranging between idioms, negated statements, polysemy, subject referencing, and quantitative reasoning. Generate either Completion A, Completion B, Completion C, or Completion D."
    return definition

def get_positive_examples():
    positives = [{"input": "Prompt: A clown is fashioning animals from long balloons. He\n\n Completion A: releases the animals into their natural habitat.\n\n Completion B: makes a giraffe and hands it to a child.\n\n Completion C: yells out for his second in command to pilot the battleship around the obstacle.\n\n Completion D: releases the balloon and it flies high into the air.", "output": "Completion B", "explanation" : "The clown is an entertainer and is twisting balloons to resemble an animal. There are no live animals, and these types of twistable balloons are not able to fly or float up."},
                 {"input": "Prompt: I am feeling hungry. I think I will\n\n Completion A: call my mother.\n\n Completion B: have some ravioli.\n\n Completion C: fly out the window.\n\n Completion D: go on a run outside.", "output": "Completion B", "explanation" : "If one is hungry, then they will eat some food to satiate their hunger. One must look at the entire context rather than just the current sentence when selecting the best completion to the prompt."},
                 {"input": "Prompt: I am feeling nervous about my midterm tomorrow. I fear that\n\n Completion A: the professor will delay the midterm.\n\n Completion B: I will doodle on my exam and receive points for it.\n\n Competion C: my grandpa has diabetes.\n\n Completion D: I will fail.", "output": "Completion D", "explanation" : "If one is feeling nervous about their midterm the next day, then they are most likely worried and anxious about the grade they will receive. They will not doodle on their exam because they will surely not do well in that case. The professor delaying a midterm is usually not why a person would feel nervous about the midterm. One may be worried about their grandpa having diabetes, but that is not relevant to taking a midterm."}]
    return positives

def get_negative_examples():
    negatives = [{"input": "Prompt: The man entered his house. The man\n\n Completion A: can't find the keys to unlock the door.\n\n Completion B: goes to school at his university.\n\n Completion C: eats the garbage.\n\n Completion D: takes his shoes off.", "output": "Completion A", "explanation" : "The man must have found the keys to unlock the door in order to have entered his house in the first place. After he entered the house, it is most plausible that he took his shoes off to not get his house dirty. Thus, Completion D is actually the correct answer."},
                 {"input": "The boy likes animals, but only invertebrates. He\n\n Completion A: likes pigs.\n\n Completion B: likes vertebrates.\n\n Completion C: likes spiders.\n\n Completion D: likes elephants.", "output": "Completion D", "explanation" : "Out of the four possible completions, only one of them mentions an invertebrate. Spiders are invertebrates since they do not have a spine or vertebral column. Thus, Completion C is actually the correct answer."}]
    return negatives

def get_instances(prompt_completions):
    instances = []
    for prompt_completion, answer in prompt_completions:
        instance = {"input" : prompt_completion, "output" : [answer]}
        instances.append(instance)
    print(len(instances))
    return instances

def create_json(prompt_completions, json_filename):
    json_file = {}
    json_file["Contributors"] = ["Eshaan Pathak"]
    json_file["Source"] = ["codah (https://aclanthology.org/W19-2008.pdf)"]
    json_file["Categories"] = ["Classification"]
    json_file["Definition"] = get_definition()
    json_file["Positive Examples"] = get_positive_examples()
    json_file["Negative Examples"] = get_negative_examples()
    json_file["Instances"] = get_instances(prompt_completions)
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(json_file, f, indent=4)


if __name__ == "__main__":
    filename = "full_data.tsv"
    prompt_completions = get_questions(filename)
    json_filename = "task156_codah_classification_adversarial.json"
    create_json(prompt_completions, json_filename)
