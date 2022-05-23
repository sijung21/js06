#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import multiprocessing as mp
from src.nd01 import clock, ND01MainWindow


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    print(f'Start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

    mp.freeze_support()
    q = Queue()
    _q = Queue()

    _producer = producer

    p = Process(name='clock', target=clock, args=(q,), daemon=True)
    _p = Process(name='producer', target=_producer, args=(_q,), daemon=True)

    p.start()
    _p.start()

    os.makedirs(f'{JS06Settings.get("data_csv_path")}', exist_ok=True)
    os.makedirs(f'{JS06Settings.get("target_csv_path")}', exist_ok=True)
    os.makedirs(f'{JS06Settings.get("image_save_path")}', exist_ok=True)

    app = QApplication(sys.argv)
    window = ND01MainWindow(q, _q)
    sys.exit(app.exec())
