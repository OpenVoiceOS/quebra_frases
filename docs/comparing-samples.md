# Comparing samples

<!-- agent-hint
covers: how the get_*_tokens and get_*_chunks functions find the words and word runs that a list of sample sentences share or do not share
source: quebra_frases/tokens.py, quebra_frases/chunks.py:get_common_chunks, quebra_frases/chunks.py:get_uncommon_chunks, quebra_frases/chunks.py:get_exclusive_chunks, test/test_chunking.py:test_get_tokens, test/test_chunking.py:test_get_chunks
generated: no
verify: python -m doctest -o NORMALIZE_WHITESPACE docs/comparing-samples.md
see: docs/chunks.md, docs/words.md, docs/api.md
-->

This page explains the six functions that compare a list of sample sentences. They find the words, or the runs of words, that the samples share and that they do not share.

## Compare the tokens

Each function splits every sample with [`word_tokenize`](words.md) and compares each sample with the other samples.

| Function | The tokens of a sample that it keeps |
| --- | --- |
| `get_common_tokens(samples, squash=True)` | the tokens that every other sample has |
| `get_uncommon_tokens(samples, squash=True)` | the tokens that at least one other sample does not have |
| `get_exclusive_tokens(samples, squash=True)` | the tokens that no other sample has |

With `squash=True`, the result is one set of all the kept tokens. With `squash=False`, the result is one list per sample, in the order of the samples, with the tokens in text order.

```python
>>> from quebra_frases import get_common_tokens, get_uncommon_tokens, get_exclusive_tokens
>>> samples = ["what do you dream about",
...            "what did you dream about",
...            "what are your dreams about"]
>>> get_common_tokens(samples, squash=False)
[['what', 'about'], ['what', 'about'], ['what', 'about']]
>>> get_uncommon_tokens(samples, squash=False)
[['do', 'you', 'dream'], ['did', 'you', 'dream'], ['are', 'your', 'dreams']]
>>> get_exclusive_tokens(samples, squash=False)
[['do'], ['did'], ['are', 'your', 'dreams']]
>>> sorted(get_exclusive_tokens(samples))
['are', 'did', 'do', 'dreams', 'your']

```

The set that `squash=True` returns has no fixed order. Sort it when the order matters.

The other samples of a sample are the samples that differ from it as strings. A copy of the same sample does not count. When all the samples are the same string, every token is common.

```python
>>> from quebra_frases import get_common_tokens
>>> sorted(get_common_tokens(["a b", "a b"]))
['a', 'b']

```

## Compare the word runs

The chunk functions cut each sample at the tokens of one group, then join the words of each run with one space.

| Function | Where it cuts each sample |
| --- | --- |
| `get_common_chunks(samples, squash=True)` | at the uncommon tokens |
| `get_uncommon_chunks(samples, squash=True)` | at the common tokens |
| `get_exclusive_chunks(samples, squash=True)` | at the tokens that are common or uncommon, but not exclusive |

The `squash` argument works as it does for the token functions.

```python
>>> from quebra_frases import get_common_chunks, get_uncommon_chunks, get_exclusive_chunks
>>> samples = ["what do you dream about",
...            "what did you dream about",
...            "what are your dreams about"]
>>> get_common_chunks(samples, squash=False)
[['what', 'about'], ['what', 'about'], ['what', 'about']]
>>> get_uncommon_chunks(samples, squash=False)
[['do you dream'], ['did you dream'], ['are your dreams']]
>>> get_exclusive_chunks(samples, squash=False)
[['do'], ['did'], ['are your dreams']]

```

The join puts one space between all tokens, punctuation included. The chunks are not slices of the samples.

```python
>>> from quebra_frases import get_common_chunks
>>> get_common_chunks(["hello, world", "hello, there"], squash=False)
[['hello ,'], ['hello ,']]

```

---

[Index](index.md) · Previous: [Chunks](chunks.md) · Next: [API reference](api.md)
