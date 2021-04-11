# HOME-interface
[![Build](https://github.com/megacorpincorporated/hint/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/megacorpincorporated/hint/actions/workflows/build.yml)

This is the cloud part of the HOME project, a home automation open source initiative. The project consists of a frontend
and backend part. The backend is based on the [Django](https://www.djangoproject.com/) framework, frontend uses
[Angular](https://angular.io/). Part of the HOME cloud is also a central [RabbitMQ](https://www.rabbitmq.com/) broker to
mediate messages sent from [hubs](https://github.com/megacorpincorporated/hume) part of the HOME network. To manage 
frontend websocket topic updates, [Redis](https://redis.io/) is used as a backend to dispatch websocket events to
consumers.

## Python
This project currently uses Python `3.9.2`. Install all dependencies from the project `requirements.txt`.

### Tips
Use [pyenv](https://github.com/pyenv/pyenv) to manage your Python versions.

Use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) to manage project Python dependencies.

## NodeJS
Currently used NodeJS version is `14.16.1`.

### Tips
Use [NVM](https://github.com/nvm-sh/nvm) to manage your NodeJS versions.

## Development
Here follows some instructions to start development on the HINT project. This section consists of getting RabbitMQ, 
Redis, Django, and Angular up and running so that code changes trigger reloads that are useable directly.

### Backend
Serve the Django project as you would with any other Django project: `./manage.py runserver`.

#### Create local settings
Django settings are managed through a set of base settings `backend/settings/base.py` and local user settings. Local settings
override the base settings.

In order to create local user settings, create a `local.py` file under `backend/settings/` and insert the following:

```
from .base import *  # noqa


HUME_BROKER_USERNAME = <Central RabbitMQ Username>
HUME_BROKER_PASSWORD = <Central RabbitMQ Password>

HUME_BROKER_IP = <Central RabbitMQ IP>
HUME_BROKER_PORT = <Central RabbitMQ Port>

MASTER_COMMAND_QUEUE_NAME = "hint_master"  # Or another queue name of your choosing
```
`local.py` should be updated whenever you need custom settings to your local environment. For example, if a custom SQL
database is to be used locally. Any settings that should be shared must be stated in `base.py` as `local.py` is not
under version control.

#### RabbitMQ
HINT requires a RabbitMQ instance that it can listen to messages from hubs on. Make sure the address and port of the
RabbitMQ instance correspond to the `HUME_BROKER_IP` and `HUME_BROKER_PORT` settings, as well as the
`HUME_BROKER_USERNAME` and `HUME_BROKER_PASSWORD` shall correspond to a user with sufficient rights to create a
message queue. `MASTER_COMMAND_QUEUE_NAME` is customizeable, but ensure it corresponds to the queue name where HOME hubs
will post messages.

#### Redis
Redis is used to enable pub/sub for websocket frontend updates, to update users in real time of hub events. By default,
HINT expects a local Redis instance running on port `6379`.

#### Database
By default, HINT uses SQLite for development purposes. Other SQL databases can be used just as well. Override Django
settings in your `local.py` file if you want to use something else. 

### Frontend

#### Angular
Install the [Angular CLI](https://cli.angular.io/) through [npm](https://www.npmjs.com/). It's useful for creating new
components etc. Install all dependencies from the frontend `package-lock.json` as with any other NodeJS project. Use
the Angular CLI to update project dependencies.

#### Watch for file changes
Issue `ng build --watch --output-path=<path-to-hint>/backend/static/ang/` to compile the frontend project to get served
by the Django development server. The command will make sure the compiled JS files get served from a known Django static
directory.
