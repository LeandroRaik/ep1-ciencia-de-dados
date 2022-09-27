#!/bin/bash

FILE=file.json
LOG="--nolog"
echo -e "\nCarregando dados..\n"

[ -f $FILE ] && rm $FILE

[[ "$1" == "-l" ]] || [[ "$1" == "--log" ]] && LOG=""

scrapy runspider main.py -o file.json $LOG

#scrapy runspider main.py -o file.csv -t csv $LOG
