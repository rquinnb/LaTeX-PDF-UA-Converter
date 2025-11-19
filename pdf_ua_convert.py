#!/usr/bin/env python3
"""
PDF/UA Converter for LaTeX Documents

Converts LaTeX-generated PDFs to PDF/UA (Universal Accessibility) compliant format
by fixing missing ToUnicode mappings and adding proper structure tags.

Developed by: Ryan Black
Email: rquinnb@ksu.edu for issues
Version: 1.1 Alpha
Repository: https://github.com/rquinnb/LaTeX-PDF-UA-Converter
"""

__version__ = "1.1.0-alpha"
__repo_url__ = "https://github.com/rquinnb/LaTeX-PDF-UA-Converter"

import sys
import re
import argparse
import requests
from pathlib import Path
from pikepdf import Pdf, Dictionary, Name, Array, String, Stream
from bs4 import BeautifulSoup

try:
    from latex_glyph_symbols import LATEX_GLYPH_SYMBOLS as GLYPH_TO_SYMBOL
except ImportError:
    print("Error: latex_glyph_symbols.py not found in the same directory.")
    sys.exit(1)

def check_for_updates():
    """Check if a newer version is available on GitHub"""
    try:
        response = requests.get(
            "https://api.github.com/repos/rquinnb/LaTeX-PDF-UA-Converter/releases/latest",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get('tag_name', '').lstrip('v')
            current_version = __version__.replace('-alpha', '').replace('-beta', '')

            if latest_version and latest_version > current_version:
                print(f"\n  Update available: v{latest_version} (current: v{__version__})")
                print(f"  Download: {data.get('html_url', __repo_url__)}\n")
                return True
    except:
        pass  # Silently fail if GitHub is unreachable
    return False

def main():
    # Check for updates (non-blocking)
    check_for_updates()

    parser = argparse.ArgumentParser(
        description='Convert PDF(s) to PDF/UA compliant format',
        epilog='Examples:\n'
               '  %(prog)s file.pdf                          # Single file, output: file_ua.pdf\n'
               '  %(prog)s file.pdf -o output.pdf            # Single file, custom output name\n'
               '  %(prog)s input_dir/ -d output_dir/         # All PDFs in directory\n'
               '  %(prog)s input_dir/ -d output_dir/ -r      # Recursive with tree structure\n'
               '  %(prog)s "lecture*.pdf"                    # Wildcard matching\n'
               '  %(prog)s input_dir/ -p "output_{name}.pdf" # Custom naming pattern',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('input', help='Input PDF file, directory, or wildcard pattern (e.g., "*.pdf")')
    parser.add_argument('-o', '--output', help='Output PDF file (only for single file input)')
    parser.add_argument('-d', '--output-dir', default='ua_output',
                       help='Output directory for batch processing (default: ua_output)')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Process directories recursively, maintaining tree structure')
    parser.add_argument('-p', '--pattern', default='{stem}_ua{suffix}',
                       help='Output filename pattern. Use {stem} for basename, {suffix} for extension, {name} for full name (default: {stem}_ua{suffix})')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite existing output files without prompting')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be processed without actually converting')

    args = parser.parse_args()

    # Collect all PDF files to process
    pdf_files = []
    input_path = Path(args.input)

    # Check if input is a wildcard pattern
    if '*' in args.input or '?' in args.input:
        # Handle wildcard
        pdf_files = list(Path('.').glob(args.input))
        pdf_files = [f for f in pdf_files if f.is_file() and f.suffix.lower() == '.pdf']
        if not pdf_files:
            print(f"No PDF files found matching pattern: {args.input}")
            sys.exit(1)
    elif input_path.is_file():
        if args.output:
            output_file = args.output
        else:
            output_file = format_output_name(input_path, args.pattern, input_path.parent)

        if args.dry_run:
            print(f"Would convert: {input_path} -> {output_file}")
            return

        convert_pdf(str(input_path), str(output_file), verbose=args.verbose)
        return
    elif input_path.is_dir():
        # Directory mode
        if args.recursive:
            # Recursive: find all PDFs in tree
            pdf_files = list(input_path.rglob('*.pdf'))
        else:
            # Non-recursive: only direct children
            pdf_files = list(input_path.glob('*.pdf'))

        if not pdf_files:
            print(f"No PDF files found in: {input_path}")
            sys.exit(1)
    else:
        print(f"Error: Input not found: {args.input}")
        sys.exit(1)

    # Batch processing mode
    output_dir = Path(args.output_dir)

    print(f"Found {len(pdf_files)} PDF file(s) to process")

    if args.dry_run:
        print("\n=== DRY RUN - No files will be modified ===\n")

    for i, pdf_file in enumerate(pdf_files, 1):
        # Determine output path
        if args.recursive and input_path.is_dir():
            relative_path = pdf_file.relative_to(input_path)
            output_path = output_dir / relative_path.parent / format_output_name(pdf_file, args.pattern)
        else:
            output_path = output_dir / format_output_name(pdf_file, args.pattern)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists() and not args.overwrite:
            print(f"[{i}/{len(pdf_files)}] Skipping {pdf_file.name} (output exists)")
            continue

        if args.dry_run:
            print(f"[{i}/{len(pdf_files)}] Would convert: {pdf_file} -> {output_path}")
        else:
            print(f"[{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
            try:
                convert_pdf(str(pdf_file), str(output_path), verbose=args.verbose)
            except Exception as e:
                print(f"  ERROR: Failed to convert {pdf_file.name}: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()

    if not args.dry_run:
        print(f"\n=== Conversion complete ===")
        print(f"Output directory: {output_dir.absolute()}")

def format_output_name(input_path, pattern, output_dir=None):
    """Format output filename using pattern"""
    # Available placeholders: {stem}, {suffix}, {name}
    stem = input_path.stem
    suffix = input_path.suffix
    name = input_path.name

    output_name = pattern.format(stem=stem, suffix=suffix, name=name)

    if output_dir:
        return str(Path(output_dir) / output_name)
    else:
        return output_name

def lookup_unicode_online(symbol, verbose=False):
    """Look up Unicode value for symbol by querying fileformat.info"""
    try:
        import urllib.parse
        encoded = urllib.parse.quote(symbol)
        search_url = f"https://www.fileformat.info/info/unicode/char/search.htm?q={encoded}"

        response = requests.get(search_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            matches = re.findall(r'U\+([0-9A-Fa-f]{4,6})', text)
            if matches:
                return matches[0].upper()
    except Exception as e:
        if verbose:
            print(f"    Warning: Online lookup failed: {e}")

    return None

def fix_font_tounicode(pdf, font_obj, font_name, verbose=False):
    """Find glyphs defined in font but missing from ToUnicode CMap"""

    if '/ToUnicode' not in font_obj:
        return {}

    tounicode_stream = font_obj.ToUnicode
    tounicode_data = tounicode_stream.read_bytes().decode('latin-1', errors='ignore')

    existing_mappings = set()

    bfchar_blocks = re.findall(r'beginbfchar(.*?)endbfchar', tounicode_data, re.DOTALL)
    for block in bfchar_blocks:
        matches = re.findall(r'<([0-9A-Fa-f]{2,4})>\s*<([0-9A-Fa-f]+)>', block)
        for char_code_hex, unicode_hex in matches:
            existing_mappings.add(int(char_code_hex, 16))

    bfrange_blocks = re.findall(r'beginbfrange(.*?)endbfrange', tounicode_data, re.DOTALL)
    for block in bfrange_blocks:
        matches = re.findall(r'<([0-9A-Fa-f]{2,4})>\s*<([0-9A-Fa-f]{2,4})>\s*<([0-9A-Fa-f]+)>', block)
        for start_hex, end_hex, unicode_start_hex in matches:
            start = int(start_hex, 16)
            end = int(end_hex, 16)
            for code in range(start, end + 1):
                existing_mappings.add(code)

    font_encoding = {}
    if '/FontDescriptor' in font_obj and '/FontFile' in font_obj.FontDescriptor:
        try:
            font_stream = font_obj.FontDescriptor.FontFile
            font_data = font_stream.read_bytes()
            font_text = font_data.decode('latin-1', errors='ignore')
            encoding_matches = re.findall(r'dup\s+(\d+)\s+/(\S+)\s+put', font_text)
            for code_str, glyph_name in encoding_matches:
                font_encoding[int(code_str)] = glyph_name
        except:
            pass

    if verbose:
        print(f"    ToUnicode has {len(existing_mappings)} mappings")
        print(f"    Font defines {len(font_encoding)} glyphs")

    missing_codes = set(font_encoding.keys()) - existing_mappings

    if not missing_codes:
        if verbose:
            print(f"    All font glyphs have ToUnicode mappings!")
        return {}

    if verbose:
        print(f"    {len(missing_codes)} glyphs MISSING from ToUnicode!")

    new_mappings = {}

    for char_code in sorted(missing_codes):
        glyph_name = font_encoding[char_code]

        if verbose:
            print(f"    Missing: code 0x{char_code:02X} = /{glyph_name}")

        if glyph_name in GLYPH_TO_SYMBOL:
            symbol = GLYPH_TO_SYMBOL[glyph_name]
            if verbose:
                print(f"    Lookup table resolved /{glyph_name} to: U+{ord(symbol):04X}")

            unicode_hex = lookup_unicode_online(symbol, verbose)
            if unicode_hex:
                new_mappings[char_code] = unicode_hex
                if verbose:
                    print(f"    SUCCESS: U+{unicode_hex}")
            else:
                new_mappings[char_code] = f"{ord(symbol):04X}"
                if verbose:
                    print(f"    Using direct Unicode: U+{ord(symbol):04X}")
        else:
            if verbose:
                print(f"    Glyph /{glyph_name} not in lookup table - SKIPPED")

    return new_mappings

class ContentParser:
    """Parse PDF content streams to extract text with formatting info"""

    def __init__(self):
        self.text_blocks = []
        self.current_font = None
        self.current_size = None

    def parse(self, content_data):
        """Parse content stream and extract text blocks with font info"""
        content_str = content_data.decode('latin-1', errors='ignore')
        lines = content_str.split('\n')

        for line in lines:
            # Font selection: /F1 12 Tf
            font_match = re.match(r'/(\S+)\s+([\d.]+)\s+Tf', line.strip())
            if font_match:
                self.current_font = font_match.group(1)
                self.current_size = float(font_match.group(2))
                continue

            # Text showing operations
            if self.current_font and self.current_size:
                # Simple text: (text) Tj
                text_match = re.search(r'\(([^)]+)\)\s*Tj', line)
                if text_match:
                    text = text_match.group(1)
                    self.text_blocks.append({
                        'text': text,
                        'font': self.current_font,
                        'size': self.current_size
                    })
                    continue

                # Array text: [(text1) offset (text2) ...] TJ
                array_match = re.search(r'\[(.*?)\]\s*TJ', line)
                if array_match:
                    content = array_match.group(1)
                    texts = re.findall(r'\(([^)]+)\)', content)
                    if texts:
                        combined_text = ''.join(texts)
                        self.text_blocks.append({
                            'text': combined_text,
                            'font': self.current_font,
                            'size': self.current_size
                        })

        return self.text_blocks

def classify_text_element(font_size):
    """Classify text element based on font size"""
    if font_size >= 14:
        return 'H'  # Heading (H1 or H2)
    elif font_size >= 12:
        return 'H3'  # Subheading
    elif font_size >= 8:
        return 'P'  # Paragraph
    else:
        return 'Artifact'  # Footer, page numbers, etc.

def tag_content_with_structure(pdf, page, content_data, page_num, verbose=False):
    """Tag content with proper structure tags instead of artifacts"""

    parser = ContentParser()
    text_blocks = parser.parse(content_data)

    if verbose and text_blocks:
        print(f"    Found {len(text_blocks)} text blocks")

    # Build new content stream with marked content tags
    # Strategy: Wrap entire content blocks between text operations
    content_str = content_data.decode('latin-1', errors='ignore')
    lines = content_str.split('\n')

    # Track state
    current_font = None
    current_size = None
    current_tag = None
    current_mcid = None
    mcid_counter = 0
    struct_elements = []
    in_marked_content = False
    first_heading = True  # Track if we've seen the first heading

    new_content = bytearray()
    buffer = bytearray()  # Buffer content until we know what tag to use

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Track font changes (but don't continue - line might also have text)
        font_match = re.search(r'/(\S+)\s+([\d.]+)\s+Tf', line_stripped)
        if font_match:
            current_font = font_match.group(1)
            current_size = float(font_match.group(2))

        # Check if this line has text output
        has_text = re.search(r'\)\s*Tj\s*$', line_stripped) or re.search(r'\]\s*TJ\s*$', line_stripped)

        if has_text and current_font and current_size:
            # Classify this text block
            elem_type = classify_text_element(current_size)

            # Determine tag
            if elem_type == 'H':
                if first_heading:
                    tag = 'H1'  # First heading is H1
                    first_heading = False
                else:
                    tag = 'H1'  # All section headings are H1 in this document
            elif elem_type == 'H3':
                tag = 'H3'
            elif elem_type == 'P':
                tag = 'P'
            else:
                tag = 'Artifact'

            # If we're starting a new tag type or first content
            if tag != current_tag or not in_marked_content:
                # Close previous marked content if open
                if in_marked_content:
                    new_content += b'EMC\n'
                    in_marked_content = False

                # Start new marked content
                if tag != 'Artifact':
                    mcid = mcid_counter
                    mcid_counter += 1
                    current_mcid = mcid
                    current_tag = tag

                    new_content += f'/{tag} <</MCID {mcid}>> BDC\n'.encode('latin-1')
                    new_content += buffer
                    new_content += line.encode('latin-1') + b'\n'

                    struct_elements.append({
                        'type': tag,
                        'mcid': mcid,
                        'page': page
                    })
                    in_marked_content = True
                else:
                    # Artifact
                    new_content += b'/Artifact BMC\n'
                    new_content += buffer
                    new_content += line.encode('latin-1') + b'\n'
                    new_content += b'EMC\n'
                    current_tag = 'Artifact'
                    in_marked_content = False
            else:
                # Continue in same marked content
                new_content += buffer
                new_content += line.encode('latin-1') + b'\n'

            buffer = bytearray()
        else:
            # Non-text operation, add to buffer
            buffer += line.encode('latin-1') + b'\n'

    # Flush any remaining buffer
    if buffer:
        if in_marked_content:
            new_content += buffer
        else:
            # Wrap remaining content as artifact
            new_content += b'/Artifact BMC\n'
            new_content += buffer
            new_content += b'EMC\n'

    # Close any open marked content
    if in_marked_content:
        new_content += b'EMC\n'

    return bytes(new_content), struct_elements

def convert_pdf(input_file, output_file, verbose=False):
    if verbose:
        print(f"Opening {input_file}")
    pdf = Pdf.open(input_file)

    if verbose:
        print("Adding PDF/UA compliance structures")

    # Set MarkInfo in catalog
    pdf.Root.MarkInfo = Dictionary(Marked=True)

    # Set ViewerPreferences
    pdf.Root.ViewerPreferences = Dictionary(DisplayDocTitle=True)

    # Set language
    pdf.Root.Lang = String("en-US")

    # Get or create metadata
    title = "Document"
    if pdf.docinfo and pdf.docinfo.get('/Title'):
        title = str(pdf.docinfo['/Title'])

    # Set XMP metadata
    xmp = f'''<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about=""
        xmlns:pdfuaid="http://www.aiim.org/pdfua/ns/id/"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:pdf="http://ns.adobe.com/pdf/1.3/">
      <pdfuaid:part>1</pdfuaid:part>
      <dc:title>
        <rdf:Alt>
          <rdf:li xml:lang="x-default">{title}</rdf:li>
        </rdf:Alt>
      </dc:title>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''

    # Set XMP metadata directly
    metadata_stream = Stream(pdf, xmp.encode('utf-8'))
    metadata_stream.Type = Name.Metadata
    metadata_stream.Subtype = Name.XML
    pdf.Root.Metadata = metadata_stream

    if verbose:
        print("Checking for non-embedded fonts")

    # Check for non-embedded fonts (PDF/UA violation)
    non_embedded_fonts = []
    for page in pdf.pages:
        if '/Resources' in page and '/Font' in page.Resources:
            fonts = page.Resources.Font
            for font_name, font_obj in fonts.items():
                if '/BaseFont' in font_obj:
                    base_font = str(font_obj.BaseFont)
                    subtype = str(font_obj.get('/Subtype', 'Unknown'))

                    # Check if font is embedded
                    is_embedded = False
                    if '/FontDescriptor' in font_obj:
                        font_desc = font_obj.FontDescriptor
                        is_embedded = any(key in font_desc for key in ['/FontFile', '/FontFile2', '/FontFile3'])

                    if not is_embedded and subtype != '/Type3':  # Type3 fonts don't need embedding
                        if base_font not in non_embedded_fonts:
                            non_embedded_fonts.append(base_font)

    if non_embedded_fonts:
        print(f"\n  WARNING: PDF/UA VIOLATION DETECTED!")
        print(f"  The following fonts are NOT embedded:")
        for font in non_embedded_fonts:
            print(f"    - {font}")
        print(f"\n  PDF/UA requires ALL fonts to be embedded.")
        print(f"  This is an issue with the SOURCE PDF, not this converter.")
        print(f"  Please recreate the source PDF with embedded fonts.")
        print(f"\n  Continuing anyway, but output will NOT be PDF/UA compliant...\n")

    if verbose:
        print("Fixing font ToUnicode mappings")

    processed_fonts = set()
    total_fixed = 0

    for page in pdf.pages:
        if '/Resources' in page and '/Font' in page.Resources:
            fonts = page.Resources.Font
            for font_name, font_obj in fonts.items():
                if '/BaseFont' in font_obj:
                    font_id = str(font_obj.objgen)
                    if font_id in processed_fonts:
                        continue
                    processed_fonts.add(font_id)

                    if '/ToUnicode' in font_obj:
                        if verbose:
                            print(f"  Analyzing {font_obj.BaseFont} (resource name: {font_name})...")

                        new_mappings = fix_font_tounicode(pdf, font_obj, str(font_name).lstrip('/'), verbose)

                        if new_mappings:
                            tounicode_stream = font_obj.ToUnicode
                            tounicode_data = tounicode_stream.read_bytes().decode('latin-1', errors='ignore')

                            if 'beginbfchar' in tounicode_data:
                                insert_pos = tounicode_data.rfind('endbfchar')
                                if insert_pos != -1:
                                    count_match = re.search(r'(\d+)\s+beginbfchar', tounicode_data)
                                    if count_match:
                                        old_count = int(count_match.group(1))
                                        new_count = old_count + len(new_mappings)
                                        tounicode_data = re.sub(
                                            r'(\d+)(\s+beginbfchar)',
                                            f'{new_count}\\2',
                                            tounicode_data,
                                            count=1
                                        )

                                    new_entries = '\n'.join([f'<{code:02X}> <{uni}>' for code, uni in sorted(new_mappings.items())]) + '\n'
                                    tounicode_data = tounicode_data[:insert_pos] + new_entries + tounicode_data[insert_pos:]

                            new_stream = Stream(pdf, tounicode_data.encode('latin-1'))
                            new_stream.Type = Name.CMap
                            font_obj.ToUnicode = new_stream
                            total_fixed += len(new_mappings)
                            if verbose:
                                print(f"    Added {len(new_mappings)} missing mappings to ToUnicode")

    if total_fixed > 0 and not verbose:
        print(f"  Fixed {total_fixed} missing glyph mappings")

    if verbose:
        print("Creating document structure with headings and paragraphs")

    # Create structure elements for content and links
    all_struct_elems = []
    parent_tree_by_page = {}  # Map StructParents value -> list of struct elems by MCID

    for page_num, page in enumerate(pdf.pages):
        if verbose:
            print(f"  Processing page {page_num + 1}/{len(pdf.pages)}")

        if '/Annots' in page:
            page.Tabs = Name.S

        # Tag content with structure
        if '/Contents' in page:
            contents = page.Contents

            # Read existing content
            if isinstance(contents, Array):
                content_data = b''
                for content_stream in contents:
                    content_data += content_stream.read_bytes()
            else:
                content_data = contents.read_bytes()

            # Tag content with proper structure
            new_content, struct_elements = tag_content_with_structure(
                pdf, page, content_data, page_num, verbose
            )

            # Update page content
            page.Contents = Stream(pdf, new_content)

            # Set StructParents on page for marked content
            if struct_elements:
                page.StructParents = page_num

                # Track structure elements by MCID for this page
                if page_num not in parent_tree_by_page:
                    parent_tree_by_page[page_num] = {}

                # Create structure elements for each marked content
                for elem_info in struct_elements:
                    struct_elem = Dictionary(
                        Type=Name.StructElem,
                        S=Name('/' + elem_info['type']),
                        P=None,  # Will be set later
                        K=elem_info['mcid'],
                        Pg=page.obj,
                        Lang=String("en-US")
                    )
                    struct_elem_ref = pdf.make_indirect(struct_elem)
                    all_struct_elems.append(struct_elem_ref)

                    # Add to parent tree structure by MCID
                    parent_tree_by_page[page_num][elem_info['mcid']] = struct_elem_ref

        # Tag link annotations
        if '/Annots' in page:
            for annot_idx, annot in enumerate(page.Annots):
                if annot.get('/Subtype') == Name.Link:
                    # Add Contents key for alternate description
                    annot.Contents = String("Link")

                    # Set StructParent on annotation (use high number to avoid collision with page StructParents)
                    struct_parent_val = 10000 + (page_num * 100) + annot_idx
                    annot.StructParent = struct_parent_val

                    # Create structure element for link
                    link_struct = Dictionary(
                        Type=Name.StructElem,
                        S=Name.Link,
                        P=None,
                        K=Dictionary(
                            Type=Name.OBJR,
                            Obj=annot,
                            Pg=page.obj
                        ),
                        Lang=String("en-US")
                    )
                    link_struct_ref = pdf.make_indirect(link_struct)
                    all_struct_elems.append(link_struct_ref)

                    # Add to parent tree (links use scalar StructParent, not array)
                    if struct_parent_val not in parent_tree_by_page:
                        parent_tree_by_page[struct_parent_val] = link_struct_ref

    # Build ParentTree Nums array
    parent_tree_nums = []
    for key in sorted(parent_tree_by_page.keys()):
        value = parent_tree_by_page[key]

        # Check if this is a Python dict (marked content by MCID) or a PDF object (link)
        if isinstance(value, dict) and not isinstance(value, (Dictionary, Array)):
            # Page with marked content: build array indexed by MCID
            max_mcid = max(value.keys()) if value else 0
            mcid_array = Array([None] * (max_mcid + 1))
            for mcid, struct_elem in value.items():
                mcid_array[mcid] = struct_elem
            parent_tree_nums.extend([key, mcid_array])
        else:
            # Annotation with scalar StructParent (single struct element)
            parent_tree_nums.extend([key, value])

    # Create structure tree root
    if all_struct_elems:
        # Create a Document container element (required for PDF/UA)
        document_elem = Dictionary(
            Type=Name.StructElem,
            S=Name.Document,
            P=None,  # Will be set to StructTreeRoot
            K=Array(all_struct_elems),
            Lang=String("en-US")
        )
        document_elem_ref = pdf.make_indirect(document_elem)

        # Create StructTreeRoot with Document as sole child
        struct_tree_root = Dictionary(
            Type=Name.StructTreeRoot,
            K=document_elem_ref,
            ParentTree=Dictionary(
                Nums=Array(parent_tree_nums)
            )
        )

        # Make structure tree root indirect and set parent references
        struct_tree_root_ref = pdf.make_indirect(struct_tree_root)
        document_elem.P = struct_tree_root_ref  # Document's parent is StructTreeRoot

        # All other elements' parent is now Document
        for struct_elem in all_struct_elems:
            struct_elem.P = document_elem_ref

        pdf.Root.StructTreeRoot = struct_tree_root_ref
    else:
        # Create empty structure tree
        struct_tree_root = Dictionary(
            Type=Name.StructTreeRoot,
            K=Array([]),
            ParentTree=Dictionary(
                Nums=Array([])
            )
        )
        pdf.Root.StructTreeRoot = pdf.make_indirect(struct_tree_root)

    if not pdf.docinfo:
        pdf.docinfo = Dictionary()

    pdf.docinfo['/Title'] = String(title)
    pdf.docinfo['/Producer'] = String('PDF/UA Converter')

    if verbose:
        print(f"Saving to {output_file}")
    pdf.save(output_file)
    pdf.close()

    print(f"  Created: {output_file}")
    if verbose:
        print(f"  Processed {len(pdf.pages)} pages")
        print(f"  Created {len(all_struct_elems)} structure elements")

if __name__ == "__main__":
    main()