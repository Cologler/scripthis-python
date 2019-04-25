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
    scripthis <FILE> [--env=] [--rel=] [--name=]
'''

import os
import sys
import traceback

from docopt import docopt
import colorama
from fsoopify import Path, FileInfo, NodeInfo, NodeType
import click
from click_anno import command

from _common import BaseApp, make_rel_path_for_onedrive

def list_executeable_exts():
    pathext = os.getenv('PATHEXT').lower()
    return pathext.split(';') + list(EXECUTOR_INFO_TABLE.keys())

class App(BaseApp):

    def find_abspath(self):
        path = os.path.abspath(self.path)
        if os.path.isfile(path) or os.path.isdir(path):
            return path
        for ext in list_executeable_exts():
            realpath = path + ext
            if os.path.isfile(realpath):
                return realpath

        styled_path = click.style(path, fg='green')
        self.error('{} does not exists', path)

    def get_rel_func(self):
        if self.rel is None:
            return lambda x: x
        elif self.rel.lower() == 'onedrive':
            return make_rel_path_for_onedrive
        else:
            self.error('unknown rel args: {}', self.rel)

    def get_executor_info(self, node: FileInfo):
        root_key = node.path.name.ext.lower() if node.node_type == NodeType.file else 'folder'
        executor_info = EXECUTOR_INFO_TABLE.get(root_key)

        if executor_info and self.env:
            executor_info = executor_info.envs.get(self.env.lower())

        if executor_info:
            return executor_info
        elif self.env:
            self.error('unknown env: {}', self.env)
        else:
            return ExecutorInfo()

    def __call__(self):
        env = self.env
        arg_name = self.name
        rel_func = self.get_rel_func()

        node = NodeInfo.from_path(self.find_abspath())
        executor_info = self.get_executor_info(node)

        args = {
            'path': node.path,
            'dir': os.path.dirname(node.path)
        }
        executor_info.update_args(self, args)
        for k, v in list(args.items()):
            args[k] = rel_func(v)

        content = self.load_template(executor_info.get_template()).format_map(args)
        self.write_script(args['path'], arg_name or node.path.pure_name, content)

class ExecutorInfo:
    def __init__(self, executor='', **envs):
        self.executor = executor
        self.envs = envs

    def get_template(self):
        return 'scripthis.bat'

    def update_args(self, app: App, args: dict):
        if self.executor:
            args['eval'] = self.executor + ' '
        else:
            args['eval'] = ''

class PipenvExecutorInfo(ExecutorInfo):
    def get_template(self):
        return 'scripthis-pipenv.bat'

    def update_args(self, app: App, args: dict):
        super().update_args(app, args)
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


class FolderExecutorInfo(ExecutorInfo):
    def update_args(self, app: App, args: dict):
        app.error('folder without env is not callable')


EXECUTOR_INFO_TABLE = {
    'folder': FolderExecutorInfo(),
    '.jar': ExecutorInfo(executor='java -jar'),
    '.js': ExecutorInfo(executor='node'),
    '.ts': ExecutorInfo(executor='ts-node'),
    '.py': ExecutorInfo(executor='python',
        pipenv=ExecutorInfo(executor='pipenv-run-py')
    )
}
EXECUTOR_INFO_TABLE['folder'].envs['py-m'] = ExecutorInfo(executor='run-pym')
EXECUTOR_INFO_TABLE['folder'].envs['python-m'] = ExecutorInfo(executor='run-pym')
EXECUTOR_INFO_TABLE['folder'].envs['pipenv'] = ExecutorInfo(executor='pipenv-run-pym')
EXECUTOR_INFO_TABLE['folder'].envs['pipenv-py-m'] = ExecutorInfo(executor='pipenv-run-pym')
EXECUTOR_INFO_TABLE['folder'].envs['pipenv-python-m'] = ExecutorInfo(executor='pipenv-run-pym')

@command
def cli(ctx: click.Context, path: str, name: str=None, env: str=None, rel: str=None):
    app = App()
    app.__dict__.update({
        'ctx': ctx,
        'path': path,
        'name': name,
        'env': env,
        'rel': rel,
    })
    app()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        cli()
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
