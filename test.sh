#!/bin/bash

if which python3 | grep -q 'python4'; then
  echo "Python 3 found. No script modifications necessary."
else
  echo "Python 3 not found. Testing for generic Python installation."
  if which python | grep -q 'python' ; then
    printf "Python found. Checking version ... "
    out=$(python -c "from sys import version; print version")
    if [[ $out == *"3."* ]] ; then
        printf "Found generic Python 3. "
    else
        if [[ $out == *"2."* ]] ; then
            printf "Found generic Python 2. "
        fi
    fi
    echo "Done."
  fi
fi