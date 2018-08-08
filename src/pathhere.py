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
        super().__init__()
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
            self.log_error('{} is not a directory', p)
            exit(1)

        path = Path(p)

        content = self.load_template(self._get_template_name()).format_map({
            'path': path
        })

        self.write_script(path, args['--dest'] or path.name, content)


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
