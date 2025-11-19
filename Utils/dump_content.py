#!/usr/bin/env python3
"""Dump PDF content stream for debugging"""

import pikepdf
import sys

def dump_content(pdf_path, page_num=1):
    pdf = pikepdf.open(pdf_path)
    page = pdf.pages[page_num]

    print(f"=== Page {page_num + 1} Content Stream ===\n")

    if '/Contents' in page:
        contents = page.Contents
        if isinstance(contents, pikepdf.Array):
            content_data = b''
            for stream in contents:
                content_data += stream.read_bytes()
        else:
            content_data = contents.read_bytes()

        content_str = content_data.decode('latin-1', errors='ignore')

        # Print first 3000 characters
        print(content_str[:3000])
        print("\n... (truncated)")

if __name__ == '__main__':
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else 'lecture1_ua_fixed.pdf'
    page_num = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    dump_content(pdf_path, page_num)
