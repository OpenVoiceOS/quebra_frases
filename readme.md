# Quebra Frases

quebra_frases chunks strings into byte sized pieces

## Usage

```python
import quebra_frases

samples = ["what do you dream about",
           "what did you dream about",
           "what are your dreams about"]
print(quebra_frases.get_common_chunks(samples))
# ['what', 'about']

delimiters = ["mycroft"]
sentence = "sometimes i develop stuff for mycroft, mycroft is FOSS!"
print(quebra_frases.chunk(sentence, delimiters))
# ['sometimes i develop stuff for', 'mycroft', ',', 'mycroft', 'is FOSS!']

print(quebra_frases.word_tokenize(sentence))
# ['sometimes', 'i', 'develop', 'stuff', 'for', 'mycroft', ',', 
# 'mycroft', 'is', 'FOSS', '!']

print(quebra_frases.char_indexed_word_tokenize(sentence))
# [(0, 'sometimes'), (10, 'i'), (12, 'develop'), (20, 'stuff'),
# (26, 'for'), (30, 'mycroft'), (37, ','), (39, 'mycroft'), (47, 'is'),
# (50, 'FOSS'), (54, '!')]

print(quebra_frases.span_indexed_word_tokenize(sentence))
# [(0, 9, 'sometimes'), (10, 11, 'i'), (12, 19, 'develop'), 
# (20, 25, 'stuff'), (26, 29, 'for'), (30, 37, 'mycroft'), 
# (37, 38, ','), (39, 46, 'mycroft'), (47, 49, 'is'), 
# (50, 54, 'FOSS'), (54, 55, '!')]
```

## Install

```bash
pip install quebra_frases
```