from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.clustering import LDA

sc = SparkContext('local', 'PySPARK LDA Example')

name = "1503079557"

# lda_model = LDAModel.load(sc, "../../models/lda/spark/%s" % name)

# transformed = lda_model.transform()

# topic_indices = lda_model.describeTopics(maxTermsPerTopic=num_words_per_topic)

spark = SparkSession.builder.master("local") \
    .appName("LDA fucker") \
    .getOrCreate()

# Loads data.
dataset = spark.read.format("libsvm").load("../../data/external/sample_lda_libsvm_data.txt")

# Trains a LDA model.
lda = LDA(k=10, maxIter=10)

model = lda.fit(dataset)

ll = model.logLikelihood(dataset)
lp = model.logPerplexity(dataset)
print("The lower bound on the log likelihood of the entire corpus: " + str(ll))
print("The upper bound bound on perplexity: " + str(lp))

# Describe topics.
topics = model.describeTopics(3)
print("The topics described by their top-weighted terms:")
topics.show(truncate=False)

# Shows the result
test_dataset = spark.read.format("libsvm").load("../../data/external/sample_lda_libsvm_data.txt")

transformed = model.transform(test_dataset)
transformed.show(truncate=False)
