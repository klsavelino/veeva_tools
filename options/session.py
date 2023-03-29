from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import keyring as kr
import time
import sys
import re
import os



LOGIN_PAGE = "https://login.salesforce.com/"
DEFAULT_DRIVER_PATH = os.getcwd()
DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp")
TIMEOUT = 20


class Session:
    def __init__(self, driver_path: str = DEFAULT_DRIVER_PATH, download_path: str = DOWNLOAD_PATH):
        # Classe Session
        # Armazena as variáveis download_path, usr, pwd e driver
        
        try:
            CREDENTIALS = kr.get_credential(LOGIN_PAGE, None)
        except:
            raise Exception("Suas credenciais não foram devidamente armazenadas no gerenciador de credenciais do Windows.")

        self.download_path = download_path
        
        # Muda diretório padrão de downloads para DOWNLOAD_PATH ou para diretório
        # especificado pelo usuário.
        
        preferences = {'download.default_directory' : download_path,
                       'download.prompt_for_download': False
                 }
        
        opts = Options().add_experimental_option('prefs', preferences)
        

        self.usr = CREDENTIALS.username
        self.pwd = CREDENTIALS.password
        
        self.driver = Chrome(service=Service(executable_path=driver_path),chrome_options=opts)
        
        
        # Acessa a página de log-in
        (self.driver.get(LOGIN_PAGE))
        
        # Localiza o input do e-mail
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.ID, 'username')))
         .send_keys(self.usr))
        
        # Localiza o input da senha
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.ID, 'password')))
         .send_keys(self.pwd))

        # Clica no botão de logar
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.ID, 'Login')))
         .click())
        
        print("Sessão iniciada")
        return
    
    def get_report(self, report: str):
        
        
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.url_contains("/lightning/page/home")))
        
        REPORTS_PAGE = "/lightning/o/Report/home?queryScope=everything"
        
        
        url = self.driver.current_url
        url = url[:(url.find(".com")+4)]
        
        BASE_URL = url + REPORTS_PAGE
        
        del url
    
        self.driver.get(BASE_URL)
        
        time.sleep(3)
        
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
         .send_keys(report))
        
        time.sleep(5)
        
        try:
            #source = self.driver.page_source()
            source = self.driver.execute_script("return document.querySelector('.bodyContainer').innerHTML")
            assert(source is not None)
            regex = r'<a href="(?:[^\\"]|\\\\|\\")*" title=\"' + report
            result = re.search(regex, source, re.MULTILINE)
            assert(result is not None)

        except:
            raise Exception("Não foi possível acessar o report.")
        
        result = result.group(0).split('"')[1] # Retorna apenas link
        
        self.driver.get(result)
        
        time.sleep(5)
        
        try:
            iframe = (WebDriverWait(self.driver, TIMEOUT)
                      .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".isView"))))
            self.driver.switch_to.frame(iframe)
        except:
            raise Exception("Não foi possível encontrar o iFrame.")
        
        # Exibe as opções do dropdown
        (WebDriverWait(self.driver, TIMEOUT)
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".slds-dropdown-trigger_click")))
        .click())
        
        # Aguarda presença e clica na opção "Exportar" no dropdown
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[title='Export']")))
         .click())
        
        # Retorna ao contexto original
        self.driver.switch_to.default_content()
        
        # Aguarda presença da opção de exportação de dados
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='data-export']")))
         .click())
    
        
        # Aguarda a presença da opção do formato dos dados a serem exportados
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CLASS_NAME, "slds-form-element"))))
        
        
        # Seleciona o formato .csv
        self.driver.execute_script("document.querySelector('.slds-select').value='localecsv';")
        
        # Lista todos os itens no diretório de download
        before = os.listdir(self.download_path)
        
        # Baixa o report
        self.close_all()
        sys.exit()
        return
    
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[title='Export']")))
         .click())
              
        
        # Tempo de espera
        time.sleep(TIMEOUT)
        
        # Lista todos os itens no diretório de download
        after = os.listdir(self.download_path)
        
        # Diferença entre os snapshots
        dir_list = list(set(after) - set(before))
        
        for file in dir_list:
            if file.endswith(".csv"):
                report_path = file
        
        # PATH do report
        report_path = os.path.join(self.download_path)
        
        print(report_path)
        
        return report_path
        
    def close_all(self):
        self.driver.close()
        self.driver.quit()

                      

