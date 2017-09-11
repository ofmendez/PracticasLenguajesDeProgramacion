#!/bin/bash

# for i in $(find ./test -name  "in*"); do # Not recommended, will break on whitespace
#     entrada=${i##*/}
#     salidaEsp='out'${i##*/in}
#     python p1.py < "$i"
#     diffs=$( comm -3  <(sort ./test/$salidaEsp) <(sort out.txt) )
#     if [[ $diffs ]]; then
#         printf   "************* DIF EN $entrada :  \n\n"
#         comm -3  <(sort ./test/$salidaEsp) <(sort out.txt) 
#         printf "\n********************.....\n"
#     else
#         echo "### $entrada ## PASS"
#     fi
# done
printf "\n  _MAIN_ \n"
python p1.py < ./in.in
cat out.txt