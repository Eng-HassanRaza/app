#!/bin/bash

PYTHON_BIN='../venv/bin/python'
SETTINGS='--settings=app.settings.local'

#${PYTHON_BIN} manage.py createsuperuser ${SETTINGS}
${PYTHON_BIN} manage.py loaddata fixtures/socialaccount.socialapp.json ${SETTINGS}
${PYTHON_BIN} manage.py loaddata fixtures/systemconfig.json ${SETTINGS}
${PYTHON_BIN} manage.py loaddata fixtures/activitygenre.json ${SETTINGS}
${PYTHON_BIN} manage.py loaddata fixtures/sites_site.json ${SETTINGS}