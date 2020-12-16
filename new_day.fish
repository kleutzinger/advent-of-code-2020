#! /usr/bin/env fish
# source me to set up a new advent of code day
# abbreviated to `advent` (run from any directory)
set advent_dir /home/kevin/gits/advent-of-code-2020
cd $advent_dir
set -x TZ "America/New_York" # -x sets environment variables
set day (date +%e) # 2 digit day of month 
if test -d $day
    echo "folder $day exists."
    echo "cd $day"
    cd $day
    cdv . # activate virtualenv
    exit 0
end
mkdir $day
cp boilerplate.py $day/run.py
cd $day
cdv . # activate virtualenv
touch input.txt
