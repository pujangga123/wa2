from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

"""
REFERENSI
https://www.geeksforgeeks.org/action-chains-in-selenium-python/
"""

class Wa:
    path_send = '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[2]/button'
    path_search = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    path_msg = '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]'
    path_driver = "drivers\\chromedriver.exe"
    delay_wa_load = 20
    browser = None
    
    def __init__(self):
        print("Construct")
        self.browser = webdriver.Chrome(self.path_driver)

    def is_ready(self, xpath):
        try:
            self.browser.find_element_by_xpath(xpath)    
            return True
        except:
            return False

    def search(self,text):
        act = ActionChains(self.browser)
        search = self.browser.find_element_by_xpath(self.path_search)
        act.click(search)
        act.send_keys(text)        
        act.perform()        

    def open(self, number=""):
        # open WA
        # jika number diisi maka akan langsung buka nomor bersangkutan
        # jika number tidak diisi, maka cuma akan buka WA (biasanya untuk keperluan link device)
        if number == "":
            self.browser.get("https://web.whatsapp.com")
        else:
            self.browser.get("https://web.whatsapp.com/send?phone="+ number + "&app_absent=1")
    
    def new_tab(self):
        self.browser.execute_script("window.open('')")

    def close(self):
        # close active tab
        self.browser.close()    

    def registered(self):
        pass

    def search_found(self):
        pass

    def type_msg(self, text):
        # menuliskan pesan ke box pesan
        act = ActionChains(self.browser)
        msg = self.browser.find_element_by_xpath(self.path_msg)
        act.click(msg)
        act.send_keys(text)        
        act.perform()

    def click_send(self):
        # klik tombol kirim pesan
        act = ActionChains(self.browser)
        btn = self.browser.find_element_by_xpath(self.path_send)
        act.click(btn)
        act.perform()

    def send_message_to(self,number,text):
        try:            
            self.open(number)
            time.sleep(20)
            self.type_msg(text)
            time.sleep(3)
            self.click_send()
            time.sleep(1)
            #self.browser.close()
            return True
        except:
            return False

