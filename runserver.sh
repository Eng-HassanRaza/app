#!/bin/bash

python manage.py runserver_plus --cert-file _tmp/server.crt --settings=app.settings.local
#python manage.py runserver_plus --cert-file _tmp/server.crt --settings=app.settings.prod
