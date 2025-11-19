#!/usr/bin/env python3
"""Debug PDF structure tree and parent tree"""

import pikepdf
import sys

def debug_structure(pdf_path):
    pdf = pikepdf.open(pdf_path)

    print(f"=== Analyzing: {pdf_path} ===\n")

    # Check structure tree and parent tree
    if '/StructTreeRoot' in pdf.Root:
        struct_tree = pdf.Root.StructTreeRoot

        print("StructTreeRoot found")

        if '/K' in struct_tree:
            kids = struct_tree.K
            print(f"Total structure elements: {len(kids)}\n")

            # Show first few elements
            print("First 5 structure elements:")
            for i in range(min(5, len(kids))):
                elem = kids[i]
                elem_type = str(elem.get('/S', 'unknown')).lstrip('/')
                mcid = elem.get('/K', 'none')
                pg = elem.get('/Pg', 'none')
                print(f"  [{i}] Type={elem_type}, K={mcid}, Pg={pg}")

        # Check ParentTree structure
        if '/ParentTree' in struct_tree:
            parent_tree = struct_tree.ParentTree
            if '/Nums' in parent_tree:
                nums = parent_tree.Nums
                print(f"\nParentTree Nums array length: {len(nums)}")
                print(f"First 10 entries: {nums[:10]}")

    # Check first page's StructParents
    if len(pdf.pages) > 0:
        page = pdf.pages[0]
        if '/StructParents' in page:
            print(f"\nPage 1 StructParents: {page.StructParents}")
        else:
            print("\nPage 1 has no StructParents")

if __name__ == '__main__':
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else 'lecture1_ua.pdf'
    debug_structure(pdf_path)
