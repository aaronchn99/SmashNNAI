 #!/bin/bash
MACHINE_TYPE=`uname -m`
if [ ${MACHINE_TYPE} == 'x86_64' ]; then
  "./data/fp64" "$PWD/data/run"
else
  "./data/fp" "$PWD/data/run"
fi


