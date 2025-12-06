#! /usr/bin/env bash
# Usage: ./new.sh [year] [day]
# If year or day is not provided, use the last year and next day.

set -euo pipefail
cd $(dirname "$0")

last_year=$(find . -type d -name '20*' | sort | tail -n 1 | cut -c3-)
last_day=$(ls ${last_year} | grep '^day' | sort | tail -n 1 | cut -c4-)

year=${1:-$last_year}
day=${2:-$((${last_day}+1))}

if [ $year -lt 2015]; then
    echo "Bad year: $year"
    exit 1
fi

day=$((day))
dayn=day$(printf "%02d" $day)
subdir=${year}/${dayn}

echo "Creating day $day, year $year"

mkdir -p ${subdir}
for f in template/*; do
    f=`basename ${f}`
    echo "cp template/$f ${subdir}/${dayn}${f##template}"
    cp template/$f ${subdir}/${dayn}${f##template}
done

# Replace 'DAYN' with DAY## in src/${dayn}_*.py
sed -i "s/DAYN/${dayn}/g" ${subdir}/${dayn}.py
sed -i "s/DAYN/${dayn}/g" ${subdir}/${dayn}_test.py

# Replace 'DAY' with day number
sed -i "s/DAY/${day}/g" ${subdir}/${dayn}.py
sed -i "s/DAY/${day}/g" ${subdir}/${dayn}_test.py

# Replace 'YEAR' with $year
sed -i "s/YEAR/${year}/g" ${subdir}/${dayn}.py
sed -i "s/YEAR/${year}/g" ${subdir}/${dayn}_test.py

# Try to download input data
if [ -f .session ]; then
    URL=https://adventofcode.com/$year/day/$day/input
    wget --header="Cookie: session=$(cat .session)" -O ${subdir}/${dayn}.dat $URL
fi
