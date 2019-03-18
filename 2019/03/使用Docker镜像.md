# 使用Docker 镜像

Docker 运行容器前需要在本地存在对应的镜像，如果镜像不存在本地，Docker会从镜像仓库下载。

## 从仓库获取镜像

### 获取镜像

从Docker Registry获取镜像的命令是docker pull。

~~~shell
docker pull [选项] [Docker Registry]<仓库名>:<标签>
~~~

具体个格式可以通过docker pull --help命令查看， 

- Docker Registry地址：地址的一般格式是<域名/IP>[：端口号]。默认地址是DockerHub
- 仓库名：这里的仓库名分两段名称，<用户名>/<软件名>。对于Docker Hub，如果不给出用户名，默认为library，也就是官方镜像

~~~shell
# 例子
$ docker pull ubuntu:14.01
14.04: Pulling from library/ubuntu
~~~

镜像是由多层存储结构构成的，下载也是一层一层的下载，并非单一文件，下载过程中给出了每一层的ID的前12位。并且下载结束后，给出该镜像完整的sha256的摘要，以确保下载一致性

### 运行

~~~shell
$ docker run -it --rm mysql bash
root@7d3208bb51ba:/# cd /etc/os-release 
bash: cd: /etc/os-release: Not a directory
root@7d3208bb51ba:/# cat /etc/os-release 
PRETTY_NAME="Debian GNU/Linux 9 (stretch)"
NAME="Debian GNU/Linux"
VERSION_ID="9"
VERSION="9 (stretch)"
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
root@a5204b1c5cc3:/# exit
exit
~~~

docker run 就是容器运行的命令，参数说明：

- -it：这是连个参数，一个是-i：交互式操作；一个是-t 终端。进入bash执行一些命令产看返回结果，因此需要进入交互式终端
- --rm：这个参数是说容器退出后随之将其删除，默认情况下，为了排除故障需求，退出的容器并不会立即删除，除非手动docker rm。
- mysql：这里指用mysql镜像为基础来启动容器
- bash：放在镜像名后的是命令，这里需要交互式Shell，因此用bash
- cat /etc/os-releaseL：查看当前系统版本的命令
- exit：退出容器

### 列出镜像

~~~shell
[root@localhost docker]# docker images
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
my/centos_with_python   v1.0.1              a636df47d9e9        23 minutes ago      279MB
mysql                   latest              91dadee7afee        7 days ago          477MB
centos                  latest              1e1148e4cc2c        3 months ago        202MB
training/sinatra        latest              49d952a36c58        4 years ago         447MB
~~~

列表包含了仓库名、标签、镜像ID、创建时间以及所占用的空间

- 虚悬镜像

无标签镜像被称为虚悬镜像（dangling image）

~~~shell
# 显示虚悬镜像
$ docker images -f dangling=true
~~~

~~~shell
# 删除虚悬镜像
$ docker rmi $(docker images -q -f dangling=true)
~~~

- 中间层镜像

为了加快镜像构建、重复利用资源，Docker会利用中间层镜像。默认的docker imges列表中只会显示顶层镜像，如果希望显示包括中间层镜像在内的所有镜像的话，需要加 - a参数

~~~shell
$ docker images -a
~~~

- 列出部分镜像

~~~shell
$ docekr images ubuntu
~~~

~~~shell
# 可以指定仓库和标签 
$ docker images ubuntu:16.04
~~~

docker images 还支持过滤参数 --filter，或者简写成 -f。

~~~shell
$ docker images -f since=mongo:3.2
~~~

如果想看某个之前的镜像，只需吧since改成before即可

~~~shell
$ docker images -f label=com.example.version=0.1
~~~

- 以特定格式显示

docker images 把所有的虚悬镜像的ID列出来，然后交给docker rmi命令作为参数来删除指定的这些镜像，这时需要用到 -q 参数

~~~shell
[root@localhost docker]# docker images -q
a636df47d9e9
91dadee7afee
1e1148e4cc2c
49d952a36c58
~~~

--filter 配合 -q产出指定范围的ID列表，然后送给另一个命令作为参数

**Go模板语法**

列出镜像结果，包含镜像ID和仓库名

~~~shell
[root@localhost docker]# docker images --format "{{.ID}}: {{.Repository}}"
a636df47d9e9: my/centos_with_python
91dadee7afee: mysql
1e1148e4cc2c: centos
49d952a36c58: training/sinatra
~~~

以表格等距显示，并且有标题行，和默认一样，可以自定义列：

~~~shell
[root@localhost docker]# docker images --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}"
IMAGE ID            REPOSITORY              TAG
a636df47d9e9        my/centos_with_python   v1.0.1
91dadee7afee        mysql                   latest
1e1148e4cc2c        centos                  latest
49d952a36c58        training/sinatra        latest
~~~

## 利用commit理解镜像构成

镜像是容器的基础，每次执行docker run的时候都会指定哪个镜像作为容器运行的基础。

**镜像是多层存储，每一层是在前一层的基础上进行修改；而容器同样也是多层存储，是在以镜像为基础层，在其基础上加一层作为容器运行时的存储层**

以定制一个web服务器为例子，了解镜像是如何构建的

~~~shell
# run=create容器+start容器
docker run --name webserver -d -p 80:80 nginx
~~~

这条命令会用nginx镜像启动一个容器名为webserver，并且映射了80:80端口，这样我们可以用浏览器访问这个nginx服务器

如果在Linux本机访问Docker，可以直接访问http://localhost；如果在虚拟机或云服务器上安装Docker，则需要将localhost换成虚拟机实际地址

访问浏览器，会看到一下欢迎界面

![2019-3-12 14-47-16](H:\md\2019-3-12 14-47-16.png)  

使用docker exec 命令进入容器，修改内容

~~~shell
[root@localhost docker]# docker exec -it webserver bash
root@b35a9322004c:/# echo '<h1>Hello Docker!<h1>' > /usr/share/nginx/html/index.html 
root@b35a9322004c:/# exit
exit
~~~

再次刷新浏览器，会发现内容改变了

![2019-3-12 15-3-14](H:\md\2019-3-12 15-3-14.png) 

使用docker diff 命令查看具体改动

~~~shell
[root@localhost docker]# docker diff webserver
C /usr
C /usr/share
C /usr/share/nginx
C /usr/share/nginx/html
C /usr/share/nginx/html/index.html
C /root
A /root/.bash_history
C /run
A /run/nginx.pid
C /var
C /var/cache
C /var/cache/nginx
A /var/cache/nginx/client_temp
A /var/cache/nginx/fastcgi_temp
A /var/cache/nginx/proxy_temp
A /var/cache/nginx/scgi_temp
A /var/cache/nginx/uwsgi_temp
~~~

当一个容器运行时，任何修改都会被记录与容器存储层里。而Docker提供了一个docker commit命令，可以将容器的存储层保存下来成为镜像。换句话说就是在原有镜像的基础上，再叠加上容器的存储层，并构成新的镜像

~~~shell
# docker commit 语法格式：
docker commit[选项]<容器ID或容器名>[<仓库名>][:<标签>]
~~~

将容器保存为镜像

~~~shell
[root@localhost docker]# docker commit \
> --author 'sky <11111111@qq.com>' \
> --message '修改默认网页' \
> webserver \
> nginx:v1.0.2 
sha256:6815d2ef49280f0afa197759f825e45cbab30710b7fe774f7625387a117ca91f
~~~

其中 --author 指修改作者，而--message 则是记录本次修改内容。与git版本控制相似

~~~shell
[root@localhost docker]# docker images
REPOSITORY              TAG                 IMAGE ID            CREATED              SIZE
nginx                   v1.0.2              6815d2ef4928        About a minute ago   109MB
my/centos_with_python   v1.0.1              a636df47d9e9        3 hours ago          279MB
nginx                   latest              881bd08c0b08        7 days ago           109MB
mysql                   latest              91dadee7afee        7 days ago           477MB
centos                  latest              1e1148e4cc2c        3 months ago         202MB
training/sinatra        latest              49d952a36c58        4 years ago          447MB
~~~

还可以使用docker history具体产看镜像内的历史记录， 如果比较nginx:latest的历史记录，

~~~shell
[root@localhost docker]# docker history nginx:v1.0.2
IMAGE               CREATED             CREATED BY                                      SIZE            
    COMMENT6815d2ef4928        3 minutes ago       nginx -g daemon off;                            247B            
    修改默认网页881bd08c0b08        7 days ago          /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon…   0B             
     <missing>           7 days ago          /bin/sh -c #(nop)  STOPSIGNAL SIGTERM           0B              
    <missing>           7 days ago          /bin/sh -c #(nop)  EXPOSE 80                    0B              
    <missing>           7 days ago          /bin/sh -c ln -sf /dev/stdout /var/log/nginx…   22B            
     <missing>           7 days ago          /bin/sh -c set -x  && apt-get update  && apt…   54MB           
     <missing>           7 days ago          /bin/sh -c #(nop)  ENV NJS_VERSION=1.15.9.0.…   0B             
     <missing>           7 days ago          /bin/sh -c #(nop)  ENV NGINX_VERSION=1.15.9-…   0B             
     <missing>           7 days ago          /bin/sh -c #(nop)  LABEL maintainer=NGINX Do…   0B             
     <missing>           7 days ago          /bin/sh -c #(nop)  CMD ["bash"]                 0B              
    <missing>           7 days ago          /bin/sh -c #(nop) ADD file:5ea7dfe8c8bc87ebe…   55.3MB         
~~~

定制好新镜像后，可以运行这个镜像

~~~shell
docker run --name web2 -d -p 81:80 nginx:v2
~~~

至此完成一次定制镜像，使用的是docker commit命令，手动操做给旧的镜像添加一层新的，形成新的镜像

- 慎用docker commit

比较docker diff webserver的结果，会发现除了真正要修改的/usr/share/nginx/html/index.html文件外，由于命令的执行，还有很多文件被改动和添加了。

此外使用docker commit 意味着对所有的镜像的操作都是黑箱操作，生成的镜像也称为黑箱镜像，换句话说，就是除了制作镜像的人知道执行过什么命令、怎么生成的镜像，别人无从得知

## 使用Dockerfile定制镜像

镜像定制就是定制每一层所添加的配置、文件，如果可以把每一层修改、安装、构建、操作的命令都写入一个脚本，用这个脚本来构建、定制镜像，那么之前提及的无法重复的问题、镜像构建透明性的问题、体积的问题就会解决，这个脚本就是Dockerfile。

- dockerfile

Dockerfile是一个文本文件，其中包含里一条条的指令，每一条指令构建一层，因此每一条指令的内容，就是描述该层应当如何构建

~~~shell
# 以nginx镜像为例
[root@localhost docker]# vim Dockerfile 
# 注释
FROM nginx
RUN echo "<h1>hello world!</h1>" > /usr/share/nginx/html/index.html
~~~

这个Dockerfile很简单，一共两行，涉及两条指令'FROM'和'RUN'

## FROM指定基础镜像

所谓定制镜像，一定是以一个镜像为基础，在其上进行定制，基础镜像必须指定，而FROM是指定基础镜像，因此Dockerfile中FROM是必备指令，并且必须是第一条指令

在Docker Hub(https://hub.docker.com/explore/)上有非常多的高质量的官方镜像如：mysql，nginx，mongo，tomcat等；也有一些方便开发的如：node，openjdk、python、ruby、golang等；基础操作系统如：ubuntu、debian、centos、fedora、alpine等

**Docker还存在一个特殊的镜像，名为scratch。这个镜像是虚拟的概念，并不实际存在，表示一个空白镜像**

~~~shell
$ FROM scratch
...
~~~

如果以scratch作为基础镜像，可以不以任何镜像作为基础，接下来所写的指令将作为镜像的第一层开始存在

- RUN执行命令

RUN指令是用来执行命令行命令的。RUN指令是定制镜像时最常用的指令之一。

~~~shell
RUN echo "<h1>hello world!</h1>" > /usr/share/nginx/html/index.html
~~~

exec格式：RUN["可执行文件"，'参数1'，“参数2”],这更像是函数调用中的格式

- shell脚本

~~~shell
[root@localhost docker]# vim Dockerfile 
# 注释
FROM debian:jessie

RUN buildDeps='gcc libc6-dev make' \
	&& apt-get update \
	&& apt-get install -y $buildDeps \
	&& wget -O redis.tar.gz 'http://download.redis.io/releases/redis-3.2.5.tar.gz' \
	&& mkdir -p /usr/src/redis \
	&& tar -xzf redis.tar.gz -C /usr/src/redis --strip-component s=1 \
	&& make -C /usr/src/redis \
	&& make -C /usr/src/redis install \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm redis.tar.gz \
	&& rm -r /usr/src/redis \
	&& apt-get purge -y --auto-remove $buildDeps
~~~

上述命令只有一个命令，就是编译，安装redis科执行文件。因此没有必要建立很多层，只是一层的事情。使用一个RUN指令，并使用&&将各个所需命令串联起来，将7层简化为一层。

Dockerfile支持Shell类的行尾添加\的命令换行方式，以及行首 # 注释格式。

这一组命令最后添加清理工作的命令，删除了为了编译构建所需的软件，清理了所有下载、展开的文件，并且还清理了apt缓存文件。

**构建镜像时，一定要确保每一层只添加真正需要添加的东西，任何无关的东西都应该清理掉**

~~~shell
[root@localhost docker]# docker build -t="my/redis_test" .
Sending build context to Docker daemon  2.048kB
Step 1/2 : FROM debian:jessie
jessie: Pulling from library/debian
85199fa09ec1: Pull complete 
Digest: sha256:f3acedf74ce1b8cd4d7963a366c8101e9cae7f48197c76b636e6d5a0bfada627
Status: Downloaded newer image for debian:jessie
 ---> b6ebaf83dd59
Step 2/2 : RUN buildDeps='gcc libc6-dev make' 	&& apt-get update 	&& apt-get install -y $buildDeps
 	&& wget -O redis.tar.gz 'http://download.redis.io/releases/redis-3.2.5.tar.gz' 	&& mkdir -p /usr/src/redis 	&& tar -xzf redis.tar.gz -C /usr/src/redis --strip-component s=1 	&& make -C /usr/src/redis 	&& make -C /usr/src/redis install 	&& rm -rf /var/lib/apt/lists/* 	&& rm redis.tar.gz 	&& rm -r /usr/src/redis 	&& apt-get purge -y --auto-remove $buildDeps ---> Running in 20b02a5118fd
Get:1 http://security.debian.org jessie/updates InRelease [44.9 kB]
Ign http://deb.debian.org jessie InRelease
Get:2 http://deb.debian.org jessie-updates InRelease [145 kB]
Get:3 http://deb.debian.org jessie Release.gpg [2420 B]
Get:4 http://deb.debian.org jessie Release [148 kB]
Get:5 http://security.debian.org jessie/updates/main amd64 Packages [818 kB]
Get:6 http://deb.debian.org jessie-updates/main amd64 Packages [23.0 kB]
Get:7 http://deb.debian.org jessie/main amd64 Packages [9098 kB]
~~~

## 构建镜像

使用nginx镜像Dockerfile来定制镜像

~~~shell
[root@localhost docker]# docker build -t nginx:v2 .
Sending build context to Docker daemon  2.048kB
Step 1/2 : FROM nginx
 ---> 881bd08c0b08
Step 2/2 : RUN echo "<h1>hello world!</h1>" > /usr/share/nginx/html/index.html
 ---> Running in 2270eca9bb25
Removing intermediate container 2270eca9bb25
 ---> 52a1e349d28b
Successfully built 52a1e349d28b
Successfully tagged nginx:v2
~~~

RUN指令启动了一个容器2270eca9bb25，执行了要求的命令，并最后提交了这一层52a1e349d28b，随后删除了所用到的容器2270eca9bb25

使用了docker build 命令构建镜像。

~~~shell
docker build [选项]<上下文路径/URL/>
~~~

指定了最终镜像名字 -t nginx:v3，构建成功后，可以运行这个镜像。

## 镜像构建上下文（Context）

docker build 命令最后有一个 . 。. 表示当前目录，而Dockerfile就在当前目录。

docker build工作原理，Docker在运行时分为Docker引擎（服务器端守护进程）和客户端工具。Docker的引擎提供了一组REST APT，被称为Docker Remote API，docker命令这样的客户端工具，通过API与Docker引擎交互，从而完成各种功能。虽然表面上是在本机执行各种docker功能，但实际上是使用的远程调用形式在服务器端(Docker引擎)完成。

- 复制

构建镜像时，可以通过COPY指令、ADD指令等，而docker build命令构建镜像时，并非在本地构建，而是服务器端，也就是Docker引擎中构建

docker build命令得知这个路径后，会将路径下所有内容打包，然后上传给Docker引擎

~~~shell
# 如果在Dockerfile这样写
$ COPY ./package.json /app/
# 这不是要复制docker build命令所在的目录下的package.json,ye不是复制Dockerfile所在目录下的package.json，而是复制上下文（context）目录下的package.json。
~~~

因此COPY 这类指令中的源文件的路径都是相对路径。

因为这些路径已经超出了上下文的范围，Docker引擎无法获得这些位置的文件。如果真的需要那些文件，应该将他们复制到上下文目录中去。



