在 Raspberry Pi 上安装 ROS 2
============================

ROS 2 同时支持 32 位 (arm32) 和 64 位 (arm64) ARM 处理器。
但是，你可以 `在这里 <https://reps.openrobotics.org/rep-2000/>`__ 看到，arm64 获得 Tier 1 支持，而 arm32 是 Tier 3。
Tier 1 支持意味着提供特定发行版的包和二进制归档文件，而 Tier 3 需要用户从源代码编译 ROS 2。

使用 ROS 2 最快、最简单的方法是使用 Tier 1 支持的配置。

这意味着要么在 Raspberry Pi 上安装 64 位 Ubuntu，要么使用 64 位版本的 Raspberry Pi OS 并在 Docker 中运行 ROS 2。

在 Raspberry Pi 上安装 Ubuntu Linux 并进行 ROS 2 二进制安装
-----------------------------------------------------------

适用于 Raspberry Pi 的 Ubuntu 可以 `在这里 <https://ubuntu.com/download/raspberry-pi>`__ 获取。

请务必按照 `REP-2000 <https://reps.openrobotics.org/rep-2000/>`__ 中的说明确认你选择了正确的版本。

适用于 Raspberry Pi 的 Ubuntu 默认不包含 *backports* 和 *updates* 软件套件，而这些是 ROS 2 二进制安装正常工作的必要条件。

因此，在安装 ROS 2 之前，请检查并编辑 Raspberry Pi 上的 ``/etc/apt/sources.list.d/ubuntu.sources`` 文件。

例如，Ubuntu 24.04 "Noble Numbat" 版本应该有一个如下所示的条目：

.. code-block:: console

    Types: deb
    URIs: http://ports.ubuntu.com/ubuntu-ports/
    Suites: noble noble-updates noble-backports       # <-- IMPORTANT LINE
    Components: main universe restricted multiverse
    Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

现在你可以使用 Ubuntu Linux 的常规二进制安装说明来安装 ROS 2。

使用 Raspberry Pi OS 并在 Docker 中运行 ROS 2
---------------------------------------------

Raspberry Pi OS 64 位版本 `可在此获取 <https://www.raspberrypi.com/software/operating-systems/>`__。

Raspberry Pi OS 基于 Debian，获得 Tier 3 支持，但它可以运行 Ubuntu Docker 容器以获得 Tier 1 支持。

刷写操作系统后，`安装 Docker <https://docs.docker.com/engine/install/debian/#install-using-the-convenience-script>`__。

官方 ROS 2 Docker 镜像可以 `在这里 <https://hub.docker.com/_/ros/tags>`__ 找到。

你可以从 ros-core、ros-base 或 perception 中选择。
有关这些变体的更多信息，请参见 `这里 <https://reps.openrobotics.org/rep-2001/>`__。

拉取并运行一个镜像：

.. code-block:: console

    $ docker pull ros:{DISTRO}-ros-core
    $ docker run -it --rm ros:{DISTRO}-ros-core

你也可以自己构建镜像：

将 `docker_images git 仓库 <https://github.com/osrf/docker_images>`__ 克隆到 Raspberry Pi 上，进入上面链接的目录，然后进入你首选变体的目录。

在该目录中，使用以下命令构建容器：

.. code-block:: console

    $ docker build -t ros_docker .

在受支持的系统上，构建 Docker 容器只需要一两分钟，因为源代码已经被构建为二进制文件。
