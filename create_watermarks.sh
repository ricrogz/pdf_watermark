#!/bin/bash

set -euo pipefail

data_file='watermarks.csv'
watermarks_dir='./watermarks'


function trim_whitespace() {
    sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' <<<"$1"
}

function create_watermark() {

convert \
    -density 300 \
    -size 1550x600 \
    -pointsize 20 \
    -fill black -background transparent \
    -gravity northwest caption:"\n\n\n$1" \
    -gravity southeast -draw "text 100,0 \"$2\"" \
    -rotate -52  -resample '80%' \
    -compress Zip \
    miff:- | \
composite \
    -geometry +200+200 \
    -tile  -dissolve '30%' - \
    -size 1190x1684 xc:transparent \
    -page A4 \
    "$3/$2.pdf"
}

function main() {

    while IFS=, read -r field1 field2
    do
        echo "${field1}, ${field2}"
        field1=$(trim_whitespace "$field1")
        field2=$(trim_whitespace "$field2")
        create_watermark "$field1" "$field2" $2
    done < "$1"

}

main $data_file $watermarks_dir