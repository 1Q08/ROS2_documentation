.. redirect-from::

   Installation/Prerelease-Testing

使用预发布二进制包进行测试
==========================

许多 ROS 软件包以预构建二进制包的形式提供。
通常，按照 :doc:`../Installation` 操作会获得已发布的二进制包版本。
此外还有一些预发布版本的二进制包，可用于在正式发布前进行测试。
如果你想试用 ROS 二进制包的预发布版本，本文介绍了几种可选方案。

当软件包被发布到某个 ROS 发行版时（使用 bloom），构建农场（buildfarm）会将它们构建成 deb 软件包，并临时存放在 **building** apt 仓库中。
随着依赖包被重新构建，一个自动过程会定期将 **building** 中的软件包同步到名为 **ros-testing** 的二级仓库。
**ros-testing** 被设计为一个浸泡（soaking）区域，开发者和前沿用户可以在此对软件包进行额外测试，之后它们会被手动同步到用户通常安装软件包的公共 ros 仓库中。

大约每两周，rosdistro 的发布管理者会手动将 **ros-testing** 的内容同步到 **main** ROS 仓库。

deb 测试仓库
------------

对于基于 Debian 的操作系统，你可以从 **ros-testing** 仓库安装二进制软件包。

1. 确保你已有一套可正常工作的、通过 deb 软件包安装的 ROS 2（见 :doc:`../Installation`）。

2. 安装 ros2-testing-apt-source 软件包。
   这会自动卸载 ros2-apt-source 软件包，因为同一时间只能启用一个仓库。

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

6. 完成测试后，你可以通过重新安装 ros-apt-source 软件包来切回普通仓库：

   .. code-block:: console

      $ sudo apt install -y ros2-apt-source

   并执行 update 和 upgrade：

   .. code-block:: console

      $ sudo apt update
      $ sudo apt dist-upgrade


RHEL 测试仓库
-------------

对于 RHEL，你可以通过在源配置中启用测试仓库，从 **ros-testing** 仓库安装二进制软件包：

1. 确保你已有一套可正常工作的、通过 rpm 软件包安装的 ROS 2（见 :doc:`RHEL 安装说明 <RHEL-Install-RPMs>`）。

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

5.  完成测试后，你可以通过重新启用主仓库来切回普通仓库：

   .. code-block:: console

      $ sudo dnf config-manager --set-disabled ros2-testing
      $ sudo dnf config-manager --set-enabled ros2

   并执行 update 和 upgrade：

   .. code-block:: console

      $ sudo dnf update
      $ sudo dnf system-upgrade

.. _Prerelease_binaries:

二进制归档
----------

对于核心软件包，我们会为 Ubuntu Linux、RHEL 和 Windows 运行每夜打包任务。
这些打包任务会生成包含预构建二进制包的归档文件，你可以将它们下载并解压到你的文件系统中。

1. 确保你已按照适用于你平台的 :doc:`最新开发版安装说明 <Alternatives/Latest-Development-Setup>` 安装了所有依赖项。

2. 访问 https://ci.ros2.org/view/packaging/ ，并从列表中选取与你平台对应的打包任务。

3. 在 "Last Successful Artifacts" 标题下，你应该能看到一个下载链接（例如 Windows 的 ``ros2-package-windows-AMD64.zip``）。

4. 下载归档文件并解压到你的文件系统中。

5. 要使用二进制归档安装，请加载归档根目录下的 ``setup.*`` 文件。

   .. tabs::

     .. group-tab:: Ubuntu Linux 与 RHEL

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

关于在 Docker 中运行 GUI 应用的支持，请参阅教程 `User GUI's with Docker <https://wiki.ros.org/docker/Tutorials/GUI>`_ 或工具 `rocker <https://github.com/osrf/rocker>`_。
