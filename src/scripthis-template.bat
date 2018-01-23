@echo off
if exist "{path}" (
    "{path}" %*
) else (
    echo {path} does not exists, please reset the bat file using scripthis.
)