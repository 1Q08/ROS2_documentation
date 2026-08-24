.. redirect-from::

   Installation/Prerelease-Testing

使用预发布二进制包进行测试
==========================

许多 ROS 软件包以预构建的二进制包形式提供。
通常，按照 :doc:`../Installation` 操作时，你会获得二进制包的正式发布版本。
此外，还有预发布版本的二进制包，它们在正式发布之前进行测试时非常有用。
如果你想试用预发布版本的 ROS 二进制包，本文介绍了几种选择。

当软件包被发布到 ROS 发行版（使用 bloom）时，buildfarm 会将其构建为 deb 软件包，并临时存储在 **building** apt 软件仓库中。
随着依赖软件包被重新构建，一个自动化流程会定期将 **building** 中的软件包同步到名为 **ros-testing** 的二级仓库中。
**ros-testing** 旨在作为一个浸泡区，让开发者和前沿用户可以在软件包被手动同步到用户通常安装软件包所用的公共 ros 仓库之前，对软件包进行额外的测试。

大约每两周，rosdistro 的发布经理会将 **ros-testing** 的内容手动同步到 **main** ROS 仓库中。

deb 测试软件仓库
----------------

对于基于 Debian 的操作系统，你可以从 **ros-testing** 仓库安装二进制软件包。

1. 确保你已经从 deb 软件包安装了可正常工作的 ROS 2（参见 :doc:`../Installation`）。

2. 安装 ros2-testing-apt-source 软件包。
   这将自动卸载 ros2-apt-source 软件包，因为一次只能启用一个软件仓库。

   .. code-block:: console

      $ sudo apt install -y ros2-testing-apt-source

3. 更新 apt 索引：

   .. code-block:: console

      $ sudo apt update

4. 现在你可以从测试仓库安装单个软件包，例如：

   .. code-block:: console

      $ sudo apt install ros-{DISTRO}-my-just-released-package

5. 或者，你可以将整个 ROS 2 安装切换到测试仓库：

   .. code-block:: console

      $ sudo apt dist-upgrade

6. 测试完成后，你可以通过重新安装 ros-apt-source 软件包切回普通仓库：

   .. code-block:: console

      $ sudo apt install -y ros2-apt-source

   然后执行更新和升级：

   .. code-block:: console

      $ sudo apt update
      $ sudo apt dist-upgrade


RHEL 测试软件仓库
-----------------

对于 RHEL，你可以通过在源配置上启用测试仓库，从 **ros-testing** 仓库安装二进制软件包：

1. 确保你已经安装了可正常工作的 RPM 软件包版 ROS 2（参见 :doc:`RHEL 安装说明 <RHEL-Install-RPMs>`）。

2. 启用测试仓库并禁用主仓库：

   .. code-block:: console

      $ sudo dnf config-manager --set-enabled ros2-testing
      $ sudo dnf config-manager --set-disabled ros2

3. 更新 dnf 索引：

   .. code-block:: console

      $ sudo dnf update

4.  现在你可以从测试仓库安装单个软件包，例如：

   .. code-block:: console

      $ sudo dnf install ros-{DISTRO}-my-just-released-package

5.  测试完成后，你可以通过重新启用主仓库切回普通仓库：

   .. code-block:: console

      $ sudo dnf config-manager --set-disabled ros2-testing
      $ sudo dnf config-manager --set-enabled ros2

   然后执行更新和升级：

   .. code-block:: console

      $ sudo dnf update
      $ sudo dnf system-upgrade

.. _Prerelease_binaries:

二进制归档
----------

对于核心软件包，我们会为 Ubuntu Linux、RHEL 和 Windows 运行每夜打包任务。
这些打包任务会生成包含预构建二进制文件的归档，可以下载并解压到你的文件系统中。

1. 根据适用于你平台的 :doc:`最新开发设置 <Alternatives/Latest-Development-Setup>`，确保你已安装所有依赖项。

2. 访问 https://ci.ros2.org/view/packaging/，从列表中选择与你平台对应的打包任务。

3. 在 "Last Successful Artifacts" 标题下，你应该会看到一个下载链接（例如对于 Windows，是 ``ros2-package-windows-AMD64.zip``）。

4. 下载归档并将其解压到你的文件系统。

5. 要使用二进制归档安装，请 source 归档根目录中的 ``setup.*`` 文件。

   .. tabs::

     .. group-tab:: Ubuntu Linux and RHEL

       .. code-block:: console

          $ source path/to/extracted/archive/setup.bash

     .. group-tab:: Windows

       .. code-block:: console

          $ call path\to\extracted\archive\setup.bat

Docker
------

对于 Ubuntu Linux，还有一个基于每夜二进制归档的每夜 Docker 镜像。

1. 拉取 Docker 镜像：

   .. code-block:: console

      $ docker pull osrf/ros2:nightly

2. 启动一个交互式容器：

   .. code-block:: console

      $ docker run -it osrf/ros2:nightly

有关在 Docker 中运行 GUI 应用程序的支持，请参阅教程 `使用 Docker 运行用户 GUI <https://wiki.ros.org/docker/Tutorials/GUI>`_ 或工具 `rocker <https://github.com/osrf/rocker>`_。
