FROM --platform=linux/amd64 python:3.9.16-slim

# VERSIONS
ENV SPARK_VERSION=3.4.0 \
HADOOP_VERSION=3 \
JAVA_VERSION=17

# SET JAVA ENV VARIABLES
#ENV JAVA_HOME="/home/jdk-${JAVA_VERSION}.0.2"
#ENV PATH="${JAVA_HOME}/bin/:${PATH}"

# DOWNLOAD JAVA 11 AND INSTALL
RUN apt-get -y update && apt-get -y install curl wget openjdk-17-jdk ca-certificates-java procps

# DOWNLOAD SPARK AND INSTALL
RUN DOWNLOAD_URL_SPARK="https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
    && wget --no-verbose -O apache-spark.tgz  "${DOWNLOAD_URL_SPARK}"\
    && mkdir -p /home/spark \
    && tar -xf apache-spark.tgz -C /home/spark --strip-components=1 \
    && rm apache-spark.tgz

# SET SPARK ENV VARIABLES
ENV SPARK_HOME="/home/spark"
ENV PATH="${SPARK_HOME}/bin/:${PATH}"

# SET PYSPARK VARIABLES
ENV PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
ENV PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH"


COPY requirements.txt .
RUN pip3 install -r requirements.txt && rm -rf requirements.txt

# Download required jars for Spark
RUN wget -P "${SPARK_HOME}/jars" https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/${SPARK_VERSION}/spark-sql-kafka-0-10_2.12-${SPARK_VERSION}.jar \
&& wget -P "${SPARK_HOME}/jars" https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_2.12/${SPARK_VERSION}/spark-streaming-kafka-0-10_2.12-${SPARK_VERSION}.jar \
&& wget -P "${SPARK_HOME}/jars" https://repo1.maven.org/maven2/org/elasticsearch/elasticsearch-spark-30_2.12/7.15.1/elasticsearch-spark-30_2.12-7.15.1.jar \
&& wget -P "${SPARK_HOME}/jars" https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/${SPARK_VERSION}/kafka-clients-${SPARK_VERSION}.jar \
&& wget -P "${SPARK_HOME}/jars" https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/${SPARK_VERSION}/spark-token-provider-kafka-0-10_2.12-${SPARK_VERSION}.jar \
&& wget -P "${SPARK_HOME}/jars" https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar \
&& apt-get remove --purge -y curl wget && rm -rf /var/lib/apt/lists/*

ARG Pathdir="$SPARK_HOME/examples/src/main/python"
# Copy the application files
COPY *.py $Pathdir

# Let's change to  "$NB_USER" command so the image runs as a non root user by default
USER $NB_UID

ENTRYPOINT ["python"]
