import regex as re
from itertools import groupby


_WORD_REGEX = re.compile(r"(?:-?\d+(?:[,.:\/]\d*)+)|\b\p{L}*(?:\.\p{L}+)+\.|[\p{L}\p{N}'-]+|[.,;:_!?<>|()=\[\]{}»«*~^`%\/\\\+#]", re.I)
_SENTENCE_SPLIT_CANDIDATE = re.compile(r'(?<=[.?])\s')
_VOWELS = set("aeiouyAEIOUYáàâãéêíóôõúüÁÀÂÃÉÊÍÓÔÕÚÜ")
_ABBREVIATIONS = {"sra", "dra", "exmo", "exma", "etc", "ex", "pp", "vs", "av", "num"}


def _is_abbreviation(word):
    # a period does not end a sentence when the token before it is:
    # - a single letter (initials: "D.", "J.")
    # - a consonant-only token (abbreviations like "Dr.", "Srs.")
    # - a known short abbreviation that the two rules above miss
    if not word:
        return False
    if len(word) == 1:
        return True
    if not any(ch in _VOWELS for ch in word):
        return True
    return word.lower() in _ABBREVIATIONS


def word_tokenize(input_string):
    return [m.group() for m in re.finditer(_WORD_REGEX, input_string)]


def char_indexed_word_tokenize(input_string):
    return [(m.start(0), m.group())
            for m in re.finditer(_WORD_REGEX, input_string)]


def span_indexed_word_tokenize(input_string):
    return [(m.start(0), m.end(0), m.group())
            for m in re.finditer(_WORD_REGEX, input_string)]


def sentence_tokenize(input_string):
    sentences = []
    last = 0
    for m in _SENTENCE_SPLIT_CANDIDATE.finditer(input_string):
        split_at = m.start()
        if input_string[split_at - 1] == '.':
            j = split_at - 2
            while j >= 0 and (input_string[j].isalpha() or input_string[j] == "'"):
                j -= 1
            word = input_string[j + 1:split_at - 1]
            if _is_abbreviation(word):
                continue
        sentences.append(input_string[last:split_at])
        last = m.end()
    sentences.append(input_string[last:])
    return sentences


def char_indexed_sentence_tokenize(input_string):
    return [(s[0], s[2]) for s in span_indexed_sentence_tokenize(input_string)]


def span_indexed_sentence_tokenize(input_string):
    sentences = sentence_tokenize(input_string)
    spans = []
    for idx, s in enumerate(sentences):
        start_idx = sum(len(_) for _ in sentences[:idx])
        if start_idx > 0:
            # account for white spaces
            start_idx += sum(1 for _ in sentences[:idx])
        end_idx = start_idx + len(s)
        spans.append((start_idx, end_idx, input_string[start_idx:end_idx]))
    return spans


def paragraph_tokenize(input_string):
    paragraphs = []
    for group_separator, chunk in groupby(input_string.splitlines(True),
                                          key=str.isspace):
        if group_separator:
            paragraphs[-1] += list(chunk)
        else:
            paragraphs.append(list(chunk))
    return [''.join(chunk) for chunk in paragraphs]


def char_indexed_paragraph_tokenize(input_string):
    return [(s[0], s[2]) for s in
            span_indexed_paragraph_tokenize(input_string)]


def span_indexed_paragraph_tokenize(input_string):
    sentences = paragraph_tokenize(input_string)
    spans = []
    for idx, s in enumerate(sentences):
        start_idx = sum(len(_) for _ in sentences[:idx])
        end_idx = start_idx + len(s)
        spans.append((start_idx, end_idx, input_string[start_idx:end_idx]))
    return spans


def get_empty_spans(input_string):
    spans = []
    start = None
    total_chars = len(input_string)
    for idx in range(total_chars):
        next_char = input_string[idx + 1] if idx < total_chars - 1 else None
        if input_string[idx].isspace():
            if start is None:
                start = idx
            if next_char is None:
                end = idx
                spans.append((start, end, input_string[start:end]))
        elif start:
            end = idx
            spans.append((start, end, input_string[start:end]))
            start = None
    return spans


def span_indexed_empty_space_tokenize(input_string):
    spans = []
    start = None
    total_chars = len(input_string)
    for idx in range(total_chars):
        next_char = input_string[idx + 1] if idx < total_chars - 1 else None
        if start is not None and \
                (input_string[idx].isspace() or next_char is None):
            end = idx + 1 if next_char is None else idx
            spans.append((start, end, input_string[start:end]))
            start = None
        elif not input_string[idx].isspace():
            if start is None:
                start = idx
    return spans


def char_indexed_empty_space_tokenize(input_string):
    return [(s[0], s[2]) for s in
            span_indexed_empty_space_tokenize(input_string)]


def empty_space_tokenize(input_string):
    return [s[2] for s in
            span_indexed_empty_space_tokenize(input_string)]
