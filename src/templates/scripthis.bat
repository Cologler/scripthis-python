@REM this script was created by scripthis
@echo off
if exist "{path}" (
    {eval}"{path}" %*
) else (
    echo {path} does not exists, please reset the bat file using scripthis.
)
