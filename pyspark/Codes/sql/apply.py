from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql import SparkSession
spark = SparkSession.builder.master('spark://hadoop-maste:7077').appName('apply').getOrCreate()
df = spark.createDataFrame( [(1, 10.0), (1, 21.0), (2, 34.0), (2, 56.0), (2, 19.0)], ("id", "v"))
@pandas_udf("id long, v double", PandasUDFType.GROUPED_MAP) 
def normalize(pdf):
     v = pdf.v
     print(type(v),type(pdf))
     return pdf.assign(v=(v - v.mean()) / v.std())
df.groupby("id").apply(normalize).show() 
spark.stop()
