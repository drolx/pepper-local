#!/bin/sh

# NOTE: Manual gunicorm usage
python -m gunicorn -w 4 --worker-class sync app.manage
