import os
import time

import requests
from requests.exceptions import SSLError
from urllib3.exceptions import MaxRetryError

from config import PASSWORD, USERNAME, VERIFICATION_URL


TEST_URL = 'https://www.baidu.com/'
KEEP_ALIVE = False


def check_connection():
    try:
        requests.head(TEST_URL)
    except (MaxRetryError, SSLError):
        return False
    return True


def login(username, password):
    form_data = {
        'DDDDD': username,
        'upass': password,
        'R1': 0,
        'R2': '',
        'R6': 0,
        'para': 00,
        '0MKKey': 123456
    }
    res = requests.post(VERIFICATION_URL, form_data)

    return res.status_code == 200 and check_connection()


def logout():
    res = requests.get(os.path.join(VERIFICATION_URL, 'F.html'))

    return res.status_code == 200 and not check_connection()


def keep_alive():
    while True:
        if not check_connection():
            print('conection disconnect, retry login')
            if login(USERNAME, PASSWORD):
                print('successfully login as {}'.format(USERNAME))
            else:
                print('login fail, retry later')
        else:
            print('conection ok')
        time.sleep(60)

if __name__ == "__main__":
    keep_alive()
