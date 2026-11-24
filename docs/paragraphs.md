# Paragraphs

<!-- agent-hint
covers: what paragraph_tokenize and its indexed forms return, where blank lines go, and the limit of the span offsets
source: quebra_frases/tokenization.py:paragraph_tokenize, quebra_frases/tokenization.py:span_indexed_paragraph_tokenize, test/test_chunking.py:test_paragraph, test/test_chunking.py:test_paragraph_tokenize_leading_separator
generated: no
verify: python -m doctest -o NORMALIZE_WHITESPACE docs/paragraphs.md
see: docs/sentences.md, docs/whitespace.md, docs/api.md
-->

This page explains the paragraph splitter: the three functions, where the blank lines go, and what a caller can rely on.

## The three functions

The three functions find the same paragraphs. They differ only in the shape of each item.

| Function | One item |
| --- | --- |
| `paragraph_tokenize(input_string)` | the paragraph |
| `char_indexed_paragraph_tokenize(input_string)` | `(start, paragraph)` |
| `span_indexed_paragraph_tokenize(input_string)` | `(start, end, paragraph)` |

```python
>>> from quebra_frases import paragraph_tokenize, char_indexed_paragraph_tokenize, span_indexed_paragraph_tokenize
>>> text = "First paragraph.\nStill first.\n\nSecond paragraph."
>>> paragraph_tokenize(text)
['First paragraph.\nStill first.\n\n', 'Second paragraph.']
>>> char_indexed_paragraph_tokenize(text)
[(0, 'First paragraph.\nStill first.\n\n'), (31, 'Second paragraph.')]
>>> span_indexed_paragraph_tokenize(text)
[(0, 31, 'First paragraph.\nStill first.\n\n'), (31, 48, 'Second paragraph.')]

```

## How the text splits

The splitter cuts the text into lines with `str.splitlines(True)`, so each line keeps its line ending. A blank line is a line that holds only whitespace. A run of lines that are not blank is a paragraph. A run of blank lines stays at the end of the paragraph before it, so the paragraphs keep every character.

```python
>>> from quebra_frases import paragraph_tokenize
>>> paragraph_tokenize("Line one.\nLine two.\n\n\nNext.\n")
['Line one.\nLine two.\n\n\n', 'Next.\n']
>>> paragraph_tokenize("a\r\n\r\nb")
['a\r\n\r\n', 'b']

```

Blank lines at the start of the text come before any paragraph. The splitter drops them. A text that holds only whitespace gives an empty list.

```python
>>> from quebra_frases import paragraph_tokenize
>>> paragraph_tokenize("\nfirst\n\nsecond")
['first\n\n', 'second']
>>> paragraph_tokenize("   \n")
[]

```

## What a caller can rely on

When the text does not start with a blank line, the paragraphs joined together give the text back. The spans then give the true position of each paragraph, and `text[start:end]` equals the paragraph.

The spans add up the lengths of the paragraphs before each one. When the text starts with a blank line, the dropped line moves every span. For the text `"\n\nfoo\n\nbar"`, the first span is `(0, 5)`, which holds `"\n\nfoo"` and not the paragraph `"foo\n\n"`. Remove the leading blank lines before you ask for spans.

---

[Index](index.md) · Previous: [How a sentence boundary is decided](sentence-boundaries.md) · Next: [Whitespace](whitespace.md)
