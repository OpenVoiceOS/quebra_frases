# Quebra Frases

`quebra_frases` chunks strings into byte sized pieces. 

It provides robust tokenization for words, sentences, and paragraphs, with support for span indexing (getting start/end character indices).

## 🚀 Zero to Hero

New to `quebra_frases`? Check out our **[Getting Started Guide](./docs/GETTING_STARTED.md)** to go from zero to hero!

For a full technical list of functions, see the **[API Reference](./docs/API.md)**.

## ✨ Features

- **Robust Word Tokenization**: Handles version numbers (`v1.0.1`), abbreviations (`Ph.D.`), hyphenated words (`state-of-the-art`), and complex punctuation.
- **Span Indexing**: Every tokenizer has a `span_indexed_` version that returns exact character offsets—essential for highlighting or entity extraction.
- **Smart Sentence Splitting**: Avoids splitting on common abbreviations and decimals.
- **Advanced Chunking**: Split text by custom delimiters (regex-safe) or find common/exclusive chunks between multiple samples.

## 📦 Usage

### Tokenization

```python
import quebra_frases

sentence = "sometimes i develop stuff for mycroft, mycroft is FOSS!"
print(quebra_frases.word_tokenize(sentence))
# ['sometimes', 'i', 'develop', 'stuff', 'for', 'mycroft', ',', 
# 'mycroft', 'is', 'FOSS', '!']

# Get exact character indices!
print(quebra_frases.span_indexed_word_tokenize(sentence))
# [(0, 9, 'sometimes'), (10, 11, 'i'), (12, 19, 'develop'), ...]
```

### Sentence & Paragraphs

```python
test_sent = "Mr. Smith bought cheapsite.com for 1.5 million dollars. Did he mind?"
print(quebra_frases.sentence_tokenize(test_sent))
# ['Mr. Smith bought cheapsite.com for 1.5 million dollars.', 'Did he mind?']
```

### Chunking

```python
delimiters = ["mycroft"]
sentence = "sometimes i develop stuff for mycroft, mycroft is FOSS!"
print(quebra_frases.chunk(sentence, delimiters))
# ['sometimes i develop stuff for', 'mycroft', ',', 'mycroft', 'is FOSS!']
```

## 🛠️ Install

```bash
pip install quebra_frases
```