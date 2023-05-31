import re
import json


def construct_english():
    test_file = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\test.json'
    with open(test_file, 'r') as f:
        data = json.load(f)

    return data

def sepatated_test():
    test_file = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\content_test\test.json'
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data