#!/bin/bash

# detect if on mac os
OS=$(uname -s)
if [ "$OS" != "Darwin" ]; then
    echo "This script is only for Mac OS"
    exit 1
fi

if [ ! -f ./credentials.txt ]; then
    echo "create a credentials.txt file with your mongoDB srv"
    exit 1
fi


if [[ "$1" == "s"* ]]; then
    # check if file exists
    if [ ! -f ./font_size ]; then
        ORIGINAL_SIZE=$(osascript -e 'tell application "Terminal" to font size of window 1')
        echo $ORIGINAL_SIZE > ./font_size
    fi

fi
# save current font size to file

# Save current font size
if [[ $1 == "i" ]]; then
    osascript -e 'tell application "Terminal" to set font size of window 1 to ((font size of window 1) + 4)'
fi


# Reset font size to original
if [[ "$1" == "q" ]]; then
    # clean up after yourself.
    echo "- cleaning up..."
    original_size=$(cat ./font_size)
    osascript -e "tell application \"Terminal\" to set font size of window 1 to $original_size"
    ORIGINAL_SIZE=$(osascript -e 'tell application "Terminal" to font size of window 1')
    rm ./font_size
    pgrep -f "plantOperator.py" | xargs kill -9
    reset

fi
