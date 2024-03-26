from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time
import os


# https://chromedriver.chromium.org/downloads  # with VPN

class Bot:
    EXECUTABLE_PATH = os.path.join('Files', 'chromedriver.exe')
    URL = r"https://zbmath.org/classification/"

    def __init__(self, options=[]):
        self.service = Service(Bot.EXECUTABLE_PATH)
        self.options = Options()
        for option in options:
            self.options.add_argument(option)

        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.get(Bot.URL)
        self.wait(1)

        self.df = pd.DataFrame(columns=HEADER)

    def start(self):
        urls = []
        for column in self().find_element(By.CLASS_NAME, 'content-main').find_elements(By.XPATH, "//div[@class='left' or @class='center' or @class='right']"):
            for article in column.find_elements(By.TAG_NAME, 'article'):
                urls.append(article.find_element(By.TAG_NAME, 'a').get_attribute('href'))

        for url in urls:
            print('Start For:', url)
            self.start_page(url)

    def start_page(self, url):
        self.go(url)
        self.wait(2)
        parents = {}  # int: code
        for item in self().find_element(By.CLASS_NAME, 'content-result').find_elements(By.CLASS_NAME, 'item'):
            level = int(item.get_attribute('class')[-1])
            article = item.find_element(By.TAG_NAME, 'article')
            code_a = article.find_element(By.CLASS_NAME, 'code').find_element(By.TAG_NAME, 'a')
            code = str(code_a.text)
            text = article.find_element(By.CLASS_NAME, 'text').find_element(By.TAG_NAME, 'a').text
            self.df.loc[len(self.df)+1] = {'Name': code, 'Parent': parents.get(level-1, ''), 'Description': text, 'URL': code_a.get_attribute('href')}
            parents[level] = code

    @classmethod
    def wait(cls, delay=1): time.sleep(delay)

    def go(self, url): self().get(url)

    def home(self): self.go(Bot.URL)

    def __call__(self): return self.driver


HEADER = ['Name', 'Parent', 'Description', 'URL']
OPTIONS = ['start-maximized']

if __name__ == "__main__":
    bot = Bot(OPTIONS)
    bot.start()
    bot.df.to_csv('msc-search.txt')

    input('press <enter> to exit...')
