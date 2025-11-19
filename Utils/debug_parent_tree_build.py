#!/usr/bin/env python3
"""Debug ParentTree building logic"""

import pikepdf
from pikepdf import Dictionary, Array

# Simulate what happens in the code
parent_tree_by_page = {}

# Page 0 marked content
parent_tree_by_page[0] = {0: 'elem1', 1: 'elem2', 2: 'elem3'}

# Page 0 link annotation
pdf = pikepdf.open('lecture1.pdf')
dummy_dict = Dictionary(Type=pikepdf.Name.StructElem, S=pikepdf.Name.Link)
link_struct_ref = pdf.make_indirect(dummy_dict)
parent_tree_by_page[10000] = link_struct_ref

print("Testing isinstance checks:")
for key, value in parent_tree_by_page.items():
    print(f"\nKey {key}:")
    print(f"  type(value): {type(value)}")
    print(f"  isinstance(value, dict): {isinstance(value, dict)}")
    print(f"  isinstance(value, Dictionary): {isinstance(value, Dictionary)}")
    print(f"  isinstance(value, (Dictionary, Array)): {isinstance(value, (Dictionary, Array))}")
    print(f"  Check: isinstance(value, dict) and not isinstance(value, (Dictionary, Array)): {isinstance(value, dict) and not isinstance(value, (Dictionary, Array))}")
