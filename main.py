import logging
import os
import time

import requests

from config import PASSWORD, USERNAME, VERIFICATION_URL

TEST_URL = 'https://www.baidu.com/'
KEEP_ALIVE = False


def get_logger():
    logger = logging.getLogger('fuck_drcom')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s: %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = get_logger()


def check_connection():
    try:
        requests.head(TEST_URL)
    except requests.ConnectionError:
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

    try:
        res = requests.post(VERIFICATION_URL, form_data)
    except requests.ConnectionError:
        return False

    return res.status_code == 200 and check_connection()


def logout():
    res = requests.get(os.path.join(VERIFICATION_URL, 'F.html'))

    return res.status_code == 200 and not check_connection()


def keep_alive():
    while True:
        if not check_connection():
            logger.info('network disconnect, retry login')
            if login(USERNAME, PASSWORD):
                logger.info('successfully login as {}'.format(USERNAME))
            else:
                logger.info('login fail, retry later')
        else:
            logger.info('conection ok')
        time.sleep(60)


if __name__ == "__main__":
    keep_alive()
