1. SparkContext 是pyspark的编程入口，作业的提交，任务的分发，应用的注册都会在SparkContext中进行，一个SparkContext实例代表着和Spark的一个连接，只有建立了连接才可以把作业提交到集群中去，实例化SparkContext之后才能创建RDD和Broadcast广播变量。
2. SparkContext 获取，启动pyspark --master spark://hadoop-maste:7077之后，可以通过SparkSession获取SparkContext对象

spark.SparkContext  \<SparkContext master=spark://hadoop-maste:7077 appName=Pysparkshell>

从打印的记录来看，sparkContext连接的Spark集群的地址是spark://hadoop-maste:7077

另一种获取sparcontext的方法是，引入pyspark.SparkContext进行创建，新建sparkContext.py文件

~~~python
from pyspark import SparkContext

from pyspark import SparkConf
conf = SparkConf()
conf.set("master","local")
sparkContext = SparkContext(conf=conf)
rdd = sparkContext.parallelize(range(100))
print(rdd.collect())
sparkContext.stop()
~~~

运行之前先将spark 目录下的log4j.properties配置文件中的日志级别改为如下：

