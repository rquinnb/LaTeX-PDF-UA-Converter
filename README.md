# PDF/UA Converter for LaTeX Documents

Converts LaTeX-generated PDFs to PDF/UA (Universal Accessibility) compliant format by fixing missing ToUnicode mappings and adding proper structure tags with semantic headings.

**Developed by:** Ryan Black
**Email:** rquinnb@ksu.edu
**Version:** 1.1 Alpha
**Repository:** https://github.com/rquinnb/LaTeX-PDF-UA-Converter

## What is PDF/UA?

PDF/UA (ISO 14289) is the international standard for accessible PDFs. It ensures that:
- Screen readers can properly interpret document content
- Document structure (headings, paragraphs, lists) is preserved
- All text has proper Unicode mappings for copy/paste and search
- Images and non-text elements have alternative descriptions

This tool specifically addresses LaTeX-generated PDFs, which often have:
- Missing ToUnicode mappings for math symbols
- No semantic structure tags (headings vs paragraphs)
- Improperly tagged or untagged content

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Install

1. Clone or download this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

### Manual Install
If you prefer to install packages individually:
```bash
pip install pikepdf requests beautifulsoup4
```

## Usage

### Basic Usage

**Convert a single PDF:**
```bash
python pdf_ua_convert.py input.pdf -o output.pdf
```

**Convert with default naming (adds _ua suffix):**
```bash
python pdf_ua_convert.py input.pdf
# Creates: input_ua.pdf
```

### Batch Processing

**Convert all PDFs in a directory:**
```bash
python pdf_ua_convert.py input_dir/ -d output_dir/
```

**Recursive directory processing:**
```bash
python pdf_ua_convert.py input_dir/ -d output_dir/ -r
```

**Wildcard matching:**
```bash
python pdf_ua_convert.py "lecture*.pdf"
```

**Custom output naming pattern:**
```bash
python pdf_ua_convert.py input_dir/ -p "{stem}_accessible{suffix}"
# lecture1.pdf -> lecture1_accessible.pdf
```

### Advanced Options

**Verbose output (detailed progress):**
```bash
python pdf_ua_convert.py input.pdf -v
```

**Overwrite existing files:**
```bash
python pdf_ua_convert.py input.pdf --overwrite
```

**Dry run (preview without converting):**
```bash
python pdf_ua_convert.py input_dir/ --dry-run
```

**See all options:**
```bash
python pdf_ua_convert.py --help
```

## How It Works

### 1. Font Analysis & Unicode Mapping
- Scans all fonts in the PDF for defined glyphs
- Identifies glyphs missing from ToUnicode CMap
- Uses comprehensive lookup table (245+ symbols) to map glyph names to Unicode
- Adds missing mappings to ensure proper text extraction and screen reader support

### 2. Structure Tagging
- Analyzes text by font size to identify headings vs body text
- Creates proper PDF structure tree with semantic tags:
  - **H1** - Main headings (14pt+)
  - **H2/H3** - Subheadings (12-14pt)
  - **P** - Paragraphs (body text)
  - **Link** - Hyperlinks
- Tags all content with Marked Content IDs (MCIDs)
- Marks decorative elements (page numbers, footers) as artifacts

### 3. PDF/UA Compliance
- Sets document as "Tagged" (MarkInfo/Marked = true)
- Creates Document container element for proper hierarchy
- Builds ParentTree to link marked content to structure elements
- Adds XMP metadata with PDF/UA identifier
- Sets viewer preferences (DisplayDocTitle = true)
- Validates that all fonts are embedded

## Supported Fonts

The lookup table includes 245+ symbols from:
- **Adobe Glyph List (AGL)** - Standard PostScript glyphs
- **Computer Modern fonts:**
  - CMEX10 - Extensible symbols (brackets, summation, integrals)
  - CMSY10 - Math symbols (arrows, operators)
  - CMMI10 - Math italic
  - CMR10 - Roman
  - CMSS10/12 - Sans serif
- **AMS fonts:**
  - MSBM10 - Negated binary relations (amssymb)
  - MSAM10 - Binary operators and relations
- **stmary10** - St Mary Road symbols
- **Greek letters** (uppercase and lowercase)
- **Math operators** (±, ×, ÷, ∑, ∏, ∫)
- **Set theory** (∈, ⊂, ⊃, ∩, ∪, ∅)
- **Logic** (∀, ∃, ¬, ∧, ∨)
- **Arrows** (→, ⇒, ↔, ↦)

## Files

### Core Files
- **pdf_ua_convert.py** - Main conversion script
- **latex_glyph_symbols.py** - Glyph name → Unicode symbol lookup table
- **requirements.txt** - Python package dependencies

### Utility Scripts (`Util/` folder)
Debugging and verification tools:
- **verify_structure.py** - Check PDF structure tree and tags
- **analyze_pdf_structure.py** - Analyze font usage and content
- **check_parent_tree.py** - Verify ParentTree structure
- **dump_content.py** - Display PDF content streams
- **show_structure_tree.py** - Display structure hierarchy

## Customizing Symbol Mappings

To add or modify a symbol mapping, edit `latex_glyph_symbols.py`:

```python
LATEX_GLYPH_SYMBOLS = {
    'alpha': 'α',  # U+03B1 (\alpha)
    'summationdisplay': '∑',  # U+2211 (\sum in display mode)
    'yourglyphname': '★',  # U+2605 (\star)
}
```

1. Find the glyph name from verbose output
2. Add/edit entry with Unicode symbol
3. Include LaTeX command in comment for reference

## Output Modes

### Default (non-verbose)
```
[1/5] Processing: lecture1.pdf
  Fixed 5 missing glyph mappings
  Created: ua_output/lecture1_ua.pdf
```

### Verbose mode (`-v`)
```
Opening lecture1.pdf
Adding PDF/UA compliance structures
Checking for non-embedded fonts
Fixing font ToUnicode mappings
  Analyzing /IPMRCZ+CMEX10 (resource name: /F60)...
    ToUnicode has 33 mappings
    Font defines 9 glyphs
    5 glyphs MISSING from ToUnicode!
    Missing: code 0x02 = /bracketleftbig
    Lookup table resolved /bracketleftbig to: U+27E6
    SUCCESS: U+27E6
    Added 5 missing mappings to ToUnicode
Creating document structure with headings and paragraphs
  Processing page 1/13
  Processing page 2/13
  ...
Saving to lecture1_ua.pdf
  Created: lecture1_ua.pdf
  Processed 13 pages
  Created 42 structure elements
```

## Troubleshooting

### "Font not embedded" warning
```
WARNING: PDF/UA VIOLATION DETECTED!
The following fonts are NOT embedded:
  - /Helvetica

PDF/UA requires ALL fonts to be embedded.
This is an issue with the SOURCE PDF, not this converter.
```

**Solution:** Recreate the source PDF with embedded fonts. LaTeX typically embeds fonts by default. This warning usually appears for PDFs created by non-LaTeX tools using "Base 14" standard fonts.

### Missing glyph not in lookup table
If verbose output shows:
```
Glyph /yourglyphname not in lookup table - SKIPPED
```

**Solution:** Add the glyph to `latex_glyph_symbols.py`:
1. Find the Unicode value for the symbol
2. Add entry: `'yourglyphname': 'symbol',  # U+XXXX`

### Import error: latex_glyph_symbols not found
**Solution:** Ensure `latex_glyph_symbols.py` is in the same directory as `pdf_ua_convert.py`

### PDF still fails accessibility check
1. Run with `-v` to see detailed processing
2. Use verification tool: `python Util/verify_structure.py output.pdf`
3. Check that source PDF has all fonts embedded
4. Verify no images without alt text (tool marks as artifacts)

## Features

✅ **Automatic ToUnicode fixing** - Resolves missing character mappings
✅ **Semantic structure tags** - H1/H2/H3/P tags based on font size
✅ **Proper heading hierarchy** - H1 as first heading, proper nesting
✅ **Link tagging** - Hyperlinks properly tagged and nested
✅ **Document container** - Required Document element for PDF/UA
✅ **ParentTree creation** - Links marked content to structure tree
✅ **Artifact marking** - Page numbers and footers marked as decorative
✅ **Batch processing** - Convert multiple PDFs at once
✅ **Non-embedded font detection** - Warns about source PDF issues
✅ **Automatic update checking** - Notifies when new version available

## Version History

### 1.1 Alpha (Current)
- Added semantic structure tagging (H1, H2, H3, P)
- Implemented proper document hierarchy with Document container
- Fixed ParentTree structure for MCID resolution
- Added non-embedded font detection and warnings
- Integrated automatic GitHub version checking
- Moved utility scripts to Util/ folder

### 1.0
- Initial release
- ToUnicode mapping fixes
- Basic PDF/UA metadata

## License

Developed for educational accessibility purposes at Kansas State University.

## Contributing

Issues, bug reports, and feature requests: https://github.com/rquinnb/LaTeX-PDF-UA-Converter/issues

## Credits

Developed by Ryan Black (rquinnb@ksu.edu) to improve accessibility of LaTeX-generated course materials and academic documents.
