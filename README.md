# Combining Sentiment Analysis with Topic Modeling on Streamed Social Network Data

This repository contains the project for my thesis as well as the thesis itself.
Information about this project beyond this README, for example about the project structure,
can be found in the thesis itself. Technical documentation is done in-code.

## Setup

The following steps need to be taken to launch the dashboard.

### Dependencies

The following dependencies need to be installed and (if applicable) added to `PATH` or otherwise set up as per their respective documentations.

1. Python 3.6
2. Python dependencies listed in `requirements.txt`
3. Bower
4. Bower dependencies listed in `bower.json`
5. Docker 1.13.1
7. Apache Spark 2.2.0
6. Apache Kafka (Go through integration guide [here](https://spark.apache.org/docs/2.2.0/streaming-kafka-integration.html))

It is strongly advised to use a `virtualenv

### Creating a Twitter App

To enable the dashboard to connect to Twitter, create an App in [Twitter Application Management](https://apps.twitter.com/),
download the access information, and place it in the root directory with the name `twitter.access.json`.

### Running the Dashboard

1. Start Kafka by running `docker-compose up`. Make sure Docker is running
2. Set the environment variables:
    - SPARK_HOME="/path/to/spark/"
    - PYSPARK_PYTHON=python3
    - PYSPARK_SUBMIT_ARGS=--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell
3. Run `python3 run.py` from `src/visualization/dashboard`

### Troubleshooting

`NoBrokersAvailable`: Pyspark cannot reach the Kafka message broker. Make sure docker-compose ran without errors.

## Miscellaneous


### Starting a pySpark Notebook Server:
Set `PYSPARK_DRIVER_PYTHON=jupyter` and  `PYSPARK_DRIVER_PYTHON_OPTS="notebook"` to run `pyspark` in Notebook-mode.
Spark can now be used in Jupyter notebooks.

### Streaming from MongoDB
Add `'--packages org.mongodb.spark:mongo-spark-connector_2.10:1.1.0'` to `PYSPARK_SUBMIT_ARGS` to be able to
use Spark with MongoDB instead of a Kafka message queue. This is useful for development/debugging, since it doesn't require connecting to the actual Twitter stream.


### Changing Models
All models are trained in Notebooks under `/notebooks`.


