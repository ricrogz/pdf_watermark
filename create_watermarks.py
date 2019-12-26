#!/usr/bin/python

import csv
import os

import fpdf

font_sz = 60.0
box_h = 35.0
font_color = 160

data_file = 'watermarks.csv'
watermarks_dir = './watermarks'


def create_watermark(watermark_text, watermark_file):
    """
    Create a pdf with a single page with the watermark.
    Hardcoded values may be updated for different effects.
    """
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_margins(0, 0, 0)
    pdf.set_auto_page_break(False)
    pdf.set_xy(1, 255)
    pdf.set_font('arial', 'B', font_sz)
    pdf.set_text_color(font_color)
    pdf.rotate(56)
    pdf.multi_cell(w=290.0,
                   h=box_h,
                   txt=watermark_text,
                   align='C',
                   border=False)

    pdf.output(watermark_file, 'F')


def transform_data(row):
    """
    Apply transformations to the data in the csv file.
    Modify this to fit your needs.
    """
    return row[0].title(), row[1].upper()


def main(data_file, watermarks_dir):
    with open(data_file) as f:
        for row in csv.reader(f, delimiter=',', skipinitialspace=True):
            if len(row) != 2:
                continue

            first, second = transform_data(row)

            # The second line will be user as output file name
            watermark_filename = f'{second}.pdf'

            watermark_path = os.path.join(watermarks_dir, watermark_filename)
            create_watermark(f'{first}\n{second}', watermark_path)


if __name__ == '__main__':
    main(data_file, watermarks_dir)
