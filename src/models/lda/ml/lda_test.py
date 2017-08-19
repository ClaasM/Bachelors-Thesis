from pyspark import SparkContext
from pyspark.ml.clustering import LocalLDAModel, LDA
from pyspark.sql import SQLContext

# Initialize
sc = SparkContext('local', 'PySPARK LDA Example')
sql_context = SQLContext(sc)

name = "1503144859"

# Cannot load a model that was saved using the RDD-based API
sameModel = LocalLDAModel.load("../../../../models/lda/spark/%s" % name)

# TODO
