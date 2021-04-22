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
        test_sent = "Mr. Smith bought cheapsite.com for 1.5 million " \
                    "dollars, i.e. he paid a lot for it. Did he mind? Adam " \
                    "Jones Jr. thinks he didn't. In any case, this isn't true..." \
                    " Well, with a probability of .9 it isn't."
        self.assertEqual(
            sentence_tokenize(test_sent),
            [
                'Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it.',
                'Did he mind?',
                "Adam Jones Jr. thinks he didn't.",
                "In any case, this isn't true...",
                "Well, with a probability of .9 it isn't."
            ]
        )
        self.assertEqual(
            char_indexed_sentence_tokenize(test_sent),
            [(0, 'Mr. Smith bought cheapsite.com for 1.5 million dollars, '
                 'i.e. he paid a lot for it.'),
             (83, 'Did he mind?'),
             (96, "Adam Jones Jr. thinks he didn't."),
             (129, "In any case, this isn't true..."),
             (161, "Well, with a probability of .9 it isn't.")]
        )
        self.assertEqual(
            span_indexed_sentence_tokenize(test_sent),
            [(0, 82, 'Mr. Smith bought cheapsite.com for 1.5 million '
                     'dollars, i.e. he paid a lot for it.'),
             (83, 95, 'Did he mind?'),
             (96, 128, "Adam Jones Jr. thinks he didn't."),
             (129, 160, "In any case, this isn't true..."),
             (161, 201, "Well, with a probability of .9 it isn't.")]
        )

    def test_paragraph(self):
        test_str = 'This is a paragraph!\n\t\nThis is another ' \
                   'one.\t\n\tUsing multiple lines\t   \n     ' \
                   '\n\tparagraph 3 says goodbye'
        self.assertEqual(
            paragraph_tokenize(test_str),
            ['This is a paragraph!\n\t\n',
             'This is another one.\t\n\tUsing multiple lines\t   \n     \n',
             '\tparagraph 3 says goodbye'])
        self.assertEqual(
            char_indexed_paragraph_tokenize(test_str),
            [(0, 'This is a paragraph!\n\t\n'),
             (23, 'This is another one.\t\n\tUsing multiple lines\t   \n     \n'),
             (77, '\tparagraph 3 says goodbye')])
        self.assertEqual(
            span_indexed_paragraph_tokenize(test_str),
            [(0, 23, 'This is a paragraph!\n\t\n'),
             (23, 77, 'This is another one.\t\n\tUsing multiple lines\t   \n     \n'),
             (77, 102, '\tparagraph 3 says goodbye')])

    def test_chunk(self):
        self.assertEqual(
            chunk("sometimes i develop stuff for mycroft, mycroft is FOSS!",
                  delimiters=["mycroft"]),
            ['sometimes i develop stuff for', 'mycroft', ',', 'mycroft',
             'is FOSS!']
        )
        self.assertEqual(
            chunk_list(['A', 'WORD', 'B', 'C', 'WORD', 'D'],
                       delimiters=['WORD']),
            [['A'], ['B', 'C'], ['D']]
        )

    def test_get_tokens(self):
        samples = ["what do you dream about",
                   "what did you dream about",
                   "what are your dreams about",
                   "what were your dreams about"]
        self.assertEqual(
            get_common_tokens(samples),
            {'what', 'about'})
        self.assertEqual(
            get_uncommon_tokens(samples),
            {'do', 'were', 'your', 'you', 'dream', 'dreams', 'did', 'are'})
        self.assertEqual(
            get_exclusive_tokens(samples),
            {'do', 'did', 'are', 'were'})

        self.assertEqual(
            get_common_tokens(samples, squash=False),
            [['what', 'about'], ['what', 'about'],
             ['what', 'about'], ['what', 'about']])
        self.assertEqual(
            get_uncommon_tokens(samples, squash=False),
            [['do', 'you', 'dream'],
             ['did', 'you', 'dream'],
             ['are', 'your', 'dreams'],
             ['were', 'your', 'dreams']])
        self.assertEqual(
            get_exclusive_tokens(samples, squash=False),
            [['do'], ['did'], ['are'], ['were']])

    def test_get_chunks(self):
        samples = ["tell me what do you dream about",
                   "tell me what did you dream about",
                   "tell me what are your dreams about",
                   "tell me what were your dreams about"]
        self.assertEqual(get_common_chunks(samples),
                         {'tell me what', 'about'})

        self.assertEqual(
            get_common_chunks(samples, squash=False),
            [['tell me what', 'about'],
             ['tell me what', 'about'],
             ['tell me what', 'about'],
             ['tell me what', 'about']])

        self.assertEqual(get_uncommon_chunks(samples),
                         {'do you dream', 'did you dream',
                          'are your dreams', 'were your dreams'})

        self.assertEqual(get_uncommon_chunks(samples, squash=False),
                         [['do you dream'],
                          ['did you dream'],
                          ['are your dreams'],
                          ['were your dreams']])

        self.assertEqual(get_exclusive_chunks(samples),
                         {'do', 'did', 'are', 'were'})

        samples = ["what is the speed of light",
                   "what is the maximum speed of a firetruck",
                   "why are fire trucks red"]
        self.assertEqual(
            get_exclusive_chunks(samples),
            {'light', 'maximum', 'a firetruck', 'why are fire trucks red'})
        self.assertEqual(
            get_exclusive_chunks(samples, squash=False),
            [['light'],
             ['maximum', 'a firetruck'],
             ['why are fire trucks red']])

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

