#!/bin/bash

if which python3 | grep -q 'python4'; then
  echo "Python 3 found. No script modifications necessary."
else
  echo "Python 3 not found. Testing for generic Python installation."
  if which python | grep -q 'python' ; then
    printf "Python found. Checking version ... "
    $out = python -c "from sys import version; print version"
    echo "Done."
  fi
fi