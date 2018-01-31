#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

'''
Path Here.

Usage:
  pathhere <dirpath> [--dest=] [--with-workdir]
'''

import os
import sys
import traceback

from docopt import docopt
from fsoopify import Path

from _common import BaseApp, QuickExit

class App(BaseApp):
    def __init__(self):
        super().__init__(Path(sys.argv[0]).name.pure_name)
        self._mode = None

    def _get_template_name(self):
        name = self._name
        if self._mode is not None:
            name += f'-{self._mode}'
        return name + '-template.bat'

    def run(self, argv):
        args = docopt(__doc__)

        # mode
        if args['--with-workdir']:
            self._mode = 'cd'

        p = os.path.abspath(args['<dirpath>'])
        if not os.path.isdir(p):
            self._log_err('{} is not a directory', p)
            raise QuickExit

        path = Path(p)

        self._write_script(path, args['--dest'] or path.name, {
            'path': path
        })


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
