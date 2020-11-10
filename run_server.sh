#!/usr/bin/env bash

source venv/bin/activate

export FLASK_APP=manager.py
export FLASK_ENV=development
export FLASK_DEBUG=0

export PRODUCTION_HOST="http://127.0.0.1:5000"
export UPLOAD_FOLDER="/Users/fortune/Developer/"

export MATHPIX_APP_ID="secret"
export MATHPIX_APP_KEY="secret"

export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'

uwsgi uwsgi.ini
