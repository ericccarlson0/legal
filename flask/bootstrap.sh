#!/bin/sh

export FLASK_APP=./app/index.py
pipenv run flask --debug run -h 0.0.0.0 -p 5001 \
--cert=/Users/ericcarlson/.ssh/cert.pem \
--key=/Users/ericcarlson/.ssh/key.pem
