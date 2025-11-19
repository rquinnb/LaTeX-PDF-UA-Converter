#!/usr/bin/env python3
"""Test content tagging logic"""

import pikepdf
import re

def test_tagging():
    pdf = pikepdf.open('lecture1.pdf')
    page = pdf.pages[1]  # Page 2

    if '/Contents' in page:
        contents = page.Contents
        if isinstance(contents, pikepdf.Array):
            content_data = b''
            for stream in contents:
                content_data += stream.read_bytes()
        else:
            content_data = contents.read_bytes()

    content_str = content_data.decode('latin-1', errors='ignore')
    lines = content_str.split('\n')

    print(f"Total lines: {len(lines)}\n")

    current_font = None
    current_size = None

    text_count = 0
    for i, line in enumerate(lines[:200]):  # First 200 lines
        line_stripped = line.strip()

        # Track font changes
        font_match = re.match(r'/(\S+)\s+([\d.]+)\s+Tf', line_stripped)
        if font_match:
            current_font = font_match.group(1)
            current_size = float(font_match.group(2))
            print(f"Line {i}: Font set to {current_font} {current_size}pt")

        # Check if this line has text output
        has_text = re.search(r'\)\s*Tj\s*$', line_stripped) or re.search(r'\]\s*TJ\s*$', line_stripped)

        if has_text:
            text_count += 1
            print(f"Line {i}: TEXT FOUND (font={current_font}, size={current_size})")
            print(f"         Line content: {line_stripped[:100]}")
            if text_count >= 5:
                break

if __name__ == '__main__':
    test_tagging()
