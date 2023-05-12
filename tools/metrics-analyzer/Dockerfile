FROM --platform=linux/amd64 gcr.io/spark-operator/spark-py:v3.1.1

# Set the working directory for the application
ARG Pathdir="/opt/spark/examples/src/main/python"

# Set the Python version to use
ENV PYSPARK_PYTHON=/usr/bin/python3
RUN export PYSPARK_PYTHON=/usr/bin/python3

# Change to root user to install dependencies
USER 0

# Install wget to download jars
RUN apt-get update --allow-releaseinfo-change && apt-get -y install wget

# Install required dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt && rm -rf requirements.txt

# Download required jars for Spark
RUN wget -P /opt/spark/jars https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.1.1/spark-sql-kafka-0-10_2.12-3.1.1.jar \
https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_2.12/3.1.1/spark-streaming-kafka-0-10_2.12-3.1.1.jar \
https://repo1.maven.org/maven2/org/elasticsearch/elasticsearch-spark-30_2.12/7.15.1/elasticsearch-spark-30_2.12-7.15.1.jar \
https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.1.1/kafka-clients-3.1.1.jar \
https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.1.1/spark-token-provider-kafka-0-10_2.12-3.1.1.jar \
https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.10.0/commons-pool2-2.10.0.jar

# Remove wget and apt-get cache
RUN apt-get remove --purge -y wget && rm -rf /var/lib/apt/lists/*

# Change back to non-root user
USER 185

# Copy the application files
COPY *.py $Pathdir

# Start the Spark Streaming job when the container starts
#CMD ["spark-submit", "--master", "local[*]", "metrics-stream.py"]