import sys
import unittest

from quebra_frases import (char_indexed_word_tokenize, sentence_tokenize,
                           span_indexed_word_tokenize, word_tokenize)
from quebra_frases.tokenization import _VOWELS


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

    def test_word_of_other_script_ends_sentence(self):
        cases = {
            "Привет мир. Как дела?": ["Привет мир.", "Как дела?"],
            "Γεια σου κόσμε. Τι κάνεις;": ["Γεια σου κόσμε.", "Τι κάνεις;"],
            "გამარჯობა მსოფლიო. როგორ ხარ?": ["გამარჯობა მსოფლიო.",
                                              "როგორ ხარ?"],
            "Բարև աշխարհ. Ինչպես ես?": ["Բարև աշխարհ.", "Ինչպես ես?"],
            "ذهب. ثم عاد.": ["ذهب.", "ثم عاد."],
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(sentence_tokenize(text), expected)

    def test_word_with_other_latin_vowel_ends_sentence(self):
        cases = {
            "C'est très. Il part.": ["C'est très.", "Il part."],
            "Widział ją. Potem wyszedł.": ["Widział ją.", "Potem wyszedł."],
            "Jeg spiste brød. Det var godt.": ["Jeg spiste brød.",
                                               "Det var godt."],
            "Jeg så en bjørn. Den løp.": ["Jeg så en bjørn.", "Den løp."],
            "Bu bir kız. O gitti.": ["Bu bir kız.", "O gitti."],
            "Bu şəhər. Orada yaşayıram.": ["Bu şəhər.", "Orada yaşayıram."],
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(sentence_tokenize(text), expected)

    def test_abbreviation_with_superscript_letter(self):
        self.assertEqual(sentence_tokenize("A Srª. Costa chegou. Fim."),
                         ["A Srª. Costa chegou.", "Fim."])

    def test_initial_of_other_script_not_sentence_end(self):
        self.assertEqual(sentence_tokenize("А. С. Пушкин написал. Конец."),
                         ["А. С. Пушкин написал.", "Конец."])

    def test_roman_numeral_without_vowel_ends_sentence(self):
        self.assertEqual(sentence_tokenize("O século XX. Acabou."),
                         ["O século XX.", "Acabou."])
        self.assertEqual(sentence_tokenize("Comprei um CD. Depois saí."),
                         ["Comprei um CD.", "Depois saí."])
        self.assertEqual(sentence_tokenize("O século XX. acabou."),
                         ["O século XX. acabou."])

    def test_numeral_that_is_an_abbreviation_stays_whole(self):
        cases = {
            "MM. Dupont et Durand sont venus.":
                ["MM. Dupont et Durand sont venus."],
            "O MM. Juiz decidiu.": ["O MM. Juiz decidiu."],
            "SS.MM. Los Reyes llegaron.": ["SS.MM. Los Reyes llegaron."],
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(sentence_tokenize(text), expected)

    def test_title_or_doubled_plural_in_capitals_stays_in_sentence(self):
        cases = {
            "A SRA. COSTA CHEGOU. FIM.": ["A SRA. COSTA CHEGOU.", "FIM."],
            "EXMO. SR. DIRETOR, ESCREVO-LHE. OBRIGADO.":
                ["EXMO. SR. DIRETOR, ESCREVO-LHE.", "OBRIGADO."],
            "BENFICA VS. PORTO ACABOU. FIM.": ["BENFICA VS. PORTO ACABOU.", "FIM."],
            "Trabaja en RR.HH. de una empresa. Le gusta.":
                ["Trabaja en RR.HH. de una empresa.", "Le gusta."],
            "La defensa de los DD.HH. es un deber. Todos lo saben.":
                ["La defensa de los DD.HH. es un deber.", "Todos lo saben."],
            "O DD. Promotor pediu a palavra. O juiz deu.":
                ["O DD. Promotor pediu a palavra.", "O juiz deu."],
            "Er war in der SS. Das wusste niemand.":
                ["Er war in der SS.", "Das wusste niemand."],
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(sentence_tokenize(text), expected)

    def test_acronym_in_capitals_ends_sentence(self):
        cases = {
            "I watched it on TV. It was good.":
                ["I watched it on TV.", "It was good."],
            "We met at the BBC. Then we left.":
                ["We met at the BBC.", "Then we left."],
            "I heard it on CNN. Nobody believed it.":
                ["I heard it on CNN.", "Nobody believed it."],
            "Send me an SMS. I will call back.":
                ["Send me an SMS.", "I will call back."],
            "The file is 20 MB. It fits.": ["The file is 20 MB.", "It fits."],
            "Vi na RTP. Depois saí.": ["Vi na RTP.", "Depois saí."],
            "Mandei o PDF. Ainda não respondeu.":
                ["Mandei o PDF.", "Ainda não respondeu."],
            "Votou no PSD. O irmão votou no PS.":
                ["Votou no PSD.", "O irmão votou no PS."],
            "O ficheiro tem 5 GB. Cabe no disco.":
                ["O ficheiro tem 5 GB.", "Cabe no disco."],
            "Lo anunció la DGT. Habrá controles.":
                ["Lo anunció la DGT.", "Habrá controles."],
            "Votó al PP. Luego se fue.": ["Votó al PP.", "Luego se fue."],
            "Il travaille à la SNCF. Sa femme aussi.":
                ["Il travaille à la SNCF.", "Sa femme aussi."],
            "Elle a voté pour le PS. Lui non.":
                ["Elle a voté pour le PS.", "Lui non."],
            "Das lief im ZDF. Danach ging ich.":
                ["Das lief im ZDF.", "Danach ging ich."],
            "Er wählt die SPD. Sie wählt die CDU.":
                ["Er wählt die SPD.", "Sie wählt die CDU."],
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(sentence_tokenize(text), expected)

    def test_consonant_letters_with_vowel_names_are_not_vowels(self):
        # TURNED Y, TURNED Y WITH BELT, Y WITH HOOK and OI (GHA)
        self.assertEqual(set("ʎ\U0001DF06ƳƴƢƣ") & _VOWELS, set())

    def test_numeral_letter_is_still_an_initial(self):
        for letter in "CDMXVL":
            text = f"{letter}. Silva chegou. Fim."
            with self.subTest(text=text):
                self.assertEqual(sentence_tokenize(text),
                                 [f"{letter}. Silva chegou.", "Fim."])
        self.assertEqual(sentence_tokenize("J. C. Silva chegou. Fim."),
                         ["J. C. Silva chegou.", "Fim."])

    def test_abbreviation_with_other_latin_consonant(self):
        self.assertEqual(sentence_tokenize("Płk. Nowak przyszedł. Koniec."),
                         ["Płk. Nowak przyszedł.", "Koniec."])
        self.assertEqual(sentence_tokenize("Św. Jan przyszedł. Koniec."),
                         ["Św. Jan przyszedł.", "Koniec."])

    def test_abbreviation_with_apostrophe(self):
        self.assertEqual(sentence_tokenize("O D'r. Silva veio."),
                         ["O D'r. Silva veio."])

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

    def test_capital_word_that_is_not_a_numeral_ends_sentence(self):
        self.assertEqual(sentence_tokenize("Mostre o ID. depois entre."),
                         ["Mostre o ID.", "depois entre."])
        self.assertEqual(sentence_tokenize("IIIII. depois"),
                         ["IIIII.", "depois"])

    def test_lowercase_word_that_spells_a_numeral_ends_sentence(self):
        self.assertEqual(sentence_tokenize("Eu vi. depois saí."),
                         ["Eu vi.", "depois saí."])

    def test_ordinal_at_start_of_text_stays_whole(self):
        self.assertEqual(sentence_tokenize("3. de maio foi o dia."),
                         ["3. de maio foi o dia."])

    def test_titlecase_digraph_after_number_ends_sentence(self):
        # "Ǆ" is a capital, but its title case "ǅ" differs from it
        self.assertEqual(sentence_tokenize("Tenho 3. Ǆep ok."),
                         ["Tenho 3.", "Ǆep ok."])

    def test_georgian_sentence_after_number_splits(self):
        self.assertEqual(sentence_tokenize("ფასი არის 3. შემდეგ ის წავიდა."),
                         ["ფასი არის 3.", "შემდეგ ის წავიდა."])

    def test_unit_symbol_after_number_ends_sentence(self):
        # one sentence per symbol in _UNITS, so that each entry has a test
        cases = [
            ("Corrió los 100 metros en 9,58 s.", "Nadie lo superó."),
            ("Tem 3 kg.", "Pesa muito."),
            ("A lâmpada dá 800 cd.", "Ilumina a sala."),
            ("La red funciona a 50 Hz.", "En América usa otra."),
            ("A rádio emite em 1440 kHz.", "Ouve-se bem."),
            ("Emite em 99,1 MHz.", "Tem muitos ouvintes."),
            ("O processador corre a 3,2 GHz.", "Aquece pouco."),
            ("O motor dá 110 kW.", "É rápido."),
            ("A bobina tem 47 pH.", "Serve para filtros."),
            ("A cidade fica a 40 km.", "Fomos de carro."),
            ("Mede 30 cm.", "Cabe na mala."),
            ("A chuva somou 12 mm.", "Choveu toda a noite."),
            ("A luz tem 532 nm.", "É verde."),
            ("A caixa tem 5 dm.", "Não cabe."),
            ("O pacote tem 250 g.", "Chega para dois."),
            ("Tome 500 mg.", "Repita à noite."),
            ("A viagem dura 3 h.", "Leve água."),
            ("O depósito leva 50 l.", "Enche-se depressa."),
            ("O camião carrega 12 t.", "Pesa demais."),
            ("O ruído chega a 90 dB.", "Faz mal aos ouvidos."),
            ("Junte 200 ml.", "Mexa bem."),
            ("A garrafa tem 75 cl.", "Serve quatro."),
            ("Junte 2 dl.", "Leve ao lume."),
            ("A adega produz 300 hl.", "Vende tudo."),
            ("A bateria guarda 50 Wh.", "Dura um dia."),
            ("A casa gasta 300 kWh.", "Paga muito."),
            ("The wall is 10 ft.", "It is high."),
            ("It weighs 5 lb.", "Carry it."),
            ("The disk spins at 7200 rpm.", "It is fast."),
            ("The engine has 125 cc.", "It is light."),
            ("He drove at 70 mph.", "Nobody stopped him."),
            ("Ia a 90 kph.", "Ninguém o parou."),
            ("It weighs 20 lbs.", "Lift it with care."),
            ("A linha dá 56 kb.", "É lenta."),
            ("The line gives 100 Mb.", "It is fast."),
            ("A fibra dá 1 Gb.", "Chega bem."),
            ("O ficheiro tem 12 kB.", "Abre logo."),
            # a symbol with a vowel is not an abbreviation and needs no entry
            ("A viagem dura 20 min.", "Leve água."),
            # the number comes before a unit written with a slash
            ("Ia a 160 km/h.", "Mais ninguém viu."),
            ("O carro emite 120 g/km.", "Mais nada."),
        ]
        for first, second in cases:
            with self.subTest(first):
                self.assertEqual(sentence_tokenize(f"{first} {second}"), [first, second])

    def test_metre_symbol_is_not_a_unit(self):
        # Lithuanian writes "m." (metai, "year") after a year, and a year
        # looks the same as a length
        self.assertEqual(sentence_tokenize("2006 m. Inspekcija pradėjo darbą."),
                         ["2006 m. Inspekcija pradėjo darbą."])
        self.assertEqual(sentence_tokenize("Está a 3850 m. s. n. m., en la meseta."),
                         ["Está a 3850 m. s. n. m., en la meseta."])

    def test_unit_symbol_before_lowercase_word_stays_in_sentence(self):
        self.assertEqual(sentence_tokenize("Mide 3 cm. de largo."), ["Mide 3 cm. de largo."])
        # a Georgian sentence starts with a letter that title case leaves unchanged
        self.assertEqual(sentence_tokenize("იწონის 5 kg. შემდეგ წავიდა."),
                         ["იწონის 5 kg.", "შემდეგ წავიდა."])

    def test_unit_symbol_before_dotted_abbreviation_keeps_sentence_whole(self):
        # German "s. S." is "siehe Seite"
        self.assertEqual(sentence_tokenize("Die Werte stehen in Tabelle 3 s. S. 45 im Anhang."),
                         ["Die Werte stehen in Tabelle 3 s. S. 45 im Anhang."])
        # a longer unit before an initial ends the sentence
        self.assertEqual(sentence_tokenize("El cráneo mide 65 cm. E. uralensis era menor."),
                         ["El cráneo mide 65 cm.", "E. uralensis era menor."])

    def test_unit_symbol_without_number_stays_abbreviation(self):
        # "h." is "hacia" here, not the hour
        self.assertEqual(sentence_tokenize("Juan Pérez (h. 1500) fue pintor."),
                         ["Juan Pérez (h. 1500) fue pintor."])
        # the symbol starts the text: no number stands before it
        self.assertEqual(sentence_tokenize("s. Silva nasceu em 1950"),
                         ["s. Silva nasceu em 1950"])

    def test_spaced_abbreviation_keeps_sentence_whole(self):
        self.assertEqual(sentence_tokenize("Llegó a las 11:00 p. m. MDT. Fin."),
                         ["Llegó a las 11:00 p. m. MDT.", "Fin."])
        self.assertEqual(sentence_tokenize("Escolha uma opção. a. Comer. b. Dormir."),
                         ["Escolha uma opção.", "a. Comer.", "b. Dormir."])

    def test_georgian_initial_not_sentence_end(self):
        # Georgian has no capitals in running text, so its initials stay
        self.assertEqual(sentence_tokenize("ი. ჭავჭავაძე დაიბადა. დასასრული."),
                         ["ი. ჭავჭავაძე დაიბადა.", "დასასრული."])

    def test_lowercase_abbreviation_keeps_sentence_whole(self):
        cases = [
            "See etc. for more.",
            "Ver o sol — cf. ilustração 1.",
            "Ik sprak met dhr. Jansen.",
            "Siehe vgl. Kapitel 3.",
            "En el s. XX hubo guerras.",
            "Adriana Abenia (n. Zaragoza, 1984) es presentadora.",
            "Chegaram d. Maria e d. João.",
            "Llegó a las 8 a. m. del lunes.",
            "Das ist gut, d. h. die Lösung passt.",
            "Exactamente a las 8:46 a. m., la ciudad se volvió silenciosa.",
            "Leve outros documentos (p. ex., visto).",
            "Cerca del año 1000 a. C., los asirios llegaron.",
            "Es el n. 5.",
            "Roe v. Wade was the law.",
            "Many cities, e.g. Paris, have one.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(sentence_tokenize(text), [text])


    def test_exclamation_mark_ends_sentence(self):
        self.assertEqual(sentence_tokenize("Que frio! Fecha a janela."),
                         ["Que frio!", "Fecha a janela."])
        self.assertEqual(sentence_tokenize("¡Hola! ¿Qué tal? Bien."),
                         ["¡Hola!", "¿Qué tal?", "Bien."])
        self.assertEqual(sentence_tokenize("Wow!! Really?! Yes."),
                         ["Wow!!", "Really?!", "Yes."])
        # a lowercase word after the mark goes on with the sentence
        self.assertEqual(sentence_tokenize("Los usuarios de Yahoo! y Microsoft."),
                         ["Los usuarios de Yahoo! y Microsoft."])
        self.assertEqual(sentence_tokenize("¡Ay! dijo él. Se fue."),
                         ["¡Ay! dijo él.", "Se fue."])

    def test_sentence_terminal_of_other_scripts_ends_sentence(self):
        # Devanagari danda, Arabic question mark, Urdu full stop, Armenian
        # full stop and Ethiopic full stop, each with a space after it
        cases = [
            ("मैं घर गया। वह आया।", ["मैं घर गया।", "वह आया।"]),
            ("هل أنت بخير؟ نعم.", ["هل أنت بخير؟", "نعم."]),
            ("میں گھر گیا۔ وہ آیا۔", ["میں گھر گیا۔", "وہ آیا۔"]),
            ("Ես տուն գնացի։ Նա եկավ։", ["Ես տուն գնացի։", "Նա եկավ։"]),
            ("ወደ ቤት ሄድኩ። እሱ መጣ።", ["ወደ ቤት ሄድኩ።", "እሱ መጣ።"]),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(sentence_tokenize(text), expected)

    def test_pause_marks_with_the_property_do_not_end_sentence(self):
        # Myanmar little section is a pause; Armenian text uses the one dot
        # leader for the mijaket, a colon
        self.assertEqual(sentence_tokenize("လူအသစ်များနှင့် တွေ့ရန်၊ သင့်ကိုယ်သင်လေ့လာရန်။"),
                         ["လူအသစ်များနှင့် တွေ့ရန်၊ သင့်ကိုယ်သင်လေ့လာရန်။"])
        self.assertEqual(sentence_tokenize("Ձնահոսքերն անբնական երևույթներ չեն․ կտրուկ թեքությունները"),
                         ["Ձնահոսքերն անբնական երևույթներ չեն․ կտրուկ թեքությունները"])
        self.assertEqual(sentence_tokenize("ကျွန်တော် အိမ်ပြန်တယ်။ သူ လာတယ်။"),
                         ["ကျွန်တော် အိမ်ပြန်တယ်။", "သူ လာတယ်။"])

    def test_chinese_and_japanese_sentence_ends_split_without_space(self):
        cases = [
            ("我有三本书。你有几本？太好了！",
             ["我有三本书。", "你有几本？", "太好了！"]),
            ("今日は晴れです。明日は雨ですか？", ["今日は晴れです。", "明日は雨ですか？"]),
            ("ｺﾝﾆﾁﾊ｡ｹﾞﾝｷ?", ["ｺﾝﾆﾁﾊ｡", "ｹﾞﾝｷ?"]),
            # a run of marks ends the sentence once
            ("真的吗？！我不信。", ["真的吗？！", "我不信。"]),
            # a space after the mark goes with neither sentence
            ("你好。 再见。", ["你好。", "再见。"]),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(sentence_tokenize(text), expected)

    def test_closing_quote_stays_with_its_sentence(self):
        self.assertEqual(sentence_tokenize("他说：“我来了。”她笑了。"),
                         ["他说：“我来了。”", "她笑了。"])
        self.assertEqual(sentence_tokenize("「はい。」彼は答えた。"),
                         ["「はい。」", "彼は答えた。"])

    def test_chinese_text_has_no_empty_sentence(self):
        self.assertEqual(sentence_tokenize("我有三本书。"), ["我有三本书。"])
        self.assertEqual(sentence_tokenize("价格是３．５元。"), ["价格是３．５元。"])

    def test_chinese_split_is_lossless(self):
        for text in ("我有三本书。你有几本？太好了！", "他说：“我来了。”她笑了。",
                     "今日は晴れです。明日は雨ですか？"):
            with self.subTest(text=text):
                self.assertEqual("".join(sentence_tokenize(text)), text)


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
