#! /usr/bin/env fish
# source me to set up a new advent of code day
# abbreviated to `advent` (run from any directory)
set advent_dir /home/kevin/gits/advent-of-code-2020
cd $advent_dir
# tomorrow's date (run this before midnight PST)
set day ( date --date="tomorrow" +%e )
set year ( date +%Y )
echo "https://adventofcode.com/$year/"
if test -d $day
    echo "folder $day exists. did not overwrite"
    echo "cd $day"
    cd $day
    cdv . # activate virtualenv
    exit 0
end
mkdir $day
cp boilerplate.py $day/run.py
echo "cd to new directory $day"
cd $day
cdv . # activate virtualenv
touch input.txt
