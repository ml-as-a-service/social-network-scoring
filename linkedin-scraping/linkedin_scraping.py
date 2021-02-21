# -*- coding: UTF-8 -*
from socket import IP_OPTIONS
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import random  
DOWNLOAD_PATH = 'C:\\Users\\Notebook\\Dropbox\\Trabajo\\FreeLancer\\Scrapy.Linkedin\\downloads'
   
#############################################################################################################
#   DRIVER SETTINGS
#############################################################################################################
def set_driver():
    # ChromeDriver Settings (12.2020)
    # ChromeDriver Settings (12.2020)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Windows Driver Path (12.2020)
    driver = webdriver.Chrome(options=chrome_options, executable_path="driver\Windows\chromedriver.exe")

    # Driver Settings
    driver.set_page_load_timeout(10)
    return driver

#############################################################################################################
#   USER INPUT
#############################################################################################################
def user_input():
    user = input("Ingrese correo: ")
    print('Su correo es >> %s' %user)
    
    password = input("Ingrese password: ")
    print('Su password es >> %s' %password)

    return (user, password)

#############################################################################################################
#   LOGIN
#############################################################################################################
def linkedin_login(driver, user, password):
    login_page = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
    driver.get(login_page)
    time.sleep(5)
    driver.find_element_by_id("username").send_keys(user)
    time.sleep(0.81)
    driver.find_element_by_id("password").send_keys(password)
    time.sleep(1.06)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    return driver

#############################################################################################################
#   GO TO TARGET PAGE
#############################################################################################################
def load_target_page (driver, target):
    try:
        print("Loard target page")
        target_page = "https://www.linkedin.com/in/" + target
        driver.get(target_page)
        print ('target_page:: Página cargada correctamente')
        return driver
    except Exception as e:
        print("target_page:: Error al cargar la pagina del target.")
        return driver

#############################################################################################################
#   SCRAPE EXPERIENCIA
#############################################################################################################
def get_experience (driver):
    # Fist scroll to Experience (if not, ul and li are not discovered)
    # Hardcoded solution for linledin
    time.sleep(4)
    window_height = driver.execute_script("return window.innerHeight")
    steps = 0
    while steps * window_height < driver.execute_script("return document.body.offsetHeight"):
        driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
        time.sleep(round(random.gauss(1, 0.3),2))
        steps += 1

    try:
        try:
            # Buscar si hay seccion de mas experiencia
            # Si hay desplegarla haciendo click en el boton
            es = driver.find_element_by_xpath("//*[@id='experience-section']")
            buttons = es.find_elements_by_tag_name("button")
            for button in buttons:
                if "experiencia" in button.text :
                    offset = -20
                    location_y = button.location.get('y') + offset
                    driver.execute_script(
                        "var location_y = arguments[0];\
                        window.scrollTo(0, window.scrollY - location_y)",\
                        location_y
                    )
                    time.sleep(round(random.gauss(1, 0.3),2))
                    button.click()
                    time.sleep(round(random.gauss(1, 0.3),2))
        except Exception as e:
            print(e)

        # Con todas las experiencias de desplegadas realizo el scraping
        ul = driver.find_element_by_xpath("//*[@id='experience-section']/ul")
        li = ul.find_elements_by_tag_name("li")
        print ("----------------------------------------")          
        for item in li:
            try: 
                cargos = item.find_elements_by_tag_name ("h3")

                if len(cargos)>=2:
                    # Multiple cargos dentro de la empresa
                    # Me importa la empresa y el periodo total
                    # No se scrapean cargos internos
                    buisness = item.find_elements_by_tag_name ("h3")[0].find_elements_by_tag_name("span")[1]
                    total_period = item.find_elements_by_tag_name ("h4")[0].find_elements_by_tag_name("span")[1]   
                    print ("Empresa: %s" %buisness.text)
                    print ("Período Total: %s" %total_period.text)

                if len(cargos)==1:
                    # Unico cargos dentro de la empresa
                    buisness = item.find_elements_by_tag_name ("p")[1]
                    period = item.find_elements_by_tag_name ("h4")[0].find_elements_by_tag_name("span")[1]
                    duration = item.find_elements_by_tag_name ("h4")[1].find_elements_by_tag_name("span")[1]
                    print ("Cargo: %s" %cargos[0].text)
                    print ("Empresa: %s" %buisness.text)
                    print ("Período: %s" %period.text)
                    print ("Duración: %s" %duration.text)
                print ("----------------------------------------")
            except:
                continue

    except Exception as e:
        print(e)
        return driver
#############################################################################################################
#   SCRAPE EXPERIENCIA
#############################################################################################################
def get_education(driver):
    try:
        try:
            # Buscar si hay seccion de mas experiencia
            # Si hay desplegarla haciendo click en el boton
            es = driver.find_element_by_xpath("//*[@id='education-section']")
            buttons = es.find_elements_by_tag_name("button")
            for button in buttons:
                if "titulación " or "titulaciones" in button.text :
                    offset = -20
                    location_y = button.location.get('y') + offset
                    driver.execute_script(
                        "var location_y = arguments[0];\
                        window.scrollTo(0, window.scrollY - location_y)",\
                        location_y
                    )
                    time.sleep(round(random.gauss(1, 0.3),2))
                    button.click()
                    time.sleep(round(random.gauss(1, 0.3),2))
        except Exception as e:
            print(e)

        ul = driver.find_element_by_xpath("//*[@id='education-section']/ul")
        li = ul.find_elements_by_tag_name("li")
        print ("----------------------------------------")  
        for item in li:
            academy = item.find_elements_by_tag_name ("h3")[0]
            degree_title = item.find_elements_by_tag_name ("p")[0].find_elements_by_tag_name("span")[1]
            print ("----------------------------------------")     
            print ("Universidad: %s" %academy.text)
            print ("Título: %s" %degree_title.text)
        print ("----------------------------------------")

    except Exception as e:
        print(e)
        return driver
#############################################################################################################
#   MAIN
#############################################################################################################
def scrape_linkedin (user, password, target):
    # Set driver parameters
    driver = set_driver()

    try:
        # Linkedin: login
        linkedin_login(driver, user, password)
        time.sleep(2)
    except:
        print ('ERROR:: logeo pagina principal')
        
    try:
        # Linkedin: go to profile page
        load_target_page(driver, target)
        time.sleep(2)
    except:
        print ('ERROR:: carga de pagina del target')

    try:   
        # Linkedin: Extract Experience data 
        get_experience(driver)
        time.sleep(2)
    except:
        print ('ERROR:: scrapeando experiencia')

    try:   
        # Linkedin: Extract Experience data      
        get_education(driver)
        time.sleep(2)
    except:
        print ('ERROR:: scrapeando educacion')

    try:
        driver.quit()
        print ('MAIN:: cerrando driver')

    except WebDriverException:
        print ('MAIN:: driver no encontrado')

#----------------------------------------------------------
#                           MAIN
#----------------------------------------------------------
import time
start = time.time()

email, password = user_input()
#profile_name = 'mariogarciaar'
profile_name = 'natalia-prevettoni-8779561b'
scrape_linkedin (email, password, profile_name)

print('It took', time.time()-start, 'seconds.')
print ('------------------------------------------------')