from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from datetime import timedelta, datetime
nexttime=(datetime.today() + timedelta(+1)).strftime('%Y_%m_%d_%H')

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

def get_pic():
    mkdir('pic')
    print("开始截图。。。")
    driver.save_screenshot('./pic/screen.png') 
    rangle = (1816,50, 1900,920)
    i = Image.open("./pic/screen.png")
    frame4 = i.crop(rangle)
    nowtime=time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime()) 
    frame4.save('./pic/'+nowtime+'.png')
    print("截图完成")

while True:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    #如果有gpu加速的话，就取消下列注释
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920x1080')
    #chrome_options.add_argument('--proxy-server=127.0.0.1:7890')
    driver = webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.fun135.com/cn/home.htm")
    driver.find_element_by_id("btnHeaderLogin").click()
    driver.find_element_by_xpath("//div[67]/div/div/div/button/span").click()
    driver.find_element_by_id("txtUsername").click()
    driver.find_element_by_id("txtUsername").click()
    driver.find_element_by_id("txtUsername").clear()
    driver.find_element_by_id("txtUsername").send_keys("hoodh1")
    driver.find_element_by_id("txtPassword").click()
    driver.find_element_by_id("txtPassword").clear()
    driver.find_element_by_id("txtPassword").send_keys("12345qwert")
    driver.find_element_by_id("btnHeaderLogin").click()
    sleep(5)
    newwindow = 'window.open("https://www.fun135.com/Gamelobby/KYG/2176/0.do?isdemo=0")'
    driver.execute_script(newwindow)
    driver.switch_to_window(driver.window_handles[0])
    driver.close()
    sleep(5)
    driver.switch_to_window(driver.window_handles[0])
    print('休眠90s等待加载。。。')
    sleep(90)
    print('休眠完成。。。')
    ActionChains(driver).move_by_offset(400, 320).click().perform()
    while True:
        nowtime=time.strftime("%Y-%m-%d_%H", time.localtime())
        if nowtime==nexttime:
            driver.close()
            nexttime=(datetime.today() + timedelta(+1)).strftime('%Y_%m_%d_%H')
            break
        get_pic()
        sleep(35*7)