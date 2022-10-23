#!/usr/bin/env python3

import glob
import os
import sys

import ghostscript
import PyPDF2

watermarks_dir = './watermarks'
output_dir = './output'
temp_dir = '/tmp/pdf_watermark'


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


def flatten(input_file, output_file):
    args = [
        "gs", "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/default", "-dNOPAUSE",
        "-dQUIET", "-dBATCH", f"-sOutputFile={output_file}", input_file
    ]

    with open(os.devnull, 'wb') as fnull:
        ghostscript.Ghostscript(*args, stderr=fnull)


def main(input_file, watermarks_dir, output_dir):
    if not os.path.exists(input_file):
        print(f"""
            Error: file '{input_file}' was not found.
              """)
        quit(1)

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    # Output file name is a combination of input and watermank file names
    prefix = os.path.basename(input_file)[:-4]
    for watermark_file in find_watermarks(watermarks_dir):
        print(watermark_file)
        suffix = os.path.basename(watermark_file)[:-4]
        temp_file = os.path.join(temp_dir, f'{prefix}_{suffix}.pdf')
        output_file = os.path.join(output_dir, f'{prefix}_{suffix}.pdf')
        add_watermark(input_file, watermark_file, temp_file)
        flatten(temp_file, output_file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""
            Usage:
                apply_watermarks.py [pdf to be watermarked]
            """)
        quit(1)

    main(sys.argv[1], watermarks_dir, output_dir)
