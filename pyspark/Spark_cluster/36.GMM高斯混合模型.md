
1. 高斯模型就是用高斯概率密度函数（正态分布曲线）精确地量化事物，将一个事物分解为若干的基于高斯概率密度函数（正态分布曲线）形成的模型。使用k来指定基于高斯概率密度函数形成的模型的个数  

~~~python

from pyspark.sql import SparkSession
from pyspark.ml.clustering import GaussianMixture
from pyspark.ml.evaluation import ClusteringEvaluator

spark = SparkSession.builder.master('local').appName('gmm').getOrCreate()
data = spark.read.format('libsvm').load('/data/mllib/sample_kmeans_data.txt')
gmm = GaussianMixture().setK(2).setSeed(1234)
model = gmm.fit(data)
predictions = model.transform(data)
evaluator = ClusteringEvaluator()
silhouette = evaluator.evaluate(predictions)
print('Silhouette with squared euclidean distance = ' + str(silhouette))
>>> 
Silhouette with squared euclidean distance = 0.9997530305375207
~~~
