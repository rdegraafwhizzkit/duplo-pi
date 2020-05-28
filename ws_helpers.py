import random
import string
import glob
import json


def random_string(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choices(letters, k=length))


def load():
    ret = []
    for pattern in glob.glob("patterns/*.json"):
        with open(pattern, 'r') as j:
            ret.append(json.load(j))
    return sorted(ret, key=lambda i: i['name'])
