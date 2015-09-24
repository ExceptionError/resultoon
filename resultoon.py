# -*- coding: utf-8 -*-

import threading

from lib.core import *

def main():
    core = Core()
    thread = threading.Thread(target = core.execute)
    thread.setDaemon(True)
    thread.start()
    core.show('preview')

if __name__ == '__main__':
    main()
