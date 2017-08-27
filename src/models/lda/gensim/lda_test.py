from gensim.models import LdaModel
from gensim.corpora import MmCorpus, Dictionary

corpus_filename = '../../../../data/processed/tweets.mm'
dict_filename = '../../../../data/processed/tweets.dict'
lda_filename = '../../../../models/lda_model/gensim/tweets.lda_model'

corpus = MmCorpus(corpus_filename)
dictionary = Dictionary.load(dict_filename)
lda = LdaModel.load(lda_filename)

# followers_data =  pyLDAvis.gensim.prepare(lda_model,corpus, dictionary)
# pyLDAvis.display(followers_data)

# TODO use the same tokenization functions in training and testing
tokenized_text = ['naked', 'wore', 'mad']

doc_bow = [dictionary.doc2bow(text) for text in [tokenized_text]]

doc_lda = lda.get_document_topics(doc_bow, minimum_probability=None, minimum_phi_value=None, per_word_topics=False)
topics = doc_lda[0]
for topic in topics:
    topic_id = topic[0]
    terms = lda.get_topic_terms(topicid=topic_id, topn=5)
    for term in terms:
        term_index = term[0]
        print(dictionary[term_index])
