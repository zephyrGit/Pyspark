## ENV 设置环境变量

格式有两种：

- ENV <key><value>
- ENV <key1>=<value1> <key2>=<key2> ...

这个指令很简单，就是设置环境变量而已，无论后面的，如：还是运行时的应用，都可以直接使用这里的环境变量

~~~bash
ENV VERSION=1.0 DEBUG=on \
	NAME="Happy Feet"
~~~

这个例子中演示了如何换行，以及对含有空格的值用双引号括起来的办法，这和
Shell 下的行为是一致的。
定义了环境变量，那么在后续的指令中，就可以使用这个环境变量。比如在官方
node 镜像 Dockerfile 中，就有类似这样的代码

~~~shell
ENV NODE_VERSION 7.2.0
RUN curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NOD
E_VERSION-linux-x64.tar.xz" \
&& curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS25
6.txt.asc" \
&& gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.tx
t.asc \
&& grep " node-v$NODE_VERSION-linux-x64.tar.xz\$" SHASUMS256.t
xt | sha256sum -c - \
&& tar -xJf "node-v$NODE_VERSION-linux-x64.tar.xz" -C /usr/loc
al --strip-components=1 \
&& rm "node-v$NODE_VERSION-linux-x64.tar.xz" SHASUMS256.txt.as
c SHASUMS256.txt \
&& ln -s /usr/local/bin/node /usr/local/bin/nodejs
~~~

在这里先定义了环境变量 NODE_VERSION ，其后的 RUN 这层里，多次使用
$NODE_VERSION 来进行操作定制。可以看到，将来升级镜像构建版本的时候，只
需要更新 7.2.0 即可， Dockerfile 构建维护变得更轻松了。
下列指令可以支持环境变量展开：
ADD 、 COPY 、 ENV 、 EXPOSE 、 LABEL 、 USER 、 WORKDIR 、 VOLUME 、
STOPSIGNAL 、 ONBUILD 。
可以从这个指令列表里感觉到，环境变量可以使用的地方很多，很强大。通过环境
变量，我们可以让一份 Dockerfile 制作更多的镜像，只需使用不同的环境变量
即可。

### ARG 构建参数

格式：ARG <参数名>[=<默认值>]

构建参数和 ENV 的效果一样，都是设置环境变量。所不同的是， ARG 所设置的构建环境的环境变量，在将来容器运行时是不会存在这些环境变量的。但是不要因此就使用 ARG 保存密码之类的信息，因为 docker history 还是可以看到所有值的。
Dockerfile 中的 ARG 指令是定义参数名称，以及定义其默认值。该默认值可以在构建命令 docker build 中用 --build-arg <参数名>=<值> 来覆盖。

## VOLUME 定义匿名卷

格式：

- VOLUME ["<路径1>", "<路径2>"]

- VOLUME <路径>

容器运行时应该尽量保持容器存储层不发生写操作，对于数据库类需要保存动态数据的应用，其数据库文件应该保存于卷(volume)中，容器运行时应该尽量保持容器存储层不发生写操作，对于数据库类需要保存动态数据的应用，其数据库文件应该保存于卷(volume)中

~~~bash
VOLUME /data
~~~

这里的 /data 目录就会在运行时自动挂载为匿名卷，任何向 /data 中写入的信息都不会记录进容器存储层，从而保证了容器存储层的无状态化。当然，运行时可以覆盖这个挂载设置。

## EXPOSE 声明端口
格式为 EXPOSE <端口1> [<端口2>...] 。
EXPOSE 指令是声明运行时容器提供服务端口，这只是一个声明，在运行时并不会因为这个声明应用就会开启这个端口的服务。在 Dockerfile 中写入这样的声明有两个好处，一个是帮助镜像使用者理解这个镜像服务的守护端口，以方便配置映射；另一个用处则是在运行时使用随机端口映射时，也就是 docker run -P时，会自动随机映射 EXPOSE 的端口。
要将 EXPOSE 和在运行时使用 -p <宿主端口>:<容器端口> 区分开来。 -p ，是
映射宿主端口和容器端口

#### WORKDIR 指定工作目录

格式为 WORKDIR <工作目录路径> 。
使用 WORKDIR 指令可以来指定工作目录（或者称为当前目录），以后各层的当前
目录就被改为指定的目录，如该目录不存在， WORKDIR 会帮你建立目录。

### USER 指定当前用户
格式： USER <用户名>[:<用户组>]
USER 指令和 WORKDIR 相似，都是改变环境状态并影响以后的层。 WORKDIR
是改变工作目录， USER 则是改变之后层的执行 RUN , CMD 以及
ENTRYPOINT 这类命令的身份。
当然，和 WORKDIR 一样， USER 只是帮助你切换到指定用户而已，这个用户必
须是事先建立好的，否则无法切换。

如果以 root 执行的脚本，在执行期间希望改变身份，比如希望以某个已经建立
好的用户来运行某个服务进程，不要使用 su 或者 sudo ，这些都需要比较麻烦
的配置，而且在 TTY 缺失的环境下经常出错。建议使用 gosu 。

#### HEALTHCHECK 健康检查

格式：

- HEALTHCHECK [选项] CMD <命令> ：设置检查容器健康状况的命令
- HEALTHCHECK NONE ：如果基础镜像有健康检查指令，使用这行可以屏蔽掉
  其健康检查指令

HEALTHCHECK 支持下列选项：

- --interval=<间隔> ：两次健康检查的间隔，默认为 30 秒；
- --timeout=<时长> ：健康检查命令运行超时时间，如果超过这个时间，本次健康检查就被视为失败，默认 30 秒；
- --retries=<次数> ：当连续失败指定次数后，则将容器状态视为 unhealthy ，默认 3 次。

假设我们有个镜像是个最简单的 Web 服务，我们希望增加健康检查来判断其 Web
服务是否在正常工作，我们可以用 curl 来帮助判断，其 Dockerfile 的
HEALTHCHECK 可以这么写：

~~~shell
FROM nginx
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib
/apt/lists/*
HEALTHCHECK --interval=5s --timeout=3s \
CMD curl -fs http://localhost/ || exit 1
~~~

为了帮助排障，健康检查命令的输出（包括 stdout 以及 stderr ）都会被存储于健康状态里，可以用 docker inspect 来查看。

~~~shell
$ docker inspect --format '{{json .State.Health}}' web | python
-m json.tool
{
    "FailingStreak": 0,
    "Log": [
    	{
            "End": "2016-11-25T14:35:37.940957051Z",
            "ExitCode": 0,
            "Output": "<!DOCTYPE html>\n<html>\n<head> \n<title> Welcome to nginx!</title>\n<style>\n body {\n width: 35
em;\n margin: 0 auto;\n font-family: Tahoma, Verdana, Arial, sans-serif;\n }\n</style>\n</head>\n<body>\n<h1>Welcome to nginx!</h1>\n<p>If you see this page, the nginx web server is successfully installed and\nworking. Further configuration is required.</p>\n\n<p>For online documentation and support please refer to\n<a href=\"http://nginx.org/\">nginx.org</a>.<br/>
\nCommercial support is available at\n<a href=\"http://nginx.com
/\">nginx.com</a>.</p>\n\n<p><em>Thank you for using nginx.</em>
</p>\n</body>\n</html>\n",
			"Start": "2016-11-25T14:35:37.780192565Z"
		}
	],
	"Status": "healthy"
}
~~~

#### ONBUILD 

格式：ONBUILD <其它指令>

ONBUILD 是一个特殊的指令，它后面跟的是其它指令，比如 RUN , COPY 等，而这些指令，在当前镜像构建时并不会被执行。只有当以当前镜像为基础镜像，去构建下一级镜像的时候才会被执行

制作 Node.js 所写的应用的镜像。我们都知道 Node.js 使用 npm 进行包管理，所有依赖、配置、启动信息等会放到 package.json 文件里。在拿到程序代码后，需要先进行 npm install 才可以获得所有需要的依赖。然后就可以通过 npm start 来启动应用。因此，一般来说会这样写 Dockerfile ：

~~~shell
FROM node:slim
RUN mkdir /app
WORKDIR /app
COPY ./package.json /app
RUN [ "npm", "install" ]
COPY . /app/
CMD [ "npm", "start" ]
~~~

把这个 Dockerfile 放到 Node.js 项目的根目录，构建好镜像后，就可以直接拿来启动容器运行。

可以做一个基础镜像，然后各个项目使用这个基础镜像呢？这样基础镜像更新，各个项目不用同步 Dockerfile 的变化，重新构建后就继承了基础镜像的更新？好吧，可以，让我们看看这样的结果。那么上面的这个 Dockerfile就会变为：

~~~shell
FROM node:slim
RUN mkdir /app
WORKDIR /app
CMD [ "npm", "start" ]
~~~

这里我们把项目相关的构建指令拿出来，放到子项目里去。假设这个基础镜像的名
字为 my-node 的话，各个项目内的自己的 Dockerfile 就变为：

~~~shell
FROM my-node
COPY ./package.json /app
RUN [ "npm", "install" ]
COPY . /app/
~~~

基础镜像变化后，各个项目都用这个 Dockerfile 重新构建镜像，会继承基础镜像的更新。

那么，问题解决了么？没有。准确说，只解决了一半。如果这个 Dockerfile 里
面有些东西需要调整呢？比如 npm install 都需要加一些参数，那怎么办？这
一行 RUN 是不可能放入基础镜像的，因为涉及到了当前项目的./package.json ，难道又要一个个修改么？所以说，这样制作基础镜像，只解决了原来的 Dockerfile 的前4条指令的变化问题，而后面三条指令的变化则完全没办法处理。

ONBUILD 可以解决这个问题。让我们用 ONBUILD 重新写一下基础镜像的
Dockerfile :

~~~shell
FROM node:slim
RUN mkdir /app
WORKDIR /app
ONBUILD COPY ./package.json /app
ONBUILD RUN [ "npm", "install" ]
ONBUILD COPY . /app/
CMD [ "npm", "start" ]
~~~

这次我们回到原始的 Dockerfile ，但是这次将项目相关的指令加上ONBUILD ，这样在构建基础镜像的时候，这三行并不会被执行。然后各个项目的Dockerfile 就变成了简单地：

~~~shell
FROM my-node
~~~

当在各个项目目录中，用这个只有一行的 Dockerfile 构建镜像时，之前基础镜像的那三行 ONBUILD 就会开始执行，成功的将当前项目的代码复制进镜像、并且针对本项目执行 npm install ，生成应用镜像。

- Dockerfie 官方文档：https://docs.docker.com/engine/reference/builder/

- Dockerfile 最佳实践文档：https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/
- Docker 官方镜像 Dockerfile ：https://github.com/docker-library/docs

