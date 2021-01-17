# pip3 install monkeylearn
# pip3 install cachetools_ext

from cachetools import cached #, LRUCache, TTLCache   
from cachetools_ext.fs import FSLRUCache    
from cachetools.keys import hashkey
from functools import partial

import hashlib

from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

import os 
 
api_token = os.environ.get('MONKEYLEARN_TOKEN')

from monkeylearn import MonkeyLearn

def api_call_key(*args,   **kwargs):
    hashed_args = ['%s' % (arg) for arg in args]
    hashed_kwargs = ['%s ' % ( key + value ) for (key, value) in kwargs.items()]
    key = hashlib.md5(':'.join(hashed_args + hashed_kwargs).encode('utf-8')).hexdigest()
    # print('envkey',key, args,kwargs)
    key = hashkey('api_call', key)
    return key

@cached(cache=FSLRUCache(maxsize=300, ttl=24*60*60), key=api_call_key)
def api_call(val):
    global api_token
    data = [val]
    # print("--------->api_call", data)
    ml = MonkeyLearn(api_token)
    # model_id = 'cl_pi3C7JiL' # en
    model_id = 'cl_u9PRHNzf'   # es
    result = ml.classifiers.classify(model_id, data)
    return result


# Primer llamado
val = "This is a bad tool!" 
result = api_call(val)
print(result.body)


# Primer llamado
val = "This is a great tool!" 
result = api_call(val)
print(result.body)


# Primer llamado
val = "Es una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramientaEs una gran herramienta"
result = api_call(val)
print(result.body)




# Primer llamado
val = "This is a bad tool!" 
result = api_call(val)
print(result.body)


# Primer llamado
val = "This is a great tool!" 
result = api_call(val)
print(result.body)


# Primer llamado
val = "This is a bad tool!" 
result = api_call(val)
print(result.body)


# Primer llamado
val = "This is a great tool!" 
result = api_call(val)
print(result.body)

