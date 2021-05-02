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

echo 'Общее количество запросов по типу:' > $OUTPUT
cat $INPUT | awk '{print $6}' | sort | uniq -c | sort -k1,1rn | awk '{print $2 " - " $1}' | sed 's/"//' >> $OUTPUT