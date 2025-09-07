#!/bin/bash
cd bc && python manage.py makemigrations \
&& sleep 1 && python manage.py migrate