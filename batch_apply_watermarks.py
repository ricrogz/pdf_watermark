#!/usr/bin/env python3

from apply_watermarks import find_watermarks
from apply_watermarks import add_watermark
from apply_watermarks import flatten

from apply_watermarks import output_dir
from apply_watermarks import temp_dir as root_temp_dir
from apply_watermarks import watermarks_dir

import os
import sys


def read_batch_input(batch_file):
    """
    Find the file that defines the inputs and reads the names of the
    .pdf files that should be watermarked. Files are checked to exist!
    """
    if not os.path.exists(batch_file):
        print(f"\nError: batch input file '{batch_file}' was not found.\n")
        quit(1)

    pdf_files = set()
    with open(batch_file) as f:
        for i, line in enumerate(f, 1):
            pdf_file = line.strip()
            if pdf_file:
                if os.path.exists(pdf_file):
                    pdf_files.add(pdf_file)
                else:
                    print(f"\nError: pdf file '{pdf_file}' at line {i} in"
                          f" '{batch_file}' was not found.\n")
                    quit(1)
    return pdf_files


def main(batch_file, output_dir):
    pdf_files = sorted(read_batch_input(batch_file))
    watermarks = sorted(find_watermarks(watermarks_dir))

    print("Applying watermarks:")
    for watermark_file in watermarks:
        print(f"\t{watermark_file}")
    print("to pdf files:")
    for pdf_file in pdf_files:
        print(f"\t{pdf_file}")
    print("")

    # Output file name is a combination of pdf input and watermark file names
    for watermark_file in watermarks:
        suffix = os.path.basename(watermark_file)[:-4]
        tgt_dir = os.path.join(output_dir, suffix)
        temp_dir = os.path.join(root_temp_dir, suffix)
        os.makedirs(tgt_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        for pdf_file in pdf_files:
            prefix = os.path.basename(pdf_file)[:-4]
            output_file = f'{prefix}_{suffix}.pdf'
            output_path = os.path.join(tgt_dir, output_file)
            temp_path = os.path.join(temp_dir, output_file)
            add_watermark(pdf_file, watermark_file, temp_path)
            flatten(temp_path, output_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""
            Usage:
                batch_apply_watermarks.py [input batch file]
            """)
        quit(1)

    main(sys.argv[1], output_dir)
