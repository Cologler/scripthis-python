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
import logging

import coloredlogs
import colorama

from fsoopify import Path

# pylint: disable=C0103
logger = logging.getLogger(__name__)
# pylint: enable=C0103

SCRIPTS_ROOT = os.environ.get('SCRIPTS_ROOT', None)

class QuickExit(Exception):
    pass

def var(text):
    return colorama.Fore.LIGHTMAGENTA_EX + text + colorama.Fore.RESET

def ensure_scripts_root():
    if not SCRIPTS_ROOT:
        logger.error('Please set the env-var `SCRIPTS_ROOT`')
        raise QuickExit
    if not os.path.isdir(SCRIPTS_ROOT):
        logger.error('<{}> is not a dir.'.format(SCRIPTS_ROOT))
        raise QuickExit

def ensure_argv():
    if len(sys.argv) != 2:
        msg = 'Please provide a executable file path.'
        msg += '\n' + colorama.Fore.RESET
        msg += ' ' * 19 + 'For example: `scripthis FILE.exe`'
        logger.error(msg)
        raise QuickExit

def link(source):
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
        logger.error(f'{var(path)} is not a file.')
        raise QuickExit

    path = Path(try_detect_path())
    logger.info(f'Creating bat for {var(path)}')
    template = os.path.join(Path(sys.argv[0]).dirname, 'template.bat')
    dest_path = os.path.join(SCRIPTS_ROOT, path.pure_name + '.bat')
    if os.path.isfile(dest_path):
        logger.info(f'Overwriting exists file: {var(dest_path)}')
    with open(template, 'r', encoding='utf8') as fp:
        content = fp.read().format(path=path)
    with open(dest_path, 'w', encoding='utf8') as fp:
        fp.write(content)
    logger.info('Done.')

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        coloredlogs.install(
            level='DEBUG',
            logger=logger,
            fmt='[%(levelname)s] %(module)s: %(message)s',
            field_styles={'levelname': {'color': 'cyan'}}
        )
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
