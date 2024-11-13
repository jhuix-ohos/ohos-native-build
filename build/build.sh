#!/bin/sh

SCRIPTS_PATH=$(cd "`dirname "$0"`"; pwd)
export PYTHONDONTWRITEBYTECODE=1
python "$SCRIPTS_PATH/build.py" $*
