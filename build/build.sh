#!/bin/sh

SCRIPTS_PATH=$(cd "`dirname "$0"`"; pwd)
python "$SCRIPTS_PATH/build.py" $*
