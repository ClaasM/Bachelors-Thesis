import nltk
text = "the quick brown fox jumps over the lazy dog"
tokens = nltk.tokenize.word_tokenize(text)
tokens
wrapped = nltk.Text(tokens)
wrapped.concordance("fox")