# Empty text, wrong types and long text

<!-- agent-hint
covers: what each splitter returns for empty text and for whitespace-only text, which error a non-string raises, and how a long text behaves
source: quebra_frases/tokenization.py, quebra_frases/chunks.py
generated: no
verify: python -m doctest -o NORMALIZE_WHITESPACE docs/inputs.md
see: words.md, sentences.md, performance.md
-->

This page shows what the splitters do with input at the edges. The edges are empty text, a value that is not a string, and no delimiters.

## Empty text and whitespace

Word, paragraph and whitespace splitting give an empty list for empty text and for whitespace. Sentence splitting gives one item, because every text holds at least one sentence, even an empty one.

```python
>>> from quebra_frases import (word_tokenize, sentence_tokenize,
...                            paragraph_tokenize, empty_space_tokenize)
>>> word_tokenize("   ")
[]
>>> paragraph_tokenize("")
[]
>>> empty_space_tokenize("  ")
[]
>>> sentence_tokenize("")
['']
>>> sentence_tokenize("   ")
['   ']

```

## Text that is not a string

Pass a `str`. A `None`, a `bytes` or a number raises an error, and the type of the error depends on the function. Catch `Exception` if your code must survive any input.

```python
>>> for function in (word_tokenize, sentence_tokenize, paragraph_tokenize):
...     try:
...         function(None)
...     except Exception as error:
...         print(function.__name__, type(error).__name__)
word_tokenize TypeError
sentence_tokenize TypeError
paragraph_tokenize AttributeError

```

## Chunks with no delimiters

`chunk` returns the whole text as one chunk when the delimiter list is empty, and an empty list for empty text.

```python
>>> from quebra_frases import chunk
>>> chunk("turn on the light", [])
['turn on the light']
>>> chunk("", ["light"])
[]

```

## Long text

The time of each splitter grows in a straight line with the length of the text. [Performance](performance.md) gives the times for texts up to 1,000,000 characters.

---

[Index](index.md) · Previous: [Comparing samples](comparing-samples.md) · Next: [Performance](performance.md)
