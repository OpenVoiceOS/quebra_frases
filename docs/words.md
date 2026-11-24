# Words

<!-- agent-hint
covers: what word_tokenize and its indexed forms return, what one token is, and what the tests guarantee
source: quebra_frases/tokenization.py:_WORD_REGEX, test/test_tokenization.py:TestWordTokenizeCoverage
generated: no
verify: python -m doctest -o NORMALIZE_WHITESPACE docs/words.md
see: docs/sentences.md, docs/whitespace.md, docs/api.md
-->

This page explains the word tokenizer: the three functions, what one token is, and what a caller can rely on.

## The three functions

The three functions find the same tokens. They differ only in the shape of each item.

| Function | One item |
| --- | --- |
| `word_tokenize(input_string)` | the token |
| `char_indexed_word_tokenize(input_string)` | `(start, token)` |
| `span_indexed_word_tokenize(input_string)` | `(start, end, token)` |

The end offset is exclusive, so `text[start:end]` gives the token back.

```python
>>> from quebra_frases import word_tokenize, char_indexed_word_tokenize, span_indexed_word_tokenize
>>> text = "Olá, mundo!"
>>> word_tokenize(text)
['Olá', ',', 'mundo', '!']
>>> char_indexed_word_tokenize(text)
[(0, 'Olá'), (3, ','), (5, 'mundo'), (10, '!')]
>>> span_indexed_word_tokenize(text)
[(0, 3, 'Olá'), (3, 4, ','), (5, 10, 'mundo'), (10, 11, '!')]

```

## What one token is

The tokenizer tries four patterns at each position, in this order. The first pattern that matches gives the token.

1. A number with a separator inside it. It has an optional minus sign, digits, and then one or more groups of a separator and digits. The separators are `,`, `.`, `:`, `/`, the Arabic decimal separator U+066B and the Arabic thousands separator U+066C. The number ends on a digit, so a separator at the end is a token of its own.
2. A dotted abbreviation such as "i.e.". It is letters with a period inside them and a period at the end.
3. A word. It is a run of letters, combining marks, number characters, apostrophes and hyphens. The zero-width non-joiner and the zero-width joiner (U+200C, U+200D) stay inside the word, because Persian and Indic words contain them.
4. Any other character that is not whitespace. A punctuation mark, a currency sign or a symbol is a token of its own.

```python
>>> from quebra_frases import word_tokenize
>>> word_tokenize("Custa 1,234.50 USD; i.e. pouco.")
['Custa', '1,234.50', 'USD', ';', 'i.e.', 'pouco', '.']
>>> word_tokenize("14:30. -5. 20%")
['14:30', '.', '-5', '.', '20', '%']
>>> word_tokenize("nem-sempre d'água")
['nem-sempre', "d'água"]

```

Combining marks stay in the word. Devanagari, Thai and other scripts write vowel signs as combining marks.

```python
>>> from quebra_frases import word_tokenize
>>> word_tokenize("नमस्ते दुनिया")
['नमस्ते', 'दुनिया']
>>> word_tokenize("می‌خواهم بروم")
['می\u200cخواهم', 'بروم']

```

## What a caller can rely on

The test `TestWordTokenizeCoverage` checks these properties over a set of sentences in many scripts. It also checks the first and the third property over every Unicode code point.

- Every character that is not whitespace is in exactly one token.
- No token holds a whitespace character.
- The spans come in text order and do not overlap, and `text[start:end]` equals the token.
- `word_tokenize` and `char_indexed_word_tokenize` return the same tokens as `span_indexed_word_tokenize`.

An empty text gives an empty list.

```python
>>> from quebra_frases import word_tokenize
>>> word_tokenize("")
[]

```

---

[Index](index.md) · Previous: [Getting started](getting-started.md) · Next: [Sentences](sentences.md)
