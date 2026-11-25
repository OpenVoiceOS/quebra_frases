# quebra_frases

<!-- agent-hint
covers: what quebra_frases does, how to install it, and a quickstart that runs on a clean install
source: quebra_frases/tokenization.py, quebra_frases/chunks.py, pyproject.toml
generated: no
verify: python -m doctest -o NORMALIZE_WHITESPACE readme.md
see: docs/index.md, docs/getting-started.md, AGENTS.md
-->

quebra_frases splits text into words, sentences, paragraphs and chunks. Each splitter also has a form that returns the character offsets of each piece. The sentence splitter knows abbreviations, initials, unit symbols and ordinals, and it splits scripts that write no space between sentences.

## Quickstart

```bash
pip install --pre quebra_frases
```

```python
>>> from quebra_frases import word_tokenize, sentence_tokenize, chunk
>>> word_tokenize("O Pedro pagou 2,50 € às 14:30.")
['O', 'Pedro', 'pagou', '2,50', '€', 'às', '14:30', '.']
>>> sentence_tokenize("Mr. Smith paid 1.5 million. Did he mind?")
['Mr. Smith paid 1.5 million.', 'Did he mind?']
>>> chunk("turn on the light and the fan", ["light", "fan"])
['turn on the', 'light', 'and the', 'fan']

```

The package needs Python 3.11 or later, and its only dependency is `regex`. The `--pre` flag installs the latest alpha release.

## Documentation

Start with [Getting started](docs/getting-started.md). The [documentation index](docs/index.md) lists every page in reading order, and the [API reference](docs/api.md) lists every public function.

The [performance page](docs/performance.md) shows the time of each splitter by text length, and the [inputs page](docs/inputs.md) shows what happens with empty text and with a value that is not a string.

The `examples/` folder holds five scripts that you can run: word tokens, sentences and paragraphs, whitespace spans, chunking, and sample comparison.

## License

Apache-2.0. See [LICENSE](LICENSE).
