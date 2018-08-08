@REM this script was created by scripthis
@echo off
if exist "{path}" (
    set PIPENV_PIPFILE={pipfile}
    {eval}"{path}" %*
) else (
    echo {path} does not exists, please reset the bat file using scripthis.
)
