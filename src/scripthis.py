#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

'''
Scripthis
    create shortcut of file.

Usage:
    scripthis <FILE> [--env=]
'''

import os
import sys
import traceback

from docopt import docopt
import colorama
from fsoopify import Path, FileInfo

from _common import BaseApp, QuickExit

KEY_EXEC = 'exec'
KEY_INIT = 'init'
KEY_TEMPLATE = 'template'
KEY_EXT_TABLE = 'ext-table'

class ExecutorInfo:
    def __init__(self, executor='', **envs):
        self.executor = executor
        self.envs = envs

    def get_template(self):
        return 'scripthis.bat'

    def update_args(self, args: dict):
        if self.executor:
            args['eval'] = self.executor + ' '
        else:
            args['eval'] = ''

class PipenvExecutorInfo(ExecutorInfo):
    def get_template(self):
        return 'scripthis-pipenv.bat'

    def update_args(self, args: dict):
        super().update_args(args)
        script_file = FileInfo(args['path'])
        args['pipfile'] = self._find_pipfile_path(script_file, 5)

    def _find_pipfile_path(self, script_file: FileInfo, depth: int):
        dir_info = script_file.get_parent()
        while depth > 0:
            pf = dir_info.get_fileinfo('Pipfile')
            if pf.is_file():
                return pf.path
            dir_info = dir_info.get_parent()
            depth -= 1
        raise RuntimeError('cannot found Pipfile.')


EXECUTOR_INFO_TABLE = {
    '.jar': ExecutorInfo(executor='java -jar'),
    '.js': ExecutorInfo(executor='node'),
    '.ts': ExecutorInfo(executor='ts-node'),
    '.py': ExecutorInfo(executor='python',
        pipenv=PipenvExecutorInfo(executor='pipenv run python')
    )
}

class App(BaseApp):
    def error_unknown_env(self, env):
        self.log_error('unknown env: {}', env)
        return exit(1)

    def run(self, argv):
        if not argv:
            msg = 'Please provide a executable file path.'
            msg += '\n' + colorama.Fore.RESET
            msg += ' ' * 19 + 'For example: `scripthis FILE.exe`'
            self.log_error(msg)
            exit(3)

        args = docopt(__doc__)
        source = args['<FILE>']
        env = args['--env']

        def list_executeable_exts():
            pathext = os.getenv('PATHEXT').lower()
            return pathext.split(';') + list(EXECUTOR_INFO_TABLE.keys())

        def try_detect_path():
            p = os.path.abspath(source)
            if os.path.isfile(p):
                return p
            for ext in list_executeable_exts():
                if os.path.isfile(p + ext):
                    return p + ext
            self.log_error('{} is not a file', p)
            exit()

        path = Path(try_detect_path())

        executor_info = EXECUTOR_INFO_TABLE.get(path.name.ext.lower())
        if executor_info is not None and env:
            executor_info = executor_info.envs.get(env.lower())

        if not executor_info and env:
            return self.error_unknown_env(env)

        executor_info = executor_info or ExecutorInfo()

        args_table = {
            'path': path,
            'dir': os.path.dirname(path)
        }

        executor_info.update_args(args_table)
        content = self.load_template(executor_info.get_template()).format_map(args_table)
        self.write_script(path, path.pure_name, content)


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
