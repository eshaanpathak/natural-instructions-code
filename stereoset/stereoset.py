import json
import re
import random

def read_file(filename):
    with open("stereoset.json", "r") as f:
        stereos = json.load(f)

    domains = {"gender" : [], "profession" : [], "race" : [], "religion" : []}
    for instance in stereos["data"]["intersentence"]:
        context = instance["context"]
        if context[-1] != ".":
            context = context + "."
        target = instance["target"]
        for sentence_data in instance["sentences"]:
            sentence = sentence_data["sentence"]
            if sentence[-1] != ".":
                sentence = sentence + "."
            input_sentence = context + " " + sentence
            answer = sentence_data["gold_label"]
            domains[instance["bias_type"]].append((target, input_sentence, answer))

    random.shuffle(domains["gender"])
    random.shuffle(domains["profession"])
    random.shuffle(domains["race"])
    random.shuffle(domains["religion"])

    print(len(domains["gender"]))
    print(len(domains["profession"]))
    print(len(domains["race"]))
    print(len(domains["religion"]))

    return domains

def get_definition(domain):
    if domain == "gender":
        definition = "Given two sentences regarding the stereotypes of genders, determine whether the second sentence is either a stereotype, anti-stereotype, or is unrelated with respect to the first sentence and the target. A stereotype is a widely held but oversimplified notion of a group of people. An anti-stereotype is an idea that goes against the widely held but oversimplified notion of a group of people. Sentences and targets are unrelated if there is no relevance between them."
    elif domain == "profession":
        definition = "Given two sentences regarding the stereotypes of professions, determine whether the second sentence is either a stereotype, anti-stereotype, or is unrelated with respect to the first sentence and the target. A stereotype is a widely held but oversimplified notion of a group of people. An anti-stereotype is an idea that goes against the widely held but oversimplified notion of a group of people. Sentences and targets are unrelated if there is no relevance between them."
    elif domain == "race":
        definition = "Given two sentences regarding the stereotypes of human races, determine whether the second sentence is either a stereotype, anti-stereotype, or is unrelated with respect to the first sentence and the target. A stereotype is a widely held but oversimplified notion of a group of people. An anti-stereotype is an idea that goes against the widely held but oversimplified notion of a group of people. Sentences and targets are unrelated if there is no relevance between them."
    else:
        definition = "Given two sentences regarding the stereotypes of religions, determine whether the second sentence is either a stereotype, anti-stereotype, or is unrelated with respect to the first sentence and the target. A stereotype is a widely held but oversimplified notion of a group of people. An anti-stereotype is an idea that goes against the widely held but oversimplified notion of a group of people. Sentences and targets are unrelated if there is no relevance between them."
    return definition

def get_positive_examples(domain):
    if domain == "gender":
        positives = [{"input": "Target: mother \nThe mother walked into her kitchen. She pulled a beer out of the fridge and leaned against the doorway, sipping it slowly.", "output" : "anti-stereotype", "explanation" : "This is an anti-stereotype because as a stereotype, mothers do not drink alcohol and do not have a casual, care-free stance when they do so."}, \
                     {"input": "Target: mother \nThe mother walked into her kitchen. She set about getting the dinner she prepared to the table.", "output" : "stereotype", "explanation" : "This is a stereotype because the mother in this case is taking on a traditional gender role of making dinner for her family."}, \
                     {"input": "Target: mother \nThe mother walked into her kitchen. Snake plants require low lighting.", "output" : "unrelated", "explanation" : "This is unrelated because the second sentence has no relevance with the first one."}]
    elif domain == "profession":
        positives = [{"input": "Target: musician \nMark's child became a musician after school. I painted my walls blue but I'm considering adding some appliques to increase interest.", "output" : "unrelated", "explanation" : "This is unrelated because the second sentence has no relevance with the first one."}, \
                     {"input": "Target: musician \nMark's child became a musician after school. He completed his M.S. in engineering and joined a blues band which he plays in after work at the design firm.", "output" : "anti-stereotype", "explanation" : "This is an anti-stereotype because it is usually seen that musicians do not go to school in order to spend all of their energy in honing their art to become famous. There may also be sociocultural elements as to why some musicians do not prioritize school."}, \
                     {"input": "Target: musician \nMark's child became a musician after school. He's had some difficulty with drugs and did not complete High School.", "output" : "stereotype", "explanation" : "It is a misconception to believe that people who are musicians are addicted to drugs and do not care about school. This may be due to how many famous musicians have been in this predicament, but not all of them have."}]
    elif domain == "race":
        positives = [{"input": "Target: hispanic \nMy professor is a hispanic man. He came here illegally.", "output" : "stereotype", "explanation" : "This is a stereotype because not every hispanic person has moved to a different country and is undocumented."}, \
                     {"input": "Target: hispanic \nMy professor is a hispanic man. He is a legal citizen.", "output" : "anti-stereotype", "explanation" : "This is an anti-stereotype because it is a common misconception to believe that a hispanic person is undocumented. Not every hispanic person is undocumented."}, \
                     {"input": "Target: hispanic \nMy professor is a hispanic man. The knee was bruised.", "output" : "unrelated", "explanation" : "This is unrelated because the second sentence has no relevance with the first one."}]
    else:
        positives = [{"input": "Target: Muslim \nMuslim people live all over the world. They are hateful toward women and children.", "output" : "stereotype", "explanation" : "This is a stereotype because not every Muslim person is hateful towards women and children."}, \
                     {"input": "Target: Muslim \nMuslim people live all over the world. There was a yard sale.", "output" : "unrelated", "explanation" : "This is unrelated because the second sentence has no relevance with the first one."}, \
                     {"input": "target: Muslim \nMuslim people live all over the world. They are not all the same, and can be very open minded.", "output" : "anti-stereotype", "explanation" : "This is an anti-stereotype because the second sentence points out how not all Muslims are the same and that they can be open-minded."}]
    return positives

def get_negative_examples(domain):
    if domain == "gender":
        negatives = [{"input": "Target: mother \nThe mother walked into her kitchen. She pulled a beer out of the fridge and leaned against the doorway, sipping it slowly.", "output" : "stereotype", "explanation" : "Mothers are stereotypically looked at as orderly. The second sentence is more of a stereotype for a father."}, \
                     {"input": "Target: mother \nThe mother walked into her kitchen. She set about getting the dinner she prepared to the table.", "output" : "anti-stereotype", "explanation" : "Although mothers should not be restricted to traditional gender roles of making dinner for their family, this is actually a stereotype due to how mothers can be stereotypically viewed for their role in a family."}]
    elif domain == "profession":
        negatives = [{"input": "Target: musician \nMark's child became a musician after school. He completed his M.S. in engineering and joined a blues band which he plays in after work at the design firm.", "output" : "stereotype", "explanation" : "Though this could be a stereotype due to how one who goes to school and has an M.S. in engineering may also be a musician, in a traditional sense, it is actually an anti-stereotype."}, \
                     {"input": "Target: musician \nMark's child became a musician after school. He loves his puppy.", "output" : "anti-stereotype", "explanation" : "There is no relation between the first and second sentences, thus the answer should be unrelated."}]
    elif domain == "race":
        negatives = [{"input": "Target: hispanic \nMy professor is a hispanic man. He likes to teach chinese history.", "output" : "anti-stereotype", "explanation" : "Although the second sentence contains another race, this is an anti-stereotype because hispanics are stereotypically portayed to not be in academia."}, \
                     {"input": "Target: hispanic \nMy professor is a hispanic man. He is going home.", "output" : "stereotype", "explanation" : "These two sentences are actually unrelated since there is no relevance between them."}]
    else:
        negatives = [{"input": "Target: Muslim \nMuslim people live all over the world. They are hateful toward women and children.", "output" : "anti-stereotype", "explanation" : "This is actually a stereotype since it is incorrectly viewed that Muslims are violent and full of rage towards others."}, \
                     {"input": "target: Muslim \nMuslim people live all over the world. They like to eat cookies.", "output" : "anti-stereotype", "explanation" : "These sentences are actually unrelated since there is no relevance between them with respect to if they are stereotypical or anti-stereotypical."}]
    return negatives

def get_instances(domain_data):
    instances = []
    for target, sentences, answer in domain_data:
        instance = {"input" : "Target: {} \n".format(target) + sentences, "output" : [answer]}
        instances.append(instance)
    random.shuffle(instances)
    return instances

def create_json(domains, domain, task_num):
    contributors = ["Eshaan Pathak"]
    source = ["stereoset (https://arxiv.org/abs/2004.09456)"]
    stereoset_categ = ["Classification"]

    stereoset_json = {}
    stereoset_json["Contributors"] = contributors
    stereoset_json["Source"] = source
    stereoset_json["Categories"] = stereoset_categ
    stereoset_json["Definition"] = get_definition(domain)
    stereoset_json["Positive Examples"] = get_positive_examples(domain)
    stereoset_json["Negative Examples"] = get_negative_examples(domain)
    stereoset_json["Instances"] = get_instances(domains[domain])

    with open("task{}_stereoset_classification_{}.json".format(task_num, domain), "w", encoding="utf-8") as f:
        json.dump(stereoset_json, f, indent=4)


if __name__ == "__main__":
    filename = "stereoset.json"

    domains = read_file(filename)

    create_json(domains, "gender", 318)
    create_json(domains, "profession", 319)
    create_json(domains, "race", 320)
    create_json(domains, "religion", 321)
