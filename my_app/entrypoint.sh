#!/usr/bin/env bash
flask db upgrade
gunicorn -w 5 -b 0.0.0.0:5005 run:app