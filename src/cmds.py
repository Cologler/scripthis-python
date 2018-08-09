# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback

from fsoopify import Path

from _common import BaseApp

class App(BaseApp):

    def run(self, argv):
        self.cmds_in_dir(self._scripts_root, 'envvar: <SCRIPTS_ROOT>')
        path_here = os.environ.get('PATH_HERE')
        if path_here:
            for path in path_here.split(os.pathsep):
                if path.startswith('"') and path.endswith('"'):
                    path = path[1:-1]
                self.cmds_in_dir(path)

    def cmds_in_dir(self, path, desc=None):
        if not os.path.isdir(path):
            return
        names = []
        for name in os.listdir(path):
            names.append(Path(name).pure_name)
        msg = 'commands in {}'
        if desc:
            msg += f' ({desc})'
        self.log_info(msg, path)
        self.print_cmds(names)

    def print_cmds(self, cmds):
        for index, name in enumerate(cmds):
            name += '\t' * (2 - len(name) % 16 // 8)
            end = '\n' if index % 6 == 5 else ''
            print(name, end=end)
        if not end:
            print('\n')


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        app = App()
        app.run(argv[1:])
    except Exception: # pylint: disable=W0703
        traceback.print_exc()

if __name__ == '__main__':
    main()
