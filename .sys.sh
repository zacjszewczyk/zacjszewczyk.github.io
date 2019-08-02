#!/bin/bash

HEADER=$'\033[95m' # Pink
OKBLUE=$'\033[94m' # Purple
OKGREEN=$'\033[92m' # Green
WARNING=$'\033[93m' # Yellow
FAIL=$'\033[91m' # Red
ENDC=$'\033[0m' # None
BOLD=$'\033[1m' # Blue
UNDERLINE=$'\033[4m' # Underline

function migrate_python () {
    echo "To search for: "$1
    echo "To replace with: "$2
    sed -i '' "s|$1|$2|g" colors.py
    sed -i '' "s|$1|$2|g" blog.py
    sed -i '' "s|$1|$2|g" ModTimes.py
    sed -i '' "s|$1|$2|g" Markdown2.py
    sed -i '' "s|$1|$2|g" Hash.py
}

printf "Testing Python 3 ... "
if which python3 | grep -q 'python3'; then
  printf $OKGREEN"Python 3 found.\n"$ENDC
  if which python3 | grep -q '/usr/local/bin/python3'; then
    echo $OKGREEN"Path to Python 3 executable matches. No script modifications necessary."$ENDC
  else
    echo $WARNING"Path to Python 3 executable does not match. Modifying ..."$ENDC
    search="#!/usr/local/bin/python3"
    replace="#!"$(which python3)
    migrate_python $search $replace
  fi
else
  printf $FAIL"Python 3 not found.$ENDC\n"
  printf $WARNING"Testing Python generic installation ... "$ENDC
  if which python | grep -q 'python' ; then
    printf $OKGREEN"'python' found. Editing path to executable ... "$ENDC
    search="#!/usr/local/bin/python3"
    replace="#!"$(which python)
    migrate_python $search $replace
    printf $OKGREEN"Done."$ENDC

    echo "Testing Python generic version ... "
    out=$(python -c "from sys import version; print version")
    if [[ $out == *"3."* ]] ; then
        printf $OKGREEN"Found generic Python 3. No further modifications necessary."$ENDC
    else
        if [[ $out == *"2."* ]] ; then
            printf $WARNING"Found generic Python 2. Script modification necessary.\n"$ENDC
            search="print("
            replace="print ("
            migrate_python $search $replace
        fi
    fi
  else
    echo $FAIL"Python not found. Please install Python."$ENDC
  fi
fi