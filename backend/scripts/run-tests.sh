#!/bin/sh
set -e

pwd
ls -la

pip install coverage

coverage run --source=. manage.py test
coverage xml -o coverage/coverage.xml

sed -i 's#<source>/\([^<]*\)#<source>\1#' coverage/coverage.xml