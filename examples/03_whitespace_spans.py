"""Example — whitespace-aware tokenizing and locating the gaps between words.

Run::

    python examples/03_whitespace_spans.py
"""
from quebra_frases import (
    empty_space_tokenize,
    span_indexed_empty_space_tokenize,
    char_indexed_empty_space_tokenize,
    get_empty_spans,
)


def main() -> None:
    text = "isto   tem \t vários \n\t espaços   estranhos"

    # Split purely on whitespace runs, no matter how wide or mixed.
    print("tokens:", empty_space_tokenize(text))

    # Span variant: exact (start, end) of every non-space run.
    print("\nword spans (sliced back from source):")
    for start, end, tok in span_indexed_empty_space_tokenize(text):
        assert text[start:end] == tok
        print(f"  [{start:>2}:{end:<2}]  {tok!r}")

    # char_indexed_* drops the end offset, keeping just the start.
    print("\nchar-indexed:", char_indexed_empty_space_tokenize(text))

    # get_empty_spans is the inverse view: the whitespace gaps themselves.
    print("\nwhitespace gaps:")
    for start, end, gap in get_empty_spans(text):
        print(f"  [{start:>2}:{end:<2}]  {gap!r}")


if __name__ == "__main__":
    main()
