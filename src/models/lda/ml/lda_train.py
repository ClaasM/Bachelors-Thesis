import time

from pyspark.ml.clustering import LDA

documents = [] # TODO

# Trains a LDA model.
lda = LDA(k=10, maxIter=10)

model = lda.fit(documents)

ll = model.logLikelihood(documents)
lp = model.logPerplexity(documents)
print("The lower bound on the log likelihood of the entire corpus: " + str(ll))
print("The upper bound bound on perplexity: " + str(lp))

# Describe topics.
topics = model.describeTopics(3)
print("The topics described by their top-weighted terms:")
topics.show(truncate=False)

# Shows the result

transformed = model.transform(documents)
transformed.show(truncate=False)

name = "%d" % time.time()
model.save(sc, "../../models/lda/spark/%s" % name)
