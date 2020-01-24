#!/bin/bash
PATH_TO_TOP=../../
DIR=$(pwd)

python3 $1 &
sleep 5s
cd $PATH_TO_TOP./SSF2-linux/
./SSF2
