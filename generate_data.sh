#!/bin/bash 

if [[ $1 != "-c" ]]; then
for file in apartment/*; do
    python3 parsing.py $file
done;
fi

cp -r apartment/*/daily* parsed-data/
cp -r apartment/*/total* parsed-data/
