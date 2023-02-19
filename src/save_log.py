#!/usr/bin/env python3
#
# Copyright 2021-2023 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)


import os
import time
from cryptography.fernet import Fernet
from model import JS08Settings


os.makedirs(f'{JS08Settings.get("log_path")}/SET', exist_ok=True)   # 폴더가 없으면 생성
ym = time.strftime('%Y%m%d', time.localtime(time.time()))[2:]       # 현재 날짜

log_path = JS08Settings.get('log_path')         # QSettings 에서 log 경로를 불러온다
if os.path.isfile(f'{log_path}/Log_{ym}.txt'):  # 만약 해당 경로에 Log 파일이 있으면,
    key = JS08Settings.get_user('log_key')
    # with open(f'{log_path}/SET/SET_{ym}') as f:
    #     pass
    # key =
else:
    key = Fernet.generate_key()
    JS08Settings.set('log_key', key)
    with open(f'{log_path}/SET/SET_{ym}.txt', 'a') as f:
        f.write(str(key.decode('utf-8')))


def log(ID: str, log_msg: str):
    fernet = Fernet(key)

    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open(f'{log_path}/Log_{ym}.txt', 'a') as f:
        data = f'[{current_time}] {ID} >> {log_msg}'
        encrypt_data = fernet.encrypt(bytes(data, 'utf-8'))
        f.write(f'{str(encrypt_data)}\n')


def decrypt_log(file: str):
    date = file[file.find('Log_', 0) + 4:-4]
    with open(f'{log_path}/SET/SET_{date}.txt') as fd:
        data = fd.readlines()
    fernet = Fernet(data[0])

    result = []
    with open(file, 'r') as fv:
        data = fv.readlines()
        for i in data:
            if not i[:3] == 'key':
                output = eval(i)
                result.append(fernet.decrypt(output).decode('utf-8'))
    return result


if __name__ == '__main__':
    # for i in range(0, 10):
    #     log('TEST', 'TEST Function')
    a = decrypt_log('F://JS08/log/Log_230202.txt')
    print(a)
