# 安装Docker

## Ubuntu

~~~shell
$ usname -a
Linux master-virtual-machine 4.15.0-20-generic #21-Ubuntu SMP Tue Apr 24 06:16:15 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
~~~

**升级内核**

~~~shell
sudo apt-get install -y --install-recommends linux-generic-lts-trusty
~~~

**使用脚本自动安装**

~~~shell
curl -sSL https://get.docker.com/ | sh
~~~

**阿里云安装脚本**

~~~shell
curl -sSL https://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
~~~

**DaoCloud的安装脚本**

~~~shell
curl -sSL https://get.daocloud.io/docker | sh
~~~

## 手动安装

安装所需的软件包

如果系统没有安装可选内核模块的话，可以执行下面的命令来安装可选内核模块包：

~~~shell
$ sudo apt-get install linx-image-extra-$(uname -r) linux-image-extra-virtual
~~~

图形界面

~~~shell
$ sudo apt-get install xserver-xorg-lts-trusty libgl1-mesa-glx-lts-trusty
~~~

添加APT镜像源

~~~shell
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates
~~~

安装Docker

~~~shell
$ sudo apt-get install docker-engine
~~~

## 启动Docker引擎

~~~shell
$ sudo service docker start
~~~

Ubuntu16.04 、Debian8 Jessie/Stretch

~~~shell
$ sudo systemctl enable docker
$ sudo systemctl start docker
~~~

建立Docker用户表

~~~shell
$ sudo groupadd docker
$sudo usermod -aG docekr $USER
~~~

## CentOS安装Docker

脚本自动安装

~~~shell
curl -sSL https://get.docker.com/ | sh
~~~

与Ubuntu一致

手动安装

添加内核参数

默认配置下，在CentOS使用Docker可能会碰到下面的这些警告信息：

~~~shell
WARNING: bridge-nf-call-iptables is disabled
WARNING: bridge-nf-call-ip6tables is disabled
~~~

添加内核配置参数以启用这些功能

~~~shell
$ sudo tee -a /etc/sysctl.conf <<-EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.brideg.bridge-nf-call-iptables = 1
EOF
~~~

然后重新加载sysctl.conf即可

~~~shell
$ sudo sysctl -p
~~~

添加 yum源

~~~shell
$ sudo tee /ect/yum.repos.d/docker.repo <<- 'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
~~~

安装Docker 与Ubuntu安装过程一致，建立docker用户组与Ubuntu一致



## 镜像加速器

国内访问Docker Hub有时会遇到困难，因此可以配置镜像加速器

- 阿里云加速器
- DaoCloud加速器
- 灵雀云加速器

注册用户并且申请加速器，会获得如**https://jxus37ad.mirror.aliyuncs.com**这样的地址，将其配置给Docker引擎

~~~shell
DOCKER_OPTS=
"--registry=mirror=https://jxus37ad.mirror.aliyuncs.com"
~~~

重新启动服务

~~~shell
$ sudo service docker restart
~~~

检查加速器是否生效

~~~shell
$ sudo ps -ef | grep dockerd
root       1147      1  0 15:13 ?        00:00:01 /usr/bin/dockerd -H fd:// --containerd=/
run/containerd/containerd.sockmaster     2139   1854  0 15:16 pts/0    00:00:00 grep --color=auto dockerd
~~~































