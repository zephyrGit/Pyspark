from pyspark import SparkContext ,SparkConf
import numpy as np

conf = SparkConf()
conf.set('master','spark://hadoop-maste:7077')
conf.set('spark.python.profile','true')
context = SparkContext(conf=conf)
rdd = context.parallelize(np.arange(10),3)
print(rdd.collect())
print(context.show_profiles())
context.dump_profiles('/datas/profiles/')
context.stop()

