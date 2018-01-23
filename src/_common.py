# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import logging

import colorama
import coloredlogs

SCRIPTS_ROOT = os.environ.get('SCRIPTS_ROOT', None)

class QuickExit(Exception):
    pass

def get_logger(name):
    logger = logging.getLogger(name)
    coloredlogs.install(
        level='DEBUG',
        logger=logger,
        fmt='[%(levelname)s] %(name)s: %(message)s',
        field_styles={'levelname': {'color': 'cyan'}}
    )
    return logger

class BaseApp:
    ''''''

    def __init__(self, name):
        self._logger = get_logger(name)
        self._scripts_root =  SCRIPTS_ROOT

        if not self._scripts_root:
            self._logger.error('Please setup the env-var `SCRIPTS_ROOT`')
            raise QuickExit

        if not os.path.isdir(self._scripts_root):
            self._logger.error(f'<{self._scripts_root}> is not a dir.')
            raise QuickExit

    def run(self, argv):
        raise NotImplementedError

    def _log_info(self, msg: str, *args):
        def var(text): # pylint: disable=C0111
            return colorama.Fore.LIGHTMAGENTA_EX + text + colorama.Fore.RESET

        msg = msg.format([var(t) for t in args])
        self._logger.info(msg)

    def _log_err(self, msg: str, *args):
        def var(text): # pylint: disable=C0111
            return colorama.Fore.LIGHTMAGENTA_EX + text + colorama.Fore.RESET

        msg = msg.format([var(t) for t in args])
        self._logger.error(msg)
