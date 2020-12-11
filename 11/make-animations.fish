#!/usr/bin/env fish
# after running run.py, combine the frames into two gifs
# only use every other frame, because there's a strobing effect
# requires imagemagick and fish shell
set first  day_11_part_1.gif
set second day_11_part_2.gif

echo "combining to $first"
convert -delay 5 -loop 0 (ls pt1_frames/*.png | sed -n 0~2p) $first
echo "combining to $second"
convert -delay 5 -loop 0 (ls pt2_frames/*.png | sed -n 0~2p) $second
