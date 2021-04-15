import re


def word_tokenize(input_string):
    return [m.group() for m in re.finditer(r'[\'.?!,;]|\w+', input_string)]


def char_indexed_word_tokenize(input_string):
    return [(m.start(0), m.group())
            for m in re.finditer(r'[\'.?!,;]|\w+', input_string)]


def span_indexed_word_tokenize(input_string):
    return [(m.start(0), m.end(0), m.group())
            for m in re.finditer(r'[\'.?!,;]|\w+', input_string)]


def chunk(text, delimiters):
    pattern = f"({'|'.join(delimiters)})"
    pts = re.split(pattern, text)
    return [p.strip() for p in pts if p.strip()]


def get_common_chunks(samples):
    s2k = {}
    all_chunks = []
    for sample in samples:
        chunks = word_tokenize(sample)
        s2k[sample] = chunks
        all_chunks += [c for c in chunks if c not in all_chunks]
    return [k for k in all_chunks if all(k in v for v in s2k.values())]


def flatten(some_list, tuples=True):
    _flatten = lambda l: [item for sublist in l for item in sublist]
    if tuples:
        while any(isinstance(x, list) or isinstance(x, tuple)
                  for x in some_list):
            some_list = _flatten(some_list)
    else:
        while any(isinstance(x, list) for x in some_list):
            some_list = _flatten(some_list)
    return some_list


def sentence_tokenize(input_string):
    return re.split(r'(?<=[^A-Z].[.?!]) +(?=[A-Z])', input_string)

