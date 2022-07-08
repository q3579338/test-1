from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import string
import random
from time import sleep
import json
import requests
import base64
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from config import config
def random_input(size, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

def getcode():
        f=open('ver.png','rb')
        image=base64.b64encode(f.read())
        host='http://api.ttshitu.com/base64'
        headers={
            'Content-Type':'application/json;charset=UTF-8'
        }
        data={
            'username': config.get('user') ,
            'password': config.get('password') ,
            "typeid": 7,
            'image':image.decode('utf-8')
        }
        res=requests.post(url=host,data=json.dumps(data))
        res=res.text
        res=json.loads(res)
        res=res['data']['result']
        return res

def get_location():
    driver.save_screenshot('screen.png') 
    rangle = (815,645, 1024,740)
    i = Image.open("screen.png")
    frame4 = i.crop(rangle)
    frame4.save('ver.png')

while True:
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if config.get('proxy')[0]==True:
        chrome_options.add_argument("--proxy-server="+config.get('proxy')[1])
    driver = webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=chrome_options)
    driver.maximize_window()
    url=config.get('url')

    driver.get(url)
    sleep(2)
    try:
        element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "_evidon-accept-button"))
            )
        driver.find_element_by_id("_evidon-accept-button").click()
    except:
        pass

    driver.find_element_by_xpath("//input").click()
    driver.find_element_by_xpath("//input").clear()
    number=random.randint(1,15)
    First_name=random_input(size=number)
    driver.find_element_by_xpath("//input").send_keys(First_name)
    driver.find_element_by_xpath("//div[2]/div/input").click()
    driver.find_element_by_xpath("//div[2]/div/input").clear()
    number=random.randint(1,15)
    Last_name=random_input(size=number)
    driver.find_element_by_xpath("//div[2]/div/input").send_keys(Last_name)
    driver.find_element_by_name("email").click()
    driver.find_element_by_name("email").clear()
    number=random.randint(6,13)
    Email=random_input(size=number)+'@hostloc.com'
    driver.find_element_by_name("email").send_keys(Email)
    driver.find_element_by_name("confirmEmail").clear()
    Confire_Email=Email
    driver.find_element_by_name("confirmEmail").send_keys(Confire_Email)
    driver.find_element_by_name("captcha").click()
    driver.find_element_by_name("captcha").clear()
    get_location()
    ver=getcode()
    driver.find_element_by_name("captcha").send_keys(ver)
    driver.find_element_by_xpath("//button[@type='button']").click()

    with open('res.txt','a+') as f:
        f.write('Email: '+Email+'\n')
        f.write('First_name: '+First_name+'\n')
        f.write('Last_name: '+Last_name+'\n')
    sleep(2)
    driver.quit()
