from pyspark import SparkContext
from pyspark.mllib.clustering import LDAModel
from pyspark.sql import SQLContext

# Initialize
sc = SparkContext('local', 'PySPARK LDA Example')
sql_context = SQLContext(sc)

# Load the model
sameModel = LDAModel.load(sc, "target/org/apache/spark/PythonLatentDirichletAllocationExample/LDAModel")

# It is not easily possible to score/classify new documents with this model.