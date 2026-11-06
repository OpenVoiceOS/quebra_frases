import unittest

from quebra_frases import sentence_tokenize


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


if __name__ == "__main__":
    unittest.main()
