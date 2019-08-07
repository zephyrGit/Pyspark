# Pyspark-Cluster

## <font>Docker 从入门到实战</font>

## Pyspark
pyspark是Spark的python API，提供了使用python编写并提交大数据处理作业的接口。在pyspark里大致分为5个主要的模块

### 1. pyspark模块，这个模块四最基础的模块，里面实现了最基础的编写Spark作业的API。这个模块里面有以下内容：
  - Sparkcontext:它是编写Spark程序的主入口
  - RDD：分布式弹性数据集，是Spark内部中最重要的抽象
  - Broadcast：在各个任务task中重复使用的广播变量
  - Accumulator：一个只能增加的累加器，在各个任务中都可以进行累加，最终进行全局累加
  - SparkConf：一个配置对象，用来对Spark中的例如资源，内核个数，提交模式等的配置
  - SparkFiles：文件访问API
  - StorageLevel：它提供了细粒度的对于数据的缓存、持久化级别
  - TaskContext：实验性质的API，用于获取运行中任务的上下文信息。

   
### 2. pyspark.sql模块，这个模块是架构在RDD之上的高级模块，提供了SQL的支持，包含以下内容：
 - SparkSession：SparkSQL的主入口，其内部仍然是调用SparkContext的
 - DataFrame：分布式的结构化的数据集，最终的计算仍然转换为RDD上的计算
 - Column：DataFrame中的列
 - Row：DataFrame中的行
 - GroupedData：这里提供聚合数据的一些方法
 - DataFrameNaFunctions:处理缺失数据的方法
 - DataFrameStatFunctions：提供统计数据的一些方法
 - functions：内建的可用于DataFrame的方法
 - types：可用的数据类型
 - Window:提供窗口函数的支持
    
      
### 3. pyspark.streaming这个模块主要是用来处理流数据
  从外部的消息中间件如kafka，flume或者直接从网络接收数据，来进行实时的流数据处理。其内部会将接收到的数据转换为DStream，DStream的内部实际上就是RDD。pyspark.streaming对流数据的支持还不是很完善，不如原生的Scala语言和Java语言。但是仍然会包括最主要的原理。


### 4. pyspark.ml这个模块主要是做机器学习的
  里面实现了很多机器学习算法，包括分类、回归、聚类、推荐。这个的内容我们会囊括最主要的机器学习算法。pyspark.ml这个模块现已经成为主要的机器学习模块，其内部实现是基于DataFrame数据框。
  
  
### 5. pyspark.mllib这个模块也是做机器学习的
  但是这个模块底层使用的RDD，RDD在性能上优化的余地较少，因此现在最新的机器学习算法都是用基于DataFrame的API来实现。但这个模块里面也有很多有用的机器学习算法。


1-7  ： SparkContext 是pyspark的编程入口，作业的提交，任务的分发
8-20 ： SparkSQL是Spark的四大组件之一，也是Spark数据处理中用的最多的组件。SparkSQL在SparkCore的基础上对外提供了SQL接口，可以让熟悉SQL的技术人员快速上手
21-39： Spark机器学习及常用算法
