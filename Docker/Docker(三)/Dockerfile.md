## 使用 Dockerfile 定制镜像

如果我们可以把每一层修改、安装、构建、操作的命令都写入一个脚本，用这个脚本来构建、定制镜像，那么之前提及的无法重复的问题、镜像构建透明性的问题、体积的问题就都会解决。这个脚本就是 Dockerfile 。

Dockerfile 是一个文本文件，其内包含了一条条的指令(Instruction)，每一条指令
构建一层，因此每一条指令的内容，就是描述该层应当如何构建。

在一个空白目录中，建立一个文本文件，并命名为 Dockerfile ：

~~~shell
$ mkdir mynginx
$ cd mynginx
$ touch Dockerfile
# 其内容为
FROM nginx
RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index
.html
~~~

涉及到了两条指令， FROM 和 RUN。

### FROM 指定基础镜像

FROM 就是指定基础镜像，因此一个 Dockerfile 中 FROM 是必备的指令，并且必须是第一条指令。

除了选择现有镜像为基础镜像外，Docker 还存在一个特殊的镜像，名为scratch 。这个镜像是虚拟的概念，并不实际存在，它表示一个空白的镜像。

~~~shell
$ FROM scratch
。。。
~~~

### RUN执行命令

RUN 指令是用来执行命令行命令的。其格式有两种:

- shell 格式：RUN <命令> 就像直接在命令行中输入的命令一样

~~~shell
RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index
.html
~~~
- exec 格式：RUN ["可行执行文件","参数1","参数2"]

Dockerfile 正确写法

~~~bash
FROM debian:stretch
RUN buildDeps='gcc libc6-dev make wget' \
&& apt-get update \
&& apt-get install -y $buildDeps \
&& wget -O redis.tar.gz "http://download.redis.io/releases/r
edis-5.0.3.tar.gz" \
&& mkdir -p /usr/src/redis \
&& tar -xzf redis.tar.gz -C /usr/src/redis --strip-component s=1 \
&& make -C /usr/src/redis \
&& make -C /usr/src/redis install \
&& rm -rf /var/lib/apt/lists/* \
&& rm redis.tar.gz \
&& rm -r /usr/src/redis \
&& apt-get purge -y --auto-remove $buildDeps
~~~

没有使用很多个 RUN 对一一对应不同的命令，而是仅仅使用一个 RUN 指令，并使用 && 将各个所需命令串起来。将之前的 7 层，简化为了 1 层。在撰写 Dockerfile 的时候，要经常提醒自己，这并不是在写 Shell 脚本，而是在定义每一层该如何构建

Dockerfile 支持 Shell 类的行尾添加 \ 的命令换行方式，以及行首 # 进行注释的格式。良好的格式，比如换行、缩进、注释等，会让维护、排障更为容易，这是一个比较好的习惯。

这一组命令的最后添加了清理工作的命令，删除了为了编译构建所需要的软件，清理了所有下载、展开的文件，并且还清理了 apt 缓存文件。

### 构建镜像

使用 docker build 命令进行镜像构建

~~~bash
docker build [选项] <上下文路径/URL/->
~~~

### 镜像构建上下文 （Context）

docker build 命令后会有一个  **<u>.</u>** ，表示当前目录。

上下文：当构建的时候，用户会指定构建镜像的上下文的路径，docker build 命令得知这路径后，会将路径下的所有内容打包，然后上传给 Docker 引擎。这样 Docker 引擎收到这个上下文包后，展开就会获得构建镜像所需的一切文件

### 其它 docker build 的用法

直接使用 Git repo 进行构建

docker 支持URL 构建，比如直接从 Git repo 中构建

~~~shell
$ docker build https://github.com/twang2218/gitlab-ce-zh.git#:11
.1
Sending build context to Docker daemon 2.048 kB
Step 1 : FROM gitlab/gitlab-ce:11.1.0-ce.0
11.1.0-ce.0: Pulling from gitlab/gitlab-ce
aed15891ba52: Already exists
773ae8583d14: Already exists
...
~~~

用给定的 tar 压缩包进行构建

~~~bash
$ docker build http://server/context.tar.gz
~~~

从标准输入中读取 Dockerfile 进行构建

~~~shell
$ docker build - < Dockerfile
# 或
$ cat Dockerfile | docker build -
~~~

从标准输入中读取上下文压缩包进行构建

~~~shell
$ docker build - < context.tar.gz
~~~

### Dockerfile 指令详解

#### COPY 复制文件

格式：

- COPY [--chown=<user>:<group>] <源路径>... <目标路径>

- COPY [--chown=<user>:<group>] ["<源路径1>",... "<目标路径>"]

和 RUN 指令一样，也有两种格式，一种类似于命令行，一种类似于函数调用。
  COPY 指令将从构建上下文目录中 <源路径> 的文件/目录复制到新的一层的镜像内的 <目标路径> 位置。比如：

~~~bash
COPY package.json /usr/src/app
~~~

源路径 可以是多个，甚至是通配符，其通配符规则要满足 Go [filepath.Match](https://golang.org/pkg/path/filepath/#Match)规则

~~~shell
COPY hom* /mydir/
COPY hom?.txt /mydir/
~~~

目标路径可以是容器内的绝对路径，也可以是相对于工作目录的相对路径

在使用该指令时，还可以加上 --chown=<user>:<group>选项来改变文件的所属用户及用户组

~~~shell
COPY --chown=55:mygroup files* /mydir/
COPY --chown=bing files* /mydir/
COPY --chown=1 files* /mydir/
COPY --chown=10:11 files* /mydir/
~~~

#### ADD 更高级的复制文件

ADD 和 COPY 的格式和性质基本一致，但是在 COPY 上增加了一些功能。

如果 <源路径> 为一个 tar 压缩文件的话，压缩格式为 gzip , bzip2 以及xz 的情况下， ADD 指令将会自动解压缩这个压缩文件到 <目标路径> 去。
在某些情况下，这个自动解压缩的功能非常有用，比如官方镜像 ubuntu 中：

~~~shell
FROM scratch
ADD ubuntu-xenial-core-cloudimg-amd64-root.tar.gz /
...
~~~

在 Docker 官方的 Dockerfile 最佳实践文档 中要求，尽可能的使用 COPY ，因COPY 的语义很明确，就是复制文件而已，而 ADD 则包含了更复杂的功能，其行为也不一定很清晰。最适合使用 ADD 的场合，就是所提及的需要自动解压缩的场合。

另外需要注意的是， ADD 指令会令镜像构建缓存失效，从而可能会令镜像构建变
得比较缓慢。
因此在 COPY 和 ADD 指令中选择的时候，可以遵循这样的原则，所有的文件复制均使用 COPY 指令，仅在需要自动解压缩的场合使用 ADD 。

在使用该指令的时候还可以加上 --chown=<user>:<group> 选项来改变文件的所属用户及所属组。

~~~bash
ADD --chown=55:mygroup files* /mydir/
ADD --chown=bin files* /mydir/
ADD --chown=1 files* /mydir/
ADD --chown=10:11 files* /mydir/
~~~

#### CMD容器启动命令

CMD 指令的格式和 RUN 相似 ，也是两种格式：

- shell 格式： CMD <命令>
- exec 格式： CMD ["可执行文件", "参数1", "参数2"...]
- 参数列表格式： CMD ["参数1", "参数2"...] 。在指定了 ENTRYPOINT 指
  令后，用 CMD 指定具体的参数。

Docker 不是虚拟机，容器就是进程。既然是进程，那么在启动容器的时候，需要指定所运行的程序及参数。 CMD 指令就是用于指定默认的容器主进程的启动命令的。

在指令格式上，一般推荐使用 exec 格式，这类格式在解析时会被解析为 JSON数组，因此一定要使用双引号 " ，而不要使用单引号。

如果使用 shell 格式的话，实际的命令会被包装为 sh -c 的参数的形式进行执行。比如：

~~~bash
CMD echo $HOME
~~~

在实际执行中，会变为

~~~bash
CMD ["sh", "-c", "echo $HOME"]
~~~

直接执行 nginx 可执行文件，并且以前台形式运行：

~~~shell
CMD ["nginx", "-g", "daemon off;"]
~~~

#### ENTRYPOINT 入口点

ENTRYPOINT 的格式和 RUN 指令一样，分为 exec 格式和 shell 格式

ENTRYPOINT 的目的和 CMD 一样，都是在指定容器启动程序及参数。

当指定了 ENTRYPOINT 后， CMD 的含义就发生了改变，不再是直接的运行其命
令，而是将 CMD 的内容作为参数传给 ENTRYPOINT 指令，换句话说实际执行
时，将变为：

~~~shell
<ENTRYPOINT> "<CMD>"
~~~

#### 让镜像变成像命令一样使用

~~~shell
FROM ubuntu:18.04
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*
CMD [ "curl", "-s", "https://ip.cn" ]
~~~

假如使用 docker build -t myip . 来构建镜像，如果要查询当前公网 IP，只需执行

~~~shell
$ docker run myip
~~~

