#!/bin/bash
source `which virtualenvwrapper.sh`

startDjango()
{
    workon hint
    sleep 0.5
    python manage.py runserver &
}
startDjango

ngBuild()
{
    cd frontend
    ng build --watch --output-path /home/frer/Projects/hint/backend/static/ang/
}
ngBuild
