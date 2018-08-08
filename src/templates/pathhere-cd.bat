@REM this script was created by scripthis
@ECHO off
IF DEFINED PATH_HERE (
    SET PATH_HERE="{path}";%PATH_HERE%
) ELSE (
    SET PATH_HERE="{path}"
)
CD "{path}"
ECHO cd {path}
