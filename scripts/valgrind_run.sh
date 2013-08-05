#!/bin/sh

BIN_SUT=$1
RES_OP=$2

if [ -z $RES_OP ]
then
    RES_OP=$CURR_DIR/output/logs/valgrind.da
fi

echo "Valgrind started `date`" >$RES_OP

valgrind -v --leak-check=full --show-reachable=yes $BIN_SUT 1>>$RES_OP 2>&1

echo "Valgrind done" >>$RES_OP
echo "exiting.."
