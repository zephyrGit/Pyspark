from pyspark import SparkContext ,SparkConf
import numpy as np

conf = SparkConf()
conf.set('master','spark://hadoop-maste:7077')
context = SparkContext(conf=conf)

rdd = context.binaryFiles('/datas/pics/')
print('applicationId:',context.applicationId)
result = rdd.collect()
for data in result:
	print(data[0],data[1][:10])
context.stop()

