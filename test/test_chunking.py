import unittest
from quebra_frases import *


class TestChunking(unittest.TestCase):

    def test_word(self):
        self.assertEqual(
            word_tokenize(
                "sometimes i develop stuff for mycroft, mycroft is FOSS!", ),
            ['sometimes', 'i', 'develop', 'stuff', 'for', 'mycroft', ',',
             'mycroft', 'is', 'FOSS', '!'])

        self.assertEqual(
            char_indexed_word_tokenize(
                "sometimes i develop stuff for mycroft, mycroft is FOSS!", ),
            [(0, 'sometimes'), (10, 'i'), (12, 'develop'), (20, 'stuff'),
             (26, 'for'), (30, 'mycroft'), (37, ','), (39, 'mycroft'),
             (47, 'is'), (50, 'FOSS'), (54, '!')])

        self.assertEqual(
            span_indexed_word_tokenize("sometimes i develop stuff for "
                                       "mycroft, mycroft is FOSS!", ),
            [(0, 9, 'sometimes'), (10, 11, 'i'), (12, 19, 'develop'),
             (20, 25, 'stuff'), (26, 29, 'for'), (30, 37, 'mycroft'),
             (37, 38, ','), (39, 46, 'mycroft'), (47, 49, 'is'),
             (50, 54, 'FOSS'), (54, 55, '!')])

    def test_sentence(self):
        self.assertEqual(
            sentence_tokenize(
                "Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it. Did he mind? Adam Jones Jr. thinks he didn't. In any case, this isn't true... Well, with a probability of .9 it isn't."),
            [
                'Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it.',
                'Did he mind?',
                "Adam Jones Jr. thinks he didn't.",
                "In any case, this isn't true...",
                "Well, with a probability of .9 it isn't."]
        )

    def test_chunk(self):
        self.assertEqual(
            chunk("sometimes i develop stuff for mycroft, mycroft is FOSS!",
                  delimiters=["mycroft"]),
            ['sometimes i develop stuff for', 'mycroft', ',', 'mycroft',
             'is FOSS!']
        )

    def test_common_chunks(self):
        # single token chunks
        samples = ["what do you dream about",
                   "what did you dream about",
                   "what are your dreams about"]
        self.assertEqual(
            get_common_chunks(samples),
            ['what', 'about'])

        samples = ["what is the speed of light in a vacuum",
                   "what is the speed of sound in the air"]
        self.assertEqual(
            get_common_chunks(samples),
            ['what', 'is', 'the', 'speed', 'of', 'in'])

    def test_utils(self):
        self.assertEqual(
            flatten([["A", "B"], ["C"]]), ["A", "B", "C"]
        )
        self.assertEqual(
            flatten([("A", "B")]), ["A", "B"]
        )
        self.assertEqual(
            flatten([("A", "B"), ["C"], [["D", ["E", ["F"]]]]]),
            ["A", "B", "C", "D", "E", "F"]
        )
