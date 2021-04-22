import re
from itertools import groupby


def word_tokenize(input_string):
    return [m.group() for m in re.finditer(r'[\'.?!,;]|\w+', input_string)]


def char_indexed_word_tokenize(input_string):
    return [(m.start(0), m.group())
            for m in re.finditer(r'[\'.?!,;]|\w+', input_string)]


def span_indexed_word_tokenize(input_string):
    return [(m.start(0), m.end(0), m.group())
            for m in re.finditer(r'[\'.?!,;]|\w+', input_string)]


def sentence_tokenize(input_string):
    return re.split(r'(?<=[^A-Z].[.?!]) +(?=[A-Z])', input_string)


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
