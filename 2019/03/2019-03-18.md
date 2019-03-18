# 操作 Docker 容器

容器是 Docker 又一核心概念

容器是独立运行的一个或一组应用，以及它们的运行态环境。

## 启动容器

容器有两种方式，一种是基于镜像新建一个容器并启动，另外一个是将在中止状态的容器重新启动

### 新建并启动

所需命令为 docker run

下面命令会输出一个 hello docker 之后终止容器，这与在本地直接执行 /bin/echo 几乎没有任何区别

~~~shell
[root@localhost ~]# docker run ubuntu:16.04 /bin/echo 'hello docker'
hello docker
~~~

下面命令启动一个 bash 终端，允许用户进行交互

~~~shell
[root@localhost ~]# docker run -i -t ubuntu:16.04 /bin/bash
root@d55fc7477c2d:/# 
~~~

其中 -t 选项让 Docker 分配一个伪终端，并绑定到容器的标准输入上， -i 则让容器的标准输入保持打开

在交互模式下，用户可以通所创建的终端来输入命令

~~~shell
root@d55fc7477c2d:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
root@d55fc7477c2d:/# 
~~~

当利用 docker run 来创建容器时， Docker 在后台运行的标准操作包括：

- 检查本地是否存在指定的镜像，不存在就从共有仓库下载
- 利用镜像创建并启动一个容器
- 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
- 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
- 从地址池配置一个IP地址给容器
- 执行用户指定的应用程序
- 执行完毕后容器终止

### 启动已终止容器

可以利用 docker start 命令，直接将一个已终止的容器启动运行

容器的核心所执行的应用程序，所需要的资源都是应用程序运行所必需的。在伪终端中利用 ps 或 top 来查看进程信息

~~~shell
root@d55fc7477c2d:/# ps
   PID TTY          TIME CMD
     1 pts/0    00:00:00 bash
    11 pts/0    00:00:00 ps
~~~

由上可见，容器中仅运行了指定的bash应用，这种特点使得 Docker 对资源的利用率极高，是货真价实的轻量级虚拟化

### 后台运行

需要让 Docker 在后台运行而不是直接把执行命令的结果输出在当前宿主机下，可以通过添加 -d 参数来实现

- 不适用 -d 参数运行容器， 容器会把输出结果打印到宿主机上

~~~shell
[root@localhost ~]# docker run ubuntu:16.04 /bin/sh -c "while true; do echo hello Docker;
 sleep 1; done"
hello Docker
hello Docker
hello Docker
hello Docker
~~~

- 使用了 -d 参数

~~~shell
[root@localhost ~]# docker run -d  ubuntu:16.04 /bin/sh -c "while true; do echo hello Doc
ker; sleep 1; done"0a3239fb83d6a8c875a2cf93e104bf514d4663b9c06cfbae8177d47543803e10
~~~

此时容器会在后台运行，并不会把输出结果打印到宿主机上（输出结果使用docker logs 查看）

注：容器运行是否会长久运行，是与docker run指定的命令有关，和 -d 参数无关

使用 -d 参数启动后会返回一个唯一的id，可以通过 docker ps 命令来查看容器信息

获取容器的输出信息，可以通过docker logs命令

~~~shell
# docker logs [container ID or NAMES]
[root@localhost ~]# docker logs 0a3239fb83d6  
hello Docker
hello Docker
hello Docker
hello Docker
hello Docker
~~~

### 终止容器

可以使用 docker stop 来终止一个运行中的容器

~~~shell
[root@localhost ~]# docker stop 0a3239fb83d6
0a3239fb83d6
~~~

处于终止状态的容器，可以通过 docker start 命令 重新启动

docker restart 命令会将一个运行态的容器终止，然后重新启动它

### 进入容器

在使用 -d 参数时，容器会进入后台，某些时候需要进入容器进行操作， 有很多方法，包括 docker attach 命令或 nsenter 工具等

- **attach命令**

docker attach 是 Docker 自带的命令

~~~shell
[root@localhost ~]# docker run -idt ubuntu:16.04
dd38f4350342d6e672e2fa149092b9635fdb6aafa142762bf923650b71a5d24f
[root@localhost ~]# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS   
           PORTS               NAMESdd38f4350342        ubuntu:16.04        "/bin/bash"         6 seconds ago       Up 5 seco
nds                            serene_lamarr
[root@localhost ~]# docker attach serene_lamarr
root@dd38f4350342:/# 
~~~

但使用 attach 命令有时候并不方便， 当多个窗口同时attach到同一个容器的时候，所有的窗口都会同步显示，当某个窗口命令阻塞时，其他窗口也无法执行操作。

- **nsenter命令**

安装 

nsenter 工具在 util-linux 包2.23版本后包含。如果 util-linux包没有该命令，可以按照下面的方法从源码安装

~~~shell
[root@localhost tmp]#$ cd /tmp; curl https://www.kernel.org/pub/linux/utils/util-linu
x/v2.24/util-linux-2.24.tar.gz | tar -zxf-; cd util-linux-2.24;
$ ./configure --without-ncurses
$ make nsenter && sudo cp nsenter /usr/local/bin
/util-linux-2.30.tar.gz
~~~

- **注：如安装过程报错如下，请运行 yum install gcc**

~~~shell
configure: error: in `/tmp/util-linux-2.24':
configure: error: no acceptable C compiler found in $PATH
See `config.log' for more details
~~~

### 使用

nsenter 启动一个新的 shell 进程（默认是/bin/bash），同时会把这个新进程切换到和目标（target）进程相同的命名空间，这样就相当于进入了容器内部。nsenter 要正常工作需要 root 权限。

Ubuntu：14.04仍然使用的是util-linux2.20。 安装最新版本的util-linux（2.30）版，运行如下命令：

~~~shell
wget https://www.kernel.org/pub/linux/utils/util-linux/v2.30/u
til-linux-2.30.tar.xz; tar xJvf util-linux-2.30.tar.xz
$ cd util-linux-2.30
$ ./configure --without-ncurses && make nsenter
$ sudo cp nsenter /usr/local/bin
~~~

为了链接到容器，还需要找到容器的第一个进程PID，可以通过下面命令获取

~~~shell
PID=$(docker inspect --format "{{.State.Pid}}" <container>)
~~~

通过这个PID，就可以链接到这个容器

~~~shell
$ nsenter --target $PID --mount --uts --ipc --net --pid
~~~

例子

~~~shell
[root@localhost docker]# docker run -idt ubuntu:16.04
5012d6f6f0ab1d4ef82760a36ad281f13a6670b6d4fcad158ae7753a94b9fa00
[root@localhost docker]# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS      
        PORTS               NAMES5012d6f6f0ab        ubuntu:16.04        "/bin/bash"         5 seconds ago       Up 4 seconds
                            elastic_wing
docker inspect 5012d6f6f0ab
[
    {
        "Id": "5012d6f6f0ab1d4ef82760a36ad281f13a6670b6d4fcad158ae7753a94b9fa00",
        "Created": "2019-03-15T06:51:18.188460153Z",
        "Path": "/bin/bash",
        "Args": [],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
......
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02",
                    "DriverOpts": null
                }
            }
        }
    }
]
[root@localhost docker]# docker inspect -f {{.State.Pid}} 5012d6f6f0ab
19787
[root@localhost docker]# nsenter --target 19787 --mount --uts --ipc --net --pid
root@5012d6f6f0ab:/#
~~~

更简单的，下载.bashrc_docker，并将其内容放到.bashrc中。

~~~shell
$ wget -P ~ https://github.com/yeasy/docker_practice/raw/master/
_local/.bashrc_docker;
$ echo "[ -f ~/.bashrc_docker ] && . ~/.bashrc_docker" >> ~/.bas
hrc; source ~/.bashrc
~~~

这个文件中定义了很多Docker命令，例如docker-pid可以获取某个容器的PID；docker-enter可以进入容器或直接在容器内执行命令

~~~shell
$ echo $(docker-pid <container>)
$ docker-enter <container> ls
~~~

### 导入和导出容器

使用 docker export 命令

~~~shell
[root@localhost docker]# docker ps -a
CONTAINER ID        IMAGE                          COMMAND                  CREATED             STATUS                    PORTS               NAMES
5012d6f6f0ab        ubuntu:16.04                   "/bin/bash"              2 days ago   
1d4a4a317115        myip                           "curl -s http://ip.c…"   4 days ago          Exited (6) 4 days ago                         infallible_merkle
76a2e2359207        centos                         "/bin/bash"              4 days ago          Exited (0) 4 days ago                         hardcore_diffie
                        
[root@localhost docker]# docker export 364d38afa29c > myip.tar

[root@localhost docker]# ls
Dockerfile  myip.tar
~~~

### 导入容器快照

使用 docker import 命令

~~~shell
[root@localhost docker]# cat myip.tar | docker import - tset/myip:v1.0.1
[root@localhost docker]# docker images
REPOSITORY              TAG                 IMAGE ID            CREATED        
     SIZEtset/myip               v1.0.1              320228c9dcec        14 seconds ago 
     126MBopenvz/ubuntu           14.04               824857189f82        3 days ago     
     215MB
~~~

此外，也可以通过指定URL或者某个目录来导入

~~~shell
[root@localhost docker]# docker import http://example.com/exampleimage.tgz exam
ple/imagerepo
~~~

**注：可以使用 docker load导入镜像存储文件到本地镜像库，也可以使用 docker import来导入一个容器快照到本地镜像库；两者的区别在于：容器快照会丢弃所有的历史记录和元数据信息，而镜像存储文件将保存完整的记录**

### 清理所有处于终止状态的容器

使用 docker ps -a 查看所有已创建的包括终止的容器，可以使用 docker rm $(docker ps -a -q) 可以全部清理掉



