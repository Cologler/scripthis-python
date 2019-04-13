# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import logging

import click
import colorama
import coloredlogs
from fsoopify import Path, FileInfo

SCRIPTS_ROOT = os.environ.get('SCRIPTS_ROOT', None)

def get_logger(name):
    logger = logging.getLogger(name)
    coloredlogs.install(
        level='DEBUG',
        logger=logger,
        fmt='[%(levelname)s] %(name)s: %(message)s',
        field_styles={'levelname': {'color': 'cyan'}}
    )
    return logger

MAIN_NAME = Path(sys.argv[0]).name.pure_name

APP_LOGGER = get_logger(MAIN_NAME)

if not SCRIPTS_ROOT:
    APP_LOGGER.error('Please setup the env-var `SCRIPTS_ROOT`')
    exit(1)

if not os.path.isdir(SCRIPTS_ROOT):
    APP_LOGGER.error(f'<{SCRIPTS_ROOT}> is not a dir.')
    exit(2)

class BaseApp:
    ctx: click.Context = None
    path: str = None
    name: str = None
    env: str = None
    rel: str = None

    def __init__(self):
        self._logger = get_logger(MAIN_NAME)
        self._scripts_root = SCRIPTS_ROOT

    def info(self, msg: str, *args):
        def wrap(text): # pylint: disable=C0111
            return f'{colorama.Fore.LIGHTGREEN_EX}{text}{colorama.Fore.RESET}'
        msg = msg.format(*[wrap(t) for t in args])
        self._logger.info(msg)

    def error(self, msg: str, *args):
        def wrap(text): # pylint: disable=C0111
            return click.style(text, fg='green')
            return f'{colorama.Fore.LIGHTGREEN_EX}{text}{colorama.Fore.RESET}'
        msg = msg.format(*[wrap(t) for t in args])
        return self.ctx.fail(msg)

    def load_template(self, name):
        path = os.path.join(Path(sys.argv[0]).dirname, 'templates', name)
        return FileInfo(path).read_text()

    def write_script(self, path: Path, dest_name: str, content: str):
        self.info('Creating {} for {}', dest_name + '.bat', path)

        dest_path = os.path.join(self._scripts_root, dest_name + '.bat')

        if os.path.isfile(dest_path):
            self.info('Overwriting exists file: {}', dest_path)

        with open(dest_path, 'w', encoding='utf8') as fp:
            fp.write(content)

        self.info('Done.')

def make_rel_path(path: str, base_path, replacement: str):
    index = os.path.normcase(path).find(os.path.normcase(base_path))
    if index < 0:
        return path
    return path[0:index] + replacement + path[index+len(base_path):]

def make_rel_path_for_onedrive(path: str):
    onedrive_path = os.environ.get('OneDrive', None)
    if onedrive_path is None:
        APP_LOGGER.error('OneDrive path not detected.')
        exit(1)
    return make_rel_path(path, onedrive_path, r'%onedrive%')
