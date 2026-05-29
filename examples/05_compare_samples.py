"""Example — compare several utterances to find shared and distinctive parts.

Run::

    python examples/05_compare_samples.py
"""
from quebra_frases import (
    get_common_tokens,
    get_uncommon_tokens,
    get_exclusive_tokens,
    get_common_chunks,
    get_uncommon_chunks,
)


def main() -> None:
    samples = [
        "qual é a temperatura na cozinha",
        "qual é a temperatura na sala",
        "qual é a temperatura no quarto",
    ]

    # Tokens that appear in every sample.
    print("common tokens:", sorted(get_common_tokens(samples)))

    # Tokens missing from at least one sample.
    print("uncommon tokens:", sorted(get_uncommon_tokens(samples)))

    # Tokens unique to a single sample (appear nowhere else).
    print("exclusive tokens:", sorted(get_exclusive_tokens(samples)))

    # Chunks are word-runs grouped by the comparison: the shared scaffold...
    print("\ncommon chunks:", sorted(get_common_chunks(samples)))

    # ...versus the parts that vary between utterances.
    print("uncommon chunks:", sorted(get_uncommon_chunks(samples)))


if __name__ == "__main__":
    main()
