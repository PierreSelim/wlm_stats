#!/bin/sh

wget -O files-2014.txt http://tools.wmflabs.org/wlm-stats/files-2014.txt
python aggregation.py > wlmfr14.csv
python generate_data.py
