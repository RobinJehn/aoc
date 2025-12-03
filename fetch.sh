#!/bin/bash

# Usage: ./fetch.sh year [day]

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Check if SESSION variable is set
if [ -z "$SESSION" ]; then
    echo "Error: SESSION variable not set. Aborting."
    exit 1
fi

# Function to download input for a given day
download_day() {
    YEAR=$1
    DAY=$(printf "%02d" $2)  # Pad day with leading zero
    URL="https://adventofcode.com/$YEAR/day/${DAY#0}/input"  # Remove leading zero for URL
    DIR="$YEAR/inputs"
    FILE="$DIR/day_$DAY.txt"

    # Check if the required directories exist, create if not
    if [ ! -d "$DIR" ]; then
        mkdir -p "$DIR"
    fi

    if curl -s -b "session=$SESSION" "$URL" --output "$FILE"; then
        echo "Downloaded $YEAR Day ${DAY#0} to $FILE"
    else
        echo "Failed $YEAR Day ${DAY#0}"
    fi
}

# Download data for all days or a single day
if [ -z "$2" ]; then
    for DAY in {1..25}; do
        download_day $1 $DAY
    done
else
    download_day $1 $2
fi
