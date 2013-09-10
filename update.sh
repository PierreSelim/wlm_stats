#!/bin/sh

rm -f files.txt
wget http://toolserver.org/~emijrp/wlm/files.txt
python aggregation.py > wlmfr13.csv
python generate_data.py