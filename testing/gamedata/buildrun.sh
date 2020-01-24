#!/bin/bash
PATH_TO_TOP=../../
DIR=$(pwd)

cd $PATH_TO_TOP./SSF2-linux/data/
cp  SSF2.swf run
cd $DIR
python3 $1 &
sleep 5s
cd $PATH_TO_TOP./SSF2-linux/
./SSF2
