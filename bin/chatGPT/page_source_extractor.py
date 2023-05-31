import os
import re
import json
from lxml import etree
from loguru import logger

def extract(history_path):

    re_input = '<div class="markdown-body markdownContent--clvGcXya"><p>(.*?)</p>'
    result = {}

    with open(history_path, 'r', encoding='gbk') as file:
        # 读取文件的全部内容
        text = file.read()

    text = text.replace('\n', '')

    content = re.findall(re_input, text)

    for i, j in enumerate(content[:-1]):
        if i % 2 == 0:
            result[j] = re.findall(re_input, text)[i+1]

    #result[content[-1]] = re.findall('<ol>(.*?)</ol>', text)[0].replace('<li>', '').replace('</li>', '')


    return result

def save_json(file_path, dict):
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(dict, file, indent=4, ensure_ascii=False)

path = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\history_test'
json_path = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\result_test'


for i in os.listdir(path):
    result = {}
    file_path = os.path.join(path, i)

    with open(file_path, 'r') as f:
        text = f.read()

    formatted = etree.HTML(text)

    questions = formatted.xpath("//div[@class='questionItem--dS3Alcnv']/div/div/div")
    answers = formatted.xpath(
        "//div[@class='answerItem--U4_Uv3iw']/div/div[@class='containerWrap--lFLVsVCe']/div/div/div[@class='markdown-body markdownContent--clvGcXya']")

    if len(questions) == len(answers):
        logger.info('question and answer match')
        for question, answer in zip(questions, answers):
            s_q = etree.tostring(question, encoding="utf-8").decode()
            s_a = etree.tostring(answer, encoding="utf-8").decode()

            result[re.sub('<[^<]+?>', '', s_q).replace('\n', '')] = re.sub('<[^<]+?>', '', s_a).replace('\n', '')
            save_json(os.path.join(json_path, i[8:-4] + '.json'), result)


    else:
        logger.error('not match')
        break
