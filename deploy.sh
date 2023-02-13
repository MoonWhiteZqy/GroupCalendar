#!/bin/bash
ps aux | grep uwsgi | awk '{print $2}'|xargs kill -9
#nohup python3 star.py >> ./fanweb.log 2>&1 &
uwsgi -d --ini calendar.ini
