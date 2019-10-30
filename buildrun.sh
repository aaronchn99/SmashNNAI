#!/bin/bash
cd ./SSF2-linux/data/
cp  SSF2.swf run
cd ../../
python SSF2Connection.py &
cd SSF2-linux/
./SSF2
