#!/bin/sh

INCLUDE="$1"
DEFINES="$2"
SRC="$3"
SA_OP="$4"

SA=cppcheck
#SA=splint

if [ -e $SA_OP.sa ]
then
  mv $SA_OP.sa $SA_OP.sa.bkp
fi

if [ $SA = "cppcheck" ]
then
    $SA --enable=all $INCLUDE $DEFINES $SRC 1> $SA_OP.sa 2>&1
else
    $SA +posixlib +skip_sys_headers $DEFINES -I/usr/include/x86_64-linux-gnu/ $INCLUDE $SRC 1> $SA_OP.sa 2>&1
fi

if [ -e $SA_OP.sa.bkp ]
then
  diff $SA_OP.sa $SA_OP.sa.bkp >> $CURR_DIR/output/logs/sa_op.log
fi
