#!/bin/bash
DIR=$(pwd)

cd src/
python3 NN.py &
sleep 10s
cd $DIR/SSF2-linux/
./SSF2
