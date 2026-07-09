# 🚀 Quebra Frases: Zero to Hero

Welcome to **quebra_frases**! Whether you are a total beginner looking to split some text or an advanced NLP developer needing precise control over tokens and spans, you're in the right place.

## 📖 Table of Contents
1. [What is Quebra Frases?](#what-is-quebra-frases)
2. [Quick Start (For Noobs)](#quick-start-for-noobs)
3. [Tokenization Deep Dive](#tokenization-deep-dive)
4. [Advanced Chunking](#advanced-chunking)
5. [Working with Spans (For Advanced Devs)](#working-with-spans-for-advanced-devs)
6. [Best Practices](#best-practices)

---

## 1. What is Quebra Frases?
In Portuguese, "Quebra Frases" means "Phrase Breaker". It is a lightweight, regex-based Python library designed to chunk strings into byte-sized pieces. It handles:
- **Words**: Splitting sentences into individual words and punctuation.
- **Sentences**: Intelligently splitting paragraphs into sentences.
- **Paragraphs**: Splitting text into paragraphs.
- **Chunks**: Grouping text based on specific delimiters or commonalities.

---

## 2. Quick Start (For Noobs)

### Installation
```bash
pip install quebra_frases
```

### Your first script
If you just want to get the words in a sentence, it's this easy:

```python
import quebra_frases

text = "Hello world! This is easy."
words = quebra_frases.word_tokenize(text)
print(words)
# Output: ['Hello', 'world', '!', 'This', 'is', 'easy', '.']
```

Want sentences instead?
```python
sentences = quebra_frases.sentence_tokenize(text)
print(sentences)
# Output: ['Hello world!', 'This is easy.']
```

---

## 3. Tokenization Deep Dive

`quebra_frases` uses a powerful internal regex that handles many real-world edge cases:

- **Version Numbers**: `v1.2.3` stays together.
- **Abbreviations**: `Ph.D.` and `i.e.` are treated as single tokens.
- **Hyphenated Words**: `state-of-the-art` is one token.
- **Numbers & Punctuation**: Correctly handles decimals (`1.5`) and separate punctuation.

### Paragraph Tokenization
Splitting by newlines can be tricky. `quebra_frases` handles multiple newlines and preserves indentation logic:

```python
text = "First paragraph.\n\nSecond one starts here."
paras = quebra_frases.paragraph_tokenize(text)
```

---

## 4. Advanced Chunking

Chunking is where you split text based on specific words or find what's common between multiple strings.

### Splitting by Delimiters
```python
text = "I like apples, but I hate oranges."
# Split whenever "but" is found
chunks = quebra_frases.chunk(text, delimiters=["but"])
print(chunks)
# Output: ['I like apples,', 'but', 'I hate oranges.']
```

### Finding Common/Exclusive Chunks
Imagine you have several similar voice commands:
```python
samples = [
    "turn on the kitchen light",
    "turn off the kitchen light",
    "brighten the kitchen light"
]

common = quebra_frases.get_common_chunks(samples)
# Returns things like {"the kitchen light"}
```

---

## 5. Working with Spans (For Advanced Devs)

For many NLP tasks, knowing the *content* isn't enough; you need to know *where* it is in the original string. This is where **Span Indexing** comes in.

Most functions have a `span_indexed_` version:

```python
text = "Hello world"
spans = quebra_frases.span_indexed_word_tokenize(text)

for start, end, content in spans:
    print(f"Found '{content}' at indices {start}:{end}")
    # Verify: 
    assert text[start:end] == content
```

### Why use Spans?
1. **Highlighting**: Useful for UI applications to highlight specific words.
2. **Entity Extraction**: If you find a "Date" entity, you need the exact indices to replace or label it.
3. **Non-destructive cleaning**: You can modify parts of a string without losing track of the rest.

---

## 6. Best Practices

- **Performance**: While regex is fast, if you are processing gigabytes of text, consider batching your calls.
- **Regex Safety**: If you use the `chunk` function with user-provided delimiters, `quebra_frases` automatically escapes them for you, so you don't have to worry about regex injection.
- **Python Versions**: Works on Python 3.6 through 3.11+.

---

## Next Steps
Check out the [API Reference](./API.md) for a full list of available functions and their parameters.
