#!/bin/bash

mkdir -p data/gutenberg

for id in $(seq 2001 10000); do
	output="data/gutenberg/$id.txt"

	echo "Downloading book $id..."

	if wget -q -w 2 \
		-O "$output" \
		"https://www.gutenberg.org/cache/epub/$id/pg$id.txt"; then

		if [ -s "$output" ]; then
			echo "	OK"
		else
			echo "	Not text -- removing"
			rm "$output"
		fi

	else
		echo "	Download failed"
		rm -f "$output"
	fi
done
