# quebra_frases documentation

<!-- agent-hint
covers: the reading order of the hand-written docs pages, one line per page
source: docs/
generated: no
verify: diff <(ls docs/*.md | sed 's|docs/||' | grep -v '^index\.md$' | sort) <(grep -o '^| \[[^]]*\]([a-z-]*\.md)' docs/index.md | sed 's/.*(//; s/)$//' | sort)
see: readme.md, docs/getting-started.md
-->

quebra_frases splits text into words, sentences, paragraphs and chunks, with the character offsets of each piece. Read the pages in this order.

| Page | What you get there |
| --- | --- |
| [Getting started](getting-started.md) | Install the package and run each kind of split once, with real output. |
| [Words](words.md) | What one word token is, and what the word tokenizer guarantees. |
| [Sentences](sentences.md) | The sentence functions, the whitespace between sentences, and what they guarantee. |
| [How a sentence boundary is decided](sentence-boundaries.md) | Every rule that keeps or rejects a split point, with the abbreviation and unit lists and their sources. |
| [Paragraphs](paragraphs.md) | How blank lines split a text into paragraphs. |
| [Whitespace](whitespace.md) | The split on whitespace runs, and the whitespace runs themselves. |
| [Chunks](chunks.md) | Cut a string or a list at the delimiters you give. |
| [Comparing samples](comparing-samples.md) | Find the words and word runs that sample sentences share or do not share. |
| [Empty text, wrong types and long text](inputs.md) | What each splitter returns for empty text, for a value that is not a string, and for no delimiters. |
| [Performance](performance.md) | How the time of each splitter grows with the length of the text, and how to measure it. |
| [API reference](api.md) | Every public function, with its signature and return value. |

---

[Index](index.md) · Previous: none · Next: [Getting started](getting-started.md)
