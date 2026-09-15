树莓派上的 ROS 2
================

ROS 2 同时支持 32 位（arm32）和 64 位（arm64）ARM 处理器。
不过，你可以在 `这里 <https://reps.openrobotics.org/rep-2000/>`__ 看到，arm64 获得 Tier 1 支持，而 arm32 属于 Tier 3。
Tier 1 支持意味着有发行版专用的软件包和二进制归档可用，而 Tier 3 则要求用户从源码编译 ROS 2。

使用 ROS 2 最快、最简单的方式是使用 Tier 1 支持的配置。

这意味着要么在树莓派上安装 64 位 Ubuntu，要么使用 64 位版本的 Raspberry Pi OS 并在 Docker 中运行 ROS 2。

在树莓派上使用 Ubuntu Linux 并安装二进制版 ROS 2
------------------------------------------------

适用于树莓派的 Ubuntu 可在 `这里 <https://ubuntu.com/download/raspberry-pi>`__ 获取。

请务必确认你选择的版本与 `REP-2000 <https://reps.openrobotics.org/rep-2000/>`__ 中描述的一致。

现在你便可以按照 Ubuntu Linux 的常规二进制安装说明来安装 ROS 2。

使用 Raspberry Pi OS 并在 docker 中运行 ROS 2
---------------------------------------------

Raspberry Pi OS 64 位版本可在 `这里获取 <https://www.raspberrypi.com/software/operating-systems/>`__。

Raspberry Pi OS 基于 Debian，属于 Tier 3 支持，但它可以运行 Ubuntu docker 容器以获得 Tier 1 支持。

刷写操作系统之后，`安装 Docker <https://docs.docker.com/engine/install/debian/#install-using-the-convenience-script>`__。

官方 ROS 2 Docker 镜像可在 `这里 <https://hub.docker.com/_/ros/tags>`__ 找到。

你可以从 ros-core、ros-base 或 perception 中选择。
关于这些变体的更多信息，请参见 `这里 <https://reps.openrobotics.org/rep-2001/>`__。

拉取并运行镜像：

.. code-block:: console

    $ docker pull ros:{DISTRO}-ros-core
    $ docker run -it --rm ros:{DISTRO}-ros-core

你也可以自行构建镜像：

将 `docker_images git 仓库 <https://github.com/osrf/docker_images>`__ 克隆到树莓派上，切换到上面链接的目录，然后进入你偏好的变体所在的目录。

在该目录内，使用以下命令构建容器：

.. code-block:: console

    $ docker build -t ros_docker .

在受支持的系统中，构建 docker 容器只需一两分钟，因为源代码已经构建成二进制文件。
