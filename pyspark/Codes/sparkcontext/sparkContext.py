
from pyspark import SparkContext
from pyspark import SparkConf

conf = SparkConf()
#conf.set('master','local')
conf.set('master','spark://hadoop-maste:7077')
sparkContext = SparkContext(conf=conf)
rdd = sparkContext.parallelize(range(100))
print(rdd.collect())

sparkContext.stop()
