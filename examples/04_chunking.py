"""Example — split on custom delimiters and locate the pieces in the source.

Run::

    python examples/04_chunking.py
"""
from quebra_frases import chunk, chunk_list, find_spans, word_tokenize


def main() -> None:
    text = "ligar a luz; baixar as persianas, e tocar música"

    # chunk() splits on any of the given delimiter strings, stripped by default.
    print("chunks:", chunk(text, [";", ","]))

    # strip=False keeps the delimiters and surrounding whitespace as tokens.
    print("\nraw (strip=False):", chunk(text, [";", ","], strip=False))

    # chunk_list() groups an already-tokenized list, dropping the delimiters.
    tokens = word_tokenize("acende a luz e toca uma canção")
    groups = chunk_list(tokens, ["e"])
    print("\ntoken groups around 'e':", groups)

    # find_spans() returns (start, end, text) for delimiter pieces present
    # in the sample set, so you can map matches back onto the source.
    text2 = "azul,verde,azul,vermelho"
    print("\nspans of known colours:")
    for start, end, piece in find_spans(text2, ["azul", "verde"]):
        assert text2[start:end] == piece
        print(f"  [{start:>2}:{end:<2}]  {piece!r}")


if __name__ == "__main__":
    main()
