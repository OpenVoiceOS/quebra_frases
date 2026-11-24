# API reference

<!-- agent-hint
covers: every public function of quebra_frases with its signature, its return value and the page that explains it
source: quebra_frases/__init__.py, quebra_frases/tokenization.py, quebra_frases/chunks.py, quebra_frases/tokens.py, quebra_frases/list_utils.py, quebra_frases/version.py
generated: no
verify: python -c "import inspect,re,sys,quebra_frases as q; doc=set(re.findall(r'^\| \x60(\w+\(.*?\))\x60', open('docs/api.md').read(), re.M)); code={n+str(inspect.signature(o)) for n,o in vars(q).items() if inspect.isfunction(o) and n[0]!='_'}; sys.exit(doc!=code)" && python -m doctest -o NORMALIZE_WHITESPACE docs/api.md
see: docs/index.md, docs/getting-started.md
-->

This page lists every public function of quebra_frases, with its signature and what it returns. Each row links to the page that explains the function.

## Import names

`quebra_frases/__init__.py` imports every name from the four modules `tokens`, `list_utils`, `chunks` and `tokenization`, and `__version__` from `version`. Import the functions from the package.

```python
>>> from quebra_frases import sentence_tokenize, __version__
>>> isinstance(__version__, str)
True

```

The package defines no `__all__`. `from quebra_frases import *` therefore also imports the modules that the submodules import, such as `re`, `itertools`, `unicodedata` and `groupby`. The tables below list only the functions that the package defines.

## Tokenization

These functions are in `quebra_frases/tokenization.py`. A span is `(start, end, text)` with an exclusive end. A char index is `(start, text)`.

| Function | Returns | Page |
| --- | --- | --- |
| `word_tokenize(input_string)` | list of tokens | [Words](words.md) |
| `char_indexed_word_tokenize(input_string)` | list of `(start, token)` | [Words](words.md) |
| `span_indexed_word_tokenize(input_string)` | list of `(start, end, token)` | [Words](words.md) |
| `sentence_tokenize(input_string)` | list of sentences | [Sentences](sentences.md) |
| `char_indexed_sentence_tokenize(input_string)` | list of `(start, sentence)` | [Sentences](sentences.md) |
| `span_indexed_sentence_tokenize(input_string)` | list of `(start, end, sentence)` | [Sentences](sentences.md) |
| `paragraph_tokenize(input_string)` | list of paragraphs | [Paragraphs](paragraphs.md) |
| `char_indexed_paragraph_tokenize(input_string)` | list of `(start, paragraph)` | [Paragraphs](paragraphs.md) |
| `span_indexed_paragraph_tokenize(input_string)` | list of `(start, end, paragraph)` | [Paragraphs](paragraphs.md) |
| `empty_space_tokenize(input_string)` | list of the runs that are not whitespace | [Whitespace](whitespace.md) |
| `char_indexed_empty_space_tokenize(input_string)` | list of `(start, run)` | [Whitespace](whitespace.md) |
| `span_indexed_empty_space_tokenize(input_string)` | list of `(start, end, run)` | [Whitespace](whitespace.md) |
| `get_empty_spans(input_string)` | list of `(start, end, run)` for the whitespace runs | [Whitespace](whitespace.md) |

## Chunks

These functions are in `quebra_frases/chunks.py`.

| Function | Returns | Page |
| --- | --- | --- |
| `chunk(text, delimiters, strip=True)` | list of strings: the text cut at the delimiters, the delimiters included | [Chunks](chunks.md) |
| `find_spans(text, samples)` | list of `(start, end, sample)` for each sample in the text | [Chunks](chunks.md) |
| `chunk_list(some_list, delimiters)` | list of lists: the items between the delimiters | [Chunks](chunks.md) |
| `get_common_chunks(samples, squash=True)` | set of word runs, or one list per sample | [Comparing samples](comparing-samples.md) |
| `get_uncommon_chunks(samples, squash=True)` | set of word runs, or one list per sample | [Comparing samples](comparing-samples.md) |
| `get_exclusive_chunks(samples, squash=True)` | set of word runs, or one list per sample | [Comparing samples](comparing-samples.md) |

## Tokens

These functions are in `quebra_frases/tokens.py`.

| Function | Returns | Page |
| --- | --- | --- |
| `get_common_tokens(samples, squash=True)` | set of tokens, or one list per sample | [Comparing samples](comparing-samples.md) |
| `get_uncommon_tokens(samples, squash=True)` | set of tokens, or one list per sample | [Comparing samples](comparing-samples.md) |
| `get_exclusive_tokens(samples, squash=True)` | set of tokens, or one list per sample | [Comparing samples](comparing-samples.md) |

## List utilities

This function is in `quebra_frases/list_utils.py`.

| Function | Returns | Page |
| --- | --- | --- |
| `flatten(some_list, tuples=True)` | a flat list | this page |

`flatten` removes every level of nesting. With `tuples=True`, it also opens tuples. With `tuples=False`, a tuple stays whole when the list holds no nested list.

A string at the same level as a nested list splits into its characters: `flatten(["ab", ["c"]])` returns `['a', 'b', 'c']`.

```python
>>> from quebra_frases import flatten
>>> flatten([("A", "B"), ["C"], [["D", ["E", ["F"]]]]])
['A', 'B', 'C', 'D', 'E', 'F']
>>> flatten([("A", "B")], tuples=False)
[('A', 'B')]

```

## Version

`quebra_frases.__version__` is the package version as a string, such as `0.3.8a6`. `quebra_frases/version.py` builds it from `VERSION_MAJOR`, `VERSION_MINOR`, `VERSION_BUILD` and `VERSION_ALPHA`, and the release process rewrites those lines.

---

[Index](index.md) · Previous: [Comparing samples](comparing-samples.md) · Next: none
