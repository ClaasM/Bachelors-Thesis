import re
import nltk
import json
from nltk.tokenize import RegexpTokenizer

"""
Serializable functions to be executed on the spark execution nodes.
These are mostly factories.
Contains some utility functions to preprocess and tokenizer etc. tweets.
They are here instead of the data-directory since they are also used in streaming,
because the features need to be consistent in training, testing and streaming.
"""


def preprocessor():
    """
    Removes all #hashtags, @mentions and other commonly used special characters used directly in front of
    or behind valid words as well as URL's and then only keeps valid words.
    :param text: the text to be preprocessed
    :return: the preprocessed text
    """

    def _preprocess(text):
        # Remove url's
        text = re.sub(r"http\S+", "", text)
        # Remove all the other stuff
        return " ".join([word for word in re.split("[\s;,.#:-@!?'\"]", text) if word.isalpha()])

    return _preprocess


def tokenizer(remove_stopwords=True):
    """
    Tokenization function for LDA. Used for training _and_ during streaming
    :return:
    """
    regex_tokenizer = RegexpTokenizer(r'\w+')
    # nltk stopword list plus some miscellaneous terms with low informativeness
    stoplist = set(['amp', 'get', 'got', 'hey', 'hmm', 'hoo', 'hop', 'iep', 'let', 'ooo', 'par',
                    'pdt', 'pln', 'pst', 'wha', 'yep', 'yer', 'aest', 'didn', 'nzdt', 'via',
                    'one', 'com', 'new', 'like', 'great', 'make', 'top', 'awesome', 'best',
                    'good', 'wow', 'yes', 'say', 'yay', 'would', 'thanks', 'thank', 'going',
                    'new', 'use', 'should', 'could', 'best', 'really', 'see', 'want', 'nice',
                    'while', 'know', 'que', 'sur', 'con'] + nltk.corpus.stopwords.words("english"))

    def _tokenize(text):
        # Tokenize
        tokens = regex_tokenizer.tokenize(text.lower())
        # Remove words with length < 3
        tokens = [token for token in tokens if len(token) > 2]
        if remove_stopwords:
            # Remove stop words
            tokens = [token for token in tokens if token not in stoplist]
        return tokens

    return _tokenize


def lda(dictionary, model):
    """
    Factory for the LDA spark function
    :return:
    """

    def _lda(tokens):
        # doc2bow expects an array of unicode tokens
        doc_bow = [dictionary.doc2bow(token) for token in [tokens]]
        doc_lda = model.get_document_topics(doc_bow,
                                            minimum_probability=None,
                                            minimum_phi_value=None,
                                            per_word_topics=False)
        topics = doc_lda[0]
        topics_ret = dict()
        for topic in topics:
            topic_id = topic[0]
            topic_probability = topic[1]
            terms = model.get_topic_terms(topicid=topic_id, topn=5)
            topics_ret[topic_id] = {
                'probability': topic_probability,
                # Maximum 5 Terms per Topic
                'terms': [dictionary[term[0]] for term in terms[:5]]
            }
        return topics_ret

    return _lda


def extract_features(document, word_features):
    """
    Used to get a word vector required by the naive bayes classifier for training and during streaming
    :param document: tokens
    :param word_features: all words
    :return:
    """
    document_words = set(document)
    features = []
    for word in word_features:
        features.append(word in document_words)
    return features


def sentiment_analyzer(dictionary, classifier):
    """
    Factory for the sentiment analysis function
    :param dictionary: gensim-dictionary
    :param classifier: sentiment classifier
    :return: the sentiment analysis function
    """

    def _analyze_sentiment(tokens):
        """
        Classifies a preprocessed tweet using the sentiment classifier
        :param tokens: preprocessed tweet
        :return:
        """
        return classifier.predict([extract_features(document=tokens, word_features=dictionary.token2id)])[0]

    return _analyze_sentiment


def analyzer(dictionary, sentiment_classifier, lda_model):
    """
    Factory for the spark function that performs all the analysis and prerocessing of each tweet
    :param dictionary: gensim-dictionary
    :param sentiment_classifier: to classify the sentiment of each tweet
    :param lda_model: to model the topic(s) of each tweet
    :return: the spark function to do so
    """

    # Initialize all the stuff the execution node needs (the context is transmitted)
    preprocess = preprocessor()
    lda_tokenize = tokenizer(remove_stopwords=True)
    sa_tokenize = tokenizer(remove_stopwords=False)
    model_topics = lda(dictionary=dictionary, model=lda_model)
    analyze_sentiment = sentiment_analyzer(dictionary=dictionary, classifier=sentiment_classifier)

    def _analyze(element):

        """
        Performs all the analysis we want on the raw incoming tweet
        :param element: the incoming tweet
        :return: the update to be sent to the dashboard
        """

        # The actual tweet is the second element in a tupel
        tweet_str = element[1]
        # It's still a string, so parse it
        tweet = json.loads(tweet_str)
        # Just the text needed
        raw_text = tweet['text']
        # Using the same preprocessing function as everywhere else, for consistency
        text = preprocess(raw_text)
        # Use the same tokenization functions as everywhere else, for consistency
        tokens_sa = sa_tokenize(text)
        tokens_lda = lda_tokenize(text)

        # The update should contain...
        update = dict()
        # ...the sentiment score...
        update['sentiment'] = analyze_sentiment(tokens_sa)
        # ...the topics...
        update['topics'] = model_topics(tokens_lda)
        # ...and the tweet itself (or at least what we need from it in the frontend).
        update['tweet'] = {
            'text': raw_text,
            'user': {
                'name': tweet['user']['name']
            }
        }

        return update

    return _analyze
