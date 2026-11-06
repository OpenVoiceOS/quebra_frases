import sys
import unittest

from quebra_frases import (char_indexed_word_tokenize, sentence_tokenize,
                           span_indexed_word_tokenize, word_tokenize)


class TestSentenceTokenize(unittest.TestCase):
    def test_join_lossless(self):
        # sentence_tokenize must never drop or duplicate characters:
        # joining the parts back with the whitespace it split on must
        # reproduce the original input exactly.
        samples = [
            "D. Afonso reinou de 1139 a 1185. Sr. Silva chegou às 16:30.",
            "Dr. Who arrived. He left.",
            "J. R. R. Tolkien wrote it. It sold.",
            "Custa 3 euros, i.e. pouco. Fim.",
            "A Sra. Costa chegou. Sentou-se.",
            "ex. isto. Aquilo.",
            "Vi o cão. Ele correu.",
            "Está frio. Muito frio.",
            "Acabou? Sim. Fim!",
        ]
        for s in samples:
            parts = sentence_tokenize(s)
            self.assertEqual(" ".join(parts), s)

    def test_single_letter_initial_not_sentence_end(self):
        # "D." (Dom) must not be split off as its own sentence
        sents = sentence_tokenize(
            "D. Afonso reinou de 1139 a 1185. Sr. Silva chegou às 16:30."
        )
        self.assertEqual(
            sents,
            [
                "D. Afonso reinou de 1139 a 1185.",
                "Sr. Silva chegou às 16:30.",
            ],
        )

    def test_consonant_only_abbreviation(self):
        sents = sentence_tokenize("Dr. Who arrived. He left.")
        self.assertEqual(sents, ["Dr. Who arrived.", "He left."])

    def test_multiple_initials(self):
        sents = sentence_tokenize("J. R. R. Tolkien wrote it. It sold.")
        self.assertEqual(sents, ["J. R. R. Tolkien wrote it.", "It sold."])

    def test_lowercase_latin_abbreviation(self):
        sents = sentence_tokenize("Custa 3 euros, i.e. pouco. Fim.")
        self.assertEqual(sents, ["Custa 3 euros, i.e. pouco.", "Fim."])

    def test_vowel_bearing_abbreviation_list(self):
        sents = sentence_tokenize("A Sra. Costa chegou. Sentou-se.")
        self.assertEqual(sents, ["A Sra. Costa chegou.", "Sentou-se."])

    def test_lowercase_explicit_abbreviation(self):
        sents = sentence_tokenize("ex. isto. Aquilo.")
        self.assertEqual(sents, ["ex. isto.", "Aquilo."])

    def test_genuine_sentence_ends_still_split(self):
        self.assertEqual(
            sentence_tokenize("Vi o cão. Ele correu."),
            ["Vi o cão.", "Ele correu."],
        )
        self.assertEqual(
            sentence_tokenize("Está frio. Muito frio."),
            ["Está frio.", "Muito frio."],
        )
        self.assertEqual(
            sentence_tokenize("Acabou? Sim. Fim!"),
            ["Acabou?", "Sim.", "Fim!"],
        )

    def test_ordinal_before_lowercase_not_sentence_end(self):
        self.assertEqual(sentence_tokenize("No dia 3. de maio."),
                         ["No dia 3. de maio."])
        self.assertEqual(sentence_tokenize("O século XIV. acabou."),
                         ["O século XIV. acabou."])
        self.assertEqual(sentence_tokenize("No dia ٣. de maio."),
                         ["No dia ٣. de maio."])

    def test_number_before_capital_still_ends_sentence(self):
        self.assertEqual(sentence_tokenize("Tenho 3. Ele tem 4."),
                         ["Tenho 3.", "Ele tem 4."])
        self.assertEqual(sentence_tokenize("O século XIV. Acabou."),
                         ["O século XIV.", "Acabou."])

    def test_ordinal_languages_stay_whole(self):
        self.assertEqual(sentence_tokenize("Dnia 3. maja wyjechał."),
                         ["Dnia 3. maja wyjechał."])
        self.assertEqual(sentence_tokenize("A XIV. században élt."),
                         ["A XIV. században élt."])

    def test_word_before_lowercase_still_ends_sentence(self):
        self.assertEqual(sentence_tokenize("Saiu. depois voltou."),
                         ["Saiu.", "depois voltou."])

    def test_number_that_is_not_an_ordinal_ends_sentence(self):
        self.assertEqual(sentence_tokenize("Chegou às 14:30. depois saiu."),
                         ["Chegou às 14:30.", "depois saiu."])
        self.assertEqual(sentence_tokenize("Custa 2,50. depois pagou."),
                         ["Custa 2,50.", "depois pagou."])
        self.assertEqual(sentence_tokenize("Teve COVID-19. depois voltou."),
                         ["Teve COVID-19.", "depois voltou."])
        self.assertEqual(sentence_tokenize("Vale x². depois"),
                         ["Vale x².", "depois"])
        self.assertEqual(sentence_tokenize("Vale ². depois"),
                         ["Vale ².", "depois"])

    def test_georgian_sentence_after_number_splits(self):
        self.assertEqual(sentence_tokenize("ფასი არის 3. შემდეგ ის წავიდა."),
                         ["ფასი არის 3.", "შემდეგ ის წავიდა."])


SENTENCES = [
    "O Dr. Silva pagou 2,50 € às 14:30. Custa $5, ou 20%! #FF0000 — fim",
    "Costs £3.99 or ¥500 — maybe 1,234.50 USD; see p. 4–5.",
    "«Olá», disse ela… e saiu. 3/4 = 0,75 ± 0,01 °C",
    "¿Qué hora es? ¡Son las 12:00! Mañana, 12/03/2024.",
    "Le café coûte 2,50 € — n'est-ce pas ? « Oui » !",
    "„Guten Tag“, sagte er – und ging. 5 € pro Stück.",
    "मैं ₹१२.५० देता हूँ। नमस्ते दुनिया!",
    "السعر ١٢٫٥ دينار، أليس كذلك؟ ٪٢٠",
    "می‌خواهم بروم.",
    "日本語のテキスト、です。価格は¥1,000。",
    "เพิ่มความสว่างไฟ 50% ด้วย! ฿100",
    "Привет, мир — это тест № 5; €-курс 1,5.",
    "email me @ a&b <x> {y} [z] | ~ ^ ` © ® ™ § ¶ † ‡ • ‰",
    "call 911. pay $5, then 3/4. -2.5 and - 2 and 2 - 2",
    "a​b ﻿c d­e 😀👍🏽 ❤️",
    "  leading and trailing  \t\n ",
]


def assert_spans_cover(test, text, spans):
    # every span is the slice it claims, spans run in order without
    # overlap, and every character that is not space is in exactly one span
    covered = [0] * len(text)
    last_end = 0
    for start, end, token in spans:
        if text[start:end] != token or not last_end <= start < end:
            test.fail(f"bad span {(start, end, token)!r} after {last_end}")
        last_end = end
        for idx in range(start, end):
            covered[idx] += 1
    missed = [f"U+{ord(ch):04X} at {idx}" for idx, ch in enumerate(text)
              if not ch.isspace() and covered[idx] != 1]
    test.assertEqual(missed[:20], [], f"{len(missed)} characters missed")


class TestWordTokenizeCoverage(unittest.TestCase):

    def test_every_character_is_in_one_token(self):
        for text in SENTENCES:
            with self.subTest(text=text):
                spans = span_indexed_word_tokenize(text)
                assert_spans_cover(self, text, spans)
                for _, _, token in spans:
                    self.assertFalse(any(ch.isspace() for ch in token),
                                     token)
                self.assertEqual(word_tokenize(text),
                                 [t for _, _, t in spans])
                self.assertEqual(char_indexed_word_tokenize(text),
                                 [(s, t) for s, _, t in spans])

    def test_every_code_point_is_in_one_token(self):
        # each code point stands alone, after a letter and after a digit
        text = "".join(f" {ch} a{ch} 1{ch}2"
                       for ch in map(chr, range(sys.maxunicode + 1))
                       if not 0xD800 <= ord(ch) <= 0xDFFF)
        assert_spans_cover(self, text, span_indexed_word_tokenize(text))


class TestWordTokenizeSymbols(unittest.TestCase):

    def test_currency_dash_and_symbols_are_tokens(self):
        text = "O Dr. Silva pagou 2,50 € às 14:30. Custa $5, ou 20%! #FF0000 — fim"
        self.assertEqual(
            word_tokenize(text),
            ['O', 'Dr', '.', 'Silva', 'pagou', '2,50', '€', 'às', '14:30',
             '.', 'Custa', '$', '5', ',', 'ou', '20', '%', '!', '#',
             'FF0000', '—', 'fim'])
        spans = span_indexed_word_tokenize(text)
        self.assertIn((23, 24, '€'), spans)
        self.assertIn((28, 33, '14:30'), spans)
        self.assertIn((33, 34, '.'), spans)
        self.assertIn((41, 42, '$'), spans)
        self.assertIn((61, 62, '—'), spans)
        self.assertEqual(spans[-1], (63, 66, 'fim'))

    def test_punctuation_of_other_scripts(self):
        self.assertEqual(word_tokenize("a–b"), ['a', '–', 'b'])
        self.assertEqual(word_tokenize("«Olá»"), ['«', 'Olá', '»'])
        self.assertEqual(word_tokenize("„de“"), ['„', 'de', '“'])
        self.assertEqual(word_tokenize("¿Qué?"), ['¿', 'Qué', '?'])
        self.assertEqual(word_tokenize("日本語、です。"),
                         ['日本語', '、', 'です', '。'])
        self.assertEqual(word_tokenize("مرحبا، كيف؟"),
                         ['مرحبا', '،', 'كيف', '؟'])
        self.assertEqual(word_tokenize("बढ़ाओ।"), ['बढ़ाओ', '।'])
        self.assertEqual(word_tokenize("a&b @c 10°C"),
                         ['a', '&', 'b', '@', 'c', '10', '°', 'C'])

    def test_joiners_stay_inside_the_word(self):
        # ZWNJ in Persian, ZWJ in a Devanagari conjunct
        self.assertEqual(word_tokenize("می‌خواهم بروم"),
                         ['می‌خواهم', 'بروم'])
        self.assertEqual(word_tokenize("क्‍ष"), ['क्‍ष'])


class TestWordTokenizeNumbers(unittest.TestCase):

    def test_number_ends_on_a_digit(self):
        self.assertEqual(word_tokenize("14:30."), ['14:30', '.'])
        self.assertEqual(word_tokenize("5,"), ['5', ','])
        self.assertEqual(word_tokenize("call 911."), ['call', '911', '.'])
        self.assertEqual(word_tokenize("custa 2,5."), ['custa', '2,5', '.'])
        self.assertEqual(word_tokenize("-5."), ['-5', '.'])
        self.assertEqual(word_tokenize("3/4."), ['3/4', '.'])
        self.assertEqual(word_tokenize("3/"), ['3', '/'])
        self.assertEqual(word_tokenize("2:"), ['2', ':'])
        self.assertEqual(word_tokenize("1..2"), ['1', '.', '.', '2'])
        self.assertEqual(word_tokenize("pay $5, then go"),
                         ['pay', '$', '5', ',', 'then', 'go'])

    def test_whole_numbers_stay_whole(self):
        for number in ["1.234,50", "1,234.50", "-5", "-2.5", "3/4",
                       "12/03/2024", "14:30", "2.5.3"]:
            with self.subTest(number=number):
                self.assertEqual(word_tokenize(number), [number])
        self.assertEqual(word_tokenize("2,50€"), ['2,50', '€'])
        self.assertEqual(word_tokenize("20%"), ['20', '%'])

    def test_digits_of_other_scripts(self):
        # Arabic-Indic digits with the Arabic decimal (U+066B) and
        # thousands (U+066C) separators, and Devanagari digits
        self.assertEqual(word_tokenize("١٢٫٥"), ['١٢٫٥'])
        self.assertEqual(word_tokenize("١٬٢٣٤٫٥٠"), ['١٬٢٣٤٫٥٠'])
        self.assertEqual(word_tokenize("الساعة ١٢:٣٠."),
                         ['الساعة', '١٢:٣٠', '.'])
        self.assertEqual(word_tokenize("१२.५० रुपये।"),
                         ['१२.५०', 'रुपये', '।'])
        self.assertEqual(word_tokenize("۱۲٫۵"), ['۱۲٫۵'])


if __name__ == "__main__":
    unittest.main()
