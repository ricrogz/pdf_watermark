#!/bin/bash

set -euo pipefail

data_file='watermarks.csv'
watermarks_dir='./watermarks'


function trim_whitespace() {
    sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' <<<"$1"
}

function create_watermark() {

convert \
    -density 144 \
    -size 1190x1684 xc:transparent \
    -fill black \
    -pointsize 35 -weight 800 \
    -gravity center \
    -annotate -55,-55,20,50 "$1\n$2" \
    miff:- | \
composite \
    -dissolve '30%' - \
    -size 1190x1684 xc:transparent \
    -page A4 \
    -compress Zip \
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