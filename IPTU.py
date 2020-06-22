from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time, os, random
from datetime import date

class iptuClass:
    #parâmetros para inicialização
    def __init__(self, driver):
        self.driver = driver
        self.url = 'http://iptuonline.siatu.pbh.gov.br/IptuOnline/index.xhtml'
        self.search_bar = 'inputIndice'  # name
        self.btn_search = 'pesquisar'  # id

    #Abrir pagina requisitada
    def navigate(self):
        self.driver.get(self.url)

    @staticmethod
    def type_like_a_person(sentence, single_input_field):
        """ Este código irá basicamente permitir que você simule a digitação como uma pessoa """
        for letter in sentence:
            single_input_field.send_keys(letter)
            time.sleep(random.randint(1, 5) / 20)

    #Faz a pesquisa
    def search(self, ID='None'):
        comment_input_box = self.driver.find_element_by_name(self.search_bar)
        time.sleep(random.randint(2, 5))
        self.type_like_a_person(
            ID, comment_input_box)
        time.sleep(random.randint(1, 3))
        #self.driver.find_element_by_name(self.search_bar).send_keys(ID)
        self.driver.find_element_by_id(self.btn_search).click()
        #element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "form:retornarIndex")))

    def clearSearchBar(self):
        self.driver.find_element_by_id(self.search_bar).clear()

    #Abre e salva o arquivo
    def getHTML(self, path, ID):
        Month = {1: 'Jan',
                2: 'Fev',
                3: 'Mar',
                4: 'Abr',
                5: 'Mai',
                6: 'Jun',
                7: 'Jul',
                8: 'Ago',
                9: 'Set',
                10: 'Out',
                11: 'Nov',
                12: 'Dez'
        }
        self.driver.find_element_by_xpath("//*[contains(@onclick, 'blank')]").click()
        time.sleep(random.randint(2, 5))
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
        try:
            self.driver.find_element_by_id(self.search_bar).clear()
        except:
            data_atual = date.today()
            currentMonth = data_atual.month
            currentMonth = Month[currentMonth]
            htmlname = os.path.join(path,  str(ID) + '-' + currentMonth + '.html')
            outputpdf = os.path.join(path, str(ID) + '.png')
            with open(htmlname, 'w') as f:
                f.write(self.driver.page_source)
            time.sleep(random.randint(1, 2))
            #total_width = 500
            #total_height = 3000
            #self.driver.set_window_size(total_width, total_height)
            #self.driver.execute_script("document.body.style.zoom = '60%';")
            #self.driver.find_element_by_tag_name('body').screenshot(r'C:\Users\arthu\Desktop\Destino\shavlau.png')
            #self.driver.save_screenshot(outputpdf)

            self.driver.close() #Fecha aba atual

            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
            self.driver.find_element_by_xpath("//*[contains(@onclick, 'retornarIndex')]").click()
            IDextraido.append(ID)
                #pass

    def returnHome(self, ID):
        try:
            self.driver.find_element_by_id(self.search_bar).clear()
        except:
            #time.sleep(5)
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
            self.driver.find_element_by_xpath("//*[contains(@onclick, 'retornarIndex')]").click()

#if __name__ == "__main__":S

def execute(data):
    path_driver = r"C:\IPTU_crawler\driver\chromedriver.exe" #Define o caminho do arquivo ninário
    #Faz a extração em segundo plano
    download_dir = r"C:IPTU_crawler"
    chrome_options = Options()
    chrome_options.headless = False  #True a extração em segundo plano
    #Ativa os drivers necessarios para execução
    driver = webdriver.Chrome(options = chrome_options, executable_path = path_driver)
    IPTUvar = iptuClass(driver)
    IPTUvar.navigate()
    #Loop para executar o crawler em cada linha do arquivo csv
    IDextraido = []
    print(len(data['Indice Cadastral']))
    for rows in range(len(data['Indice Cadastral'])):
        iptuID = data['Indice Cadastral'][rows]
        path_file = data['Pasta'][rows]
        htmlx = os.path.join(path_file,  str(iptuID) + '.html')
        if os.path.exists(htmlx) == False:
            try:
                IPTUvar.search(str(iptuID))
                time.sleep(random.randint(3, 6)) #Espera ate que a pesquisa seja concluida
                IPTUvar.getHTML(path_file, iptuID)
            except:
                IDextraido.append(iptuID)
                #time.sleep(1)
        else:
            IDextraido.append(iptuID)
    #with open(r"C:\IPTU_crawler\Extraidos.txt", 'w') as f:
    #    f.write(IDextraido)
    print(IDextraido)
    driver.quit() #Fim
