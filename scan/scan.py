import json
import re
import random

def split_line(s):
    in_out = re.split("OUT: ", s)
    in_out[0] = in_out[0].rstrip()
    in_out[0] = re.split("IN: ", in_out[0])[1]
    return in_out

def read_file(filename):
    command_actions = set()
    with open(filename, "r") as f:
        for line in f:
            line = line.strip("\n")
            command_actions.add(line)
    command_actions = list(command_actions)
    command_action_dict = dict()
    action_command_dict = dict()
    for s in command_actions:
        command, action = split_line(s)
        if command not in command_action_dict:
            command_action_dict[command] = [action]
        elif command in command_action_dict:
            command_action_dict[command].append(action)
        if action not in action_command_dict:
            action_command_dict[action] = [command]
        elif action in action_command_dict:
            action_command_dict[action].append(command)
    print("filename: {} | {} | {}".format(filename, len(command_action_dict), len(action_command_dict)))
    return command_action_dict, action_command_dict

def get_definition(command_action):
    if command_action:
        definition = "Given a command in a limited form of natural language, provide the correct sequence of actions that executes the command to thus navigate an agent in its environment. A command can be broken down into many different actions. Actions are uppercase and are individual steps that serve as the building blocks for a command. For commands, 'left' and 'right' are used to denote the direction of an action. The word 'opposite' turns the agent backward in the specified direction. The word 'around' makes the agent execute an action while turning around in the specified direction. The word 'and' means to execute the next scope of the command following the previous scope of the command. The word 'after' signifies to execute the previous scope of the command following the next scope of the command. The words 'twice' and 'thrice' trigger repetition of a command that they scope over two times or three times, respectively. There are only six actions: 'I_LOOK', 'I_WALK', 'I_RUN', 'I_JUMP', 'I_TURN_LEFT', and 'I_TURN_RIGHT'. These actions respectively align with the commands 'look', 'walk', 'run', 'jump', 'turn left', and 'turn right'. Actions and commands do not have quotations in the input and output."
    else:
        definition = "Given a sequence of actions to navigate an agent in its environment, provide the correct command in a limited form of natural language that matches the sequence of actions when executed. Commands are lowercase and encapsulate the logic of the sequence of actions. Actions are individual steps that serve as the building blocks for a command. There are only six actions: 'I_LOOK', 'I_WALK', 'I_RUN', 'I_JUMP', 'I_TURN_LEFT', and 'I_TURN_RIGHT'. These actions respectively align with the commands 'look', 'walk', 'run', 'jump', 'turn left', and 'turn right'. For commands, 'left' and 'right' are used to denote the direction of an action. opposite turns the agent backward in the specified direction. The word 'around' makes the agent execute an action while turning around in the specified direction. The word 'and' means to execute the next scope of the command following the previous scope of the command. The word 'after' signifies to execute the previous scope of the command following the next scope of the command. The words 'twice' and 'thrice' trigger repetition of a command that they scope over two times or three times, respectively. Actions and commands do not have quotations in the input and output."
    return definition

def get_positive_examples(command_action):
    if command_action:
        positives = [{"input": "jump left", "output" : "I_TURN_LEFT I_JUMP", "explanation" : "The agent must first turn left and then jump in order to jump to the left."}, \
                     {"input": "jump around right", "output" : "I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP", "explanation" : "The agent must turn right and jump four times in a row to circle back to its original position."}, \
                     {"input": "turn around left and look right twice", "output" : "I_TURN_LEFT I_TURN_LEFT I_TURN_LEFT I_TURN_LEFT I_TURN_RIGHT I_LOOK I_TURN_RIGHT I_LOOK", "explanation" : "The agent must turn to the left four times and then alternate between turning right and looking twice."}]
    else:
        positives = [{"input": "I_TURN_LEFT I_JUMP", "output" : "jump left", "explanation" : "If the agent turned to the left and jumped, then the agent jumped to the left."}, \
                     {"input": "I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP", "output" : "jump around right", "explanation" : "If the agent turned right and jumped four times in a row, then the agent jumped around to the right."}, \
                     {"input": "I_TURN_LEFT I_TURN_LEFT I_TURN_LEFT I_TURN_LEFT I_TURN_RIGHT I_LOOK I_TURN_RIGHT I_LOOK", "output" : "turn around left and look right twice", "explanation" : "If the agent turned to the left four times, then it turned around to the left. If it turned right and looked twice, then it looked right twice."}]
    return positives

def get_negative_examples(command_action):
    if command_action:
        negatives = [{"input": "jump right", "output" : "I_JUMP I_TURN_RIGHT", "explanation" : "The agent cannot jump and then turn to the right in order to jump to the right. To jump and then turn to the right, the command will tell the agent to 'jump and turn right'. The correct output is 'I_TURN_RIGHT I_JUMP'."}, \
                     {"input": "jump around left", "output" : "I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP", "explanation" : "Although the agent is back at its original position, it did not properly follow directions by turning to the right to jump around on the left side."}]
    else:
        negatives = [{"input": "I_JUMP I_TURN_RIGHT", "output" : "jump right", "explanation" : "The agent jumped forward and then turned to the right instead of jumping to the right. This output matches 'I_TURN_RIGHT I_JUMP'. The correct output should be 'jump and turn right'."}, \
                     {"input": "I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP", "output" : "jump around left", "explanation" : "The correct output is 'jump around right' because of how the agent is turning to the right before each time it jumps."}]
    return negatives

def get_instances(inp_out):
    instances = []
    for ind, (inp, out) in enumerate(inp_out):
        if ind >= 6500:
            break
        instance = {"input" : inp, "output" : out}
        instances.append(instance)
    return instances

def shuffle_dict(dictionary):
    keys = list(dictionary.keys())
    random.shuffle(keys)
    return [(key, dictionary[key]) for key in keys]

def create_jsons(command_action_dict, action_command_dict, task_num, split_type):
    contributors = ["Eshaan Pathak"]
    source = ["scan (https://github.com/brendenlake/SCAN)"]
    command_action_categ = ["Structured Text Generation"]
    action_command_categ = ["Long Text Generation"]

    command_action_json = {}
    action_command_json = {}

    command_action_json["Contributors"] = contributors
    action_command_json["Contributors"] = contributors

    command_action_json["Source"] = source
    action_command_json["Source"] = source

    command_action_json["Categories"] = command_action_categ
    action_command_json["Categories"] = action_command_categ

    command_action_json["Definition"] = get_definition(True)
    action_command_json["Definition"] = get_definition(False)

    command_action_json["Positive Examples"] = get_positive_examples(True)
    action_command_json["Positive Examples"] = get_positive_examples(False)

    command_action_json["Negative Examples"] = get_negative_examples(True)
    action_command_json["Negative Examples"] = get_negative_examples(False)

    command_action_json["Instances"] = get_instances(command_action_dict)
    action_command_json["Instances"] = get_instances(action_command_dict)

    with open("task{}_scan_structured_text_generation_command_action_{}.json".format(task_num, split_type), "w", encoding="utf-8") as f:
        json.dump(command_action_json, f, indent=4)
    with open("task{}_scan_long_text_generation_action_command_{}.json".format(task_num + 1, split_type), "w", encoding="utf-8") as f:
        json.dump(action_command_json, f, indent=4)


if __name__ == "__main__":
    all_filename = "tasks.txt"
    short_filename = "tasks_train_length.txt"
    long_filename = "tasks_test_length.txt"

    command_action_dict, action_command_dict = read_file(all_filename)
    command_action_lst = shuffle_dict(command_action_dict)
    action_command_lst = shuffle_dict(action_command_dict)
    create_jsons(command_action_lst, action_command_lst, 126, "all")

    command_action_dict, action_command_dict = read_file(short_filename)
    command_action_lst = shuffle_dict(command_action_dict)
    action_command_lst = shuffle_dict(action_command_dict)
    create_jsons(command_action_lst, action_command_lst, 128, "short")

    command_action_dict, action_command_dict = read_file(long_filename)
    command_action_lst = shuffle_dict(command_action_dict)
    action_command_lst = shuffle_dict(action_command_dict)
    create_jsons(command_action_lst, action_command_lst, 130, "long")
