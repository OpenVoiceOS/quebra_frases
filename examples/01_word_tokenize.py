"""Example — split text into words and punctuation, with char offsets.

Run::

    python examples/01_word_tokenize.py
"""
from quebra_frases import (
    word_tokenize,
    char_indexed_word_tokenize,
    span_indexed_word_tokenize,
)


def main() -> None:
    text = "O Pedro comprou 2 pastéis de nata por 1,50 euros!"

    # Plain tokens: words and punctuation come out as separate items.
    print("tokens:", word_tokenize(text))

    # char_indexed_* keeps the start offset of every token.
    print("\nchar-indexed:")
    for start, tok in char_indexed_word_tokenize(text):
        print(f"  {start:>3}  {tok!r}")

    # span_indexed_* gives (start, end) so you can slice back into the source.
    print("\nspan-indexed (sliced back from source):")
    for start, end, tok in span_indexed_word_tokenize(text):
        assert text[start:end] == tok
        print(f"  [{start:>2}:{end:<2}]  {tok!r}")

    # Numbers with decimal commas and percent-style markers stay grouped.
    print("\nnumbers:", word_tokenize("São 3,14 metros e 100% certos"))


if __name__ == "__main__":
    main()
