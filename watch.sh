#!/bin/bash

# Recomputes 'all_parsed' whenever parse_entry gets modified
while [ 1 ]; do
    find parse_entry -newer all_parsed | grep "" > /dev/null || inotifywait -e MODIFY parse_entry
    date
    for i in arxiv/4-bibs/*; do
	echo "cat \"$i\" | ./parse_entry";
    done | parallel > all_parsed
done
