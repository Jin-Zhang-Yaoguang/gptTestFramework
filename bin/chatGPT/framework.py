import time
import random
import json
from selenium import webdriver
from bin.chatGPT import config

# webdriver setup
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
# 隐藏"Chrome正在受到自动软件的控制"
options.add_argument('disable-infobars')


class GPTTest():
    def __init__(self):
        self.CHROMEDRIVER_PATH = "/Users/jin/Downloads/chromedriver"
        self.INIT_URL = config.url

    def _login(self):
        # create webdriver and search linkedin login page
        driver = webdriver.Chrome(options=options, executable_path=self.CHROMEDRIVER_PATH)

        # 进入初始化界面
        driver.get(self.INIT_URL)

        # 判断当前是否登录完成
        time.sleep(10)

        # 存储 cookie and driver
        cookie_list = driver.get_cookies()
        self.cookie = cookie_list
        self.driver = driver

    def _save_cookie(self, file_path):
        with open(file_path, 'w') as f:
            # 将cookies保存为json格式
            f.write(json.dumps(self.cookie))

    def _load_cookie(self, file_path):
        # create webdriver and search linkedin login page
        driver = webdriver.Chrome(options=options, executable_path=self.CHROMEDRIVER_PATH)

        # 进入初始化界面
        driver.get(self.INIT_URL)

        # 首先清除由于浏览器打开已有的cookies
        self.driver.delete_all_cookies()

        with open(file_path, 'r') as cookief:
            cookieslist = json.load(cookief)
            for cookie in cookieslist:
                self.driver.add_cookie(cookie)

        self.driver.refresh()
        # 存储 cookie and driver
        cookie_list = driver.get_cookies()
        self.cookie = cookie_list
        self.driver = driver

    def chat(self, prompt):
        self.driver.find_element(by='xpath',value='*//textarea[@id="primary-textarea"]').send_keys(prompt)
        try:
            self.driver.find_element(by='xpath', value='*//div[@class="chatBtn--RFpkrgo_"]').click()
        except:
            pass
        time.sleep(10)

        # 如果看到重新生成则结束，否则等待
        flag = 1
        while flag:
            if self.driver.find_elements(by='xpath', value='*//div[@class="btn--Bw0FbWYV"]/span')[1].text = '重新生成':
                time.sleep(5)
            else:
                flag = 0

    def save_chat_history(self, file_path):
        with open(file_path, 'w') as f:
            # 将cookies保存为json格式
            f.write(self.driver.page_source)



if __name__ == '__main__':
    # 1 登录
    test_instance = GPTTest()
    test_instance._login()

    prompt = """劳拉找到一个标有饼干的盒子，她很高兴，因为这是她的最爱。 但打开盒子后，她发现里面装满了铅笔。 所以她把这个盒子给了她哥哥，她哥哥找了很久他的铅笔. 根据prompt提供的信息回答问题：1.盒子里有什么？2.劳拉起初认为盒子里是什么？3.劳拉的哥哥打开盒子之前会想到什么？"""

    test_instance.chat(prompt)
    test_instance.save_chat_history('/Users/jin/Desktop/project/python/gptTestFramework/bin/chatGPT/history/history')




