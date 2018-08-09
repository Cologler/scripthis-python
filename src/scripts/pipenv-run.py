# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# call pipenv run *args without change work dir.
# ----------

import os
import sys
import traceback

from fsoopify import FileInfo, NodeInfo

def find_pipfile_path(script_file: FileInfo, depth: int):
    dir_info = script_file.get_parent()
    while depth > 0:
        pf = dir_info.get_fileinfo('Pipfile')
        if pf.is_file():
            return pf.path
        dir_info = dir_info.get_parent()
        depth -= 1
    raise RuntimeError('cannot found Pipfile.')

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        if len(sys.argv) > 1:
            script_file = NodeInfo.from_path(sys.argv[1])
            script_file = script_file or NodeInfo.from_path(sys.argv[1] + '.py')
            if script_file:
                abspath = os.path.abspath(script_file.path)
                sys.argv[1] = abspath
                script_file = NodeInfo.from_path(abspath)

                import pipenv.environments as environments
                environments.PIPENV_PIPFILE = find_pipfile_path(script_file, 5)

        sys.argv = ['pipenv', 'run', 'python'] + sys.argv[1:]

        from pipenv import cli
        cli()
    except Exception: # pylint: disable=W0703
        traceback.print_exc()

if __name__ == '__main__':
    main()
