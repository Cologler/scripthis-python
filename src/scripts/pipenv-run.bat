@echo off
pushd %~dp1
pipenv run python %*
popd
