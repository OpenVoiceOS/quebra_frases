# Chunks

<!-- agent-hint
covers: how chunk, find_spans and chunk_list cut a text or a token list at the delimiters a caller gives
source: quebra_frases/chunks.py:chunk, quebra_frases/chunks.py:find_spans, quebra_frases/chunks.py:chunk_list, test/test_chunking.py:test_chunk, test/test_chunking.py:TestReportedDefects
generated: no
verify: python -m doctest -o NORMALIZE_WHITESPACE docs/chunks.md
see: docs/comparing-samples.md, docs/api.md
-->

This page explains the three functions that cut at delimiters you give: `chunk` cuts a string, `find_spans` locates the delimiters in a string, and `chunk_list` cuts a list.

## Cut a string: chunk

`chunk(text, delimiters, strip=True)` cuts the text at each occurrence of a delimiter. The delimiters stay in the result as chunks of their own.

```python
>>> from quebra_frases import chunk
>>> chunk("turn on the light and the fan", ["light", "fan"])
['turn on the', 'light', 'and the', 'fan']

```

With `strip=True`, the function strips the whitespace from each chunk and drops the chunks that are empty. With `strip=False`, it returns the pieces as they are, empty strings included. The pieces then join to give the text back.

```python
>>> from quebra_frases import chunk
>>> chunk("turn on the light and the fan", ["light", "fan"], strip=False)
['turn on the ', 'light', ' and the ', 'fan', '']

```

A delimiter is a literal string, not a regular expression. The function escapes each delimiter, so "." matches only a period, and "+" or "(" does not raise an error. The tests check this.

```python
>>> from quebra_frases import chunk
>>> chunk("a.b|c", ["."])
['a', '.', 'b|c']
>>> chunk("a+b", ["+"])
['a', '+', 'b']

```

With no delimiters, the text is one chunk.

```python
>>> from quebra_frases import chunk
>>> chunk("ab", [])
['ab']

```

A delimiter matches anywhere in the text, also inside a word. At one position, the first delimiter in the list that matches wins.

```python
>>> from quebra_frases import chunk
>>> chunk("mycroftian", ["mycroft"])
['mycroft', 'ian']
>>> chunk("a b", ["a", "a b"])
['a', 'b']

```

## Locate the delimiters: find_spans

`find_spans(text, samples)` returns `(start, end, sample)` for each occurrence of a sample string in the text. It cuts the text the same way as `chunk(text, samples, strip=False)`.

```python
>>> from quebra_frases import find_spans
>>> find_spans("turn on the light and the fan", ["light", "fan"])
[(12, 17, 'light'), (26, 29, 'fan')]

```

## Cut a list: chunk_list

`chunk_list(some_list, delimiters)` groups the items between the delimiters. Unlike `chunk`, it drops the delimiters, and it returns no empty groups.

```python
>>> from quebra_frases import chunk_list
>>> chunk_list(['A', 'WORD', 'B', 'C', 'WORD', 'D'], ['WORD'])
[['A'], ['B', 'C'], ['D']]
>>> chunk_list(['WORD', 'A', 'WORD', 'WORD'], ['WORD'])
[['A']]

```

---

[Index](index.md) · Previous: [Whitespace](whitespace.md) · Next: [Comparing samples](comparing-samples.md)
