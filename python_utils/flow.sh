#!/usr/bin/env bash
set -e

echo ">>> 正在从pip正式/测试环境检索线上最新版本...."
formal_latest=`pip search zac-pyutils | grep zac-pyutils`
test_latest=`pip search zac-pyutils -i https://test.pypi.org/pypi | grep zac-pyutils`
setup_version=`cat setup.py | grep -Eo "version='[0-9\.]+'"`
echo "正式环境最新版本为: $formal_latest"
echo "测试环境最新版本为: $test_latest"
echo "当前setup.py配置的版本为: $setup_version"

read -r -p ">>> 确认setup.py版本号正确... [y/n] " input
if [[ ${input} = "y" ]]; then
    rm -rf dist
    python setup.py sdist build
    read -r -p ">>> 更新到正式还是测试?  [formal/test]" target
    if [[ ${target} = "test" ]]; then
    echo "更新到测试 || https://test.pypi.org/project/zac-pyutils/ | account: 2ach_test"
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    echo "pip install zac-pyutils  --upgrade -i https://test.pypi.org/pypi"
    else
    echo "更新到正式 || https://pypi.org/project/zac-pyutils/ | account: 2ach"
    twine upload dist/*
    echo "pip install zac-pyutils  --upgrade -i https://pypi.python.org/pypi"
    fi
elif [[ ${input} = "n" ]]; then
    echo "exit..."
    exit 0
fi
