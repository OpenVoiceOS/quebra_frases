"""Word and sentence tokenization.

A unit symbol after a number ends a sentence ("Tem 3 kg. Pesa muito."). The
number comes first because the SI Brochure, 9th edition (BIPM 2019), 5.4.3
says: "The numerical value always precedes the unit and a space is always
used to separate the unit from the number." A symbol with a vowel ("min",
"mol", "Pa") ends a sentence anyway, so _UNITS holds only the symbols that
would otherwise read as an abbreviation. The source of each symbol:

- SI Brochure Table 2, base units: m, s, kg, cd.
- SI Brochure Table 4, Hz and W, with the prefixes of Table 7: Hz, kHz, MHz,
  GHz, kW, and pH (picohenry, from H).
- SI Brochure Table 7, prefixes on the metre and on the gram (section 3
  attaches them to "g"): km, cm, mm, nm, dm, g, mg.
- SI Brochure Table 8, units accepted for use with the SI: h, l, t, dB, and
  the litre with the prefixes of Table 7: ml, cl, dl, hl. Wh and kWh are W
  (Table 4) times h, written as one word.
- NIST Special Publication 811 (2008), Appendix B.8: ft, lb, rpm. Section
  6.1.8 names cc as the abbreviation in use for cm3.
- Wiktionary, English entries: mph, kph, lbs (plural of lb), kb, Mb, Gb (for
  kbit, Mbit, Gbit) and kB (kilobyte).
"""
import unicodedata
from itertools import groupby

import regex as re


# \p{M} (combining marks) belongs with \p{L}: Thai, Devanagari, Bengali,
# Tamil and other abugidas write vowel signs, viramas and tone marks as
# Mn/Mc code points inside a word ("เพิ่ม", "नमस्ते"). Leaving them out of
# the letter class made every mark end the token and vanish from the output.
# ZWNJ and ZWJ (U+200C, U+200D) sit inside Persian and Indic words, and
# Unicode word segmentation (UAX #29, rule WB4) never breaks a word at them.
# A number ends on a digit: a separator with no digit after it is the
# punctuation that follows the number ("14:30.", "5,"). U+066B and U+066C
# are the Arabic decimal and thousands separators.
# The last alternative makes any other character that is not space a token
# of its own: punctuation, a currency sign, a dash or any other symbol. No
# character is left out of the tokens.
_WORD_REGEX = re.compile(
    r"(?:-?\d+(?:[,.:\/\u066b\u066c]\d+)+)"
    r"|\b[\p{L}\p{M}]*(?:\.[\p{L}\p{M}]+)+\."
    r"|[\p{L}\p{M}\p{N}\u200c\u200d'-]+"
    r"|\S", re.I)
# the whole whitespace run, not one character of it: matching a single
# space leaves the rest of the run at the head of the next sentence
_SENTENCE_SPLIT_CANDIDATE = re.compile(r'(?<=[.?])\s+')
# Unicode has no vowel property, and abjads such as Arabic and Hebrew do not
# write most vowels at all, so the consonant-only test holds only for Latin
_LATIN_WORD = re.compile(r"[\p{Latin}']+")
# A Latin letter is a vowel when NFD takes it to a, e, i, o, u or y ("è",
# "ü", "ą"), or to one of the letters below ("ǿ" to "ø"). NFD leaves these
# letters whole. Each one has a Unicode character name that holds a vowel
# or a vowel ligature, as in LATIN SMALL LETTER AE, O WITH STROKE, DOTLESS I,
# SCHWA, OPEN E, LIGATURE OE and LIGATURE FI. Letters whose name holds a
# vowel but which stand for a consonant are left out: TURNED Y (a lateral
# approximant in Unicode NamesList.txt), TURNED Y WITH BELT (the belt marks
# a lateral fricative, as in L WITH BELT), Y WITH HOOK (a palatal in Fula
# and Hausa) and OI (formal alias GHA in NameAliases.txt).
# Modifier letters are not in the list, so "Srª." stays an abbreviation.
_VOWELS = set(
    "aeiouyAEIOUY"
    "ÆØæøıĲĳŒœƆƎƏƐƖƗƟƱǝȢȣȺɄɆɇɎɏɐɑ"
    "ɒɔɘəɚɛɜɝɞɨɩɪɵɶɷʉʊʏʚᴀᴁᴂᴇᴈᴉᴏᴐᴑᴒᴓᴔ"
    "ᴕᴖᴗᴜᴝᴞᵫᵻᵼᵾᵿᶏᶐᶒᶓᶔᶕᶖᶗᶙẚỾỿⱥⱭⱯⱰⱸⱺⱻꜲꜳ"
    "ꜴꜵꜶꜷꜸꜹꜺꜻꜼꜽꝊꝋꝌꝍꝎꝏꞚꞛꞜꞝꞞꞟꞫꞮꞶꞷꞸꞹꞺꞻꞼꞽ"
    "ꞾꞿꟀꟁꟷꟾꬰꬱꬲꬳꬴꬽꬾꬿꭀꭁꭂꭃꭄꭎꭏꭐꭑꭒꭚꭡꭢꭣꭤﬁﬃＡ"
    "ＥＩＯＵＹａｅｉｏｕｙ𝼚𝼛"
)
# "v" (versus, "Roe v. Wade") is the one single letter listed: it holds the
# sentence before a capital, where any other lowercase letter ends it
_ABBREVIATIONS = {"sra", "dra", "exmo", "exma", "etc", "ex", "pp", "vs", "av", "num", "v"}
_UNITS = {"m", "s", "kg", "cd", "Hz", "kHz", "MHz", "GHz", "kW", "pH",
          "km", "cm", "mm", "nm", "dm", "g", "mg", "h", "l", "t", "dB",
          "ml", "cl", "dl", "hl", "Wh", "kWh", "ft", "lb", "rpm", "cc",
          "mph", "kph", "lbs", "kb", "Mb", "Gb", "kB"}
# capital words that are titles or doubled-letter plurals ("SR.", "EXMO.",
# Spanish "RR.HH.", "DD.HH.", "VV.AA.", Portuguese "DD." Digníssimo); "PP"
# and "SS" are left out because they are also party names ("PP.", "der SS.")
_CAPITAL_ABBREVIATIONS = {"MM", "SR", "SRA", "SRS", "SRAS", "DR", "DRA", "DRS",
                          "EXMO", "EXMA", "VS", "RR", "HH", "DD", "VV"}
# a well-formed Roman numeral from I to MMMCMXCIX; capital words of the same
# letters that are not numerals ("ID", "IIIII") do not match
_ROMAN_NUMERAL = re.compile(
    r"(?=[IVXLCDM])M{0,3}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})")


def _is_abbreviation(word):
    # a period does not end a sentence when the token before it is:
    # - a single letter (initials: "D.", "J.")
    # - a title or doubled-letter plural in capitals ("SR.", "MM.", "RR.HH.");
    #   any other word of two or more capitals is an acronym ("TV.", "BBC.")
    #   or a Roman numeral ("XX.") and ends the sentence
    # - a consonant-only Latin token (abbreviations like "Dr.", "Srs.")
    # - a known short abbreviation that the rules above miss
    if not word:
        return False
    if len(word) == 1:
        return True
    if word.isupper():
        return word in _CAPITAL_ABBREVIATIONS
    if _LATIN_WORD.fullmatch(word) and not any(
            ch in _VOWELS for ch in unicodedata.normalize("NFD", word)):
        return True
    return word.lower() in _ABBREVIATIONS


def word_tokenize(input_string):
    return [m.group() for m in re.finditer(_WORD_REGEX, input_string)]


def char_indexed_word_tokenize(input_string):
    return [(m.start(0), m.group())
            for m in re.finditer(_WORD_REGEX, input_string)]


def span_indexed_word_tokenize(input_string):
    return [(m.start(0), m.end(0), m.group())
            for m in re.finditer(_WORD_REGEX, input_string)]


def sentence_tokenize(input_string):
    sentences = []
    last = 0
    for m in _SENTENCE_SPLIT_CANDIDATE.finditer(input_string):
        split_at = m.start()
        if input_string[split_at - 1] == '.':
            j = split_at - 2
            while j >= 0 and (input_string[j].isalpha() or input_string[j] == "'"):
                j -= 1
            word = input_string[j + 1:split_at - 1]
            nxt = input_string[m.end():m.end() + 1]
            if _is_abbreviation(word):
                # a single letter holds the sentence in a dotted abbreviation:
                # after a period ("i.e.", "e.g."), after a letter, a period
                # and a space ("p. m.", "d. h.", a list item "opção. a. Comer")
                # and before a letter and a period ("a. C."), but not before
                # an ellipsis ("x. K...")
                dotted = len(word) == 1 and (
                    (j >= 0 and input_string[j] == ".")
                    or (j >= 2 and input_string[j].isspace()
                        and input_string[j - 1] == "." and input_string[j - 2].isalpha())
                    or (nxt.isalpha() and input_string[m.end() + 1:m.end() + 2] == "."
                        and input_string[m.end() + 2:m.end() + 3] != "."))
                # a unit symbol after a number ends the sentence ("3 kg.",
                # "160 km/h.")
                k = j
                while k >= 0 and (input_string[k].isalpha() or input_string[k] == "/"):
                    k -= 1
                while k >= 0 and input_string[k].isspace():
                    k -= 1
                unit = word in _UNITS and k >= 0 and input_string[k].isdecimal()
                # so does a lowercase letter before a capital ("um x. Dois");
                # title case leaves a Georgian letter unchanged, and a
                # Georgian sentence starts with one
                lone = len(word) == 1 and word != word.title() \
                    and word not in _ABBREVIATIONS and nxt.isupper()
                if dotted or not (unit or lone):
                    continue
            # an ordinal ("3. de maio", "XIV. acabou") does not end the
            # sentence when the next word goes on in lower case. The number
            # must stand alone: "14:30.", "2,50." and "COVID-19." end in a
            # digit but are not ordinals.
            k = split_at - 1
            while k > 0 and input_string[k - 1].isdecimal():
                k -= 1
            bare_number = k < split_at - 1 and \
                (k == 0 or input_string[k - 1].isspace())
            ordinal = bare_number or _ROMAN_NUMERAL.fullmatch(word)
            # Georgian letters count as lowercase, but a Georgian sentence
            # starts with them too. Title case leaves them unchanged, so only
            # a letter that title case changes shows the sentence goes on.
            if ordinal and nxt.islower() and nxt != nxt.title():
                continue
        sentences.append(input_string[last:split_at])
        last = m.end()
    sentences.append(input_string[last:])
    return sentences


def char_indexed_sentence_tokenize(input_string):
    return [(s[0], s[2]) for s in span_indexed_sentence_tokenize(input_string)]


def span_indexed_sentence_tokenize(input_string):
    sentences = sentence_tokenize(input_string)
    spans = []
    cursor = 0
    for sentence in sentences:
        # locate each sentence in the source rather than adding up the
        # lengths of the ones before it: that arithmetic assumes exactly one
        # character between sentences and drifts wherever there are more
        start_idx = input_string.find(sentence, cursor)
        if start_idx < 0:
            start_idx = cursor
        end_idx = start_idx + len(sentence)
        spans.append((start_idx, end_idx, input_string[start_idx:end_idx]))
        cursor = end_idx
    return spans


def paragraph_tokenize(input_string):
    paragraphs = []
    for group_separator, chunk in groupby(input_string.splitlines(True),
                                          key=str.isspace):
        if group_separator:
            # a separator run belongs to the paragraph it follows; leading
            # whitespace follows nothing, so there is no paragraph to attach
            # it to and it is not a paragraph of its own
            if paragraphs:
                paragraphs[-1] += list(chunk)
        else:
            paragraphs.append(list(chunk))
    return [''.join(chunk) for chunk in paragraphs]


def char_indexed_paragraph_tokenize(input_string):
    return [(s[0], s[2]) for s in
            span_indexed_paragraph_tokenize(input_string)]


def span_indexed_paragraph_tokenize(input_string):
    sentences = paragraph_tokenize(input_string)
    spans = []
    for idx, s in enumerate(sentences):
        start_idx = sum(len(_) for _ in sentences[:idx])
        end_idx = start_idx + len(s)
        spans.append((start_idx, end_idx, input_string[start_idx:end_idx]))
    return spans


def get_empty_spans(input_string):
    spans = []
    start = None
    total_chars = len(input_string)
    for idx in range(total_chars):
        next_char = input_string[idx + 1] if idx < total_chars - 1 else None
        if input_string[idx].isspace():
            if start is None:
                start = idx
            if next_char is None:
                # the span end is exclusive, and idx is the last character
                end = idx + 1
                spans.append((start, end, input_string[start:end]))
        elif start is not None:
            end = idx
            spans.append((start, end, input_string[start:end]))
            start = None
    return spans


def span_indexed_empty_space_tokenize(input_string):
    spans = []
    start = None
    total_chars = len(input_string)
    for idx in range(total_chars):
        next_char = input_string[idx + 1] if idx < total_chars - 1 else None
        if start is not None and \
                (input_string[idx].isspace() or next_char is None):
            end = idx + 1 if next_char is None else idx
            spans.append((start, end, input_string[start:end]))
            start = None
        elif not input_string[idx].isspace():
            if start is None:
                start = idx
    return spans


def char_indexed_empty_space_tokenize(input_string):
    return [(s[0], s[2]) for s in
            span_indexed_empty_space_tokenize(input_string)]


def empty_space_tokenize(input_string):
    return [s[2] for s in
            span_indexed_empty_space_tokenize(input_string)]
