# pip3 install monkeylearn

from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

import os 
 
api_token = os.environ.get('MONKEYLEARN_TOKEN')

from monkeylearn import MonkeyLearn

ml = MonkeyLearn(api_token)
data = ["This is a great tool!"]
model_id = 'cl_pi3C7JiL'
result = ml.classifiers.classify(model_id, data)
print(result.body)

 