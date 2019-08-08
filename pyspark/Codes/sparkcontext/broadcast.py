from pyspark import SparkContext ,SparkConf
import numpy as np

conf = SparkConf()
conf.set('master','spark://hadoop-maste:7077')
context = SparkContext(conf=conf)
broad = context.broadcast(' hello ')
rdd = context.parallelize(np.arange(27),3)
print('applicationId:',context.applicationId)
print(rdd.map(lambda x:str(x)+broad.value).collect())

context.stop()

