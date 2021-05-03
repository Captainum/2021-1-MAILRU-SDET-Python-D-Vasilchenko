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

echo "Топ 10 самых частых запросов:" > $OUTPUT
cat $INPUT | awk '{print $7}' | sort | uniq -c | sort -k1,1rn | awk 'NR==1,NR==10 {print "\n" $2 "\n" $1}' >> $OUTPUT