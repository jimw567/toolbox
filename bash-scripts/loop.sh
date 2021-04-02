#!/bin/bash

set -e

LIMIT=$1
shift
for ((i=1; i <= LIMIT ; i++))
do
    echo "------------------ START iteration $i ------------------------------"
    echo $@
    $@
    echo "------------------ END iteration $i Return code $? -----------------"
    sleep 1
done
