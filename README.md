This project is made up of 4 components that each play a part in analysing twitter sentiment,
and each have to run in a separate process.

1. Producer - Initializes the Twitter stream and connects it to Kafka
2. Queue - Using Kafka, right now just as a pub/sub message queue. Even though this is second in the pipeline, this has to be run first, otherwise the producer script will fail with nothing to stream into.
3. Consumer - Takes the messages out of the queue in batches and performs the algorithms on the data, i.e. LDA topic modeling.
4. Visualization - a web app that visualizes the outputs from the consumer-algorithm

For instructions on how to run each component, see the component's README.