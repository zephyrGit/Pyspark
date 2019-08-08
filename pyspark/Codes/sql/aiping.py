from pyspark.sql import SparkSession
import pymysql as mysql
import pandas as pd
conn=mysql.connect(host="hadoop-mysql",user="root",passwd="root",db="test",charset='utf8')
sql="select * from ps_resume"
df=pd.read_sql(sql,conn)
print(df.head(5))
spark = SparkSession.builder.master('spark://hadoop-maste:7077').appName('ai').getOrCreate()
sc = spark.sparkContext
rdd = sc.parallelize(df.values,10)
print(rdd.take(2))
#spark_df = spark.createDataFrame(df)
#print(spark_df.show())

spark.stop()
