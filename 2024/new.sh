#! /usr/bin/env bash

day=$1
if [ $day -lt 10 ]; then day=0${day##*0}; fi
day=day${day}

mkdir ${day}
for f in template/*; do
    f=`basename ${f}`
    echo "cp template/$f ${day}/${day}${f##template}"
    cp template/$f ${day}/${day}${f##template}
done

# Replace 'template' with $day in src/${day}_*.py
sed -i "s/template/${day}/g" ${day}/${day}.py
sed -i "s/template/${day}/g" ${day}/${day}_test.py

# Replace 'Template' with capitalized $day in src/${day}_*.py
sed -i "s/Template/${day^}/g" ${day}/${day}.py
sed -i "s/Template/${day^}/g" ${day}/${day}_test.py