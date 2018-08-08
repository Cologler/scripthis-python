REM this script was created by scripthis
@echo off
if exist "{path}" (
    if "{eval}" == "" (
        "{path}" %*
    ) else (
        {eval} "{path}" %*
    )
) else (
    echo {path} does not exists, please reset the bat file using scripthis.
)
