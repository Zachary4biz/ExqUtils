#!/usr/bin/env bash
rm -rf dist
python setup.py sdist build
if [[ $1 == "test" ]]; then
echo ">>> uploading to || TEST || https://test.pypi.python.org | account is 2ach_test"
echo "check result at https://test.pypi.org/project/zac-pyutils/"
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
else
echo ">>> uploading to || FORMAL || https://pypi.python.org | account is 2ach"
twine upload dist/*
fi
