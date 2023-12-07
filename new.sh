#! /usr/bin/env bash

day=$1
if [ $day -lt 10 ]
then
    day=0${day}
fi
day=day${day}

touch data/${day}.txt
echo foo > test_data/${day}.txt
cp src/template.py src/${day}.py
cp src/template_test.py src/${day}_test.py

# Replace 'template' with $day in src/${day}_*.py
sed -i "s/template/${day}/g" src/${day}.py
sed -i "s/template/${day}/g" src/${day}_test.py

# Replace 'Template' with capitalized $day in src/${day}_*.py
sed -i "s/Template/${day^}/g" src/${day}.py
sed -i "s/Template/${day^}/g" src/${day}_test.py