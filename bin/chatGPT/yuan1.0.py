from yuan_api.inspurai import Yuan, set_yuan_account,Example
from test_constructor import *
from loguru import logger

# 1. set account
set_yuan_account("allen", "18805841931")

yuan = Yuan(engine='dialog',
            #input_prefix="question: “",
            #input_suffix="”",
            #output_prefix="answer: “",
            #output_suffix="”",
            )

def save_json(file_path, dict):
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(dict, file, indent=4, ensure_ascii=False)

tests = ['analogicalReasoning',
'cognitiveReflection',
'criticalThinking',
'datcreativity',
'EI-branch1',
'EI-branch2',
'EI-branch3',
'EI-branch4',
'emaphySkills',
'inferentialReasoning',
'readingComprehension',
'remoteAssociate',
'self-efficacy',
'sense_of_humor',
'social_interests',
'strangeStory',
'systemThinking',
'ToMTest']
origin_path = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\yuan_result\test_{}_result.json'
data = construct_english()
result = {}
for index, test in enumerate(tests):
    result = {}
    questions = data[test]
    for question in questions:

        response = yuan.submit_API(question, trun="“")
        result[question] = response

        '''flag = 0
        while flag == 0:
            response = yuan.submit_API(question, trun="“")
            if "请求异常" not in str(response):
                result[question] = response
                flag = 1
                logger.info(f'{question} \n {response}' )
            else:
                continue'''
    save_json(origin_path.format(test), result)
    logger.info(f"{test} saved")
