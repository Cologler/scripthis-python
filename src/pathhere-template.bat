@ECHO off
IF DEFINED PATH_HERE (
    SET PATH_HERE="{path}";%PATH_HERE%
) ELSE (
    SET PATH_HERE="{path}"
)
PATH = "{path}";%PATH%
ECHO added {path} to path.