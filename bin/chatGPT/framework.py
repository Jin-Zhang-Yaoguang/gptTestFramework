import time
import random
import json
from selenium import webdriver
# from bin.chatGPT import config
import config
from test_constructor import *
from loguru import logger
# from page_source_extractor import *

"""# webdriver setup
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
# 隐藏"Chrome正在受到自动软件的控制"
options.add_argument('disable-infobars')"""



# webdriver setup
options = webdriver.FirefoxOptions()
options.set_preference("dom.webdriver.enabled", False)
options.set_preference('useAutomationExtension', False)
options.set_preference('dom.webnotifications.enabled', False)



class GPTTest():
    def __init__(self, url):
        # self.CHROMEDRIVER_PATH = "/Users/jin/Downloads/chromedriver"
        self.INIT_URL = url

    def _login(self):
        # create webdriver and search linkedin login page
        # driver = webdriver.Chrome(options=options, executable_path=self.CHROMEDRIVER_PATH)
        driver = webdriver.Firefox(options=options)

        # 进入初始化界面
        driver.get(self.INIT_URL)

        # 判断当前是否登录完成
        time.sleep(30)

        # 存储 cookie and driver
        cookie_list = driver.get_cookies()
        self.cookie = cookie_list
        self.driver = driver

    def _login_tiangong(self):
        driver = webdriver.Firefox(options=options)
        driver.get(self.INIT_URL)
        driver.find_element(by='xpath', value="*//input[@type='tel']").send_keys(18805841931)
        driver.find_element(by='xpath', value='*//button').click()
        time.sleep(1)
        driver.find_element(by='xpath', value="*//input[@type='password']").send_keys('18805841931Kan')
        driver.find_element(by='xpath', value='*//button').click()

        driver.refresh()

        self.driver = driver

    def _login_xunfei(self):
        driver = webdriver.Firefox(options=options)
        driver.get(self.INIT_URL)
        driver.refresh()
        time.sleep(5)
        driver.find_element(by='xpath', value="*//div[@class=' spark-tab tab-account active-tab']").click()
        time.sleep(2)
        driver.find_element(by='xpath', value="*//input[@id='username']").send_keys(18805841931)
        time.sleep(1)
        driver.find_element(by='xpath', value="*//input[@id='password']").send_keys('18805841931Kan')
        time.sleep(1)

        driver.refresh()
        self.driver = driver

    def _save_cookie(self, file_path):
        with open(file_path, 'w') as f:
            # 将cookies保存为json格式
            f.write(json.dumps(self.cookie))

    def _load_cookie(self, file_path):
        # create webdriver and search linkedin login page
        # driver = webdriver.Chrome(options=options, executable_path=self.CHROMEDRIVER_PATH)
        driver = webdriver.Firefox(options=options)


        # 进入初始化界面
        driver.get(self.INIT_URL)

        # 首先清除由于浏览器打开已有的cookies
        driver.delete_all_cookies()

        with open(file_path, 'r') as cookief:
            cookieslist = json.load(cookief)
            for cookie in cookieslist:
                driver.add_cookie(cookie)

        driver.refresh()
        # 存储 cookie and driver
        # cookie_list = driver.get_cookies()
        # self.cookie = cookie_list
        self.driver = driver

    def chat(self, prompt, llm):
        if llm == 'tongyi':
            self.driver.find_element(by='xpath', value='*//textarea[@id="primary-textarea"]').send_keys(prompt)
            try:
                self.driver.find_element(by='xpath', value='*//div[@class="chatBtn--RFpkrgo_"]').click()
            except:
                pass
            time.sleep(10)

            # 如果看到重新生成则结束，否则等待
            flag = 1
            while flag == 1:
                if self.driver.find_elements(by='xpath', value='*//div[@class="btn--Bw0FbWYV"]/span')[1].text == '重新生成':
                    flag = 0
                else:
                    time.sleep(5)
        if llm == 'wenxin':
            try:
                time.sleep(5)
                self.driver.find_element(by='xpath', value='*//span[@class="KTFDGqJT"]').click()
            except:
                pass
            time.sleep(5)
            self.driver.find_element(by='xpath', value='*//textarea[@class="ant-input wBs12eIN"]').send_keys(prompt)
            try:
                self.driver.find_element(by='xpath', value='*//span[@class="pa6BxUpp"]').click()
            except:
                pass
            time.sleep(5)

            # 如果看到重新生成则结束，否则等待
            flag = 1
            while flag == 1:
                if self.driver.find_elements(by='xpath', value='*//span[@class="yyjIo3Fm"]')[0].text == '重新生成':
                    flag = 0
                else:
                    time.sleep(3)

        if llm == 'xunfei':
            self.driver.find_element(by='xpath', value='*//textarea[@maxlength="7000"]').send_keys(prompt)
            time.sleep(1)
            try:
                self.driver.find_element(by='xpath', value='*//div[@class="ask-window_send__xTavC"]').click()
            except:
                pass
            time.sleep(10)

            # 如果看到重新生成则结束，否则等待
            flag = 1
            while flag == 1:
                if self.driver.find_elements(by='xpath', value='*//div[@class="chat-window_re_answer__JEyKu"]')[1].text == '重新回答':
                    flag = 0
                else:
                    time.sleep(5)

        if llm == 'tiangong':
            while True:
                if self.driver.find_element(by='xpath', value="*//textarea[@class='el-textarea__inner']"):
                    break
                else:
                    time.sleep(5)
                    logger.info('text area loading')
            self.driver.find_element(by='xpath', value="*//textarea[@class='el-textarea__inner']").send_keys(prompt)
            self.driver.find_element(by='xpath', value="*//div[@class='sureSubmitDiv flex alignCenter']").click()
            time.sleep(5)

            # 如果看到重新生成则结束，否则等待
            flag = 1
            while flag == 1:
                try:
                    if self.driver.find_elements(by='xpath', value="*//button[@class='btn flex justifyCenter alignCenter']")[1].text == '重新生成':
                        flag = 0
                    else:
                        time.sleep(2)
                        logger.info('answering')
                except:
                    time.sleep(2)
                    logger.info('not found')

    def save_chat_history(self, file_path):
        with open(file_path, 'w', encoding='gbk') as f:
            # 将cookies保存为json格式
            f.write(self.driver.page_source)


def full():
    for i in [0, 1, 2, 3, 4]:
        #if i == 0:
            #test_instance._login()
            #test_instance._save_cookie(cookie_path)
        #else:
        test_instance._load_cookie(cookie_path)


        data = construct_english()
        for index, test in enumerate(tests):
            if i == 0 and index <= 11:
                continue
            else:
                questions = data[test]
                for question in questions:
                    test_instance.chat(question)

                test_instance.save_chat_history(origin_history_path.format(i, index))

                # save_json(result_path.format(i, index), extract(origin_history_path.format(i, index)))
                logger.info(f"{i} round {index} test chat history extracted")

                test_instance.driver.quit()

                test_instance._load_cookie(cookie_path)

def part(cookie, llm, origin_history_path, tests, data):
    for i in range(5):
        #if i == 0:
        test_instance._login()
        test_instance._save_cookie(cookie)
        # else:
        #test_instance._load_cookie(cookie)
        #test_instance._login_tiangong()
        #test_instance._login_xunfei()

        # for index, test in enumerate(tests):
        for index, test in enumerate(tests):
            questions = data[test]
            for question in questions:
                test_instance.chat(question, llm)

            test_instance.save_chat_history(origin_history_path.format(i, index))

            # save_json(result_path.format(i, index), extract(origin_history_path_tongyi.format(i, index)))
            logger.info(f"{i} round {index} test chat history extracted")

            test_instance.driver.quit()

            test_instance._load_cookie(cookie)
def full_wenxin():
    for i in range(5):
        for index, test in enumerate(tests):
            '''if i == 0 and index == 0:
                test_instance._login()
                test_instance._save_cookie(cookie_path)
            else:
                test_instance._load_cookie(cookie_path)'''
            #test_instance._load_cookie(cookie_path)

            if index == 4 or index == 9 or index == 10:
                continue
            else:
                questions = data[test]
                for question in questions:
                    test_instance.chat(question, 'wenxin')

                test_instance.save_chat_history(origin_history_path_wenxin.format(i, index))

                logger.info(f"{i} round {index} test chat history extracted")

                test_instance.driver.quit()

                test_instance._load_cookie(cookie_path)


if __name__ == '__main__':
    # logger.add("Tongyi.log")

    cookie_path = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\cookie.txt'
    cookie_path_xunfei = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\cookie\cookie_xunfei.txt'
    cookie_path_tongyi = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\cookie\cookie_tongyi.txt'
    cookie_path_wenxin = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\cookie\cookie_wenxin.txt'
    cookie_path_tiangong = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\cookie\cookie_tiangong.txt'

    result_path = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\result\result_round{}_test{}.json'
    origin_history_path_tongyi = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\history_test\history_round{}_test{}.txt'
    origin_history_path_wenxin = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\history_whole\history_wenxin\wenxin_history_round{}_test{}.txt'
    origin_history_path_tiangong = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\history_whole\history_tiangong\tiangong_history_round{}_test{}.txt'
    origin_history_path_xunfei = r'C:\Users\allen\Desktop\Pytorch,Data Structure, Algorithms\CKGSB\bot\gptTestFramework-main\bin\chatGPT\history_whole\history_xunfei\xunfei_history_round{}_test{}.txt'

    test_instance = GPTTest(config.url_xunfei)

    # prompt = """劳拉找到一个标有饼干的盒子，她很高兴，因为这是她的最爱。 但打开盒子后，她发现里面装满了铅笔。 所以她把这个盒子给了她哥哥，她哥哥找了很久他的铅笔. 根据prompt提供的信息回答问题：1.盒子里有什么？2.劳拉起初认为盒子里是什么？3.劳拉的哥哥打开盒子之前会想到什么？"""
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

    test_test = ['EI-branch1_seperated',
             'inferentialReasoning',
             'readingComprehension_seperated']

    data = construct_english()
    # data = sepatated_test()

    # full()
    # part(cookie_path_tiangong, 'tiangong', origin_history_path_tiangong, tests, data)
    part(cookie_path_xunfei, 'xunfei', origin_history_path_xunfei, tests, data)
    # full_wenxin()

    #test_instance._login()
    #test_instance._save_cookie(cookie_path_xunfei)

