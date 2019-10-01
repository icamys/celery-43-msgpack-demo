#!/usr/bin/env bash
docker run -d --name rabbit-celery-bug-demo -p 5672:5672 -p 15672:15672 rabbitmq:3.7.18-management
