@REM this script was created by scripthis
@echo off
if exist "{path}" (
    pushd {dir}
    {eval}"{path}" %*
    popd
) else (
    echo {path} does not exists, please reset the bat file using scripthis.
    exit /b 1
)
