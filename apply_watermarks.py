#!/usr/bin/python3

import glob
import os
import sys

import PyPDF2

watermarks_dir = './watermarks'
output_dir = './output'


def find_watermarks(watermarks_dir):
    fname_expr = os.path.join(watermarks_dir, '*.[Pp][Dd][Ff]')
    return glob.glob(fname_expr)


def add_watermark(input_file, watermark_file, output_file):
    """
    Apply the watermarks page by page. We apply the content on top of
    the watermark, because if we do it the other way, the watermark
    might hide stuff. Unfortunately, this means that the watermark
    gets modifed, and needs to be reloaded each time.
    """

    pdf_writer = PyPDF2.PdfFileWriter()

    with open(output_file, "wb") as filehandle_output:
        pdf = PyPDF2.PdfFileReader(input_file)
        for page_num in range(pdf.numPages):
            page = pdf.getPage(page_num)

            wpdf = PyPDF2.PdfFileReader(watermark_file)
            watermark = wpdf.getPage(0)
            page.mergePage(watermark)
            pdf_writer.addPage(page)

        pdf_writer.write(filehandle_output)


def main(input_file, watermarks_dir, output_dir):
    if not os.path.exists(input_file):
        print(f"""
            Error: file '{input_file}' was not found.
              """)
        quit(1)

    # Output file name is a combination of input and watermank file names
    prefix = os.path.basename(input_file)[:-4]
    for watermark_file in find_watermarks(watermarks_dir):
        print(watermark_file)
        suffix = os.path.basename(watermark_file)[:-4]
        output_file = os.path.join(output_dir, f'{prefix}_{suffix}.pdf')

        add_watermark(input_file, watermark_file, output_file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""
            Usage:
                apply_watermarks.py [pdf to be watermarked]
            """)
        quit(1)

    main(sys.argv[1], watermarks_dir, output_dir)
