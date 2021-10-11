from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import json
import time

"""
REFERENSI
https://www.geeksforgeeks.org/action-chains-in-selenium-python/
"""

class Wa:
    path_send = '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[2]/button'
    path_search = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    path_msg = '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]'
    path_invalid_msg = '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[1]'
    path_users = '//*[@id="pane-side"]/div[1]/div/div/div[xx]/div/div/div[2]/div[1]/div[1]/span' # counter user diganti dengan 'xx'
    path_driver = "drivers\\chromedriver.exe"
    delay_wa_load = 20 
    browser = None
    verbose = False  # debug mode
    
    def __init__(self, verbose=False, headless=False, logging = False):
        self.verbose = verbose

        if self.verbose:
            print("WA2: Construct")   

        try:
            with open("xpath.json") as f:
                vars = json.load(f)
                self.path_send = vars['path_send']
                self.path_search = vars['path_search']
                self.path_msg = vars['path_msg']
                self.path_invalid_msg = vars['path_msg']
                self.path_users = vars['path_users']
        except:
            print("ERROR: fail to load 'xpath.json'")
            exit()

        options = Options()
        if logging == False:
            options.add_experimental_option("excludeSwitches", ["enable-logging"])     
        self.browser = webdriver.Chrome(self.path_driver,chrome_options=options)
        

    def debug(self, msg):
        # print debug message
        # self.verbose must be True for debut to print message
        if self.verbose:
            print("WA2:", msg)

    def is_ready(self, xpath):
        # check if xpath is ready
        try:
            self.browser.find_element_by_xpath(xpath)    
            return True
        except:
            return False

    def open(self, number=""):
        # open WA
        # jika number diisi maka akan langsung buka nomor bersangkutan
        # jika number tidak diisi, maka cuma akan buka WA (biasanya untuk keperluan link device)
        if number == "":
            self.browser.get("https://web.whatsapp.com")
        else:
            self.browser.get("https://web.whatsapp.com/send?phone="+ number + "&app_absent=1")

        # tunggu sampai WA siap (dan proses link selesai)
        while not self.is_ready(self.path_search):
            time.sleep(3)
            self.debug("Waiting WA session")
    
    def new_tab(self):
        # open new tab
        #   currently unused
        self.browser.execute_script("window.open('')")

    def close(self):
        # close active tab
        self.browser.close()        

    def list_panel(self,a,b):
        n = a
        result = []
        while n<=b:
            try:
                obj = self.browser.find_element_by_xpath(self.path_users.replace("xx",n))
                result.push(obj.text)
            except:
                pass
            finally:
                n +=1
        return result
                

    def search_user(self, name, wait_time=3):
        # search user
        # the search is CASE SENSITIVE
        # if found, set open user chat
        # if not, return False
        self.debug(f"Search '{name}'")
        act = ActionChains(self.browser)
        # search
        sb = self.browser.find_element_by_xpath(self.path_search) # SearchBox
        act.click(sb)               # focus search box
        act.send_keys(Keys.ESCAPE)  # clear search box
        act.click(sb)               # bring back focus to search box
        act.send_keys(name)         # type name to search
        act.perform()

        time.sleep(wait_time) # waktu tunggu untuk pencarian
        
        try:
            # search <span> with title = [searched user name]
            obj = self.browser.find_element_by_css_selector("span[title='{}']".format(name))
            act = ActionChains(self.browser)
            act.click(obj).perform() # if found, click user  
            return True
        except:
            return False
        

    def type_msg(self, text):
        # menuliskan pesan ke box pesan
        self.debug( "Typing Message")
        act = ActionChains(self.browser)
        msg = self.browser.find_element_by_xpath(self.path_msg)
        act.click(msg)
        act.send_keys(text)        
        act.perform()

    def click_send(self):
        # klik tombol kirim pesan
        self.debug("Send")
        act = ActionChains(self.browser)
        btn = self.browser.find_element_by_xpath(self.path_send)
        act.click(btn)
        act.perform()

    def send_to_user(self,name,text, wait_time=3):
        # cari user dan kirim pesan
        #   pencarian nama user adalah CASE SENSITIVE
        if self.search_user(name, wait_time):
            self.type_msg(text)
            time.sleep(3)
            self.click_send()
            return True
        else:
            return False

    def send_message_to(self,number,text):
        # mengirimkan pesan berdasarkan nomor telepon        
        #   fungsi akan mengembalikan nilai True jika nomor valid, False jika nomor tidak valids
        self.debug(f"send_message_to {number} : {text}")
        try:            
            self.open(number)

            # jika ada pesan 'invalid path', maka nomor tidak valid
            if self.is_ready(self.path_invalid_msg):
                im = self.browser.find_element_by_xpath(self.path_invalid_msg)
                if im.text != '':
                    self.debug(f"{number} not valid")
                    return False
            
            # tunggu sampai kotak msg siap
            while not self.is_ready(self.path_msg):
                self.debug("waiting ...")
                time.sleep(2)
            self.type_msg(text)
            time.sleep(3)
            self.click_send()
            time.sleep(1)
            #self.browser.close()
            return True
        except:
            return False

