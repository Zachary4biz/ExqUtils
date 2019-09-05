#!/usr/bin/env bash
set -e
read -r -p "确认setup.py已更改版本号... [y/n] " input
if [[ ${input} = "y" ]]; then
    rm -rf dist
    python setup.py sdist build
    read -r -p "更新到正式还是测试?  [formal/test]" target
    if [[ ${target} = "test" ]]; then
    echo ">>> 更新到测试 || https://test.pypi.org/project/zac-pyutils/ | account: 2ach_test"
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    echo "pip install zac-pyutils  --upgrade -i https://test.pypi.org/pypi"
    else
    echo ">>> 更新到正式 || https://pypi.org/project/zac-pyutils/ | account: 2ach"
    twine upload dist/*
    echo "pip install zac-pyutils  --upgrade -i https://pypi.python.org/pypi"
    fi
elif [[ ${input} = "n" ]]; then
    echo "exit..."
    exit 0
fi
