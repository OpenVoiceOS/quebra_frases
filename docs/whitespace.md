# Whitespace

<!-- agent-hint
covers: the functions that split on whitespace runs and the function that returns the whitespace runs, with their known limits at the end of a text
source: quebra_frases/tokenization.py:span_indexed_empty_space_tokenize, quebra_frases/tokenization.py:get_empty_spans, test/test_chunking.py:test_empty, test/test_chunking.py:TestReportedDefects
generated: no
verify: python -m doctest -o NORMALIZE_WHITESPACE docs/whitespace.md
see: docs/words.md, docs/paragraphs.md, docs/api.md
-->

This page explains the functions that split a text on whitespace only, and the function that returns the whitespace itself. Use them when punctuation must stay attached to its word.

## Split on whitespace

The three functions find the same pieces: the runs of characters that are not whitespace. They differ only in the shape of each item.

| Function | One item |
| --- | --- |
| `empty_space_tokenize(input_string)` | the piece |
| `char_indexed_empty_space_tokenize(input_string)` | `(start, piece)` |
| `span_indexed_empty_space_tokenize(input_string)` | `(start, end, piece)` |

A whitespace run of any width and any mix of spaces, tabs and line breaks separates two pieces.

```python
>>> from quebra_frases import empty_space_tokenize, char_indexed_empty_space_tokenize, span_indexed_empty_space_tokenize
>>> text = "isto   tem \t vários espaços"
>>> empty_space_tokenize(text)
['isto', 'tem', 'vários', 'espaços']
>>> char_indexed_empty_space_tokenize(text)
[(0, 'isto'), (7, 'tem'), (13, 'vários'), (20, 'espaços')]
>>> span_indexed_empty_space_tokenize(text)
[(0, 4, 'isto'), (7, 10, 'tem'), (13, 19, 'vários'), (20, 27, 'espaços')]

```

Punctuation stays in the piece, unlike in [Words](words.md).

```python
>>> from quebra_frases import empty_space_tokenize
>>> empty_space_tokenize("Olá, mundo!")
['Olá,', 'mundo!']

```

### Known limits at the end of the text

The last piece of a text has two known faults:

- When the last piece is one character long, the functions drop it. `empty_space_tokenize("a b")` returns `['a']`.
- When the text ends with exactly one whitespace character, the last piece includes it. `span_indexed_empty_space_tokenize("ab ")` returns `[(0, 3, 'ab ')]`.

## Get the whitespace runs

`get_empty_spans(input_string)` returns each whitespace run as `(start, end, run)`. The end offset is exclusive, so `text[start:end]` gives the run back. The tests check a run at the start of the text and a run at the end of the text.

```python
>>> from quebra_frases import get_empty_spans
>>> get_empty_spans("isto   tem \t vários espaços")
[(4, 7, '   '), (10, 13, ' \t '), (19, 20, ' ')]
>>> get_empty_spans("  a  ")
[(0, 2, '  '), (3, 5, '  ')]

```

---

[Index](index.md) · Previous: [Paragraphs](paragraphs.md) · Next: [Chunks](chunks.md)
