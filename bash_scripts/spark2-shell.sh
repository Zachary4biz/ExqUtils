#!/bin/bash
# 拷贝更新一些jar包
\cp apus-dist-1.0-SNAPSHOT/lib/algo-common-1.0-SNAPSHOT.jar ~/lib/
\cp apus-dist-1.0-SNAPSHOT/lib/algo-news-recommender-1.0-SNAPSHOT.jar ~/lib/

libpath="/home/zhoutong/lib"
DEPEDENCE_JARS=""
for jar in `ls -1 ${libpath}/*.jar`
do
  DEPEDENCE_JARS=${DEPEDENCE_JARS},$jar
done
DEPEDENCE_JARS=${DEPEDENCE_JARS}

#export HADOOP_USER_NAME=atlas
export SPARK_KAFKA_VERSION=0.10
# /opt/spark2.2/bin/spark-shell \
#--master yarn-client  \
#--driver-memory 10g  \
#--num-executors 16 \
#--executor-memory 10g  \
#--executor-cores 4  \
#--queue biz.ml \
#--conf spark.default.parallelism=256 \
#--conf spark.port.maxRetries=100  \
#--conf spark.driver.maxResultSize=16g  \
#--conf spark.streaming.kafka.consumer.cache.enabled=false \
#--conf spark.yarn.executor.memoryOverhead=2g \
#--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.2.0 \
#--packages org.mongodb.spark:mongo-spark-connector_2.11:2.2.0 \
#--jars ${DEPEDENCE_JARS} 

spark2-shell \
--conf spark.default.parallelism=256 \
--conf spark.port.maxRetries=100  \
--conf spark.driver.maxResultSize=16g  \
--conf spark.streaming.kafka.consumer.cache.enabled=false \
--conf spark.yarn.executor.memoryOverhead=2g \
--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.2.0 \
--packages org.mongodb.spark:mongo-spark-connector_2.11:2.2.0 \
--jars ${DEPEDENCE_JARS}