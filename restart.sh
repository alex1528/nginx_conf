#!/bin/bash

export PYTHONPATH=.

ps -ef |grep main_service.py |grep -v grep |awk '{print $2}' |xargs sudo kill

nohup python web/main_service.py &
