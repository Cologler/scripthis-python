@REM this script was created by scripthis
@echo off
if exist "{path}" (
    pushd {dir}
    {eval}"{path}" %*
    popd %cwd%
) else (
    echo {path} does not exists, please reset the bat file using scripthis.
)
