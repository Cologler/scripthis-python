#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback

import colorama
from fsoopify import Path

from _common import BaseApp, QuickExit

class App(BaseApp):
    def __init__(self):
        super().__init__(Path(sys.argv[0]).name.pure_name)

    def run(self, argv):
        if len(argv) != 1:
            msg = 'Please provide a executable file path.'
            msg += '\n' + colorama.Fore.RESET
            msg += ' ' * 19 + 'For example: `scripthis FILE.exe`'
            self._log_err(msg)
            exit()

        source = argv[0]

        def list_executeable_exts():
            pathext = os.getenv('PATHEXT').lower()
            return pathext.split(';')

        def try_detect_path():
            p = os.path.abspath(source)
            if os.path.isfile(p):
                return p
            for ext in list_executeable_exts():
                if os.path.isfile(p + ext):
                    return p + ext
            self._log_err('{} is not a file', p)
            exit()

        path = Path(try_detect_path())

        self._write_script(path, path.pure_name, {
            'path': path
        });


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        app = App()
        app.run(argv[1:])
    except QuickExit:
        return
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
