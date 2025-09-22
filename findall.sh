#!/bin/bash

if [ "$1" == "" ] ; then
	echo use: findall.sh str_to_find
	exit
fi

find . -name "*.py" -type f | xargs -i grep -H $1 {} 
