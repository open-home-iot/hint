# NB!
# LEAVE LABELLING TO THE ACTION WORKFLOW!

FROM rabbitmq:3.11.1-management

COPY rabbitmq/definitions.json /etc/rabbitmq/definitions.json
COPY rabbitmq/rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
COPY rabbitmq/enabled_plugins /etc/rabbitmq/enabled_plugins

RUN rm -rf /etc/rabbitmq/conf.d
