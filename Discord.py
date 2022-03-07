#!/usr/bin python

# removing single button

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
import _thread as thread

usernames_stored = []

# def declaration():
opt = Options()
# opt.add_argument("--disable-infobars")
# opt.add_argument("--headless")
opt.add_argument("--disable-gpu")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument('--ignore-certificate-errors')
opt.add_argument('--ignore-ssl-errors')
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 0,
    "profile.default_content_setting_values.geolocation": 0,
    "profile.default_content_setting_values.notifications": 2
})

DRIVER_PATH = 'chromedriver.exe'
driver_bill = webdriver.Chrome(options=opt, executable_path=DRIVER_PATH)


# driver_bill.get("https://discord.com/login")
driver_bill.get("https://discord.com/channels/831821113989660674/833635708001320980")

driver_bill.find_element(By.NAME, "email").send_keys("malikwajid887@gmail.com")
# email_name.send_keys("malikwajid887@gmail.com")
# driver_bill.find_element_by_name("email").send_keys("malikwajid887@gmail.com")
driver_bill.find_element(By.NAME,"password").send_keys("mobile016")
# driver_bill.find_element_by_name("password").send_keys("mobile016")

driver_bill.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]").click()
print("\nstart 20s sleep")
sleep(20)
print("\nEnd 20s sleep")

try:
    driver_bill.find_element(By.CLASS_NAME, "closeIcon-150W3V").click()
except:
    print("57", "Error in close button")

# sleep(2)
# try:
#     sidebar = driver_bill.find_element(By.CLASS_NAME, "membersWrap-2h-GB4")
#     # sidebar.send_keys()
#     sidebar.send_keys(Keys.END)
# except Exception as e:
#     print("\n69 --------", e)

def send_message(user_id):
    sleep(2)
    try:
        driver_bill.find_element(By.CSS_SELECTOR, "div[data-list-item-id='members-833635708001320980___"+ str(user_id) +"']").click()
    except Exception as e:
        print("\n78 --------", e)

    sleep(5)
    try:
        username = driver_bill.find_element(By.CLASS_NAME, "username-2b1r56").text.strip()

        discrimBase = driver_bill.find_element(By.CLASS_NAME, "discrimBase-24vY8o").text.strip()
        complete_name = str(username) + str(discrimBase)
        if not complete_name in usernames_stored:
            usernames_stored.append(complete_name)
            print('\n\n', user_id, username, discrimBase, '\n\n')
        else:
            print(user_id,complete_name, 'already in the list')
        pass
    except:
        pass
    try:
        # driver_bill.find_element(By.CSS_SELECTOR, "input[class='inputDefault-_djjkz']").send_keys("Hi there how are you")
        driver_bill.find_element(By.CLASS_NAME, "input-2_SIlA").send_keys("Hi there how are you")
    except Exception as e:
        print("\n83 --------", e)

sleep(20)
# driver_bill.get("https://discord.com/channels/831821113989660674/833635708001320980")

if __name__ ==  "__main__":
    send_message(10)
    send_message(11)
    send_message(10)
    send_message(11)