@REM this script was created by scripthis
@echo off
if defined PATH_HERE (
    set PATH_HERE="{path}";%PATH_HERE%
) else (
    set PATH_HERE="{path}"
)
if exist "{path}" (
    set PATH="{path}";%PATH%
    echo added {path} to path.
) else (
    echo {path} does not exists, please reset the bat file using scripthis.
)
