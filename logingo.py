from sys import platform
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from time import sleep
import pyrebase
import requests
import json

firebaseConfig={
    'apiKey': "AIzaSyB3KR9qWJyQ9_3FdvgwgNKTiSSxFVv-Jwo",
    'authDomain': "discordbot-011221.firebaseapp.com",
    'databaseURL': "https://discordbot-011221-default-rtdb.firebaseio.com",
    'projectId': "discordbot-011221",
    'storageBucket': "discordbot-011221.appspot.com",
    'messagingSenderId': "431127808567",
    'appId': "1:431127808567:web:10e41831f6347bffc10db2",
    'measurementId': "G-FYNRE35WP1"}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

usernames_stored = []

gl = GoLogin({
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MTc2ZWViMzZkNmM2MjYyZTU4NTA4NjciLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2MTllMmJlNjViYmRlNDcwODRiYjA5OWMifQ.pLNuFoKUa0WUUdAapL-yotODjyZj-ZNZjva-d5eR9iY',
    'profile_id': '61aa6f2fdc8acbe8b9081328',
})

if platform == "linux" or platform == "linux2":
    chrome_driver_path = './chromedriver'
elif platform == "darwin":
    chrome_driver_path = './mac/chromedriver'
elif platform == "win32":
    chrome_driver_path = 'chromedriver.exe'

debugger_address = gl.start()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)
chrome_options.add_argument("user-agent=whatever you want")
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

# driver.get("http://www.python.org")

def list_all_users(group_name, user_name, discrim_base):
    print('\n 51 List all users')
    all_users = requests.get("https://discordbot-011221-default-rtdb.firebaseio.com/"+group_name+".json")
    if all_users.json() == None:
        return False
    elif not user_name in all_users.json().keys(): 
        return False
    elif all_users.json()[user_name]['discrimbase'] == discrim_base:
        return True
    else:
        return False

    # all_users = requests.get("https://discordbot-011221-default-rtdb.firebaseio.com/"+group_name+".json")
    # all_users = [str(name) for name in all_users.json() if not name == None]
    # print(all_users)
    # if user_name in all_users:
    #     return True
    # else:
    #     return False
    print('\n 60 Exit List all users')
    # return all_users

def add_users(group_name, user_name, discrim_base):
    print('\n 63 Addusers')
    try:
        data= {
            "m_sent": True,
            "name" : user_name,
            "discrimbase" : discrim_base,
        }
        db.child(group_name).child(user_name).set(data)
        print('\n Success!')
    except Exception as e:
        print('\n83', e)

def logindescord(channel_link, user_email, user_password):
    driver.get(channel_link)
    # driver.get("https://discord.com/channels/831821113989660674/833635708001320980")

    try:
        driver.find_element(By.NAME, "email").send_keys(user_email)
        # driver.find_element(By.NAME, "email").send_keys("kundan3331998@gmail.com")
    except:
        print('34- on email')
    # email_name.send_keys("malikwajid887@gmail.com")
    # driver.find_element_by_name("email").send_keys("malikwajid887@gmail.com")
    try:
        driver.find_element(By.NAME,"password").send_keys(user_password)
        # driver.find_element(By.NAME,"password").send_keys("Mobile016")
    except:
        print('34- on password')
    # driver.find_element_by_name("password").send_keys("mobile016")

    try:
        driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]").click()
        print("\nstart 20s sleep")
        sleep(20)
        print("\nEnd 20s sleep")
    except:
        print('34- on close button')

    try:
        driver.find_element(By.CLASS_NAME, "closeIcon-150W3V").click()
    except:
        print("57", "Error in close button")
    sleep(2)

def send_message(user_id, group_name, channel_link, message_sent):
    try:
        WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-list-item-id='members-833635708001320980___0']"))
        )

        # driver.find_element(By.CSS_SELECTOR, "div[data-list-item-id='members-833635708001320980___"+ str(user_id) +"']").click()
        # driver.find_element(By.CSS_SELECTOR, "div[class='member-3-YXUe container-2Pjhx- clickable-1JJAn8' index='"+ str(user_id) +"']").click()
        driver.find_element(By.XPATH ,'//div[@class="member-3-YXUe container-2Pjhx- clickable-1JJAn8" and @index="'+ str(user_id) +'"]').click()
        sleep(5)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "username-2b1r56")))

            username = driver.find_element(By.CLASS_NAME, "username-2b1r56").text.strip()

            discrimBase = driver.find_element(By.CLASS_NAME, "discrimBase-24vY8o").text.strip()
            complete_name = str(username) + str(discrimBase)
            try:
                if list_all_users(group_name, username, discrimBase):
                    print('\n\nNote:', complete_name ,'Already in the list\n')
                else:
                    print('Adding User:', complete_name,'\n')
                    add_users(group_name, username, discrimBase)
                    try:
                        # driver.find_element(By.CSS_SELECTOR, "input[class='inputDefault-_djjkz']").send_keys("Hi there how are you")
                        driver.find_element(By.CLASS_NAME, "input-2_SIlA").send_keys(message_sent)
                        driver.find_element(By.CLASS_NAME, "input-2_SIlA").send_keys(Keys.ENTER)
                        sleep(10)
                        WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='headerText-2F0828']"))
                        )
                        driver.get(channel_link)
                    except Exception as e:
                        print("\n120 --------", e)
            except Exception as er:
                print('\n 122', er)
            # if not complete_name in usernames_stored:
            #     usernames_stored.append(complete_name)
            #     print('\n\n', user_id, username, discrimBase, '\n\n')
            # else:
            #     print(user_id,complete_name, 'already in the list')
            # pass
        except Exception as ew:
            print('\n 127', ew)
            pass    
    except Exception as e:
        print("\n130 --------", e)

def scroll_sidebar():
    print('\n ScrollBar')
    try:
        liElement = driver.find_element(By.CSS_SELECTOR, "div[data-list-id='members-833635708001320980']")
    
        # driver.execute_script("arguments[0].scrollIntoView(true);", liElement)
        for i in range(10):
        # scroll_sidebar()
            liElement.send_keys(Keys.ARROW_DOWN*10)
        sleep(5)
        # driver.execute_script("window.scrollBy(0, 250)", liElement)
    except Exception as e:
        print('\n 149', e)

def google():
    driver.get("https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAmgQ")
    driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys("abdulwajidds5@gmail.com")
    driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/span').click()
    try:
        driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys("mobile016")
    except:
        driver.find_element_by_name("password").send_keys("mobile016")

def youtube():
    driver.get("https://www.youtube.com/watch?v=FQpyOw55LGc")

def outlook():
    driver.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1638525047&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3d6d02bd7d-e33f-c82a-43e2-4fc720d47bcf&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld")

    sleep(1)
    # try:
    #     driver.find_element(By.NAME, "loginfmt").send_keys("lizjjo174@outlook.com")
    # except Exception as e:
    #     print('158- on email', e)
    # sleep(2)

    # try:
    #     driver.find_element(By.ID, "idSIButton9").click()
    # except Exception as e:
    #     print('164- on Next', e)
    # sleep(2)
    
    # try:
    #     driver.find_element(By.NAME, "passwd").send_keys("lRMaXHsSA")
    # except Exception as e:
    #     print('170- on password', e)
    # sleep(3)
    
    # try:
    #     driver.find_element(By.ID, "idSIButton9").click()
    # except Exception as e:
    #     print('176- on Sign In', e)

    sleep(5)
    try:
        # driver.find_elements_by_xpath("//*[@class='ms-Button' and @class='GJoz3Svb7GjPbATIMTlpL' and @class='_2W_XxC_p1PufyiP8wuAvwF' and @class='lZNvAQjEfdlNWkGGuJb7d' and @class='ms-Button--commandBar' and @class='root-168]").click()
        # driver.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div/div/button').click()
        driver.find_element(By.ID, "id__6").click()
    except Exception as e:
        print('183- on New message', e)

    sleep(12)
    try:
        # driver.find_element_by_xpath("//*[@class='ms-BasePicker-input' or @class='pickerInput_cc9894a7']").send_keys("abdulwajid616@outlook.com")
        # element = driver.find_element(By.CLASS_NAME, "ms-BasePicker-input").send_keys("abdulwajid616@outlook.com")
        element = driver.find_element(By.CSS_SELECTOR , "input[class='ms-BasePicker-input pickerInput_cc9894a7']")
        element.send_keys("abdulwajid616@outlook.com")
        element.send_keys(Keys.ENTER)

        print('\n190 = ',element)
        # driver.find_element(By.CSS_SELECTOR(".ms-BasePicker-input.pickerInput_cc9894a7")).send_keys("abdulwajid616@outlook.com")
    except Exception as e:
        print('189- on Message To', e)

if __name__ == "__main__":
    ChannelLink = "https://discord.com/channels/831821113989660674/833635708001320980"
    UserEmail = "kundan3331998@gmail.com"
    UserPassword = "Mobile016"

    GroupName = "Checking"
    MessageSent = "Good Luck to you!"

    logindescord(ChannelLink, UserEmail, UserPassword)

    # sleep(5)
    # for i in range(10):
    #     scroll_sidebar()
        # sleep(4)
    # new_mem = 0
    for i in range(100):
        # if new_mem > 10:
        #     scroll_sidebar()
        #     new_mem = 0
        send_message(i+10, GroupName, ChannelLink, MessageSent)
        sleep(3)
        # new_mem += 1

    sleep(1000)
    driver.close()
    sleep(3)
    gl.stop()