#!/bin/bash

ps -ef |grep main_service.py |grep -v grep |awk '{print $2}' |xargs sudo kill
