from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import keyring as kr
import time
import sys
import re
import os



LOGIN_PAGE = "https://login.salesforce.com/"
DEFAULT_DRIVER_PATH = os.getcwd()
DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", "TEMPDIR")
TIMEOUT = 20


class Session:
    def __init__(self, kr_usr: str, kr_addr: str = LOGIN_PAGE,  driver_path: str = DEFAULT_DRIVER_PATH, download_path: str = DOWNLOAD_PATH):
        
        '''
        # Classe "Session" #
        Fornece base para quaisquer outros métodos que requeiram autenticação na plataforma.
        
        Armazena as variáveis:
        driver: Instância chromedriver devidamente configurada para uso
        download_path: Caminho para download de arquivos na sessão
        '''
        
        self.download_path = download_path
        
        # Caso o dir não exista, ele será criado
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        
        try:
            pwd = kr.get_password(kr_addr, kr_usr) # Resgata as credenciais
        except:
            raise Exception("""Suas credenciais não foram devidamente armazenadas no gerenciador de credenciais do Windows.""")
            exit()

        # Muda diretório padrão de downloads para DOWNLOAD_PATH ou para diretório
        # especificado pelo usuário.
        
        '''
        preferences = {"download.default_directory" : download_path,
                       "download.prompt_for_download": False,
                       "intl.accept_languages":
                 }'''
        
        opts = Options()
        opts.add_experimental_option("prefs", {"devtools.download.default_directory": self.download_path})

        self.driver = Chrome(service=Service(executable_path=driver_path),chrome_options=opts)
        
        '''
        # Automação de login #
        Chama o chromedriver e loga no serviço com as credenciais resgatadas do keyring.
        '''
        
        
        # Acessa a página de log-in
        (self.driver.get(LOGIN_PAGE))
        
        # Localiza o input do e-mail e envia a chave
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.ID, 'username')))
         .send_keys(kr_usr))
        
        # Localiza o input da senha e envia a chave
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.ID, 'password')))
         .send_keys(pwd))

        # Clica no botão de logar
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.ID, 'Login')))
         .click())
        
        print("Sessão iniciada")
        
        return
    
    def get_report(self, report: str):
        '''
        # Método get_report(report) #
        
        Ferramenta que resgata report usando o nome do mesmo passado como parâmetro.
        
        Retorna PATH absoluto report baixado.
        '''

        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.url_contains("/lightning/page/home")))
        
        REPORTS_PAGE = "/lightning/o/Report/home?queryScope=everything"
        
        
        url = self.driver.current_url
        url = url[:(url.find(".com")+4)]
        
        BASE_URL = url + REPORTS_PAGE
        
        del url
    
        self.driver.get(BASE_URL)
        
        time.sleep(12)
        
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
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".report-action-ReportExportAction")))).find_element(By.CSS_SELECTOR, "*").click()
        
        
        # Retorna ao contexto original
        self.driver.switch_to.default_content()
        
        download_behavior = {
            "behavior": "allow",
            "downloadPath": self.download_path
            }
        
        self.driver.execute_cdp_cmd("Page.setDownloadBehavior", download_behavior)
        
        # Aguarda presença da opção de exportação de dados
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='data-export']")))
         .click())
    
        
        # Aguarda a presença da opção do formato dos dados a serem exportados
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CLASS_NAME, "slds-form-element"))))
        
        time.sleep(2)
        
        
        # Seleciona o formato .csv

        Select(self.driver.find_element(By.CSS_SELECTOR, ".slds-select")).select_by_value("localecsv")
        
        
        
        input()
        self.close_all()
        exit()
        
        
        # Lista todos os itens no diretório de download
        before = os.listdir(self.download_path)
        
        # Baixa o report
        (WebDriverWait(self.driver, TIMEOUT)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[title='Export']")))
         .click())
              
        
        # Tempo de espera
        time.sleep(TIMEOUT)
        
        # Lista todos os itens no diretório de download
        after = os.listdir(self.download_path)
        
        # Diferença entre os snapshots
        dir_list = list(set(after) - set(before))
        
        try:
            for file in dir_list:
                if file.endswith(".csv"):
                    report_path = file
        except:
            raise Exception("Não foi possível encontrar o arquivo criado.")
        
        # PATH do report
        report_path = os.path.join(self.download_path, report_path)
        
        print(report_path)
        
        return report_path
        
    def close_all(self):
        self.driver.close()
        self.driver.quit()

                      

