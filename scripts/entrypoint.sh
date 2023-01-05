#!/bin/bash

set -e

uwsgi --http :${PORT} --module wsgi:app --master --processes 4 --threads 2
