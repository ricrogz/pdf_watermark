# pdf_watermark
A very simple tool to create and apply watermarks to pdf files using python

# Usage

1. Add the watermarks to the data file (`watermarks.csv` by default). Each watermark should be in a separate line and consist of exactly two fields separated by a comma. Lines with other than 2 fields will be skipped.
2. Run the `create_watermarks.py` script. This will create the watermark pdfs in the `watermarks` directory. By default, watermark files will be named using the second field in the data file.
3. Use `apply_watermarks.py [pdf to be watermarked]` to apply the watermarks. The watermark directory will be scanned for watermarks, and each of them will be used to generate a new watermarked copy of the input file, which will be placed inside the `output` directory.

The two scripts are independent, so that watermarks can be added/replaced manually before application.

The watermark data can be programatically modified before writing the watermark file. See the `transform_data()` function in the creation script.


