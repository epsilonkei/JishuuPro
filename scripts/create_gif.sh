#!/usr/bin/env bash
# $1 is target gif_file name

ffmpeg -framerate 5 -i PazuSolver/out2/Map%d.jpg $1
