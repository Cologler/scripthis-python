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
from fsoopify import Path

SCRIPTS_ROOT = os.environ.get('SCRIPTS_ROOT', None)

class QuickExit(Exception):
    pass

def ensure_scripts_root():
    if not SCRIPTS_ROOT:
        print('[ERROR] Please set the env-var `SCRIPTS_ROOT`')
        raise QuickExit
    if not os.path.isdir(SCRIPTS_ROOT):
        print('[ERROR] <{}> is not a dir.'.format(SCRIPTS_ROOT))
        raise QuickExit

def ensure_argv():
    if len(sys.argv) != 2:
        print('[ERROR] Please provide a executable file path.')
        print('        For example: `scripthis FILE.exe`')
        raise QuickExit

def link(source):
    path = Path(os.path.abspath(source))
    if not os.path.isfile(path):
        print('[ERROR] <{}> is not a file.'.format(path))
        raise QuickExit
    print('[INFO] Creating bat for <{}>'.format(path))
    template = os.path.join(Path(sys.argv[0]).dirname, 'template.bat')
    dest_path = os.path.join(SCRIPTS_ROOT, path.pure_name + '.bat')
    if os.path.isfile(dest_path):
        print('[INFO] Overwriting exists file: {}'.format(dest_path))
    with open(template, 'r', encoding='utf8') as fp:
        content = fp.read().format(path=path)
    with open(dest_path, 'w', encoding='utf8') as fp:
        fp.write(content)
    print('[INFO] Done.')

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        ensure_scripts_root()
        ensure_argv()
        link(argv[1])
    except QuickExit:
        return
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
