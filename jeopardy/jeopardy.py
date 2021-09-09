import json
import re
import random

def read_file(filename):
    with open("jeopardy_questions.json", "r") as f:
        jeopardy_qs = json.load(f)

    rounds = {"Jeopardy!" : [], "Double Jeopardy!" : [], "Final Jeopardy!" : [], "Tiebreaker" : []}

    examples = {"In the winter of 1971-72, a record 1,122 inches of snow fell at Rainier Paradise Ranger Station in this state", \
                "No. 8: 30 steals for the Birmingham Barons; 2,306 steals for the Bulls", \
                "Signer of the Dec. of Indep., framer of the Constitution of Mass., second President of the United States", \
                "Built in 312 B.C. to link Rome & the South of Italy, it's still in use today", \
                "The city of Yuma in this state has a record average of 4,055 hours of sunshine each year", \
                "YouTube, in 2006", \
                "Sailors wore these long before the groovy folks in the '60s", \
                "In 1956 this President's cabinet gave him a Grandma Moses painting of his Gettysburg farm", \
                "\"Miles Ahead\" is a 1957 album by this jazz trumpeter", \
                "He became a lawyer in London in 1891", \
                "It's a notation on a percussion store to clash", \
                "Made available for download in July 2000 by UCSC, the 739MB file of this \"Project\" consists of As, Ts, Gs & Cs", \
                "This author was born in 1926, the daughter of Amasa, an Alabama lawyer, & Frances, whose maiden name was Finch", \
                "She's the Bronte sister who wrote \"Wuthering Heights\"", \
                "Its largest airport is named for a World War II hero; its second largest, for a World War II battle", \
                "His pride had cast him out from heaven, with all his host of rebel angels"}

    for instance in jeopardy_qs:
        question = instance["question"]
        if "<" in question or ">" in question or "/" in question or "[" in question or "]" in question or question in examples:
            continue

        answer = re.sub(" \(.*\)|\(.*\) ", "", instance["answer"])
        answer = answer.lower()

        rounds[instance["round"]].append((instance["category"], question, answer))

    return rounds

def get_definition(def_type):
    if def_type == 0:
        definition = "Given a category and a trivia clue of relatively easy difficulty, generate the best answer that belongs in the category and is described by the clue. For simplicity, all answers should be lowercased."
    elif def_type == 1:
        definition = "Given a category and a trivia clue of relatively medium difficulty, generate the best answer that belongs in the category and is described by the clue. For simplicity, all answers should be lowercased."
    elif def_type == 2:
        definition = "Given a category and a trivia clue of relatively hard difficulty, generate the best answer that belongs in the category and is described by the clue. For simplicity, all answers should be lowercased."
    else:
        definition = "Given a category and a trivia clue of varying difficulties, generate the best answer that belongs in the category and is described by the clue. For simplicity, all answers should be lowercased."
    return definition

def get_positive_examples(difficulty):
    if difficulty == 0:
        positives = [{"input": "Category: EVERYBODY TALKS ABOUT IT...\n\nClue: In the winter of 1971-72, a record 1,122 inches of snow fell at Rainier Paradise Ranger Station in this state", "output" : "washington", "explanation" : "Rainier Paradise Ranger Station is located in the Mount Rainier National Park, which is located south of Seattle in the state of Washington."}, \
                     {"input": "Category: ESPN's TOP 10 ALL-TIME ATHLETES\n\nClue: No. 8: 30 steals for the Birmingham Barons; 2,306 steals for the Bulls", "output" : "michael jordan", "explanation" : "Michael Jordan is widely regarded as one of the greatest athletes of all time. He played basketball for the Chicago Bulls in the National Basketball Association and played baseball for the Birmingham Barons in the Minor League Baseball during his first retirement from basketball."}, \
                     {"input": "Category: EPITAPHS & TRIBUTES\n\nClue: Signer of the Dec. of Indep., framer of the Constitution of Mass., second President of the United States", "output" : "john adams", "explanation" : "There are only two presidents who signed the United States Declaration of Independence: John Adams and Thomas Jefferson. However, the Massachusetts Constitution was framed by John Adams and not Thomas Jefferson. Thomas Jefferson primarily worked for the state of Virginia."}]
    elif difficulty == 1:
        positives = [{"input": "Category: WHO'S BUYING?\n\nClue: YouTube, in 2006", "output" : "google", "explanation" : "Google acquired, i.e. bought, YouTube in 2006 for $1.65 billion."}, \
                     {"input": "Category: PRESIDENTS\n\nClue: In 1956 this President's cabinet gave him a Grandma Moses painting of his Gettysburg farm", "output" : "eisenhower", "explanation" : "Dwight Eisenhower was the President of the United States in 1956."}, \
                     {"input": "Category: LOOK OUT \"BELL\"OW\n\nClue: Sailors wore these long before the groovy folks in the '60s", "output" : "bell-bottoms", "explanation" : "Notice how the category involves wordplay on both the clue and the answer. A common saying for sailors is \"look out below\" while bell-bottoms contains \"bell\" in the category. Bell-bottoms are also what the \"groovy folks\" like the hippies wore in the 1960s."}]
    elif difficulty == 2:
        positives = [{"input": "Category: HOMOPHONIC PAIRS\n\nClue: It's a notation on a percussion store to clash", "output" : "cymbal symbol", "explanation" : "\"Cymbal\" and \"symbol\" both have the same pronunciations but different meanings, hence they are homophonic pairs. A symbol is the notation and a cymbal is a percussion instrument that clashes and rings."}, \
                     {"input": "Category: SCIENCE NEWS\n\nClue: Made available for download in July 2000 by UCSC, the 739MB file of this \"Project\" consists of As, Ts, Gs & Cs", "output" : "the human genome project", "explanation" : "The Human Genome Project was the international research effort to determine the DNA sequence of the entire human genome. DNA sequences only contain the letters \"A\", \"T\", \"G\", and \"C\"."}, \
                     {"input": "Category: 20th CENTURY\n\nClue: This author was born in 1926, the daughter of Amasa, an Alabama lawyer, & Frances, whose maiden name was Finch", "output" : "harper lee", "explanation" : "Harper Lee is the author of the best-selling book \"To Kill A Mockingbird\" where Atticus Finch is a lawyer in Alabama, hence how the characters in her book are loosely influenced by her life and family members."}]
    else:
        positives = [{"input": "Category: HOMOPHONIC PAIRS\n\nClue: It's a notation on a percussion store to clash", "output" : "cymbal symbol", "explanation" : "\"Cymbal\" and \"symbol\" both have the same pronunciations but different meanings, hence they are homophonic pairs. A symbol is the notation and a cymbal is a percussion instrument that clashes and rings."}, \
                     {"input": "Category: EPITAPHS & TRIBUTES\n\nClue: Signer of the Dec. of Indep., framer of the Constitution of Mass., second President of the United States", "output" : "john adams", "explanation" : "There are only two presidents who signed the United States Declaration of Independence: John Adams and Thomas Jefferson. However, the Massachusetts Constitution was framed by John Adams and not Thomas Jefferson. Thomas Jefferson primarily worked for the state of Virginia."}, \
                     {"input": "Category: LOOK OUT \"BELL\"OW\n\nClue: Sailors wore these long before the groovy folks in the '60s", "output" : "bell-bottoms", "explanation" : "Notice how the category involves wordplay on both the clue and the answer. A common saying for sailors is \"look out below\" while bell-bottoms contains \"bell\" in the category. Bell-bottoms are also what the \"groovy folks\" like the hippies wore in the 1960s."}]

    return positives

def get_negative_examples(difficulty):
    if difficulty == 0:
        negatives = [{"input": "Category: HISTORY\n\nClue: Built in 312 B.C. to link Rome & the South of Italy, it's still in use today", "output" : "the silk road", "explanation" : "The correct answer is actually the Appian Way. The Silk Road is no longer in use and actually connected all of Europe, Africa, the Middle East, and Asia. The Silk Road also did not go through Italy, though it did emerge around 200 B.C.."}, \
                     {"input": "Category: EVERYBODY TALKS ABOUT IT...\n\nClue: The city of Yuma in this state has a record average of 4,055 hours of sunshine each year", "output" : "california", "explanation" : "The correct answer is actually Arizona. Yuma is on the California-Arizona border, but it is located in Arizona. Arizona is also more likely to have more hours of sun than California since more of its land is semiarid and arid than California's land is."}]
    elif difficulty == 1:
        negatives = [{"input": "Category: ALL THAT JAZZ\n\nClue: \"Miles Ahead\" is a 1957 album by this jazz trumpeter", "output" : "john coltrane", "explanation" : "John Coltrane was a jazz saxophonist while Miles Davis was a jazz trumpeter. The title of the album is also a play on words of Miles Davis's name."}, \
                     {"input": "Category: GANDHI, FDR OR CHURCHILL\n\nClue: He became a lawyer in London in 1891", "output" : "churchill", "explanation" : "Churchill was actually not a lawyer in England. FDR was only 9 years old in 1891, so he was too young to be a lawyer. Gandhi was a lawyer in London in 1891."}]
    elif difficulty == 2:
        negatives = [{"input": "Category: U.S. CITIES\n\nClue: Its largest airport is named for a World War II hero; its second largest, for a World War II battle", "output" : "new york city", "explanation" : "The correct answer is actually Chicago where the largest airport is named after Edward O'Hare and the second largest airport is named after the Battle of Midway."}, \
                     {"input": "Category: FAMOUS WOMEN\n\nClue: She's the Bronte sister who wrote \"Wuthering Heights\"", "output" : "charlotte bronte", "explanation" : "The correct answer is actually Emily Bronte. Charlotte Bronte is famous for writing \"Jane Eyre\" whereas Emily Bronte is famous for writing \"Wuthering Heights\"."}]
    else:
        negatives = [{"input": "Category: ALL THAT JAZZ\n\nClue: \"Miles Ahead\" is a 1957 album by this jazz trumpeter", "output" : "john coltrane", "explanation" : "John Coltrane was a jazz saxophonist while Miles Davis was a jazz trumpeter. The title of the album is also a play on words of Miles Davis's name."}, \
                     {"input": "Category: FAMOUS WOMEN\n\nClue: She's the Bronte sister who wrote \"Wuthering Heights\"", "output" : "charlotte bronte", "explanation" : "The correct answer is actually Emily Bronte. Charlotte Bronte is famous for writing \"Jane Eyre\" whereas Emily Bronte is famous for writing \"Wuthering Heights\"."}]
    return negatives

def get_instances(round_qa):
    instances = []
    instance_set = set()
    for category, question, answer in round_qa:
        question = re.sub("^'|'$", "", question)
        instance_input = "Category: " + category + "\n\n" + "Clue: " + question
        if (instance_input.lower(), answer.lower()) in instance_set:
            continue
        instance = {"input" : instance_input, "output" : [answer]}
        instances.append(instance)
        instance_set.add((instance_input.lower(), answer.lower()))
    print(len(instances))
    random.shuffle(instances)
    return instances

def create_jsons(rounds, task_num, difficulty, round_type):
    contributors = ["Eshaan Pathak"]
    source = ["jeopardy (https://www.reddit.com/r/datasets/comments/1uyd0t/200000_jeopardy_questions_in_a_json_file/)"]
    question_answer_categ = ["Answer Generation"]

    question_answer_json = {}
    question_answer_json["Contributors"] = contributors
    question_answer_json["Source"] = source
    question_answer_json["Categories"] = question_answer_categ
    question_answer_json["Definition"] = get_definition(difficulty)
    question_answer_json["Positive Examples"] = get_positive_examples(difficulty)
    question_answer_json["Negative Examples"] = get_negative_examples(difficulty)

    if round_type[0] == "":
        all_rounds = rounds["Jeopardy!"] + rounds["Double Jeopardy!"] + rounds["Final Jeopardy!"]
        random.shuffle(all_rounds)
        question_answer_json["Instances"] = get_instances(all_rounds[:6500])
    else:
        question_answer_json["Instances"] = get_instances(rounds[round_type[0]][:6500])

    with open("task{}_jeopardy_answer_generation_{}.json".format(task_num, round_type[1]), "w", encoding="utf-8") as f:
        json.dump(question_answer_json, f, indent=4)


if __name__ == "__main__":
    filename = "jeopardy_questions.json"

    rounds = read_file(filename)

    create_jsons(rounds, 305, 0, ("Jeopardy!", "normal"))
    create_jsons(rounds, 306, 1, ("Double Jeopardy!", "double"))
    create_jsons(rounds, 307, 2, ("Final Jeopardy!", "final"))
    create_jsons(rounds, 308, 3, ("", "all"))
