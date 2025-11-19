r"""
LaTeX Glyph Name to Unicode Symbol Mappings

This lookup table maps PostScript glyph names to their corresponding Unicode symbols.
Combines Adobe Glyph List (AGL) standard mappings with LaTeX-specific math symbols.

To add or modify a mapping:
1. Find the glyph name (e.g., "alpha", "summationdisplay")
2. Add/edit the entry with the Unicode symbol
3. Include the LaTeX command in the comment for reference

Format: 'glyphname': 'symbol',  # U+XXXX DESCRIPTION (\latexcommand)
"""

LATEX_GLYPH_SYMBOLS = {
    # Basic Latin
    'A': 'A',  # U+0041
    'B': 'B',  # U+0042
    'C': 'C',  # U+0043
    'E': 'E',  # U+0045
    'F': 'F',  # U+0046
    'H': 'H',  # U+0048
    'I': 'I',  # U+0049
    'K': 'K',  # U+004B
    'L': 'L',  # U+004C
    'M': 'M',  # U+004D
    'O': 'O',  # U+004F
    'P': 'P',  # U+0050
    'Q': 'Q',  # U+0051
    'R': 'R',  # U+0052
    'S': 'S',  # U+0053
    'T': 'T',  # U+0054
    'U': 'U',  # U+0055
    'Z': 'Z',  # U+005A
    'a': 'a',  # U+0061
    'b': 'b',  # U+0062
    'c': 'c',  # U+0063
    'd': 'd',  # U+0064
    'e': 'e',  # U+0065
    'f': 'f',  # U+0066
    'g': 'g',  # U+0067
    'h': 'h',  # U+0068
    'i': 'i',  # U+0069
    'j': 'j',  # U+006A
    'k': 'k',  # U+006B
    'l': 'l',  # U+006C
    'm': 'm',  # U+006D
    'n': 'n',  # U+006E
    'o': 'o',  # U+006F
    'p': 'p',  # U+0070
    'q': 'q',  # U+0071
    'r': 'r',  # U+0072
    's': 's',  # U+0073
    't': 't',  # U+0074
    'u': 'u',  # U+0075
    'v': 'v',  # U+0076
    'w': 'w',  # U+0077
    'x': 'x',  # U+0078
    'y': 'y',  # U+0079
    'z': 'z',  # U+007A

    # Numbers
    'zero': '0',  # U+0030
    'one': '1',  # U+0031
    'two': '2',  # U+0032
    'three': '3',  # U+0033
    'four': '4',  # U+0034
    'five': '5',  # U+0035
    'six': '6',  # U+0036
    'seven': '7',  # U+0037
    'eight': '8',  # U+0038
    'nine': '9',  # U+0039

    # Basic symbols
    'exclam': '!',  # U+0021
    'numbersign': '#',  # U+0023
    'parenleft': '(',  # U+0028
    'parenright': ')',  # U+0029
    'plus': '+',  # U+002B
    'comma': ',',  # U+002C
    'period': '.',  # U+002E
    'slash': '/',  # U+002F
    'colon': ':',  # U+003A
    'equal': '=',  # U+003D
    'less': '<',  # U+003C
    'greater': '>',  # U+003E
    'bracketleft': '[',  # U+005B
    'backslash': '\\',  # U+005C
    'bracketright': ']',  # U+005D
    'braceleft': '{',  # U+007B
    'bar': '|',  # U+007C
    'braceright': '}',  # U+007D

    # Greek letters - uppercase
    'Delta': '∆',  # U+2206 (\Delta)
    'Gamma': 'Γ',  # U+0393 (\Gamma)
    'Lambda': 'Λ',  # U+039B (\Lambda)
    'Omega': 'Ω',  # U+2126 (\Omega)
    'Phi': 'Φ',  # U+03A6 (\Phi)
    'Pi': 'Π',  # U+03A0 (\Pi)
    'Psi': 'Ψ',  # U+03A8 (\Psi)
    'Sigma': 'Σ',  # U+03A3 (\Sigma)
    'Theta': 'Θ',  # U+0398 (\Theta)
    'Upsilon': 'Υ',  # U+03A5 (\Upsilon)
    'Xi': 'Ξ',  # U+039E (\Xi)

    # Greek letters - lowercase
    'alpha': 'α',  # U+03B1 (\alpha)
    'beta': 'β',  # U+03B2 (\beta)
    'chi': 'χ',  # U+03C7 (\chi)
    'delta': 'δ',  # U+03B4 (\delta)
    'epsilon': 'ε',  # U+03B5 (\epsilon)
    'eta': 'η',  # U+03B7 (\eta)
    'gamma': 'γ',  # U+03B3 (\gamma)
    'iota': 'ι',  # U+03B9 (\iota)
    'kappa': 'κ',  # U+03BA (\kappa)
    'lambda': 'λ',  # U+03BB (\lambda)
    'mu': 'µ',  # U+00B5 (\mu)
    'nu': 'ν',  # U+03BD (\nu)
    'omega': 'ω',  # U+03C9 (\omega)
    'phi': 'φ',  # U+03C6 (\phi)
    'phi1': 'ϕ',  # U+03D5 (\varphi)
    'pi': 'π',  # U+03C0 (\pi)
    'psi': 'ψ',  # U+03C8 (\psi)
    'rho': 'ρ',  # U+03C1 (\rho)
    'sigma': 'σ',  # U+03C3 (\sigma)
    'sigma1': 'ς',  # U+03C2 (\varsigma)
    'tau': 'τ',  # U+03C4 (\tau)
    'theta': 'θ',  # U+03B8 (\theta)
    'theta1': 'ϑ',  # U+03D1 (\vartheta)
    'upsilon': 'υ',  # U+03C5 (\upsilon)
    'xi': 'ξ',  # U+03BE (\xi)
    'zeta': 'ζ',  # U+03B6 (\zeta)

    # Hebrew letters
    'aleph': 'ℵ',  # U+2135 (\aleph)
    'gimel': 'ג',  # U+05D2 (\gimel)

    # Math operators
    'plus': '+',  # U+002B
    'minus': '−',  # U+2212
    'multiply': '×',  # U+00D7 (\times)
    'divide': '÷',  # U+00F7 (\div)
    'plusminus': '±',  # U+00B1 (\pm)
    'minusplus': '∓',  # U+2213 (\mp)
    'asteriskmath': '∗',  # U+2217 (\ast)
    'periodcentered': '·',  # U+00B7 (\cdot)

    # Relations
    'lessequal': '≤',  # U+2264 (\leq)
    'greaterequal': '≥',  # U+2265 (\geq)
    'notequal': '≠',  # U+2260 (\neq)
    'equivalence': '≡',  # U+2261 (\equiv)
    'approxequal': '≈',  # U+2248 (\approx)
    'similar': '∼',  # U+223C (\sim)
    'proportional': '∝',  # U+221D (\propto)
    'muchless': '≪',  # U+226A (\ll)
    'muchgreater': '≫',  # U+226B (\gg)
    'notless': '≮',  # U+226E (\nless)
    'notgreater': '≯',  # U+226F (\ngtr)
    'precedes': '≺',  # U+227A (\prec)
    'notprecedes': '⊀',  # U+2280 (\nprec)

    # Set theory
    'element': '∈',  # U+2208 (\in)
    'propersubset': '⊂',  # U+2282 (\subset)
    'propersuperset': '⊃',  # U+2283 (\supset)
    'reflexsubset': '⊆',  # U+2286 (\subseteq)
    'reflexsuperset': '⊇',  # U+2287 (\supseteq)
    'intersection': '∩',  # U+2229 (\cap)
    'union': '∪',  # U+222A (\cup)
    'emptyset': '∅',  # U+2205 (\emptyset)

    # Logic
    'universal': '∀',  # U+2200 (\forall)
    'existential': '∃',  # U+2203 (\exists)
    'logicalnot': '¬',  # U+00AC (\neg)
    'logicaland': '∧',  # U+2227 (\land)
    'logicalor': '∨',  # U+2228 (\lor)

    # Arrows
    'arrowleft': '←',  # U+2190 (\leftarrow)
    'arrowright': '→',  # U+2192 (\rightarrow)
    'arrowup': '↑',  # U+2191 (\uparrow)
    'arrowdown': '↓',  # U+2193 (\downarrow)
    'arrowdblleft': '⇐',  # U+21D0 (\Leftarrow)
    'arrowdblright': '⇒',  # U+21D2 (\Rightarrow)
    'arrowdblup': '⇑',  # U+21D1 (\Uparrow)
    'arrowdbldown': '⇓',  # U+21D3 (\Downarrow)
    'arrowdblboth': '⇔',  # U+21D4 (\Leftrightarrow)
    'mapsto': '↦',  # U+21A6 (\mapsto)

    # Circled operators
    'circleplus': '⊕',  # U+2295 (\oplus)
    'circlemultiply': '⊗',  # U+2297 (\otimes)
    'openbullet': '◦',  # U+25E6 (\circ)

    # Other symbols
    'infinity': '∞',  # U+221E (\infty)
    'partialdiff': '∂',  # U+2202 (\partial)
    'nabla': '∇',  # U+2207 (\nabla)
    'angle': '∠',  # U+2220 (\angle)
    'perpendicular': '⊥',  # U+22A5 (\perp)
    'bullet': '•',  # U+2022 (\bullet)
    'dagger': '†',  # U+2020 (\dagger)
    'daggerdbl': '‡',  # U+2021 (\ddagger)
    'dotlessi': 'ı',  # U+0131 (\imath)
    'weierstrass': '℘',  # U+2118 (\wp)
    'eth': 'ð',  # U+00F0 (\eth)

    # CMEX10 - Big delimiters and operators
    'bracketleftbig': '⟦',  # U+27E6 (\big[)
    'bracketrightbig': '⟧',  # U+27E7 (\big])
    'bracketleftbigg': '⟦',  # U+27E6 (\bigg[)
    'bracketrightbigg': '⟧',  # U+27E7 (\bigg])
    'bracketleftBig': '⟦',  # U+27E6 (\Big[)
    'bracketrightBig': '⟧',  # U+27E7 (\Big])
    'bracketleftBigg': '⟦',  # U+27E6 (\Bigg[)
    'bracketrightBigg': '⟧',  # U+27E7 (\Bigg])
    'summationdisplay': '∑',  # U+2211 (\sum in display mode)
    'summationtext': '∑',  # U+2211 (\sum in text mode)
    'productdisplay': '∏',  # U+220F (\prod in display mode)
    'producttext': '∏',  # U+220F (\prod in text mode)
    'coproductdisplay': '∐',  # U+2210 (\coprod in display mode)
    'coproducttext': '∐',  # U+2210 (\coprod in text mode)
    'integraldisplay': '∫',  # U+222B (\int in display mode)
    'integraltext': '∫',  # U+222B (\int in text mode)
    'parenleftbig': '(',  # U+0028 (\big()
    'parenrightbig': ')',  # U+0029 (\big))
    'parenleftBig': '(',  # U+0028 (\Big()
    'parenrightBig': ')',  # U+0029 (\Big))
    'parenleftbigg': '(',  # U+0028 (\bigg()
    'parenrightbigg': ')',  # U+0029 (\bigg))
    'parenleftBigg': '(',  # U+0028 (\Bigg()
    'parenrightBigg': ')',  # U+0029 (\Bigg))
    'braceleftbig': '{',  # U+007B (\big\{)
    'bracerightbig': '}',  # U+007D (\big\})
    'braceleftBig': '{',  # U+007B (\Big\{)
    'bracerightBig': '}',  # U+007D (\Big\})
    'braceleftbigg': '{',  # U+007B (\bigg\{)
    'bracerightbigg': '}',  # U+007D (\bigg\})
    'braceleftBigg': '{',  # U+007B (\Bigg\{)
    'bracerightBigg': '}',  # U+007D (\Bigg\})

    # Extensible delimiter parts (map to base symbols)
    'parenlefttp': '(',  # U+0028
    'parenrighttp': ')',  # U+0029
    'parenleftbt': '(',  # U+0028
    'parenrightbt': ')',  # U+0029
    'parenleftex': '(',  # U+0028
    'parenrightex': ')',  # U+0029
    'bracketlefttp': '[',  # U+005B
    'bracketrighttp': ']',  # U+005D
    'bracketleftbt': '[',  # U+005B
    'bracketrightbt': ']',  # U+005D
    'bracketleftex': '[',  # U+005B
    'bracketrightex': ']',  # U+005D
    'bracelefttp': '{',  # U+007B
    'bracerighttp': '}',  # U+007D
    'braceleftbt': '{',  # U+007B
    'bracerightbt': '}',  # U+007D
    'braceleftmid': '{',  # U+007B
    'bracerightmid': '}',  # U+007D
    'braceex': '|',  # U+007C
    'arrowvertex': '|',  # U+007C
    'vextendsingle': '|',  # U+007C
    'vextenddouble': '∥',  # U+2225
    'radical': '√',  # U+221A (\sqrt)
    'radicalex': '√',  # U+221A

    # MSBM10 - AMS negated binary relations
    'lessornotsimilar': '⋦',  # U+22E6 (\lnsim)
    'greaterornotsimilar': '⋧',  # U+22E7 (\gnsim)
    'notshortbar': '∤',  # U+2224 (\nmid)
    'notshortparallel': '∦',  # U+2226 (\nparallel)
    'subsetornoteql': '⊊',  # U+228A (\varsubsetneq)
    'supersetornoteql': '⊋',  # U+228B (\varsupsetneq)

    # stmary10 - St Mary Road symbols
    'hugetriangleup': '△',  # U+25B3 (\bigtriangleup)
    'hugetriangledown': '▽',  # U+25BD (\bigtriangledown)
    'llbracket': '⟦',  # U+27E6 (\llbracket)
    'rrbracket': '⟧',  # U+27E7 (\rrbracket)
    'llparenthesis': '⦅',  # U+2985
    'rrparenthesis': '⦆',  # U+2986

    # Additional AGL mappings
    'Oslash': 'Ø',  # U+00D8
    'bracketleftbt': '',  # U+F8F0 (private use)
    'bracketlefttp': '',  # U+F8F1 (private use)
    'bracketrightbt': '',  # U+F8F2 (private use)
    'bracketrighttp': '',  # U+F8F3 (private use)
    'dotlessj': '',  # U+F6BE (private use)
}
