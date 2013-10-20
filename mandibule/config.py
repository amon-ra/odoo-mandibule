from mandibule import env
import os.path
import json


CONFIG_PATH = env.save_user_config_path('mandibule')

def get_config():
    try:
        with open(os.path.join(CONFIG_PATH, 'config'), 'r') as fp:
            return json.load(fp)
    except IOError:
        return []


def save_config(data):
    try:
        with open(os.path.join(CONFIG_PATH, 'config'), 'w') as fp:
            json.dump(fp, data)
            return True
    except IOError:
        return False
