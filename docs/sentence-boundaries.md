# How a sentence boundary is decided

<!-- agent-hint
covers: every rule sentence_tokenize applies to pick or reject a split point, with the abbreviation and unit lists and the sources the code cites
source: quebra_frases/tokenization.py:sentence_tokenize, quebra_frases/tokenization.py:_is_abbreviation, quebra_frases/tokenization.py (module docstring, _SENTENCE_SPLIT_CANDIDATE, _ABBREVIATIONS, _CAPITAL_ABBREVIATIONS, _UNITS, _VOWELS, _ROMAN_NUMERAL)
generated: no
verify: python -m doctest -o NORMALIZE_WHITESPACE docs/sentence-boundaries.md
see: docs/sentences.md, docs/words.md
-->

This page gives the rules that `sentence_tokenize` applies, in the order the code applies them. Read it to find out why a text splits, or does not split, at a given mark.

The splitter first finds candidate split points. It then checks each candidate and keeps or rejects it.

## Step 1: Find the candidate split points

A candidate is a mark with the Unicode `Sentence_Terminal` property, followed by a run of whitespace. UAX #29, Unicode Text Segmentation, uses this property for sentence breaks. It covers ".", "?", "!", the Devanagari danda "।", the Arabic question mark "؟", "。" and others.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("नमस्ते। आप कैसे हैं?")
['नमस्ते।', 'आप कैसे हैं?']

```

Two marks have the property but are never a candidate. The code cites a source for each:

| Mark | Why it does not end a sentence | Source the code cites |
| --- | --- | --- |
| U+104A, MYANMAR SIGN LITTLE SECTION | It has "significance close to comma" | r12a, [Myanmar (Burmese) orthography notes](https://r12a.github.io/scripts/mymr/my) |
| U+2024, ONE DOT LEADER | It is "also used as an Armenian semicolon (mijaket)" | Unicode NamesList |

Chinese and Japanese put no space after a sentence. After the marks `。｡！？︒︕︖﹖﹗`, the next character that is not a space starts a candidate, with no whitespace needed. A closing bracket or quote after the mark stays with the sentence. The fullwidth full stop "．" is not in this list, because it also separates the digits of a number such as "３．５".

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("「はい。」彼は答えた。")
['「はい。」', '彼は答えた。']
>>> sentence_tokenize("价格是３．５元。")
['价格是３．５元。']

```

## Step 2: Keep a spaced closing mark with its sentence

French sets a space before a closing guillemet, as in "« Òc ! »". When closing brackets or quotes follow the whitespace of a candidate, the split moves past them. They stay with the sentence they close. If the text ends with them, the candidate is rejected.

A closing mark after a line break stays where it is. It opens the next paragraph of a quote that runs over more than one paragraph.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("« Òc ! » E puèi parlèt.")
['« Òc ! »', 'E puèi parlèt.']
>>> sentence_tokenize("Ço qu'a dit: « Òc ! »")
["Ço qu'a dit: « Òc ! »"]
>>> sentence_tokenize("« Premier.\n» Deuxième paragraphe.")
['« Premier.', '» Deuxième paragraphe.']

```

## Step 3: Look at the next character

Some checks below ask whether the sentence goes on after the mark. It goes on when the next character is a lowercase letter that title case changes.

Georgian letters count as lowercase, but a Georgian sentence also starts with them. Title case leaves a Georgian letter unchanged, so a Georgian letter does not count as going on.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("ფასი არის 3. შემდეგ ის წავიდა.")
['ფასი არის 3.', 'შემდეგ ის წავიდა.']

```

## Step 4: Check an exclamation mark

After "!", the candidate is rejected when the sentence goes on in lower case. Every other "!" ends a sentence.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("Los usuarios de Yahoo! y Microsoft.")
['Los usuarios de Yahoo! y Microsoft.']
>>> sentence_tokenize("¡Ay! dijo él. Se fue.")
['¡Ay! dijo él.', 'Se fue.']
>>> sentence_tokenize("Que frio! Fecha a janela.")
['Que frio!', 'Fecha a janela.']

```

Other marks, such as "?", get no check. Each of them ends a sentence.

## Step 5: Check the word before a period

After ".", the splitter reads the word before the period. The word is the run of letters and apostrophes that ends at the period. The word is an abbreviation, and the period does not end the sentence, when one of these is true:

1. The word is one letter. This covers initials such as "J." in any script.
2. The word is all capitals and is in the list of capital abbreviations below. Any other word in capitals, such as an acronym ("TV.") or a Roman numeral ("XX."), is not an abbreviation.
3. The word is in Latin script and has no vowel. This covers "Dr.", "Srs." and "Płk.".
4. The word is not in capitals, and in lower case it is in the list of short abbreviations below.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("J. R. R. Tolkien wrote it. It sold.")
['J. R. R. Tolkien wrote it.', 'It sold.']
>>> sentence_tokenize("O SR. COSTA chegou. Fim.")
['O SR. COSTA chegou.', 'Fim.']
>>> sentence_tokenize("Vi na TV. Depois saí.")
['Vi na TV.', 'Depois saí.']
>>> sentence_tokenize("Płk. Nowak przyszedł. Koniec.")
['Płk. Nowak przyszedł.', 'Koniec.']
>>> sentence_tokenize("A Sra. Costa chegou. Sentou-se.")
['A Sra. Costa chegou.', 'Sentou-se.']

```

### The capital abbreviations

The list is `_CAPITAL_ABBREVIATIONS`: MM, SR, SRA, SRS, SRAS, DR, DRA, DRS, EXMO, EXMA, VS, RR, HH, DD, VV.

The code comment says these are titles in capitals ("SR.", "EXMO.") and doubled-letter plurals: Spanish "RR.HH.", "DD.HH." and "VV.AA.", and Portuguese "DD." for "Digníssimo". The comment leaves out "PP" and "SS", because they are also party names ("PP.", "der SS.").

### The short abbreviations

The list is `_ABBREVIATIONS`: sra, dra, exmo, exma, etc, ex, pp, vs, av, num. Eight of these words hold a vowel, so the vowel test misses them: sra, dra, exmo, exma, etc, ex, av, num. The words pp and vs hold no vowel, and the vowel test already catches them. The code cites no source for this list.

### What counts as a vowel

Unicode has no vowel property, so the code keeps its own set, `_VOWELS`. A Latin letter is a vowel when its NFD form holds a, e, i, o, u or y. This covers "è", "ü" and "ą". The set also holds the Latin letters that NFD leaves whole and whose Unicode name holds a vowel or a vowel ligature, such as "æ", "ø", "ı", "ə", "ɛ" and "œ".

The code leaves out four letters whose name holds a vowel but which stand for a consonant. The comment gives the reason for each:

| Letter | Reason in the code comment |
| --- | --- |
| TURNED Y, "ʎ" | a lateral approximant in Unicode NamesList.txt |
| TURNED Y WITH BELT | the belt marks a lateral fricative, as in L WITH BELT |
| Y WITH HOOK, "ƴ" | a palatal in Fula and Hausa |
| OI, "ƣ" | formal alias GHA in NameAliases.txt |

Modifier letters are not in the set, so "Srª." stays an abbreviation. The vowel test applies only to Latin words, because abjads such as Arabic and Hebrew do not write most vowels.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("A Srª. Costa chegou. Fim.")
['A Srª. Costa chegou.', 'Fim.']

```

## Step 6: Let a unit symbol after a number end the sentence

An abbreviation that is a unit symbol after a number ends the sentence, as in "Tem 3 kg.". The number comes first, because the SI Brochure, 9th edition (BIPM 2019), section 5.4.3, says: "The numerical value always precedes the unit and a space is always used to separate the unit from the number." Only a decimal digit before the symbol counts as a number. The digit can come before a compound unit, as in "160 km/h.".

The unit still does not end the sentence in two cases. The first case is when the sentence goes on in lower case ("3 cm. de largo"). The second case is a one-letter unit that starts a dotted abbreviation ("3 s. S. 45").

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("Tem 3 kg. Pesa muito.")
['Tem 3 kg.', 'Pesa muito.']
>>> sentence_tokenize("Vai a 160 km/h. Abranda.")
['Vai a 160 km/h.', 'Abranda.']
>>> sentence_tokenize("Mide 3 cm. de largo.")
['Mide 3 cm. de largo.']
>>> sentence_tokenize("Die Werte stehen in Tabelle 3 s. S. 45 im Anhang.")
['Die Werte stehen in Tabelle 3 s. S. 45 im Anhang.']
>>> sentence_tokenize("Juan Pérez (h. 1500) fue pintor.")
['Juan Pérez (h. 1500) fue pintor.']

```

### The unit symbols

The list is `_UNITS`. It holds only the symbols that read as an abbreviation by Step 5. A symbol with a vowel, such as "min", "mol" or "Pa", ends a sentence anyway. The module docstring gives the source of each symbol:

| Symbols | Source the code cites |
| --- | --- |
| s, kg, cd | SI Brochure Table 2, base units |
| Hz, kHz, MHz, GHz, kW, pH | SI Brochure Table 4 (Hz, W and H), with the prefixes of Table 7. "pH" is the picohenry. |
| km, cm, mm, nm, dm, g, mg | SI Brochure Table 7, prefixes on the metre and on the gram (section 3 attaches them to "g") |
| h, l, t, dB, ml, cl, dl, hl | SI Brochure Table 8, "Non-SI units", and the litre with the prefixes of Table 7 |
| Wh, kWh | W (Table 4) times h, written as one word |
| ft, lb, rpm, cc | NIST Special Publication 811 (2008), Appendix B.8. Section 6.1.8 lists cc, for cm3, among the abbreviations it does not permit, but text uses it. |
| mph, kph, lbs, kb, Mb, Gb, kB | Wiktionary, English entries. "lbs" is the plural of lb. kb, Mb and Gb stand for kbit, Mbit and Gbit. kB is the kilobyte. |

The metre, "m", is not in the list. Lithuanian writes "m." (metai, "year") after each year ("2006 m. Inspekcija"), and the text does not tell a year from a length ("3850 m."). Acidity puts the number after the symbol ("pH 7"), so a pH value does not end a sentence.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("2006 m. Inspekcija pradėjo darbą.")
['2006 m. Inspekcija pradėjo darbą.']
>>> sentence_tokenize("Leva 5 min. Depois sai.")
['Leva 5 min.', 'Depois sai.']

```

## Step 7: Keep an ordinal with its sentence

After the checks of Step 5 and Step 6, one more check applies to a period. An ordinal before the period does not end the sentence when the sentence goes on in lower case. An ordinal is a number that stands alone ("3. de maio") or a well-formed Roman numeral from I to MMMCMXCIX ("XIV. acabou").

A number stands alone when a space or the start of the text comes before its digits. "14:30.", "2,50." and "COVID-19." end in a digit but are not ordinals. A capital word with Roman numeral letters that is not a well-formed numeral, such as "ID" or "IIIII", is not an ordinal.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("No dia 3. de maio.")
['No dia 3. de maio.']
>>> sentence_tokenize("O século XIV. acabou.")
['O século XIV. acabou.']
>>> sentence_tokenize("O século XIV. Acabou.")
['O século XIV.', 'Acabou.']
>>> sentence_tokenize("Chegou às 14:30. depois saiu.")
['Chegou às 14:30.', 'depois saiu.']
>>> sentence_tokenize("Mostre o ID. depois entre.")
['Mostre o ID.', 'depois entre.']

```

A word that is not an abbreviation or an ordinal ends the sentence, also before a lowercase word.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("Saiu. depois voltou.")
['Saiu.', 'depois voltou.']

```

---

[Index](index.md) · Previous: [Sentences](sentences.md) · Next: [Paragraphs](paragraphs.md)
