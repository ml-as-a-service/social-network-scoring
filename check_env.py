# remember to create a .env file with EMAIL and PASSWORD settings

from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

import os 

email = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')

print(email, password)