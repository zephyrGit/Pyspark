from pyspark import SparkFiles
import numpy as np
from pyspark import SparkContext
from pyspark import SparkConf

conf = SparkConf()
conf.set('master','spark://hadoop-maste:7077')
context = SparkContext(conf=conf)
path = 'http://192.168.0.6:808/num_data'
context.addFile(path)

rdd = context.parallelize(np.arange(10))
def fun(iterable):
	with open(SparkFiles.get('num_data')) as f:
		value = int(f.readline())
		return [x*value for x in iterable]

print(rdd.mapPartitions(fun).collect())

context.stop()	

