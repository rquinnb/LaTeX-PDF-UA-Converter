#!/usr/bin/env python3
"""Check specific ParentTree key"""

import pikepdf

pdf = pikepdf.open('lecture1_ua.pdf')

if '/StructTreeRoot' in pdf.Root:
    struct_tree = pdf.Root.StructTreeRoot

    if '/ParentTree' in struct_tree:
        parent_tree = struct_tree.ParentTree
        if '/Nums' in parent_tree:
            nums = parent_tree.Nums

            # Find key 10000
            for i in range(0, len(nums), 2):
                if i+1 < len(nums):
                    key = nums[i]
                    value = nums[i+1]

                    if key == 10000:
                        print(f"Found key 10000:")
                        try:
                            length = len(value)
                            print(f"  Type: Array with {length} elements")
                            for j, elem in enumerate(value[:3]):
                                if elem is not None:
                                    elem_type = elem.get('/S', 'unknown') if hasattr(elem, 'get') else str(elem)
                                    print(f"    [{j}]: {elem_type}")
                                else:
                                    print(f"    [{j}]: None")
                        except:
                            elem_type = value.get('/S', 'unknown') if hasattr(value, 'get') else 'unknown'
                            print(f"  Type: Single element")
                            print(f"  S (type): {elem_type}")
                        break
