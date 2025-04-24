import os
from dotenv import load_dotenv, dotenv_values

load_dotenv() # looks for .env and loads it into the environment
my_secret_env_value = os.getenv('MY_SECRET')

env_values = dotenv_values(".env") # alternatively, get a dict from .env without modifying the environment
my_secret_dict_value = env_values["MY_SECRET"]

print(f"MY_SECRET from env:\t{my_secret_env_value}")
print(f"MY_SECRET from dict:\t{my_secret_dict_value}")

