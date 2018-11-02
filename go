#!/bin/bash

echo "assignment 5"  

python removeDuplicates.py

python assignment5.py

if [find . -name 'inferno.json' ]
	echo "found"
	mv inferno.json /infernoball/infernolevels
	mv nextLevel.json inferno.json
	ruby hashSplitter.rb inferno.json
fi





