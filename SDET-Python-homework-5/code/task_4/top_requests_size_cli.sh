#!/bin/bash

usage() {
    echo -e "usage:\t$0 <inputfile> <outputfile>"
    echo -e "\t-h: open this window"
}

if [ "$#" -ne 1 ] && [ "$#" -ne 2 ];
then
    usage
    exit 1
fi

if [[ "$#" -eq 1 ]] && [[ "$1" == -h ]];
then
    usage
    exit 0
elif [[ "$#" -ne 2 ]];
then
    usage
    exit 1
fi

INPUT=$1
OUTPUT=$2

echo -e 'Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой:\n' > $OUTPUT
cat $INPUT | awk '{print $7, $9, $10, $1}' | grep ' 4[0-9][0-9] ' | sort -k3,3rn | awk 'NR==1, NR==5 {print $1 "\n" $2 "\n" $3 "\n" $4 "\n"}' >> $OUTPUT