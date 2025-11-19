#!/usr/bin/env python3
"""Check if link annotation on page 0 is properly tagged"""

import pikepdf

pdf = pikepdf.open('lecture1_ua.pdf')

# Get page 0
page = pdf.pages[0]

print("=== Page 0 Analysis ===\n")

# Check if page has StructParents
if '/StructParents' in page:
    print(f"Page StructParents: {page.StructParents}")
else:
    print("Page has no StructParents (expected for title page)")

# Check annotations
if '/Annots' in page:
    print(f"\nPage has {len(page.Annots)} annotation(s)")

    for i, annot in enumerate(page.Annots):
        if annot.get('/Subtype') == pikepdf.Name.Link:
            print(f"\nLink annotation {i}:")
            if '/StructParent' in annot:
                sp = annot.StructParent
                print(f"  StructParent: {sp}")

                # Look up in ParentTree
                if '/StructTreeRoot' in pdf.Root:
                    struct_tree = pdf.Root.StructTreeRoot
                    if '/ParentTree' in struct_tree:
                        parent_tree = struct_tree.ParentTree
                        if '/Nums' in parent_tree:
                            nums = parent_tree.Nums

                            # Find the StructParent value
                            for j in range(0, len(nums), 2):
                                if j+1 < len(nums) and nums[j] == sp:
                                    struct_elem = nums[j+1]
                                    print(f"  Found in ParentTree:")

                                    # Check if it has /S key (structure element)
                                    if hasattr(struct_elem, 'get') and '/S' in struct_elem:
                                        elem_type = struct_elem.get('/S', 'unknown')
                                        print(f"    Type: Structure Element")
                                        print(f"    S (standard type): {elem_type}")

                                        # Check the P (parent)
                                        if '/P' in struct_elem:
                                            p = struct_elem.P
                                            if hasattr(p, 'get') and '/Type' in p:
                                                p_type = p.Type
                                                print(f"    P (parent) Type: {p_type}")
                                            else:
                                                print(f"    P (parent): {p}")
                                        else:
                                            print(f"    ERROR: No /P (parent) key!")

                                        # Check the K (kids)
                                        if '/K' in struct_elem:
                                            k = struct_elem.K
                                            if hasattr(k, 'get') and '/Type' in k:
                                                k_type = k.Type
                                                print(f"    K Type: {k_type}")
                                                if k_type == pikepdf.Name.OBJR:
                                                    print(f"    K is OBJR (object reference) - CORRECT!")
                                    else:
                                        print(f"    Type: Array or other (len={len(struct_elem)})")
                                    break
            else:
                print(f"  ERROR: No StructParent!")
else:
    print("\nPage has no annotations")
