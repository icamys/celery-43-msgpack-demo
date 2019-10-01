#!/usr/bin/env bash
watchmedo  auto-restart --directory=. --pattern=*.py --recursive -- \
    celery -A tasks worker --loglevel info
