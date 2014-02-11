#!/bin/sh
export XDG_DATA_DIRS=$(dirname $(readlink -m $0))/build/mo/:$XDG_DATA_DIRS
PYTHONPATH=`dirname $0`:$PYTHONPATH `dirname $0`/bin/mandibule
