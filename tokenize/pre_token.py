'''
Fitting spaCy to pre-tokenize html https://spacy.io/usage/linguistic-features#native-tokenizers
https://spacy.io/usage/linguistic-features#native-tokenizer-additions

Author: Aaron
'''
import spacy
from spacy.tokenizer import Tokenizer

from spacy import util

import os
import re

sourceFile = os.path.join(os.path.realpath(os.path.join(os.path.dirname(__file__), '../processing/mod_htmlfiles')), 'modified_cnn.txt')

with open(sourceFile, 'r', encoding="ISO-8859-1") as f:
    try:
        target_html = f.read() 
    except Exception as e:
        print('During file reading, this error occurred:', e)

# target_html = re.sub(r"\n", "", target_html)
# print(target_html)


nlp = spacy.load("en_core_web_sm", disable=["tok2vec","tagger", "attribute_ruler", "lemmatizer"])


# * Ditioncary of Special Cases: none
special_cases = {}

# * prefix_search, preceding punctuation: <
prefixes = nlp.Defaults.prefixes
prefixes = list(prefixes)
prefixes.remove("<")
prefixes.remove('"')
prefixes.remove('—')
prefixes.remove('–')
prefix_search = (util.compile_prefix_regex(prefixes).search)

# * suffix_search, succeeding punctuation: >
suffixes = nlp.Defaults.suffixes
suffixes = list(suffixes)
suffixes.remove(">")
suffixes.remove('"')
suffix_search = (util.compile_suffix_regex(suffixes).search)

# * infixes_finditer, non-whitespace separators: \n ="
infix_re = re.compile('\n|=""|="')


# * token_match, always stay together
# token_match = re.compile('[A-z]+\/[A-z]+|[A-z]+-[A-z]+').search

def custom_tokenizer(nlp):
    return Tokenizer(nlp.vocab, rules=special_cases,
                                prefix_search=prefix_search,
                                suffix_search=suffix_search,
                                infix_finditer=infix_re.finditer)

nlp.tokenizer = custom_tokenizer(nlp)
doc = nlp(target_html)

# * remove \n from output
outputList = [t.text for t in doc]
outputList = list(filter(lambda a: re.search('\n', a) is None, outputList))
output = str(outputList)

with open(os.path.join('./tokenize', f"./{os.path.basename(sourceFile)}"), 'w') as f_out:
        try: 
            f_out.write(output)
        except Exception as e:
            print('During style file writing:', e)
