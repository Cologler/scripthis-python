@REM this script was created by scripthis
@echo off
if defined PATH_HERE (
    set PATH_HERE="{path}";%PATH_HERE%
) else (
    set PATH_HERE="{path}"
)
if exist "{path}" (
    cd "{path}"
    echo chdir: {path}
) else (
    echo {path} does not exists, please reset the bat file using scripthis.
)
