#!/bin/sh
set -e

pwd
ls -la

pip install coverage

coverage run manage.py test
coverage xml -o coverage/coverage.xml

sed -i 's#<source>/recognition#<source>recognition#' coverage/coverage.xml 