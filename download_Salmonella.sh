#!/bin/bash
currentSeconds=$(date -j -f "%Y-%m-%d" $1 "+%s")
endSeconds=$(date -j -f "%Y-%m-%d" $2 "+%s")
offset=604800

while [ "$currentSeconds" -le "$endSeconds" ]
do
  currentDateTs=$(date -j -f "%s" $currentSeconds "+%Y-%m-%d")
  nextSeconds=$(($currentSeconds+$offset))
  nextDateTs=$(date -j -f "%s" $nextSeconds "+%Y-%m-%d")
  python metadata.py --name Salmonella --start $currentDateTs --end $nextDateTs --time 1.0
  currentSeconds=$nextSeconds
  sleep 5
done
