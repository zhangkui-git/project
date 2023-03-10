#!/bin/sh

ps -ef | grep python3 |  grep -v grep |cut -c 9-15 | xargs kill -9 

ps -ef | grep -v grep | grep python3
