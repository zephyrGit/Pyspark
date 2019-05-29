# .Spark学习(Python版本)：连接Hive读写数据（DataFrame）

![96](https://upload.jianshu.io/users/upload_avatars/1780773/f1bda814e766?imageMogr2/auto-orient/strip|imageView2/1/w/96/h/96)



> ###### Step1. 让Spark包含Hive支持

为了让Spark能够访问Hive，必须为Spark添加Hive支持。按照之前的步骤，我们下载的是Spark官方提供的预编译版本，通常是不包含Hive支持的，需要采用源码编译，编译得到一个包含Hive支持的Spark版本。

这里直接使用林子雨老师已经编译好的包含hive支持的Spark: [spark-2.1.0-bin-h27hive.tgz](https://pan.baidu.com/s/1nv8Y2hj). 然后按照[1.Spark学习(Python版本)：Spark安装](https://www.jianshu.com/p/5e05cdf44fcd)中介绍的方法安装即可。

命令如下：

```
cd ~/下载/
sudo tar -zxf ~/下载/spark-2.1.0-bin-h27hive.tgz -C /usr/local
cd /usr/local
sudo mv ./spark-2.1.0-bin-h27hive ./sparkwithhive
sudo chown -R mashu:mashu ./sparkwithhive #mashu是我的用户名
cd /usr/local/sparkwithhive/
cp ./conf/spark-env.sh.template ./conf/spark-env.sh
vim ./conf/spark-env.sh
```

vim编辑器打开了spark-env.sh文件，请在这个文件的开头第一行增加一行如下内容：
`export SPARK_DIST_CLASSPATH=$(/usr/local/hadoop/bin/hadoop classpath)`

然后，保存文件，退出vim编辑器，继续执行下面命令.

```
cd /usr/local/sparkwithhive
#下面运行一个样例程序，测试是否成功安装
bin/run-example SparkPi 2>&1 | grep "Pi is"
```

如果能够得到下面信息，就说明成功了。
`Pi is roughly 3.146315731578658`

为了让Spark能够访问Hive，需要把Hive的配置文件hive-site.xml拷贝到Spark的conf目录下，请在Shell命令提示符状态下操作：

```
mashu@mashu-Inspiron-5458:/usr/local/sparkwithhive$ cd /usr/local/sparkwithhive/conf
mashu@mashu-Inspiron-5458:/usr/local/sparkwithhive/conf$ cp /usr/local/hive/conf/hive-site.xml .
```

启动pyspark，

```
mashu@mashu-Inspiron-5458:/usr/local/sparkwithhive/conf$ cd /usr/local/sparkwithhive
mashu@mashu-Inspiron-5458:/usr/local/sparkwithhive$ ./bin/pyspark
>>> from pyspark.sql import HiveContext
>>> 
```

> ###### `输入上面的语句没有报错就说明当前启动的Spark版本可以支持Hive了吗？NO!`

###### `1. 由于Spark1.0到2.0后jar包文件结构改变，所以启动hive会出现以下报错`





![img](https://upload-images.jianshu.io/upload_images/1780773-c0140ca442d251fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/701/format/webp)

```
我们需要修改下hive启动脚本，命令如下：
```



```
mashu@mashu-Inspiron-5458:~$ cd /usr/local/hive/bin
mashu@mashu-Inspiron-5458:/usr/local/hive/bin$ vim hive
```



![img](https://upload-images.jianshu.io/upload_images/1780773-125b8e2bc2568f51.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/912/format/webp)

###### `2. 我们更换了新的Spark包，因此用新的支持Hive的Spark包时，需要把环境变量也更新一下：`

```
我自己的电脑上老的Spark是2.3.0版本，新的Spark是2.1.0版本，除了SPARK_HOME要修改外，还要修改py4j-0.10.X-src.zip的版本号。如图：
```



![img](https://upload-images.jianshu.io/upload_images/1780773-c66057bf55fa5e1a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/939/format/webp)

> ###### Step2. 在Hive中创建数据库和表

依次启动MySQL、Hadoop、Hive、和pyspark（包含Hive支持）。

```
mashu@mashu-Inspiron-5458:~$ service mysql start  #可以在Linux的任何目录下执行该命令
mashu@mashu-Inspiron-5458:~$ cd /usr/local/hadoop
mashu@mashu-Inspiron-5458:/usr/local/hadoop$ ./sbin/start-dfs.sh
mashu@mashu-Inspiron-5458:/usr/local/hadoop$ hive

mashu@mashu-Inspiron-5458:~$ cd /usr/local/sparkwithhive
mashu@mashu-Inspiron-5458:/usr/local/sparkwithhive$ ./bin/pyspark
```

进入Hive，新建一个数据库sparktest，并在这个数据库下面创建一个表student，并录入两条数据。

```
hive> create database if not exists sparktest;//创建数据库sparktest
hive> show databases; //显示一下是否创建出了sparktest数据库
//下面在数据库sparktest中创建一个表student
hive> create table if not exists sparktest.student(
> id int,
> name string,
> gender string,
> age int);
hive> alter table student change id id int auto_increment primary key;
hive> use sparktest; //切换到sparktest
hive> show tables; //显示sparktest数据库下面有哪些表
hive> insert into student values(1,'Xueqian','F',23); //插入一条记录
hive> insert into student values(2,'Weiliang','M',24); //再插入一条记录
hive> select * from student; //显示student表中的记录
OK
1   Xueqian F   23
2   Weiliang    M   24
Time taken: 1.145 seconds, Fetched: 2 row(s)
```

> ###### Step3. Spark连接Hive读数据

假设已经启动了MySQL、Hadoop、Hive、和pyspark（包含Hive支持）。
在进行编程之前，我们需要做一些准备工作，我们需要修改“/usr/local/sparkwithhive/conf/spark-env.sh”这个配置文件：

```
cd /usr/local/sparkwithhive/conf/
vim spark-env.sh
```

在spark-env.sh中添加：

```
export JAVA_HOME=/usr/lib/jvm/default-java
export CLASSPATH=$CLASSPATH:/usr/local/hive/lib
export SCALA_HOME=/usr/local/scala
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
export HIVE_CONF_DIR=/usr/local/hive/conf
export SPARK_CLASSPATH=$SPARK_CLASSPATH:/usr/local/hive/lib/mysql-connector-java-5.1.40-bin.jar
```

现在终于可以编写调试Spark连接Hive读写数据的代码了。
请在pyspark（包含Hive支持）中执行以下命令从Hive中读取数据：

```
from pyspark.sql import HiveContext
hive_context = HiveContext(sc)
hive_context.sql('use sparktest')
hive_context.sql('select * from student').show()
```

输出了表内容如下：
`注意这时Spark的版本号是2.1.0（即为我们后来安装的支持Hive的Spark的版本哦～）`



![img](https://upload-images.jianshu.io/upload_images/1780773-fa9e65df00f09a24.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/527/format/webp)



> ###### Step4. Spark连接Hive写数据

到pyspark（含Hive支持）终端窗口，输入以下命令：

```
from pyspark.sql.types import Row
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType
from pyspark.sql.types import IntegerType
from pyspark.sql import HiveContext
hive_context = HiveContext(sc)
hive_context.sql('use sparktest')
studentRDD = spark.sparkContext.parallelize(["3 Rongcheng M 26","4 Guanhua M 27"]).map(lambda line : line.split(" "))
schema = StructType([StructField("id", IntegerType(), True),StructField("name", StringType(), True),StructField("gender", StringType(), True),StructField("age",IntegerType(), True)])
rowRDD = studentRDD.map(lambda p : Row(int(p[0]),p[1].strip(), p[2].strip(),int(p[3])))
//建立起Row对象和模式之间的对应关系，也就是把数据和模式对应起来
studentDF = spark.createDataFrame(rowRDD, schema)
studentDF.registerTempTable("tempTable")
hive_context.sql('insert into student select * from tempTable')
```

再切换到hive窗口查询student表的变化：插入操作执行成功!
(林子雨老师课程[4.5.3 连接Hive读写数据](http://dblab.xmu.edu.cn/blog/1729-2/)有些许遗漏和错误，上文对这些做了少许修改。)



![img](https://upload-images.jianshu.io/upload_images/1780773-0130a2ec51431295.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/525/format/webp)



