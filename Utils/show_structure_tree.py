#!/usr/bin/env python3
"""Show structure tree hierarchy"""

import pikepdf

pdf = pikepdf.open('lecture1_ua.pdf')

if '/StructTreeRoot' in pdf.Root:
    struct_tree = pdf.Root.StructTreeRoot
    if '/K' in struct_tree:
        root_kid = struct_tree.K

        # Check if K is a single element or array
        if hasattr(root_kid, 'get') and '/S' in root_kid:
            # Single element (should be Document)
            print(f"StructTreeRoot/K: {root_kid.S}\n")

            if '/K' in root_kid:
                kids = root_kid.K
                print(f"Document has {len(kids)} children:\n")

                for i in range(min(10, len(kids))):
                    elem = kids[i]
                    if hasattr(elem, 'get'):
                        elem_type = elem.get('/S', 'unknown')
                        k_val = elem.get('/K', 'none')

                        # Simplify K display
                        if hasattr(k_val, 'get') and '/Type' in k_val:
                            k_display = f"OBJR (annotation)"
                        elif isinstance(k_val, int):
                            k_display = f"MCID {k_val}"
                        else:
                            k_display = str(type(k_val).__name__)

                        print(f"  [{i}] {elem_type} (K={k_display})")
        else:
            print("StructTreeRoot/K is an array (old flat structure)")
