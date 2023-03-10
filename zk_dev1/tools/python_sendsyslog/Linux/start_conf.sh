#/bin/sh

python3 main.py   config  &

ps -ef | grep -v grep | grep python3
