# Performance

<!-- agent-hint
covers: how long each splitter takes for texts of 1,000 to 1,000,000 characters, and how to measure it
source: scripts/docs_figures.py, docs/figures/timings.tsv
generated: no, but docs/figures/timing-by-length.svg comes from scripts/docs_figures.py and docs/figures/timings.tsv from its --measure run. Edit the script, not the output
verify: python scripts/docs_figures.py --check && python -m doctest -o NORMALIZE_WHITESPACE docs/performance.md
see: inputs.md, words.md, sentences.md
-->

This page shows how the time of each splitter grows with the length of the text, and how to measure it on your machine. The numbers come from one laptop, so read the shape, not the digits.

## Time grows in a straight line

The figure times four splitters on texts of 1,000 to 1,000,000 characters. The text repeats a sentence with an abbreviation, a number, a time and a question.

![Lines on a log-log scale of the median milliseconds for texts of 1,000 to 1,000,000 characters. At 1,000 characters: sentence 0.27, word 0.2, empty_space 0.057, paragraph 0.0075. At 1,000,000 characters: sentence 258, word 192, empty_space 83, paragraph 7.3.](figures/timing-by-length.svg)

*Figure: the median of 5 runs for each splitter. Read the slope: each line rises by a factor of 10 for each factor of 10 in length, so the cost for each character stays the same.*

At 1,000,000 characters the sentence splitter takes about a quarter of a second, and the paragraph splitter takes under 10 ms. A text of one page, about 3,000 characters, takes under a millisecond to split into sentences.

## Measure on your machine

From the root of a checkout, run:

```bash
python scripts/docs_figures.py --measure
```

The command times each splitter 5 times on each length, and writes `docs/figures/timings.tsv`. Run `python scripts/docs_figures.py` to draw the figure from that file.

```python
>>> import time
>>> from quebra_frases import sentence_tokenize
>>> start = time.perf_counter()
>>> count = len(sentence_tokenize("Mr. Smith paid 1.5 million. Did he mind? " * 1000))
>>> count
2000
>>> time.perf_counter() - start < 5
True

```

---

[Index](index.md) · Previous: [Empty text, wrong types and long text](inputs.md) · Next: [API reference](api.md)
