## Dockerfile（三）

### 多阶段构建

在 Docker 17.05 版本前，构建 Docker 镜像时，通常会采用两种方式：

- **全部放入一个 Dockerfile**

一种方式是将所有的构建过程编包含在一个 Dockerfile 中，包括项目及其依赖库的编译、测试、打包等流程，这里可能会带来的一些问题：

1. Dockerfile 特别长，可维护性降低
2. 镜像层次多，镜像体积较大，部署时间变长
3. 源代码存在泄露的风险

例如：

编写 app.go 文件，输出 Hello World

~~~shell
package main
import "fmt"
func main(){
	fmt.Printf("Hello World!");
}
~~~

编写 Dockerfile.one 文件

~~~shell
FROM golang:1.9-alpine
RUN apk --no-cache add git ca-certificates
WORKDIR /go/src/github.com/go/helloworld/
COPY app.go .
RUN go get -d -v github.com/go-sql-driver/mysql \
&& CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o
app . \
&& cp /go/src/github.com/go/helloworld/app /root
WORKDIR /root/
CMD ["./app"]
~~~

构建镜像

~~~shell
$ docker build -t go/helloworld:1 -f Dockerfile.one .
~~~

- **分散到多个Dockerfile**

另一种方式，就是我们事先在一个 Dockerfile 将项目及其依赖库编译测试打包好后，再将其拷贝到运行环境中，这种方式需要我们编写两个 Dockerfile 和一些编译脚本才能将其两个阶段自动整合起来，这种方式虽然可以很好地规避第一种方式存在的风险，但明显部署过程较复杂。

编写 Dockerfile.build 文件

~~~shell
FROM golang:1.9-alpine
RUN apk --no-cache add git
WORKDIR /go/src/github.com/go/helloworld
COPY app.go .
RUN go get -d -v github.com/go-sql-driver/mysql \
&& CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o
app .
~~~

编写 Dockerfile.copy 文件

~~~shell
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY app .
CMD ["./app"]
~~~

新建 build.sh

~~~shell
#!/bin/sh
echo Building go/helloworld:build
docker build -t go/helloworld:build . -f Dockerfile.build
docker create --name extract go/helloworld:build
docker cp extract:/go/src/github.com/go/helloworld/app ./app
docker rm -f extract
echo Building go/helloworld:2
docker build --no-cache -t go/helloworld:2 . -f Dockerfile.copy
rm ./app
~~~

现在运行脚本即可构建镜像

~~~bash
$ chmod +x build.sh
$ ./build.sh
~~~

对比 两种方式生成的镜像大小

~~~shell
$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
go/helloworld 2 f7cf3465432c 22 seconds ago 6.47MB
go/helloworld 1 f55d3e16affc 2 minutes ago 295MB
~~~

- **使用多阶段构建**

Docker v17.05 开始支持多阶段构建 ( multistage builds )。使用多阶段构建我们就可以很容易解决前面提到的问题，并且只需要编写一个Dockerfile ：

~~~shell
FROM golang:1.9-alpine as builder
RUN apk --no-cache add git
WORKDIR /go/src/github.com/go/helloworld/
RUN go get -d -v github.com/go-sql-driver/mysql
COPY app.go .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o a
pp .
FROM alpine:latest as prod
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=0 /go/src/github.com/go/helloworld/app .
CMD ["./app"]
~~~

构建镜像

~~~shell
$ docker build -t go/helloworld:3 .
~~~

- **只构建某一阶段的镜像**

我们可以使用 as 来为某一阶段命名，例如

~~~shell
FROM golang:1.9-alpine as builder
~~~

例如当我们只想构建 builder 阶段的镜像时，我们可以在使用 docker build命令时加上 --target 参数即可

~~~shell
$ docker build --target builder -t username/imagename:tag .
~~~

- **构建时从其它镜像复制文件**

上面使用 COPY --from=0/go/src/github.com/go/helloworld/app . 从上一阶段的镜像中复制文件，我们也可以复制任意镜像中的文件

~~~shell
$ COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
~~~

- **其它制作镜像的方式**

从 rootfs 压缩包导入

格式： docker import [选项]<文件> |URL| - [<仓库名>[:<标签>]]

压缩包可以是本地文件、远程 Web 文件，甚至是从标准输入中得到。压缩包将会
在镜像 / 目录展开，并直接作为镜像第一层提交。

创建一个 OpenVZ 的 Ubuntu 14.04 模板的镜像：

~~~shell
$ docker import \
http://download.openvz.org/template/precreated/ubuntu-14.04-
x86_64-minimal.tar.gz \
openvz/ubuntu:14.04
Downloading from http://download.openvz.org/template/precreated/
ubuntu-14.04-x86_64-minimal.tar.gz
sha256:f477a6e18e989839d25223f301ef738b69621c4877600ae6467c4e528
9822a79B/78.42 MB
~~~

- **docker save 和 docker load**

Docker 还提供了 docker save 和 docker load 命令，用以将镜像保存为一个文件，然后传输到另一个位置上，再加载进来。这是在没有 Docker Registry 时的做法，现在已经不推荐，镜像迁移应该直接使用 Docker Registry，无论是直接使用 Docker Hub 还是使用内网私有 Registry 都可以。

保存镜像

~~~shell
$ docker save alpine -o filename
$ file filename
filename: POSIX tar archive
~~~

这里的 filename 可以为任意名称甚至任意后缀名，但文件的本质都是归档文件

若使用 gzip压缩

~~~shell
$ docker save alpine | gzip > alpine-latest.tar.gz
~~~

然后我们将 alpine-latest.tar.gz 文件复制到了到了另一个机器上，可以用下面这个命令加载镜像：

~~~shell
$ docker load -i alpine-latest.tar.gz
  Loaded image: alpine:latest
~~~

如果我们结合这两个命令以及 ssh 甚至 pv 的话，利用 Linux 强大的管道，我们可以写一个命令完成从一个机器将镜像迁移到另一个机器，并且带进度条的功能：

~~~shell
docker save <镜像名> | bzip2 | pv | ssh <用户名>@<主机名> 'cat | docker load'
~~~

### 镜像的实现原理

每个镜像都由很多层次构成，Docker 使用 Union FS 将这些不同的层结合到一个镜
像中去。
通常 Union FS 有两个用途, 一方面可以实现不借助 LVM、RAID 将多个 disk 挂到同一个目录下,另一个更常用的就是将一个只读的分支和一个可写的分支联合在一起，Live CD 正是基于此方法可以允许在镜像不变的基础上允许用户在其上进行一
些写操作

###  操作 Docker 容器

容器是一个独立运行的一个或一组应用，以及它们的运行态环境。

#### 启动容器

容器的启动方式有两种，一种是基于镜像新建一个容器并启动，另外一种是将在终止状态的容器重新启动

#### 新建并启动

命令为：sudo docker run

下面命令会输出一个 'hello world'

~~~shell
master@ML:~$ sudo docker run ubuntu /bin/echo 'hello world'
hello world
~~~

下面的命令会启动一个 bash 终端，允许用户交互

~~~shell
master@ML:~$ sudo docker run -it ubuntu /bin/bash
root@70d670234f22:/#
root@70d670234f22:/# echo 'hello world'
hello world
~~~

其中， -t 选项是让 Docker 分配一个伪终端并绑定到容器的标准输入上，-i 则让容器的标准输入保持打开

~~~bash
root@70d670234f22:/# pwd
/
root@70d670234f22:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
~~~



当利用 docker run 创建容器时， Docker 在后台运行的标准操作包括：

- 检查本地是否存在指定镜像，不存在从共有仓库下载
- 利用镜像创建并启动一个容器
- 分配一个文件系统，并在只读的镜像层外挂载一层可读写层
- 从宿主住进配置的网桥接口中桥接一个虚拟接口到容器中
- 从地址池配置一个 ip 地址给容器
- 执行用户指定的应用程序
- 执行完毕后容器被终止

#### 启动已终止容器

可以利用 docker container start 命令，直接将一个已经终止的容器启动运行

容器的核心为所执行的应用程序，所需要的资源都是应用程序运行所必须的。可以使用 ps 或 top 来查看进程信息

~~~shell
root@b4f0165cb922:/# ps
   PID TTY          TIME CMD
     1 pts/0    00:00:00 bash
    10 pts/0    00:00:00 ps
~~~

容器中仅运行了指定的 bash 应用，这使得 Docker 对资源的利用率极高，是货真价实的轻量级虚拟化

#### 后台运行

需要让 Docker 在后台运行而不是直接把执行命令的结果输出在当前宿主机下。可以通过 -d 参数实现

~~~shell
# 不适用 -d 容器会把输出的结果打印到宿主机上
master@ML:~$ sudo docker run ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done"
hello world
hello world
# 使用 -d 参数，容器启动后会返回唯一id
master@ML:~$ sudo docker run -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done"
 598608f5521438bd1a54518913f85c04690d7e41efc9e837fa0bedd952b7b3c8
 # 查看容器的输出信息 可以通过 docker container [container ID or NAMES]
master@ML:~$ sudo docker logs 5986
hello world
hello world
hello world
~~~

#### 终止容器

使用 docker container stop 来终止运行中的容器

当 Docker 容器中指定的应用终结时，容器也自动终止

启动容器后，可以通过 exit 命令或 ctrl + d 来退出终端，所创建的终端立即终止

终止状态的容器可以使用docker container ls -a 命令查看

docker container restart 命令会将一个运行中的容器终止，然后重新启动

#### attach 命令

docker attach 是 Docker 自带的命令。

~~~shell
master@ML:~$ sudo docker run -idt ubuntu
[sudo] password for master:         
adcbd57153b62bd32f7a753a733a05aea049f05d06547ab29dd0e9471273ac28
master@ML:~$ sudo docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS            
  PORTS               NAMESadcbd57153b6        ubuntu              "/bin/bash"         50 seconds ago      Up 48 seconds     
                      youthful_beaver
master@ML:~$ sudo docker attach adcbd
root@adcbd57153b6:/# 
~~~

**注意：如果从这个 stdin 中 exit，会导致容器停止**

#### exec 命令

-i -t 参数

docker exec 后可以跟好多个参数，主要 -t -i 参数；当 -i -t 一起使用时，可以看到Linux命令提示符

~~~shell
master@ML:~$ sudo docker run -idt ubuntu
68487a5fd121121014e3f4332a318bf25344fa3cbe8ef7bbd2153ac0d203d4a4
master@ML:~$ sudo docker exec -it 6848 bash
root@68487a5fd121:/# 
~~~

如果从这个 stdin 中exit，不会导致容器的停止。

#### 导入和导出容器

如果要导出某个容器 可以使用 docker export 命令

~~~shell
master@ML:~$ sudo docker export 6848 > ubuntu.tar
~~~

#### 导入容器快照

可以使用 docker import  从容器快照中再导入为镜像

~~~shell
$ cat ubuntu.tar | docker import - test/ubuntuV:1.0
~~~

此外可以使用指定的 URL 或者某个目录来导入

~~~shell
$ docker import http://example.com/exampleimage.tgz example/imagerepo
~~~

注：用户既可以使用 docker load 来导入镜像存储文件到本地镜像库，也可以使用 docker import 来导入一个容器快照到本地镜像库。这两者的区别在于容器快照文件将丢弃所有的历史记录和元数据信息（即仅保存容器当时的快照状态），而镜像存储文件将保存完整记录，体积也要大。此外，从容器快照文件导入时可以重新指定标签等元数据信息。

#### 删除容器

使用 docker container rm 来删除一个处于终止状态的容器

~~~shell
$ docker container rm trusting_newton
trusting_newton
~~~

如果要删除运行中的容器，可以添加 -f 参数。

#### 清理所有处于终止状态的容器

用 docker container ls -a 命令可以查看所有已经创建的包括终止状态的容器，使用下面命令可以清理所有处于终止状态的容器

~~~shell
master@ML:/usr/local/d$ sudo docker container prune
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
~~~

