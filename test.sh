#!/bin/bash

# TESTING WHETHER COMMANDS EXIST

if [ -z $(command -v ffmpeg) ]; then
		echo "ffmpeg not found."
elif [ -z $(command -v ffprobe) ]; then
		echo "ffprobe not found."
else
		echo "Packages found."
fi

if [ $(python -c 'import bullet'; echo $?) = 1 ]; then
		echo "Python Module 'bullet' not found"
else
		echo "Python Module Requirements Met."
fi
