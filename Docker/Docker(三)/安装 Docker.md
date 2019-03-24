## 安装 Docker

Docker 分为 CE 和 EE 两大版本。CE 即社区版（免费，支持周期 7 个月），EE
即企业版，强调安全，付费使用，支持周期 24 个月。
Docker CE 分为 stable, test, 和 nightly 三个更新频道。每六个月发布一个 stable
版本 (18.09, 19.03, 19.09...)。
官方网站上有各种环境下的 [安装指南](https://docs.docker.com/install/)，这里主要介绍 Docker CE 在 Linux 、
Windows 10 (PC) 和 macOS 上的安装。

## Ubuntu 安装 Docker CE

**警告：切勿在没有配置 Docker APT 源的情况下直接使用 apt 命令安装**

### 准备

**系统要求**

Docker CE 支持 以下版本的 Ubuntu 操作系统

- Bionic 18.04 (LTS)
- Xenial 16.04 (LTS)
- Trusty 14.04 (LTS) (Docker CE v18.06 及以下版本)

Docker CE 可以安装在 64 位的 x86 平台或 ARM 平台上。Ubuntu 发行版中，
LTS（Long-Term-Support）长期支持版本，会获得 5 年的升级维护支持，这样的
版本会更稳定，因此在生产环境中推荐使用 LTS 版本。

### 卸载旧版本
旧版本的 Docker 称为 docker 或者 docker-engine ，使用以下命令卸载旧版本：

~~~shell
卸载 docker
sudo docker -v  
sudo apt-get remove docker docker-engine docker.io
sudo apt-get remove --auto-remove docker  
sudo apt-get remove --purge lxc-docker  
sudo apt-get autoremove --purge  
sudo apt-get install lxc-docker 
sudo docker -v
~~~

#### Ubuntu 14.04 可选内核模块

从 Ubuntu 14.04 开始，一部分内核模块移到了可选内核模块包 ( linux-image-
extra-* ) ，以减少内核软件包的体积。正常安装的系统应该会包含可选内核模块
包，而一些裁剪后的系统可能会将其精简掉。 AUFS 内核驱动属于可选内核模块
的一部分，作为推荐的 Docker 存储层驱动，一般建议安装可选内核模块包以使用
AUFS 。

如果系统没有安装可选内核模块的话，可以执行下面的命令来安装可选内核模块
包：

~~~shell
$ sudo apt-get update
$ sudo apt-get install \
	linux-image-extra-$(uname -r) \
	linux-image-extra-virtual
~~~

#### Ubuntu 16.04 + 

Ubuntu 16.04 + 上的 Docker CE 默认使用 overlay2 存储层驱动,无需手动配置。

Ubuntu 16.04 + 上的 Docker CE 默认使用 overlay2 存储层驱动,无需手动配置。

~~~shell
$ sudo apt-get update
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
	software-properties-common
~~~

鉴于国内网络问题，强烈建议使用国内源，官方源请在注释中查看。
为了确认所下载软件包的合法性，需要添加软件源的 GPG 密钥。

~~~shell
$ curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/
gpg | sudo apt-key add -
# 官方源
# $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
~~~

然后，我们需要向 source.list 中添加 Docker 软件源

~~~shell
$ sudo add-apt-repository \
"deb [arch=amd64] https://mirrors.ustc.edu.cn/dockerce/linux/ubuntu \
$(lsb_release -cs) \
stable"
# 官方源
# $ sudo add-apt-repository \
# "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
# $(lsb_release -cs) \
# stable"
~~~

以上命令会添加稳定版本的 Docker CE APT 镜像源，如果需要测试或每日构建版本的 Docker CE 请将 stable 改为 test 或者 nightly。

#### 安装 Docker CE

更新 apt 软件缓存，并安装 docekr-ce ：

~~~shell
$ sudo apt-get update
$ sudo apt-get install docker-ce
~~~

### 使用脚本自动安装

Docker 为了简化安装流程，提供了一套便捷的安装脚本，Ubuntu 上可以使用这套脚本：

~~~shell
$ curl -fsSL get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh --mirror Aliyun
~~~

#### 启动 Docker CE

~~~shell
$ sudo systemctl enable docker
$ sudo systemctl start docker
~~~

#### Ubuntu 14.04 使用 以下命令启动

~~~shell
$ sudo service docker start
~~~

#### 建立 docker 用户组

默认情况下， docker 命令会使用 Unix socket 与 Docker 引擎通讯。而只有root 用户和 docker 组的用户才可以访问 Docker 引擎的 Unix socket。出于安全考虑，一般 Linux 系统上不会直接使用 root 用户。因此，更好地做法是将需要使用 docker 的用户加入 docker 用户组。

~~~shell
# 建立 docker 组：
$ sudo groupadd docker
# 将当前用户加入 docker 组：
$ sudo usermod -aG docker $USER
~~~

