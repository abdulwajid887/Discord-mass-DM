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

def get_profile_credential(group_name, profile_name, cred_name):
    all_users = requests.get("https://discordbot-011221-default-rtdb.firebaseio.com/"+group_name+".json")
    output = all_users.json()['Profiles'][profile_name][cred_name]
    return output

token_str = get_profile_credential('credentials', 'Profile1', 'token')
profileId_str = get_profile_credential('credentials', 'Profile1', 'profile_id')

# print(token_str, '----', profileId_str)

gl = GoLogin({
    'token': token_str,
    'profile_id': profileId_str,
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

def get_credential(group_name, channel_name, cred_name):
    all_users = requests.get("https://discordbot-011221-default-rtdb.firebaseio.com/"+group_name+".json")
    output = all_users.json()['Channel'][channel_name][cred_name]
    return output
    # print(all_users.json()[channel_name][cred_name])

def get_account_credential(group_name, account_name, cred_name):
    all_users = requests.get("https://discordbot-011221-default-rtdb.firebaseio.com/"+group_name+".json")
    output = all_users.json()['Account'][account_name][cred_name]
    return output
    # print(all_users.json()[channel_name][cred_name])

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
        EC.presence_of_element_located((By.XPATH ,'//div[@class="member-3-YXUe container-2Pjhx- clickable-1JJAn8" and @index="'+ str(user_id) +'"]'))
        )
        print("\nSend message")
        # driver.find_element(By.CSS_SELECTOR, "div[data-list-item-id='members-833635708001320980___"+ str(user_id) +"']").click()
        # driver.find_element(By.CSS_SELECTOR, "div[class='member-3-YXUe container-2Pjhx- clickable-1JJAn8' index='"+ str(user_id) +"']").click()
        try:
            driver.find_element(By.XPATH ,'//div[@class="member-3-YXUe container-2Pjhx- clickable-1JJAn8" and @index="'+ str(user_id) +'"]').click()
            sleep(5)
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "username-2b1r56")))
                BotUser = False
                try:
                    isBot = driver.find_element(By.XPATH ,'//div[@class="applicationInstallButton-1M2YjM button-38aScr lookFilled-1Gx00P colorBrand-3pXr91 sizeSmall-2cSMqn grow-q77ONN"]')
                    print("\n ---------------- Its a bot!")
                    BotUser = True
                except:
                    print('\n Not Bot')
                    pass
                if not BotUser:
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
                                JS_ADD_TEXT_TO_INPUT = """
                                                        var elm = arguments[0], txt = arguments[1];
                                                        elm.value += txt;
                                                        elm.dispatchEvent(new Event('change'));
                                                        """
                                # driver.find_element(By.CSS_SELECTOR, "input[class='inputDefault-_djjkz']").send_keys("Hi there how are you")
                                # driver.
                                message_element = driver.find_element(By.CLASS_NAME, "input-2_SIlA")
                                driver.execute_script(JS_ADD_TEXT_TO_INPUT, message_element, message_sent)
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
                else:
                    pass
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
            print('\n 200', e)
    except Exception as e:
        print("\n130 --------", e)

def scroll_sidebar(user_id):
    user_id = user_id + 1
    print('\n ScrollBar')
    try:
        WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH ,'//div[@class="member-3-YXUe container-2Pjhx- clickable-1JJAn8" and @index="'+str(10)+'"]'))
        )
        # liElement = driver.find_element(By.CSS_SELECTOR, "div[data-list-id='members-833635708001320980']")
    
        # try:
        #     print("\n 210")
        #     driver.find_element(By.XPATH ,'//span[@class="navigationDescription-3hiGKr"]').click()
        # except Exception as e:
        #     print('\n 213', e)

        # liElement =  driver.find_element(By.XPATH ,'//div[@class="member-3-YXUe container-2Pjhx- clickable-1JJAn8" and @index="'+ str(user_id) +'"]').click()
        try:
            liElement =  driver.find_element(By.XPATH ,'//div[@class="member-3-YXUe container-2Pjhx- clickable-1JJAn8" and @index="'+str(user_id)+'"]')
            liElement.click()
            sleep(0.5)
            liElement.click()
            sleep(0.5)
            print('\n 218 Element found', user_id)
            pass
        except:
            print('\n 221 Not found')
            liElement =  driver.find_element(By.XPATH ,'//div[@class="member-3-YXUe container-2Pjhx- clickable-1JJAn8" and @index="10"]')
            liElement.click()
            sleep(0.5)
            liElement.click()
            sleep(0.5)

            for ind in range(10,user_id+1):
                try:
                    liElement =  driver.find_element(By.XPATH ,'//div[@class="member-3-YXUe container-2Pjhx- clickable-1JJAn8" and @index="'+str(user_id)+'"]')
                    print('\n 231 Element found', user_id)
                    break
                except:
                    print('\n 234 Not found')
                    liElement =  driver.find_element(By.XPATH ,'//div[@class="member-3-YXUe container-2Pjhx- clickable-1JJAn8" and @index="'+str(ind)+'"]')
                    liElement.send_keys(Keys.ARROW_DOWN)
                    sleep(0.01)
            # liElement.click()
            # sleep(1)
            # liElement.click()
            sleep(1)

        # for ind in range(23,user_id+1):
        #     liElement =  driver.find_element(By.XPATH ,'//div[@class="member-3-YXUe container-2Pjhx- clickable-1JJAn8" and @index="'+ str(ind) +'"]')
        #     # liElement.send_keys(Keys.ARROW_DOWN)
        #     liElement.click()
        #     sleep(1)
        #     liElement.click()
        #     sleep(1)
        #     liElement.send_keys(Keys.ARROW_DOWN)
        #     sleep(3)

        # try:
        #     print("\n 221")
        #     driver.find_element(By.XPATH ,'//span[@class="navigationDescription-3hiGKr"]').click()
        # except Exception as e:
        #     print('\n 224', e)
        # driver.execute_script("arguments[0].scrollIntoView(true);", liElement)
        # for i in range(10):
        # # scroll_sidebar()
        #     liElement.send_keys(Keys.ARROW_DOWN*10)
        # sleep(5)
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
    # ChannelLink = "https://discord.com/channels/710018244899110982/905891767558225922"
    ChannelLink = get_credential('credentials', 'channel1', 'link')
    # UserEmail = "kundan3331998@gmail.com"
    UserEmail = get_account_credential('credentials', 'account1', 'username')
    # UserPassword = "Mobile016"
    UserPassword = get_account_credential('credentials', 'account1', 'password')
    # print(UserEmail, UserPassword)

    GroupName = "Channel1"
    MessageSent = get_credential('credentials', 'channel1', 'message')+ u'\u2764'

    print("message collected")

    logindescord(ChannelLink, UserEmail, UserPassword)

    # sleep(5)
    # for i in range(10):
    #     scroll_sidebar()
        # sleep(4)
    new_mem = 0
    for i in range(1,100):
        i=1+i
        if i > 10:
            scroll_sidebar(i)
            new_mem = 0
        send_message(i, GroupName, ChannelLink, MessageSent)
        print('\n', i)
        sleep(3)
        new_mem += 1

    sleep(1000)
    driver.close()
    sleep(3)
    gl.stop()