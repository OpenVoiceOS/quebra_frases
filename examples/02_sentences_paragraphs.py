"""Example — split text into sentences and paragraphs, keeping offsets.

Run::

    python examples/02_sentences_paragraphs.py
"""
from quebra_frases import (
    sentence_tokenize,
    span_indexed_sentence_tokenize,
    paragraph_tokenize,
    span_indexed_paragraph_tokenize,
)


def main() -> None:
    text = (
        "O Sr. Costa chegou a Lisboa às 9.30 da manhã. "
        "Comprou um bilhete por 4,50 euros. "
        "Será que apanhou o comboio? Apanhou, sim."
    )

    # Abbreviations (Sr.) and decimals (9.30) do not trigger a split.
    print("sentences:")
    for s in sentence_tokenize(text):
        print(f"  - {s}")

    print("\nsentence spans (sliced back from source):")
    for start, end, s in span_indexed_sentence_tokenize(text):
        assert text[start:end] == s
        print(f"  [{start:>3}:{end:<3}]  {s}")

    document = (
        "Era uma vez um moinho à beira-rio.\n"
        "O moleiro vivia ali sozinho.\n"
        "\n"
        "Um dia chegou um forasteiro.\n"
        "Trazia notícias de longe."
    )

    # Blank lines separate paragraphs; lines within a block stay together.
    paras = paragraph_tokenize(document)
    print(f"\n{len(paras)} paragraphs:")
    for i, p in enumerate(paras, 1):
        print(f"  ({i}) {p.strip()!r}")

    print("\nparagraph spans:")
    for start, end, p in span_indexed_paragraph_tokenize(document):
        print(f"  [{start:>3}:{end:<3}]  {p.strip()[:30]!r}")


if __name__ == "__main__":
    main()
