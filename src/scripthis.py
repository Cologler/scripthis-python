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
    if SCRIPTS_ROOT is None:
        print('[ERROR] please set the env-var `SCRIPTS_ROOT`')
        raise QuickExit
    if not os.path.isdir(SCRIPTS_ROOT):
        print('[ERROR] {} is not a dir.'.format(SCRIPTS_ROOT))
        raise QuickExit

def ensure_argv_len(val):
    if len(sys.argv) != val:
        print('[ERROR] count of argv should be {}.'.format(val))
        raise QuickExit

def link(source):
    path = Path(os.path.abspath(source))
    print('[INFO] creating bat for {}'.format(path))
    with open(os.path.join(Path(sys.argv[0]).dirname, 'template.bat'), 'r', encoding='utf8') as fp:
        content = fp.read().format(path=path)
    with open(os.path.join(SCRIPTS_ROOT, path.pure_name + '.bat'), 'w', encoding='utf8') as fp:
        fp.write(content)
    print('[INFO] done.')

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        ensure_scripts_root()
        ensure_argv_len(2)
        link(argv[1])
    except QuickExit:
        return
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
