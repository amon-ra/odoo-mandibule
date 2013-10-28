from mandibule.utils import env
import os.path
import json


CONFIG_PATH = env.save_user_config_path('mandibule')

try:
    with open(os.path.join(CONFIG_PATH, 'config'), 'r') as fp:
        CONFIG = json.load(fp)
except IOError:
    CONFIG = []


def add_group(group):
    CONFIG.append(group.serialize())


def save(data):
    try:
        with open(os.path.join(CONFIG_PATH, 'config'), 'w') as fp:
            json.dump(data, fp, indent=4)
            CONFIG = data
            return True
    except IOError:
        return False
