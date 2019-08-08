from pyspark import SparkContext,SparkConf
conf = SparkConf()
conf.setAppName('Spark')
sc = SparkContext(conf = conf)
print(sc.appName)
sc.stop()
