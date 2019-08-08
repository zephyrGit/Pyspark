from pyspark import SparkFiles
import os
import numpy as np
from pyspark import SparkContext
from pyspark import SparkConf

tempdir = '/root/workspace/sparkcontext'
path = os.path.join(tempdir,'num_data')
with open(path,'w') as f:
	f.write('100')

conf = SparkConf()
conf.set('master','spark://hadoop-maste:7077')
context = SparkContext(conf=conf)
context.addFile(path)

rdd = context.parallelize(np.arange(10))
def fun(iterable):
	with open(SparkFiles.get('num_data')) as f:
		value = int(f.readline())
		return [x*value for x in iterable]

print(rdd.mapPartitions(fun).collect())

context.stop()	
