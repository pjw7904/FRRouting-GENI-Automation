#!/bin/bash

record=""

while read line
do
        if [[ $line =~ eth[0-9]+:[[:space:]]Link[[:space:]] ]]; then
                record=$line
        fi
done <<< $(sudo tail -n 200 /var/log/syslog)

echo "Record found: $record"

timing=$(echo $record | cut -d " " -f 1-2)

echo "Timestamp: $timing"

epochStamp=$(date -d "$timing" +"%s.%4N")

echo "Epoch timestamp: $epochStamp"