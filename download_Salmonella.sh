#!/bin/bash
currentSeconds=$(date -j -f "%Y-%m-%d" $1 "+%s")
endSeconds=$(date -j -f "%Y-%m-%d" $2 "+%s")
offset=518400
increment=86400

# Downloads Salmonella metadata using metadata.py in 1-week increments,
# starting at $1 and going to $2
while [ "$currentSeconds" -le "$endSeconds" ]
do
  currentDateTs=$(date -j -f "%s" $currentSeconds "+%Y-%m-%d")
  nextSeconds=$(($currentSeconds+$offset))
  nextDateTs=$(date -j -f "%s" $nextSeconds "+%Y-%m-%d")
  metadata.py --name Salmonella --start $currentDateTs --end $nextDateTs --time 3.0
  currentSeconds=$(($nextSeconds+$increment))
  sleep 3.0
done
