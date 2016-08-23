#!/bin/bash
currentSeconds=$(date -j -f "%Y-%m-%d" $2 "+%s")
endSeconds=$(date -j -f "%Y-%m-%d" $3 "+%s")
offset=518400
increment=86400

# Downloads metadata using metadata.py in 1-week increments,
# starting at $2 and going to $3. Specify the organism name with $1
while [ "$currentSeconds" -le "$endSeconds" ]
do
  currentDateTs=$(date -j -f "%s" $currentSeconds "+%Y-%m-%d")
  nextSeconds=$(($currentSeconds+$offset))
  nextDateTs=$(date -j -f "%s" $nextSeconds "+%Y-%m-%d")
  metadata.py --name $1 --start $currentDateTs --end $nextDateTs --time 3.0
  currentSeconds=$(($nextSeconds+$increment))
done
