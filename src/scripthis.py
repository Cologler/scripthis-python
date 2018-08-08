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
from fsoopify import Path

from _common import BaseApp, QuickExit

KEY_EXEC = 'exec'
KEY_INIT = 'init'
KEY_TEMPLATE = 'template'

EVAL_TABLE = {
    '.jar': {
        KEY_EXEC: 'java -jar'
    },

    '.js': {
        KEY_EXEC: 'node'
    },

    '.ts': {
        KEY_EXEC: 'ts-node'
    },

    '.py': {
        KEY_EXEC: 'python',

        'pipenv': {
            KEY_EXEC: 'pipenv run python',
            KEY_TEMPLATE: 'scripthis-tmp-cwd.bat'
        }
    }
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
            return pathext.split(';') + list(EVAL_TABLE.keys())

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

        template_name = 'scripthis.bat'
        init = ''

        eval_data = EVAL_TABLE.get(path.name.ext.lower())
        if eval_data is not None:
            if env and env != KEY_EXEC:
                eval_data = eval_data.get(env.lower())
                if eval_data is None:
                    return self.error_unknown_env(env)
            eval_stmt = eval_data[KEY_EXEC] + ' '
            template_name = eval_data.get(KEY_TEMPLATE, template_name)
            init = eval_data.get(KEY_INIT, init)
        elif env and env != KEY_EXEC:
            return self.error_unknown_env(env)
        else:
            eval_stmt = ''

        content = self.load_template(template_name).format(**{
            'path': path,
            'dir': os.path.dirname(path),
            'eval': eval_stmt,
            'init': init
        })

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
