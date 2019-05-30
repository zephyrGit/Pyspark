1.pyspark整体架构

![img](https://note.youdao.com/yws/public/resource/e9aeefa075413da0f2c8ca0594e5d1d4/xmlnote/026AB6E837FA45BEBACD593E391A22A4/10347)



2.环境准备

 a.安装anaconda:选择linux版本python3.6

![img](https://note.youdao.com/yws/public/resource/e9aeefa075413da0f2c8ca0594e5d1d4/xmlnote/1BAAF397CE9A4452BC1C0374DD11893F/10350)



b.下载好之后，使用bash Anaconda3-4.4.0-Linux-x86_64.sh命令安装anaconda【注意：anaconda采用默认的安装路径，不然在运行pyspark的时候会报“permission denied”的错误】

生成配置文件： jupyter notebook-generate-config

c.配置jupyter:





d.启动jupyter  notebook:nohup jupyter notebook --allow-root &



e.访问jupyter note book:

![img](https://note.youdao.com/yws/public/resource/e9aeefa075413da0f2c8ca0594e5d1d4/xmlnote/548F525F331D48309CC23BAFD0DBA335/10368)



f.spark集群环境：这里分享我在51上发布的面试视频。<http://edu.51cto.com/center/course/lesson/index?id=152333>



g.在后台运行pyspark命令：发现spark2默认使用的时候python2.7.5，我们要把它改成Python3.6

![img](https://note.youdao.com/yws/public/resource/e9aeefa075413da0f2c8ca0594e5d1d4/xmlnote/CB0479A379BB4565A997C1350B4F82C1/10376)



编辑用于根目录下的.bashrc文件，添加如下配置【anaconda自动添加】

![img](https://note.youdao.com/yws/public/resource/e9aeefa075413da0f2c8ca0594e5d1d4/xmlnote/289139F34C44439B8AAAFFCBE2091AFE/10582)

记得source ~/.bashrc使配置的用户变量生效。



这时再看python版本号就对了。

![img](https://note.youdao.com/yws/public/resource/e9aeefa075413da0f2c8ca0594e5d1d4/xmlnote/C02D2733954A4D1F82D51BED8F148C78/10580)



为了使用jupyter，在~/.bashrc中加入如下配置

![img](https://note.youdao.com/yws/public/resource/e9aeefa075413da0f2c8ca0594e5d1d4/xmlnote/82AA41BB41804047B54D86C592CF12F9/10587)

并source ~/.bashrc

export PYSPARK_DRIVER_PYTHON=jupyter

export PYSPARK_DRIVER_PYTHON_OPTS=notebook

在运行pyspark结果如下

![img](https://note.youdao.com/yws/public/resource/e9aeefa075413da0f2c8ca0594e5d1d4/xmlnote/D62F8CC1F6CF4335A0B474EFB7AC87D0/10591)



jupyter启动成功。Web界面如下：

![img](https://note.youdao.com/yws/public/resource/e9aeefa075413da0f2c8ca0594e5d1d4/xmlnote/735D37A089A04303A3C47351EB57F53E/10595)



目前为止，我们可以使用jupyter编写Spark程序了。