#!/bin/bash

if [ "$1" == "" ] ; then
    echo use: findall.sh strToFind
    exit
fi

funcy() {
  while read -r data; do
      echo $data | grep -v ".git/" |
	          grep -E "*.py$" | xargs -i grep -H $1 {}
  done
}

find . -maxdepth 1 -type f -name "*.py" | funcy $1
find complib -type f -name "*.py" | funcy $1
#find study -type f -name "*.py" | funcy $1

# EOF
