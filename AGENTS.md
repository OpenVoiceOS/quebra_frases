# AGENTS.md

quebra_frases splits text into words, sentences, paragraphs and chunks, with the character offsets of each piece. It is a pure Python library with one dependency, `regex`.

## Map

| Path | What it holds |
| --- | --- |
| `quebra_frases/tokenization.py` | The word, sentence, paragraph and whitespace splitters. The abbreviation, unit and vowel lists, with their sources. |
| `quebra_frases/chunks.py` | The functions `chunk`, `chunk_list`, `find_spans` and the `get_*_chunks` functions |
| `quebra_frases/tokens.py` | the `get_*_tokens` functions |
| `quebra_frases/list_utils.py` | `flatten` |
| `quebra_frases/version.py` | The version. The release process rewrites the version block. |
| `test/` | the unittest suite, run with pytest |
| `scripts/docs_figures.py` | Writes the SVG figure of `docs/figures/`, and with `--measure` the timings that it draws |
| `examples/` | five scripts that run each kind of split |
| `docs/` | The user documentation. `docs/index.md` gives the reading order. |

## Setup and test

```bash
uv venv .venv
VIRTUAL_ENV=.venv uv pip install --prerelease=allow -e '.[test]'
.venv/bin/python -m pytest test
```

CI runs the same suite on Python 3.11, 3.12, 3.13 and 3.14 (`.github/workflows/build_tests.yml`).

## Rules the code and the tests hold

- Every character that is not whitespace is in exactly one word token. No token holds whitespace. `TestWordTokenizeCoverage` checks both over sentences in many scripts, and the first over every code point. See [docs/words.md](docs/words.md).
- `sentence_tokenize` removes only the whitespace between sentences. `test_join_lossless` and `test_chinese_split_is_lossless` check it. See [docs/sentences.md](docs/sentences.md).
- The module docstring of `tokenization.py` names the source of each unit symbol. Its comments give the reason for the vowel letters and the capital abbreviations. [docs/sentence-boundaries.md](docs/sentence-boundaries.md) repeats those lists and sources. Change the page together with the code.
- A `chunk` delimiter is a literal string, not a pattern. `TestReportedDefects` checks it. See [docs/chunks.md](docs/chunks.md).
- Do not edit the version block in `quebra_frases/version.py` by hand. The release process rewrites it.
- The package supports Python 3.11 and later (`requires-python` in `pyproject.toml`).

## Checks before a push

Run the test suite, then the `verify` command of each page you changed. Each page holds it in the `agent-hint` comment under its title. Most pages verify with doctest:

```bash
.venv/bin/python -m pytest test
for f in readme.md docs/*.md; do [ "$f" = docs/index.md ] || .venv/bin/python -m doctest -o NORMALIZE_WHITESPACE "$f" || echo "FAIL $f"; done
```

`docs/figures/timing-by-length.svg` comes from `docs/figures/timings.tsv`. After a docs change, run `python scripts/docs_figures.py --check`.

`docs/index.md` and `docs/api.md` have extra checks: the index table must list every page, and the API tables must list every public function with its exact signature.
