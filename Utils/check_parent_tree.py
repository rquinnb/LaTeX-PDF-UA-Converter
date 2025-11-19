#!/usr/bin/env python3
"""Check ParentTree structure"""

import pikepdf

pdf = pikepdf.open('lecture1_ua.pdf')

if '/StructTreeRoot' in pdf.Root:
    struct_tree = pdf.Root.StructTreeRoot

    if '/ParentTree' in struct_tree:
        parent_tree = struct_tree.ParentTree
        if '/Nums' in parent_tree:
            nums = parent_tree.Nums
            print(f"ParentTree Nums array length: {len(nums)}")
            print("\nStructure of ParentTree:")

            # The Nums array is a flat list: [key1, value1, key2, value2, ...]
            print("First 5 entries:")
            for i in range(0, min(10, len(nums)), 2):
                if i+1 < len(nums):
                    key = nums[i]
                    value = nums[i+1]

                    try:
                        # Try to get length - if it works, it's an array-like object
                        length = len(value)
                        print(f"  Key {key}: Array with {length} elements")
                    except:
                        # Single object, likely a struct elem
                        elem_type = value.get('/S', 'unknown') if hasattr(value, 'get') else 'unknown'
                        print(f"  Key {key}: Single element ({elem_type})")

            print("\nLast 5 entries:")
            for i in range(max(0, len(nums)-10), len(nums), 2):
                if i+1 < len(nums):
                    key = nums[i]
                    value = nums[i+1]

                    try:
                        # Try to get length - if it works, it's an array-like object
                        length = len(value)
                        print(f"  Key {key}: Array with {length} elements")
                    except:
                        # Single object, likely a struct elem
                        elem_type = value.get('/S', 'unknown') if hasattr(value, 'get') else 'unknown'
                        print(f"  Key {key}: Single element ({elem_type})")
