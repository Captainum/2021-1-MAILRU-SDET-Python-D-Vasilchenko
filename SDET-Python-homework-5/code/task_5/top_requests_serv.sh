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

echo -e "Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой:\n" > $OUTPUT
cat $INPUT | awk '{print $1, $9}' | grep '5[0-9][0-9]' | awk '{print $1}' | sort | uniq -c | sort -k1,1rn | awk 'NR==1, NR==5 {print $2 "\n" $1 "\n"}' >> $OUTPUT