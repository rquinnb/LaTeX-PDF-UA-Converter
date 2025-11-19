#!/usr/bin/env python3
"""Verify PDF structure tags"""

import pikepdf
import sys

def verify_structure(pdf_path):
    pdf = pikepdf.open(pdf_path)

    print(f"Analyzing: {pdf_path}\n")

    # Check if document is marked
    if '/MarkInfo' in pdf.Root and pdf.Root.MarkInfo.get('/Marked'):
        print("[OK] Document is marked as tagged")
    else:
        print("[FAIL] Document is NOT marked as tagged")

    # Check structure tree
    if '/StructTreeRoot' in pdf.Root:
        struct_tree = pdf.Root.StructTreeRoot
        print("[OK] Structure tree exists")

        if '/K' in struct_tree:
            kids = struct_tree.K
            if isinstance(kids, pikepdf.Array):
                print(f"  Total structure elements: {len(kids)}")

                # Count element types
                elem_types = {}
                for elem in kids:
                    if '/S' in elem:
                        elem_type = str(elem.S).lstrip('/')
                        elem_types[elem_type] = elem_types.get(elem_type, 0) + 1

                print("\n  Structure element types:")
                for elem_type, count in sorted(elem_types.items()):
                    print(f"    {elem_type}: {count}")

    else:
        print("[FAIL] No structure tree found")

    # Check a sample page for marked content
    if len(pdf.pages) > 1:
        print(f"\n[OK] Checking page 2 content stream...")
        page = pdf.pages[1]  # Page 2 has more typical content

        if '/Contents' in page:
            contents = page.Contents
            if isinstance(contents, pikepdf.Array):
                content_data = b''
                for stream in contents:
                    content_data += stream.read_bytes()
            else:
                content_data = contents.read_bytes()

            content_str = content_data.decode('latin-1', errors='ignore')

            # Count BDC tags (marked content begin)
            h1_count = content_str.count('/H1 <</MCID')
            h2_count = content_str.count('/H2 <</MCID')
            h3_count = content_str.count('/H3 <</MCID')
            p_count = content_str.count('/P <</MCID')
            artifact_count = content_str.count('/Artifact BMC')

            print(f"  H1 tags: {h1_count}")
            print(f"  H2 tags: {h2_count}")
            print(f"  H3 tags: {h3_count}")
            print(f"  P tags: {p_count}")
            print(f"  Artifact tags: {artifact_count}")

            if h1_count > 0 or h2_count > 0 or p_count > 0:
                print(f"\n[OK] Content is properly tagged with structure!")
            else:
                print(f"\n[WARNING] No H1/H2 or P tags found - content may be hidden")

if __name__ == '__main__':
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else 'lecture1_ua_test.pdf'
    verify_structure(pdf_path)
