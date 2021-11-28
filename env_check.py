# -*- coding: utf-8
import sys
import os
import re


def env_check():
    if sys.version_info < (3, 6):
        raise OSError('请至少使用 Python 3.6 及以上版本，建议使用 Python 3.7 及以上版本')

    try:
        import selenium
    except ImportError:
        raise ImportError(
            '没有找到selenium包，请用pip安装一下吧～ pip3 install --user selenium')

    lst_conf = sorted([
        fileName for fileName in os.listdir()
        if re.match(r'^config[0-9][0-9]*\.ini$', fileName)
    ],
        key=lambda x: int(re.findall(r'[0-9]+', x)[0]))

    if len(lst_conf) == 0:
        raise ValueError('请先在config.sample.ini文件中填入个人信息，并将它改名为config.ini')

    print('环境检查通过')

    return lst_conf
