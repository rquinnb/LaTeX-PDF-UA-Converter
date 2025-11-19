#!/usr/bin/env python3
"""Analyze PDF content structure to identify headings"""

import pikepdf
import re
import sys

def analyze_pdf(pdf_path):
    pdf = pikepdf.open(pdf_path)

    for page_num, page in enumerate(pdf.pages[:3], 1):  # First 3 pages
        print(f"\n{'='*80}")
        print(f"PAGE {page_num}")
        print('='*80)

        # Get fonts used on this page
        if '/Resources' in page and '/Font' in page.Resources:
            print("\nFONTS:")
            for font_name, font_obj in page.Resources.Font.items():
                base_font = font_obj.get('/BaseFont', 'Unknown')
                print(f"  {font_name}: {base_font}")

        # Parse content stream
        if '/Contents' in page:
            contents = page.Contents
            if isinstance(contents, pikepdf.Array):
                content_data = b''
                for stream in contents:
                    content_data += stream.read_bytes()
            else:
                content_data = contents.read_bytes()

            content_str = content_data.decode('latin-1', errors='ignore')

            print("\nCONTENT OPERATIONS:")

            # Track current font and size
            current_font = None
            current_size = None

            lines = content_str.split('\n')
            for line in lines:
                # Font selection: /F1 12 Tf
                font_match = re.match(r'/(\S+)\s+([\d.]+)\s+Tf', line)
                if font_match:
                    current_font = font_match.group(1)
                    current_size = float(font_match.group(2))
                    print(f"\n  [FONT: {current_font}, SIZE: {current_size}]")

                # Text showing: (text) Tj or [(text)] TJ
                text_match = re.search(r'\(([^)]+)\)\s*Tj', line)
                if text_match and current_font:
                    text = text_match.group(1)
                    print(f"    \"{text}\" [{current_font} {current_size}pt]")

                # Array text: [(text) offset ...] TJ
                array_match = re.search(r'\[(.*?)\]\s*TJ', line)
                if array_match and current_font:
                    content = array_match.group(1)
                    # Extract text parts (in parentheses)
                    texts = re.findall(r'\(([^)]+)\)', content)
                    if texts:
                        combined = ''.join(texts)
                        print(f"    \"{combined}\" [{current_font} {current_size}pt]")

if __name__ == '__main__':
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else 'lecture1.pdf'
    analyze_pdf(pdf_path)
