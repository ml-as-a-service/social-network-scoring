import os
import random 
import time

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from dotenv import load_dotenv, find_dotenv
 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options

from cachetools import cached #, LRUCache, TTLCache   
from cachetools_ext.fs import FSLRUCache    
from cachetools.keys import hashkey
from functools import partial

import hashlib

from monkeylearn import MonkeyLearn

load_dotenv(find_dotenv())

# User credentials
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
MONKEYLEARN_TOKEN = os.environ.get('MONKEYLEARN_TOKEN')


# Required binaries
BROWSER_EXE = '/usr/bin/firefox'
GECKODRIVER = '/usr/bin/geckodriver'
FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)

#  Code to disable notifications pop up of Chrome Browser
PROFILE = webdriver.FirefoxProfile()
# PROFILE.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
PROFILE.set_preference("dom.webnotifications.enabled", False)
PROFILE.set_preference("app.update.enabled", False)
PROFILE.update_preferences()

# Get Post --------------------------------------------------------------------
browser = webdriver.Firefox(executable_path=GECKODRIVER,
                            firefox_binary=FIREFOX_BINARY,
                            firefox_profile=PROFILE,)

def safe_find_element_by_id(elements_id):
    for elem_id in elements_id:
        print("elem_id", elem_id)
        try:
            return browser.find_element_by_id(elem_id)
        except NoSuchElementException:
            print("Not Found %s " % (elem_id))
    return None

# login
def login(email, password):
    global browser 
    browser.get("https://www.facebook.com")
    browser.maximize_window()

    # filling the form
    browser.find_element_by_name('email').send_keys(email)
    browser.find_element_by_name('pass').send_keys(password)

    # clicking on login button
    safe_find_element_by_id(['u_0_b','u_0_d']).click() 
    

def get_post_key(*args,   **kwargs):
    hashed_args = ['%s' % (arg) for arg in args]
    hashed_kwargs = ['%s ' % ( key + value ) for (key, value) in kwargs.items()]
    key = hashlib.md5(':'.join(hashed_args + hashed_kwargs).encode('utf-8')).hexdigest()
    key = hashkey('get_post_key', key)
    return key

@cached(cache=FSLRUCache(maxsize=300, ttl=24*60*60), key=get_post_key)    
def get_post(profile, count=5):
    global browser 
    browser.get(profile)

    for i in range(count):
        print("Loading %d" % (i))
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(5,10))
        elements = browser.find_elements_by_xpath("//div[contains(text(), 'See original')]")
        for count, ele in enumerate(elements):
            # print("ele ", count)
            try:
                ele.click()
            except Exception: 
                pass
    elements = browser.find_elements_by_xpath('//div[@role="article"]')

    posts = []
    for count, post in enumerate(elements):
        posts.append(post.text)

    return posts

def api_call_key(*args,   **kwargs):
    hashed_args = ['%s' % (arg) for arg in args]
    hashed_kwargs = ['%s ' % ( key + value ) for (key, value) in kwargs.items()]
    key = hashlib.md5(':'.join(hashed_args + hashed_kwargs).encode('utf-8')).hexdigest()
    key = hashkey('api_call', key)
    return key

@cached(cache=FSLRUCache(maxsize=300, ttl=24*60*60), key=api_call_key)
def api_call(val):
    global MONKEYLEARN_TOKEN
    data = [val]
    # print("--------->api_call", data)
    ml = MonkeyLearn(MONKEYLEARN_TOKEN)
    # model_id = 'cl_pi3C7JiL' # en
    model_id = 'cl_u9PRHNzf'   # es
    result = ml.classifiers.classify(model_id, data)
    return result


# login(EMAIL, PASSWORD)
profile = 'https://www.facebook.com/diurno.delsur'
posts = get_post(profile,10)
# browser.close()


report = {
    'Positive': {'count':0, 'total':0},
    'Neutral' : {'count':0, 'total':0},
    'Negative' : {'count':0, 'total':0},
}

for count, post in enumerate(posts):
    print("\n\n-------------------------------------------------")
    print("post ", post)

    print("\n->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    if len(post) > 0:
        result = api_call(post)
        print(result.body)
        for r in result.body:
            for c in r['classifications']:
                tag_name = c['tag_name']
                confidence = c['confidence']
                
                report[tag_name]['count'] += 1
                report[tag_name]['total'] += confidence

                
print(report)



