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

DOWNLOAD_PATH = 'C:\\Users\\Notebook\\Dropbox\\Trabajo\\FreeLancer\\Scrapy.Linkedin\\downloads'
   
#############################################################################################################
#   DRIVER SETTINGS
#############################################################################################################
def set_driver():
    # ChromeDriver Settings (12.2020)
    chrome_options = webdriver.ChromeOptions()
    # Windows Driver Path (12.2020)
    driver = webdriver.Chrome(options=chrome_options, executable_path="driver\Windows\chromedriver.exe")

    # Driver Settings
    driver.set_page_load_timeout(10)
    return driver

#############################################################################################################
#   USER INPUT
#############################################################################################################
def user_input():
    user = input("Ingrese correo:")
    print('Su correo es %s' %user)
    
    password = input("Ingrese password:")
    print('Su password es %s' %password)

    target = input("Ingrese perfil:")
    print('Su password es %s' %target)

    return (user, password, target)

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
    driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
    time.sleep(2)

    try:
        ul = driver.find_element_by_xpath("//*[@id='experience-section']/ul")
        li = ul.find_elements_by_tag_name("li")
        counter = 0
        for item in li:
            try: 
                counter +=1
                position = item.find_elements_by_tag_name ("h3")
            
                if len(position)>1:
                    # Multiple cargos dentro de la empresa
                    newli = item.find_elements_by_tag_name("li")
                    buisness = item.find_elements_by_tag_name ("h3")[0].find_elements_by_tag_name("span")[1]
                    total_period = item.find_elements_by_tag_name ("h4")[0].find_elements_by_tag_name("span")[1]    
                    print ("Experiencia: %s (multiples cargos)" %counter)
                    print ("Empresa: %s" %buisness.text)
                    print ("Período Total: %s" %total_period.text)
                    print ('\n')

                    for subitem in newli:
                        position = subitem.find_elements_by_tag_name ("h3")[0].find_elements_by_tag_name("span")[1]
                        position_dates = subitem.find_elements_by_tag_name ("h4")[0].find_elements_by_tag_name("span")[1]
                        position_duration = subitem.find_elements_by_tag_name ("h4")[1].find_elements_by_tag_name("span")[1]
                        print ("Cargo: %s" %position.text)
                        print ("Período: %s" %position_dates.text)
                        print ("Duración: %s" %position_duration.text)
    
                else:
                    # Unico cargos dentro de la empresa
                    buisness = item.find_elements_by_tag_name ("p")[1]
                    period = item.find_elements_by_tag_name ("h4")[0].find_elements_by_tag_name("span")[1]
                    duration = item.find_elements_by_tag_name ("h4")[1].find_elements_by_tag_name("span")[1]
                    try:
                        location = item.find_elements_by_tag_name ("h4")[2].find_elements_by_tag_name("span")[1]
                    except:
                        location = 'Nan'

                    print ("----------------------------------------")     
                    print ("Experiencia: %s" %counter)
                    print ("Cargo: %s" %position[0].text)
                    print ("Empresa: %s" %buisness.text)
                    print ("Período: %s" %period.text)
                    print ("Duración: %s" %duration.text)
                    print ("Lugar: %s" %location.text)
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
    # Fist scroll to Experience (if not, ul and li are not discovered)
    # Hardcoded solution for linledin
    driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
    time.sleep(2)
    print (">>>>>")
    try:
        ul = driver.find_element_by_xpath("//*[@id='education-section']/ul")
        li = ul.find_elements_by_tag_name("li")
        counter = 0
        for item in li:
            counter +=1
            academy = item.find_elements_by_tag_name ("h3")[0]
            degree_title = item.find_elements_by_tag_name ("p")[0].find_elements_by_tag_name("span")[1]
            degree_field = item.find_elements_by_tag_name ("p")[1].find_elements_by_tag_name("span")[1]
            period = item.find_elements_by_tag_name ("h4")[0].find_elements_by_tag_name("span")[1]
            print ("----------------------------------------")     
            print ("Educación: %s" %counter)
            print ("academy: %s" %academy.text)
            print ("title: %s" %degree_title.text)
            print ("area: %s" %degree_field.text)
            print ("Período: %s" %period.text)
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

# PERFORMANCE
import time
start = time.time()

#user, password, target = user_input()
#scrape_linkedin (user, password, target)
#scrape_linkedin ('pez.payaso@hotmail.com', '$$test$$', 'mariogarciaar')
scrape_linkedin ('kenji.nakasone@outlook.com', '$$control$$', 'mariogarciaar')
print('It took', time.time()-start, 'seconds.')
print ('------------------------------------------------')