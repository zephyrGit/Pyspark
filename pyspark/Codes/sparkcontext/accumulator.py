from pyspark import SparkContext,SparkConf
import numpy as np
conf = SparkConf()
conf.set('master','spark://hadoop-maste:7077')
context = SparkContext(conf=conf)
acc = context.accumulator(0)
print(type(acc),acc.value)
rdd = context.parallelize(np.arange(101),5)
def acc_add(a):
	acc.add(a)
	return a
rdd2 = rdd.map(acc_add)
print(rdd2.collect())
print(acc.value)
context.stop()

