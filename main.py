import logging
import os
import time

import click
import requests

try:
    from config import PASSWORD, USERNAME, VERIFICATION_URL
except ImportError:
    PASSWORD = USERNAME = None
    VERIFICATION_URL = 'https://drcom.szu.edu.cn/'

TEST_URL = 'https://www.baidu.com/'


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


class OptionPromptNull(click.Option):
    # https://stackoverflow.com/questions/45868549/
    _value_key = '_default_val'

    def get_default(self, ctx):
        if not hasattr(self, self._value_key):
            default = super(OptionPromptNull, self).get_default(ctx)
            setattr(self, self._value_key, default)
        return getattr(self, self._value_key)

    def prompt_for_value(self, ctx):
        default = self.get_default(ctx)

        # only prompt if the default value is None
        if default is None:
            return super(OptionPromptNull, self).prompt_for_value(ctx)

        return default


@click.command()
@click.option('-u', '--username', prompt=True, default=USERNAME, cls=OptionPromptNull)
@click.option('-p', '--password', prompt=True, hide_input=True, default=PASSWORD, cls=OptionPromptNull)
@click.option('-a', '--keep_alive', is_flag=True, cls=OptionPromptNull)
def cli(username, password, keep_alive):
    if keep_alive:
        logger.info('keep alive mode on')
    while True:
        if not check_connection():
            logger.info('network disconnect, retry login')
            if login(USERNAME, PASSWORD):
                logger.info('successfully login as {}'.format(USERNAME))
            else:
                logger.info('login fail, retry later')
        else:
            logger.info('conection ok')
        if not keep_alive:
            return
        time.sleep(60)


if __name__ == "__main__":
    cli()
