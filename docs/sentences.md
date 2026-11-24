# Sentences

<!-- agent-hint
covers: what sentence_tokenize and its indexed forms return, what happens to the whitespace between sentences, and what the tests guarantee
source: quebra_frases/tokenization.py:sentence_tokenize, quebra_frases/tokenization.py:span_indexed_sentence_tokenize, test/test_tokenization.py:TestSentenceTokenize
generated: no
verify: python -m doctest -o NORMALIZE_WHITESPACE docs/sentences.md
see: docs/sentence-boundaries.md, docs/paragraphs.md, docs/api.md
-->

This page explains the sentence splitter: the three functions, the shape of their output, and what a caller can rely on.

The rules that pick each split point are in [How a sentence boundary is decided](sentence-boundaries.md).

## The three functions

The three functions find the same sentences. They differ only in the shape of each item.

| Function | One item |
| --- | --- |
| `sentence_tokenize(input_string)` | the sentence |
| `char_indexed_sentence_tokenize(input_string)` | `(start, sentence)` |
| `span_indexed_sentence_tokenize(input_string)` | `(start, end, sentence)` |

```python
>>> from quebra_frases import sentence_tokenize, char_indexed_sentence_tokenize, span_indexed_sentence_tokenize
>>> text = "Mr. Smith bought cheapsite.com for 1.5 million dollars. Did he mind?"
>>> sentence_tokenize(text)
['Mr. Smith bought cheapsite.com for 1.5 million dollars.', 'Did he mind?']
>>> char_indexed_sentence_tokenize(text)
[(0, 'Mr. Smith bought cheapsite.com for 1.5 million dollars.'), (56, 'Did he mind?')]
>>> span_indexed_sentence_tokenize(text)
[(0, 55, 'Mr. Smith bought cheapsite.com for 1.5 million dollars.'), (56, 68, 'Did he mind?')]

```

## The whitespace between sentences

The splitter removes the whitespace run between two sentences. The sentences keep all other characters. The spans give the true position of each sentence, also when more than one space separates them.

```python
>>> from quebra_frases import sentence_tokenize, span_indexed_sentence_tokenize
>>> sentence_tokenize("One.  Two.")
['One.', 'Two.']
>>> span_indexed_sentence_tokenize("One.  Two.")
[(0, 4, 'One.'), (6, 10, 'Two.')]

```

Chinese and Japanese write no space after a sentence. The splitter splits after their sentence marks without one, and a closing quote stays with its sentence.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("他说：“我来了。”她笑了。")
['他说：“我来了。”', '她笑了。']

```

Whitespace at the start of the text stays with the first sentence. When the text ends with whitespace after its last sentence mark, the list ends with an empty string. Strip the text first if you do not want it.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("  Olá. Tudo bem?  ")
['  Olá.', 'Tudo bem?', '']
>>> sentence_tokenize("  Olá. Tudo bem?  ".strip())
['Olá.', 'Tudo bem?']

```

An empty text gives a list with one empty string.

```python
>>> from quebra_frases import sentence_tokenize
>>> sentence_tokenize("")
['']

```

## What a caller can rely on

The code and the tests hold these properties:

- The text between two sentences is always a whitespace run, or nothing for Chinese and Japanese. Each sentence is a slice of the input. `sentence_tokenize` builds the list this way, and `test_join_lossless` and `test_chinese_split_is_lossless` check it.
- In `span_indexed_sentence_tokenize`, `text[start:end]` always equals the sentence. The function builds each item from that slice, and `test_sentence_spans_survive_a_double_space` checks the offsets.
- `char_indexed_sentence_tokenize` returns the start and the sentence of each `span_indexed_sentence_tokenize` item.

---

[Index](index.md) · Previous: [Words](words.md) · Next: [How a sentence boundary is decided](sentence-boundaries.md)
