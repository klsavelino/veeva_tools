from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
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

REPORTS_PAGE = "/lightning/o/Report/home?queryScope=everything"
LOGIN_PAGE = "https://login.salesforce.com/"
DEFAULT_DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", "TEMPDIR")
DEFAULT_TIMEOUT = 120

class Session:
    
    def __init__(self,
                 kr_usr: str, # Nome do username no Keyring
                 kr_addr: str = LOGIN_PAGE, # Nome das credenciais no Keyring
                 driver_path: str = None, # Caminho para o chromedriver.exe
                 download_path: str = DEFAULT_DOWNLOAD_PATH): # Caminho desejado para download do report
        
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
            print("""Suas credenciais não foram devidamente armazenadas no gerenciador de credenciais do Windows.""")
            raise

        # Muda diretório padrão de downloads para DOWNLOAD_PATH ou para diretório
        # especificado pelo usuário.
        
        opts = Options()
        
        opts.add_experimental_option("prefs", {"devtools.download.default_directory": self.download_path})

        if driver_path is None:
            driver_path = ChromeDriverManager().install()

        self.driver = Chrome(service=Service(executable_path=driver_path), options=opts)
        
        
        
        '''
        # Automação de login #
        Chama o chromedriver e loga no serviço com as credenciais resgatadas do keyring.
        '''
        
        
        # Acessa a página de log-in
        (self.driver.get(LOGIN_PAGE))
        
        # Localiza o input do e-mail e envia a credencial
        (self._element_wait()
         .until(EC.presence_of_element_located((By.ID, 'username')))
         .send_keys(kr_usr))
        
        # Localiza o input da senha e envia a credencial
        (self._element_wait()
         .until(EC.presence_of_element_located((By.ID, 'password')))
         .send_keys(pwd))

        # Clica no botão de logar
        (self._element_wait()
         .until(EC.presence_of_element_located((By.ID, 'Login')))
         .click())
        
        self._page_wait()
        
        print("Sessão iniciada.")
        
        return
    
    def get_report(self, report: str):
        
        '''
        # Método get_report(report) #
        
        Ferramenta que resgata report usando o nome do mesmo passado como parâmetro.
        
        Retorna PATH absoluto report baixado.
        
        '''        
        
        # Resgata o URL base
        url = self.driver.current_url
        url = url[:(url.find(".com")+4)]
        
        
        # Constrói o URL da página de reports
        BASE_URL = url + REPORTS_PAGE
        
        del url
        
        # De
        attempts = 0
        
        while attempts <= 3:
            
            # Navega até a página de reports
            self.driver.get(BASE_URL)
            
            self._page_wait()
            
            
            # ! TENTAR RETIRAR O SLEEP ! #
            time.sleep(5)
                        
            # Aguarda presença de input de texto onde irá ser inserido o report para a pesquisa
            (self._element_wait()
             .until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
             .send_keys(report))
            
            # ! TENTAR RETIRAR O SLEEP ! #
            time.sleep(5)
            
            
    
            self._page_wait()
            
            
            
            self._element_wait().until(lambda frame: self.driver.execute_script("return document.querySelector('.folderListView') !=  null"))
            
            
            try:
                
                source = self.driver.execute_script("return document.querySelector('.bodyContainer').innerHTML")
                assert(source is not None)
                
                
            except AssertionError:
                
                attempts += 1
                print(f"E001: Não foi possível acessar o innerHTML para a consulta na {attempts} tentativa.")
                
                if attempts >= 3:
                    sys.exit()
            
                continue
            
            try:
                regex = r'<a href="(?:[^\\"]|\\\\|\\")*" title=\"' + report
                result = re.search(regex, source, re.MULTILINE)
                assert(result is not None)
                
                break
            
            except AssertionError:
                
                attempts += 1
                print(f"E007: Não foi possível acessar referência do report via regex na {attempts} tentativa.")
                
                if attempts >= 3:
                    sys.exit()
                
                continue
                   
        
        result = result.group(0).split('"')[1] # Retorna apenas link
        
        self.driver.get(result)   
        self._page_wait()
        
        # Aguarda a renderização do iframe com o conteudo do report
        iframe = self._element_wait() \
            .until(EC.presence_of_element_located((By.CSS_SELECTOR,"iframe:first-of-type")))
        self.driver.switch_to.frame(iframe.get_attribute('name'))
        
        # Exibe as opções do dropdown
        (self._element_wait()
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".slds-dropdown-trigger_click")))
        .click())
        
        # Aguarda presença e clica na opção "Exportar" no dropdown
        (self._element_wait()
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".report-action-ReportExportAction")))).find_element(By.CSS_SELECTOR, "*").click()
                
        # Retorna ao contexto original
        self.driver.switch_to.default_content()
        
        # Configura Diretorio de download
        download_behavior={"behavior":"allow", "downloadPath":self.download_path}
        self.driver.execute_cdp_cmd("Page.setDownloadBehavior", download_behavior)
        
        # Aguarda presença da opção de exportação de dados
        (self._element_wait()
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='data-export']")))
         .click())
            
        # Aguarda a presença da opção do formato dos dados a serem exportados
        (self._element_wait()
         .until(EC.presence_of_element_located((By.CLASS_NAME, "slds-form-element"))))
                
        # Seleciona o formato .csv
        (self._element_wait()
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".slds-select"))))
        Select(self.driver.find_element(By.CSS_SELECTOR, ".slds-select")).select_by_value("localecsv")       
        input()
        exit()
        # Baixa o report
        (self._element_wait()
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".uiButton--brand")))
         .click())
   
        # Monitorando o Download
        self.driver.get("chrome://downloads/")    
        self._page_wait()
        self._element_wait().until(lambda download: self.driver.execute_script("return document.getElementsByTagName('downloads-manager')[0].shadowRoot.querySelector('downloads-item') != null")) == True
                
        download_start = time.time()
        download_progress = 0        
        while (download_progress<100) and ((time.time() - download_start) < DEFAULT_TIMEOUT):
            download_progress = (self.driver.execute_script('''
                var main_shadow_root = document.getElementsByTagName("downloads-manager")[0].shadowRoot;
                var progress_shadow_root = main_shadow_root.querySelector("downloads-item").shadowRoot;
                return progress_shadow_root.querySelector("#progress").value;
            '''))
            time.sleep(1)    

        # Obtendo nome do arquivo baixado
        filename=self.driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#name").innerHTML')
        report_path = os.path.join(self.download_path,filename)
        print(report_path)
        
        return report_path
    
    def _element_wait(self, timeout = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout)
    
    def _page_wait(self, timeout = DEFAULT_TIMEOUT):
        return self._element_wait(timeout).until(lambda driver: self.driver.execute_script("return document.readyState")=='complete')
    
    def __del__(self):
        self.driver.close()
        self.driver.quit()
        print("Sessão encerrada.")
        
    def end(self):
        self.__del__()

if __name__ == "__main__":
    Session("jose.maselo@servier.latam").get_report("CLM_Slides")
        