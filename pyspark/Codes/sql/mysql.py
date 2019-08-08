from pyspark.sql import SparkSession
spark = SparkSession.builder.master('spark://hadoop-maste:7077').appName('mysql').getOrCreate()
df = spark.read.jdbc('jdbc:mysql://hadoop-maste:3306/test?characterEncoding=utf8','student',numPartitions=2,properties={'user':'root','password':'root','driver':'com.mysql.jdbc.Driver'})
df.show()
spark.stop()
