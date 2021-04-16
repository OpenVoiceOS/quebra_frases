# Quebra Frases

quebra_frases chunks strings into byte sized pieces

## Usage

Tokenization

```python
import quebra_frases

sentence = "sometimes i develop stuff for mycroft, mycroft is FOSS!"
print(quebra_frases.word_tokenize(sentence))
# ['sometimes', 'i', 'develop', 'stuff', 'for', 'mycroft', ',', 
# 'mycroft', 'is', 'FOSS', '!']

print(quebra_frases.span_indexed_word_tokenize(sentence))
# [(0, 9, 'sometimes'), (10, 11, 'i'), (12, 19, 'develop'), 
# (20, 25, 'stuff'), (26, 29, 'for'), (30, 37, 'mycroft'), 
# (37, 38, ','), (39, 46, 'mycroft'), (47, 49, 'is'), 
# (50, 54, 'FOSS'), (54, 55, '!')]

print(quebra_frases.sentence_tokenize(
    "Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it. Did he mind? Adam Jones Jr. thinks he didn't. In any case, this isn't true... Well, with a probability of .9 it isn't."))
#['Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it.',
#'Did he mind?',
#"Adam Jones Jr. thinks he didn't.",
#"In any case, this isn't true...",
#"Well, with a probability of .9 it isn't."]

print(quebra_frases.span_indexed_sentence_tokenize(
    "Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it. Did he mind? Adam Jones Jr. thinks he didn't. In any case, this isn't true... Well, with a probability of .9 it isn't."))
#[(0, 82, 'Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it.'),
#(83, 95, 'Did he mind?'),
#(96, 128, "Adam Jones Jr. thinks he didn't."),
#(129, 160, "In any case, this isn't true..."),
#(161, 201, "Well, with a probability of .9 it isn't.")]
```

chunking

```python
import quebra_frases

delimiters = ["mycroft"]
sentence = "sometimes i develop stuff for mycroft, mycroft is FOSS!"
print(quebra_frases.chunk(sentence, delimiters))
# ['sometimes i develop stuff for', 'mycroft', ',', 'mycroft', 'is FOSS!']


samples = ["tell me what do you dream about",
           "tell me what did you dream about",
           "tell me what are your dreams about",
           "tell me what were your dreams about"]
print(quebra_frases.get_common_chunks(samples))
# {'tell me what', 'about'}
print(quebra_frases.get_uncommon_chunks(samples))
# {'do you dream', 'did you dream', 'are your dreams', 'were your dreams'}
print(quebra_frases.get_exclusive_chunks(samples))
# {'do', 'did', 'are', 'were'}


samples = ["what is the speed of light",
           "what is the maximum speed of a firetruck",
           "why are fire trucks red"]
print(quebra_frases.get_exclusive_chunks(samples))
# {'light', 'maximum', 'a firetruck', 'why are fire trucks red'})
print(quebra_frases.get_exclusive_chunks(samples, squash=False))
#[['light'],
#['maximum', 'a firetruck'],
#['why are fire trucks red']])
```


## Install

```bash
pip install quebra_frases
```