# 🛠️ API Reference

This document provides a detailed technical overview of all functions available in `quebra_frases`.

## Table of Contents
- [Tokenization](#tokenization)
  - [Word Tokenization](#word-tokenization)
  - [Sentence Tokenization](#sentence-tokenization)
  - [Paragraph Tokenization](#paragraph-tokenization)
  - [Empty Space Tokenization](#empty-space-tokenization)
- [Chunking](#chunking)
  - [Text Chunking](#text-chunking)
  - [List Chunking](#list-chunking)
  - [Token/Chunk Analysis](#tokenchunk-analysis)
- [Utilities](#utilities)

---

## Tokenization

### Word Tokenization

#### `word_tokenize(input_string)`
Returns a list of tokens (words and punctuation).
- **input_string**: The string to tokenize.

#### `char_indexed_word_tokenize(input_string)`
Returns a list of tuples `(start_index, token_content)`.

#### `span_indexed_word_tokenize(input_string)`
Returns a list of tuples `(start_index, end_index, token_content)`.

---

### Sentence Tokenization

#### `sentence_tokenize(input_string)`
Splits a string into a list of sentences. It uses a lookbehind/lookahead regex to avoid splitting on common abbreviations like `Mr.` or `i.e.` followed by a space.

#### `char_indexed_sentence_tokenize(input_string)`
Returns a list of tuples `(start_index, sentence_content)`.

#### `span_indexed_sentence_tokenize(input_string)`
Returns a list of tuples `(start_index, end_index, sentence_content)`.

---

### Paragraph Tokenization

#### `paragraph_tokenize(input_string)`
Splits a string into paragraphs. It preserves whitespace between paragraphs by appending it to the preceding paragraph.

#### `char_indexed_paragraph_tokenize(input_string)`
Returns a list of tuples `(start_index, paragraph_content)`.

#### `span_indexed_paragraph_tokenize(input_string)`
Returns a list of tuples `(start_index, end_index, paragraph_content)`.

---

### Empty Space Tokenization

#### `get_empty_spans(input_string)`
Returns the spans of all whitespace sequences in the string as `(start, end, content)`.

#### `empty_space_tokenize(input_string)`
Returns all non-whitespace "words", effectively splitting by any whitespace.

#### `span_indexed_empty_space_tokenize(input_string)`
Returns `(start, end, content)` for non-whitespace tokens.

---

## Chunking

### Text Chunking

#### `chunk(text, delimiters, strip=True)`
Splits a text by a list of delimiters. Delimiters are automatically regex-escaped.
- **text**: String to split.
- **delimiters**: List of strings to split by.
- **strip**: If `True`, removes leading/trailing whitespace from resulting chunks.

#### `find_spans(text, samples)`
Finds the start and end indices of specific `samples` within a `text`.

---

### List Chunking

#### `chunk_list(some_list, delimiters)`
Splits a list into sub-lists whenever an element matches a delimiter.
- **some_list**: The list to split.
- **delimiters**: Elements that trigger a split.

---

### Token/Chunk Analysis

These functions analyze a list of sample strings to find commonalities.

#### `get_common_tokens(samples, squash=True)`
Returns tokens that appear in **all** samples.
- **squash**: If `True` (default), returns a unique `set`. If `False`, returns a list of lists.

#### `get_uncommon_tokens(samples, squash=True)`
Returns tokens that are **not** present in at least one other sample.

#### `get_exclusive_tokens(samples, squash=True)`
Returns tokens that appear in **only one** sample.

#### `get_common_chunks(samples, squash=True)`
Similar to `get_common_tokens` but joins consecutive tokens into phrase chunks.

#### `get_uncommon_chunks(samples, squash=True)`
Similar to `get_uncommon_tokens` but joins consecutive tokens into phrase chunks.

#### `get_exclusive_chunks(samples, squash=True)`
Similar to `get_exclusive_tokens` but joins consecutive tokens into phrase chunks.

---

## Utilities

#### `flatten(some_list)`
Recursively flattens any nested list or tuple structure into a single flat list.
