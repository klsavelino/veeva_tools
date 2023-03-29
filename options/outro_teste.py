from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import sys
import re

import os
import time



DEFAULT_PATH = os.getcwd()
TIMEOUT = 18



class Session:
    def __init__(self,
                 usr: str,
                 pwd: str,
                 path: str = DEFAULT_PATH):
        
        self.usr = usr
        self.pwd = pwd
    
    
        driver = Chrome(service=Service(executable_path=path))
        self.driver = driver
        
        LOGIN_PAGE = "https://login.salesforce.com/"
        
        (driver.get(LOGIN_PAGE))
        
        # Localiza o input do e-mail
        (WebDriverWait(driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.ID, 'username')))
         .send_keys(usr))

        
        # Localiza o input da senha
        (WebDriverWait(driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.ID, 'password')))
         .send_keys(pwd))

        
        # Clica no botão de logar
        (WebDriverWait(driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.ID, 'Login')))
         .click())
        
        
        print("Sessão iniciada")
        #/lightning/page/home
        #/lightning/o/Report/home?queryScope=everything
        return
    
    def get_report(self, report):
        
        
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.url_contains("/lightning/page/home")))
        
        REPORTS_PAGE = "/lightning/o/Report/home?queryScope=everything"
        
        
        url = self.driver.current_url
        url = url[:(url.find(".com")+4)]
        
        BASE_URL = url + REPORTS_PAGE
        
        del url
    
        self.driver.get(BASE_URL)
        
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
         .send_keys(report))
        
        time.sleep(2)
        
        
        try:
            #source = self.driver.page_source()
            source = self.driver.execute_script("return document.querySelector('.bodyContainer').innerHTML")
            assert(source is not None)
            regex = r'<a href="(?:[^\\"]|\\\\|\\")*" title=\"' + report
            result = re.search(regex, source, re.MULTILINE)
            
            assert(result is not None)
            
            
            result = result.group(0).split('"')[1] # Retorna apenas link
            
            print(result)
            
        except:
            self.close_all()
        
        self.driver.get(result)
        
        input("Continuar?: ")
        
        
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, ".isView"))))
        
        print("Switch complete")
        
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".slds-dropdown-trigger_click")))
         .click())
        
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[title='Exportar']")))
         .click())
        
        
        self.driver.switch_to.default_content()
        
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='data-export']")))
         .click())
        
        
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CLASS_NAME, "slds-form-element"))))
        
        self.driver.execute_script("document.querySelector('.slds-select').value='localecsv';")
        
        self.close_all()
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[title='Exportar']")))
         .click())
        
    
        self.close_all()
        
    def close_all(self):

        print("Closing")

        self.driver.close()
        self.driver.quit()
        sys.exit()
        
    def info(self):
        print(f"USER: {self.usr}\nSENHA: {self.pwd}")
        return