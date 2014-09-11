#!/bin/sh

wget -O files-2014.txt http://tools.wmflabs.org/wlm-stats/files-2014.txt
python aggregation.py --csv files-2014.txt > wlmfr14.csv
python generate_data.py
