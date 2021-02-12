#!/bin/bash
source `which virtualenvwrapper.sh`

startDjango()
{
    workon hint
    #sleep 0.5
    #python manage.py runserver &
}
startDjango

startRabbitMq()
{
    docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    sleep 0.5
}
startRabbitMq

startRedis()
{
    docker run -d -it --rm --name redis -p 6379:6379 redis
    sleep 0.5
}
startRedis

ngBuild()
{
    cd frontend
    ng build --watch --output-path /home/fredrik/Projects/hint/backend/static/ang/
}
ngBuild


