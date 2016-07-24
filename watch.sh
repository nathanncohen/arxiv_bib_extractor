#!/bin/bash

block_size=10
function batchfind () {
    find "$*" -type f | tr '\n' ' ' | perl -ape "s/(([^ ]* ){0,$block_size})/\1\t/g" | tr '\t' '\n' | grep -E "."
}

# Recomputes 'all_parsed' whenever parse_entry gets modified
while [ 1 ]; do
    find parse_entry -newer all_parsed | grep "" > /dev/null || inotifywait -e MODIFY parse_entry tags/*
    date
    echo "Parsing begins"
    batchfind "arxiv/4-bibs/" | while read i; do
	echo "cat $i | ./parse_entry";
    done | parallel > all_parsed
done
