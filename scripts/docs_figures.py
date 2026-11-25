"""Write the figures of docs/ from the repository's own data.

    python scripts/docs_figures.py            # write docs/figures/*.svg
    python scripts/docs_figures.py --check    # exit 1 when a committed SVG differs from a fresh one
    python scripts/docs_figures.py --measure  # time the splitters again and write docs/figures/timings.tsv

Input: ``docs/figures/timings.tsv``, the median of 5 runs of each splitter on
texts of 1,000 to 1,000,000 characters, written by ``--measure``.
Output: ``docs/figures/timing-by-length.svg``.

The SVG file holds no timestamp, so two runs write the same bytes. A run of
``--measure`` gives other numbers on each machine, so only ``--measure``
changes ``timings.tsv``.
"""
import math
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / "docs" / "figures"
TIMINGS = FIGURES / "timings.tsv"
FUNCTIONS = ["word_tokenize", "sentence_tokenize", "empty_space_tokenize", "paragraph_tokenize"]
LENGTHS = [1_000, 10_000, 100_000, 1_000_000]
UNIT = "Mr. Smith paid 1.5 million for the house at 14:30 on Mar. 3rd. Did he mind? No, he did not!\n\n"

TEXT = "#808080"
GRID = "#80808055"
COLOURS = ["#4C8DD6", "#E0883A", "#A66CC9", "#4FA777"]
FONT = 'font-family="sans-serif" font-size="15"'


def svg(width: int, height: int, title: str, description: str, body: list) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
            f'height="{height}" role="img" aria-labelledby="t d">\n<title id="t">{title}</title>\n'
            f'<desc id="d">{description}</desc>\n' + "\n".join(body) + "\n</svg>\n")


def text(x, y, content, anchor="start", fill=TEXT) -> str:
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" {FONT}>{content}</text>'


def timing_by_length() -> str:
    rows = [line.split("\t") for line in TIMINGS.read_text(encoding="utf-8").splitlines()[1:]]
    data = {name: {} for name in FUNCTIONS}
    for name, length, ms in rows:
        data[name][int(length)] = float(ms)
    left, right, top, bottom = 70, 150, 50, 50
    width, height = 720, 380
    plot_w, plot_h = width - left - right, height - top - bottom
    x_low, x_high = 3, 6        # log10 of the length
    y_low, y_high = -2, 3       # log10 of the milliseconds: 0.01 ms to 1,000 ms

    def x(length):
        return left + (math.log10(length) - x_low) / (x_high - x_low) * plot_w

    def y(ms):
        return top + plot_h - (math.log10(ms) - y_low) / (y_high - y_low) * plot_h

    body = []
    for length in LENGTHS:
        body.append(f'<line x1="{x(length):.1f}" y1="{top}" x2="{x(length):.1f}" y2="{top + plot_h}" stroke="{GRID}"/>')
        body.append(text(f"{x(length):.1f}", top + plot_h + 22, f"{length:,}", "middle"))
    for power, label in ((-2, "0.01"), (-1, "0.1"), (0, "1"), (1, "10"), (2, "100"), (3, "1,000")):
        body.append(f'<line x1="{left}" y1="{y(10 ** power):.1f}" x2="{left + plot_w}" y2="{y(10 ** power):.1f}" stroke="{GRID}"/>')
        body.append(text(left - 8, f"{y(10 ** power) + 5:.1f}", label, "end"))
    body.append(text(left, 20, "milliseconds"))
    body.append(text(left + plot_w, height - 8, "characters", "end"))
    for colour, name in zip(COLOURS, FUNCTIONS):
        points = " ".join(f"{x(length):.1f},{y(data[name][length]):.1f}" for length in LENGTHS)
        body.append(f'<polyline points="{points}" fill="none" stroke="{colour}" stroke-width="3"/>')
        for length in LENGTHS:
            body.append(f'<circle cx="{x(length):.1f}" cy="{y(data[name][length]):.1f}" r="4" fill="{colour}"/>')
    label_y = {}
    for name in sorted(FUNCTIONS, key=lambda n: y(data[n][LENGTHS[-1]])):
        wanted = y(data[name][LENGTHS[-1]]) + 5
        label_y[name] = max(wanted, max(label_y.values(), default=-99) + 18)
    for colour, name in zip(COLOURS, FUNCTIONS):
        body.append(text(left + plot_w + 12, f"{label_y[name]:.1f}", name.removesuffix("_tokenize"), "start", colour))
    summary = "; ".join(f"{name} {data[name][1000]:.2g} ms at 1,000 characters and {data[name][1_000_000]:.3g} ms at 1,000,000"
                        for name in FUNCTIONS)
    return svg(width, height, "Time of the splitters by text length",
               f"Median milliseconds on a log scale for texts of 1,000 to 1,000,000 characters: {summary}.", body)


def measure() -> None:
    import quebra_frases

    lines = ["function\tcharacters\tmedian ms of 5 runs"]
    for name in FUNCTIONS:
        function = getattr(quebra_frases, name)
        for length in LENGTHS:
            sample = (UNIT * (length // len(UNIT) + 1))[:length]
            times = []
            for _ in range(5):
                start = time.perf_counter()
                function(sample)
                times.append((time.perf_counter() - start) * 1000)
            lines.append(f"{name}\t{length}\t{statistics.median(times):.4f}")
    TIMINGS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv) -> int:
    if argv == ["--measure"]:
        measure()
        return 0
    if argv not in ([], ["--check"]):
        print(__doc__)
        return 2
    path = FIGURES / "timing-by-length.svg"
    fresh = timing_by_length()
    if argv:
        if not path.exists() or path.read_text(encoding="utf-8") != fresh:
            print(f"{path} is out of date: run python scripts/docs_figures.py")
            return 1
        return 0
    path.write_text(fresh, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
