import unittest
from quebra_frases import *

class TestExtensive(unittest.TestCase):

    def test_word_edge_cases(self):
        # Empty string
        self.assertEqual(word_tokenize(""), [])
        
        # Only spaces
        self.assertEqual(word_tokenize("   "), [])
        
        # Punctuation only
        self.assertEqual(word_tokenize("!!!"), ["!", "!", "!"])
        
        # Mixed numbers and letters
        self.assertEqual(word_tokenize("v1.2.3"), ["v1.2.3"]) # wait, let's see what it does
        
        # Emails and URLs
        self.assertEqual(word_tokenize("test@example.com"), ["test", "@", "example.com"])
        self.assertEqual(word_tokenize("https://example.com/path"), ["https", ":", "/", "/", "example.com", "/", "path"])

    def test_sentence_edge_cases(self):
        # Multiple spaces after period
        test_sent = "Hello.  World."
        self.assertEqual(sentence_tokenize(test_sent), ["Hello.", " World."])
        # Wait, if it splits on ONE space, the second space goes to the next sentence.
        
        # Ellipsis
        self.assertEqual(sentence_tokenize("This is a test... Next."), ["This is a test...", "Next."])
        
        # No spaces
        self.assertEqual(sentence_tokenize("Hello.World"), ["Hello.World"])

    def test_paragraph_edge_cases(self):
        # Multiple newlines
        test_str = "Para 1\n\n\nPara 2"
        self.assertEqual(paragraph_tokenize(test_str), ["Para 1\n\n\n", "Para 2"])
        
        # Leading/trailing newlines
        test_str = "\nPara 1\n"
        self.assertEqual(paragraph_tokenize(test_str), ["\n", "Para 1\n"])
        
        test_str = "\n\nPara 1\n\n"
        self.assertEqual(paragraph_tokenize(test_str), ["\n\n", "Para 1\n\n"])

    def test_empty_spans_edge_cases(self):
        # Trailing space
        test_sent = "test "
        # get_empty_spans("test ") -> idx 4 is space. next_char is None.
        # start = 4. next_char is None -> spans.append((4, 4, "")) ?
        # That looks like a bug.
        spans = get_empty_spans(test_sent)
        self.assertEqual(spans, [(4, 5, " ")])

    def test_chunk_special_chars(self):
        # Delimiters with regex special chars
        delimiters = ["*"]
        text = "a * b"
        # Current implementation: re.split("(*)", "a * b") -> error!
        try:
            result = chunk(text, delimiters)
            self.assertEqual(result, ["a", "*", "b"])
        except Exception as e:
            self.fail(f"chunk() failed with special characters in delimiters: {e}")

if __name__ == "__main__":
    unittest.main()
