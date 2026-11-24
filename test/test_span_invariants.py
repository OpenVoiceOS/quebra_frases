"""Every span function returns pieces that are slices of the input, in order.

The texts are generated from a fixed seed: words, punctuation, spaces, tabs
and newlines, with whitespace at either end.
"""
import random
import unittest

from quebra_frases import (char_indexed_empty_space_tokenize,
                           char_indexed_paragraph_tokenize,
                           char_indexed_sentence_tokenize,
                           char_indexed_word_tokenize, empty_space_tokenize,
                           paragraph_tokenize, sentence_tokenize,
                           span_indexed_empty_space_tokenize,
                           span_indexed_paragraph_tokenize,
                           span_indexed_sentence_tokenize,
                           span_indexed_word_tokenize, word_tokenize)

_WORDS = ["a", "b", "ab", "foo", "Bar", "cão", "Dr.", "3", "x.", "Hi.",
          "ok?", "sim!", "fim.", "«", "»", ","]
_GAPS = [" ", " ", " ", "  ", "\t", "\n", "\n\n", " \n ", "\n \n"]


def _texts(count=500, seed=20261124):
    rng = random.Random(seed)
    texts = ["", " ", "\n", "a", "a b", "ab ", " ab", "\n\nfoo\n\nbar", "Hi. "]
    for _ in range(count):
        parts = [rng.choice(["", " ", "\n", "\n\n"])]
        for _ in range(rng.randint(1, 8)):
            parts += [rng.choice(_WORDS), rng.choice(_GAPS)]
        parts[-1] = rng.choice(["", " ", "\n", "\n\n", parts[-1]])
        texts.append("".join(parts))
    return texts


class TestSpanInvariants(unittest.TestCase):

    def assert_slices_in_order(self, text, spans, pieces, char_spans):
        self.assertEqual([piece for _, _, piece in spans], pieces, repr(text))
        self.assertEqual([(start, piece) for start, _, piece in spans],
                         char_spans, repr(text))
        previous_end = 0
        for start, end, piece in spans:
            self.assertEqual(text[start:end], piece, repr(text))
            self.assertGreaterEqual(start, previous_end, repr(text))
            # what lies between two pieces is whitespace only
            self.assertEqual(text[previous_end:start].strip(), "", repr(text))
            previous_end = end
        self.assertEqual(text[previous_end:].strip(), "", repr(text))

    def test_word_spans(self):
        for text in _texts():
            self.assert_slices_in_order(
                text, span_indexed_word_tokenize(text), word_tokenize(text),
                char_indexed_word_tokenize(text))

    def test_sentence_spans(self):
        for text in _texts():
            self.assert_slices_in_order(
                text, span_indexed_sentence_tokenize(text),
                sentence_tokenize(text), char_indexed_sentence_tokenize(text))

    def test_paragraph_spans(self):
        for text in _texts():
            spans = span_indexed_paragraph_tokenize(text)
            self.assert_slices_in_order(
                text, spans, paragraph_tokenize(text),
                char_indexed_paragraph_tokenize(text))
            # the paragraphs run on to the end of the text
            if spans:
                self.assertEqual(spans[-1][1], len(text), repr(text))

    def test_empty_space_spans(self):
        for text in _texts():
            pieces = empty_space_tokenize(text)
            # str.split() is an independent oracle for the same split
            self.assertEqual(pieces, text.split(), repr(text))
            self.assert_slices_in_order(
                text, span_indexed_empty_space_tokenize(text), pieces,
                char_indexed_empty_space_tokenize(text))


if __name__ == "__main__":
    unittest.main()
