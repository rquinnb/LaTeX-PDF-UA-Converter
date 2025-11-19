# PDF/UA Converter for LaTeX Documents

Converts LaTeX-generated PDFs to PDF/UA (Universal Accessibility) compliant format by fixing missing ToUnicode mappings and adding proper structure tags.

**Developed by:** Ryan Black
**Email:** rquinnb@ksu.edu for issues

## Files

### Core Files
- **pdf_ua_convert.py** - Main conversion script
- **latex_glyph_symbols.py** - Glyph name → Unicode symbol lookup table (245 mappings with LaTeX commands)

### Reference Files (optional)
- **LaTeX All Symbol/** - Test files and LaTeX symbol references
- **extracted_pfas/** - Extracted PostScript font files

## Usage

### Convert a single PDF
```bash
python pdf_ua_convert.py input.pdf -o output.pdf
```

### Batch convert all PDFs in a directory
```bash
python pdf_ua_convert.py input_dir/ -d output_dir/
```

### Batch convert with wildcard
```bash
python pdf_ua_convert.py "lecture*.pdf"
```

### Verbose output (detailed progress)
```bash
python pdf_ua_convert.py input.pdf -o output.pdf -v
```

### All options
```bash
python pdf_ua_convert.py --help
```

## How It Works

1. **Analyzes fonts** - Scans all fonts in the PDF for glyphs defined in font encoding
2. **Identifies missing mappings** - Finds glyphs missing from ToUnicode CMap
3. **Resolves symbols** - Uses comprehensive lookup table to map glyph names to Unicode
4. **Adds ToUnicode entries** - Inserts missing mappings into font's ToUnicode CMap
5. **Adds PDF/UA structure** - Creates structure tree, marks content, and adds metadata

## Supported Fonts

The lookup table includes 245 symbols from:
- **Adobe Glyph List (AGL)** - Standard PostScript glyphs
- **LaTeX math fonts:**
  - CMEX10 - Brackets, summation, integrals, products
  - CMSY10 - Arrows, binary operators
  - CMMI10 - Math italic
  - MSBM10 - AMS negated binary relations (amssymb)
  - MSAM10 - AMS symbols
  - stmary10 - St Mary Road symbols

## Customizing Symbol Mappings

To add or modify a symbol mapping, edit `latex_glyph_symbols.py`:

1. Find the glyph name (e.g., "alpha", "summationdisplay")
2. Add/edit the entry with the Unicode symbol
3. Include the LaTeX command in the comment

Example:
```python
'alpha': 'α',  # U+03B1 (\alpha)
'summationdisplay': '∑',  # U+2211 (\sum in display mode)
```

## Output Modes

**Default (non-verbose):**
- Shows progress for batch processing
- Reports number of glyphs fixed
- Displays output file location

**Verbose mode (`-v`):**
- Shows detailed font analysis
- Displays each missing glyph and resolution
- Shows page-by-page processing

## Requirements

```bash
pip install pikepdf requests beautifulsoup4
```

## Example Output

**Non-verbose:**
```
[1/5] Processing: lecture1.pdf
  Fixed 5 missing glyph mappings
  Created: ua_output/lecture1_ua.pdf
```

**Verbose:**
```
[1/5] Processing: lecture1.pdf
Opening lecture1.pdf
Adding PDF/UA compliance structures
Fixing font ToUnicode mappings
  Analyzing /IPMRCZ+CMEX10 (resource name: /F60)...
    ToUnicode has 33 mappings
    Font defines 9 glyphs
    5 glyphs MISSING from ToUnicode!
    Missing: code 0x02 = /bracketleftbig
    Lookup table resolved /bracketleftbig to: U+27E6
    SUCCESS: U+27E6
    ...
    Added 5 missing mappings to ToUnicode
```
