.. redirect-from::

    Tutorials/Configuring-ROS2-Environment

.. _ConfigROS2:

配置环境
========

**目标：** 本教程将向你展示如何准备你的 ROS 2 环境。

**教程级别：** 入门

**用时：** 5 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

ROS 2 依赖通过 shell 环境组合工作空间的概念。
“工作空间”是 ROS 中的一个术语，指你的系统中用于 ROS 2 开发的位置。
在典型的 ROS 2 设置中，核心 ROS 2 安装是底层（underlay）。
在该安装之后 source 的本地工作空间是覆盖层（overlay），因为它被叠加在底层之上。
同一个工作空间也可以作为另一个稍后 source 的工作空间的底层。
使用 ROS 2 进行开发时，你通常会同时激活多个工作空间。

组合工作空间使针对不同版本的 ROS 2 或不同包集合进行开发变得更加容易。
它还允许在同一台计算机上安装多个 ROS 2 发行版（“distros”，例如 Dashing 和 Eloquent），并在它们之间切换。

这可以通过每次打开新 shell 时 source setup 文件来实现，也可以通过将 source 命令一次性添加到你的 shell 启动脚本中来实现。
如果不 source setup 文件，你将无法访问 ROS 2 命令，也无法找到或使用 ROS 2 包。
换句话说，你将无法使用 ROS 2。

前置条件
--------

在开始这些教程之前，请按照 ROS 2 :doc:`../../Installation` 页面上的说明安装 ROS 2。

本教程中使用的命令假定你已按照适用于你操作系统的二进制包安装指南完成安装（Linux 为 deb 包）。
如果你是从源码构建的，仍然可以跟着做，但你的 setup 文件路径可能会有所不同。
此外，如果你从源码安装，将无法使用 ``sudo apt install ros-<distro>-<package>`` 命令（该命令在入门级教程中经常使用）。

如果你使用的是 Linux 或 macOS，但还不熟悉 shell，`这个教程 <https://www.linux.com/training-tutorials/bash-101-working-cli/>`__ 会对你有所帮助。

任务
----

1 source setup 文件
^^^^^^^^^^^^^^^^^^^

你需要在你打开的每一个新 shell 上运行这条命令，才能访问 ROS 2 命令，如下所示：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ source /opt/ros/{DISTRO}/setup.bash


      如果你不使用 bash，请将 ``.bash`` 替换为你的 shell。
      可能的值有：``setup.bash``、``setup.sh``、``setup.zsh``。

   .. group-tab:: macOS

      .. code-block:: console

        $ . ~/ros2_install/ros2-osx/setup.bash

   .. group-tab:: Windows

      .. code-block:: console

        $ call C:\dev\ros2\local_setup.bat

.. note::
    确切的命令取决于你安装 ROS 2 的位置。
    如果你遇到问题，请确保文件路径指向你的安装目录。

2 将 source 添加到你的 shell 启动脚本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果你不想每次打开新 shell 时都 source setup 文件（跳过任务 1），那么你可以将该命令添加到你的 shell 启动脚本中：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ echo "source /opt/ros/{DISTRO}/setup.bash" >> ~/.bashrc

      要撤销此操作，请找到你系统的 shell 启动脚本并删除追加的 source 命令。

   .. group-tab:: macOS

      .. code-block:: console

        $ echo "source ~/ros2_install/ros2-osx/setup.bash" >> ~/.bash_profile

      要撤销此操作，请找到你系统的 shell 启动脚本并删除追加的 source 命令。

   .. group-tab:: Windows

      仅限 PowerShell 用户，在“我的文档”中创建一个名为“WindowsPowerShell”的文件夹。
      在“WindowsPowerShell”内，创建文件“Microsoft.PowerShell_profile.ps1”。
      在该文件内，粘贴：

      .. code-block:: console

        $ C:\dev\ros2_{DISTRO}\local_setup.ps1

      每次打开新 shell 时，PowerShell 都会请求运行此脚本的权限。
      为避免该问题，你可以运行：

      .. code-block:: console

        $ Unblock-File C:\dev\ros2_{DISTRO}\local_setup.ps1

      要撤销此操作，请删除新的“Microsoft.PowerShell_profile.ps1”文件。

3 检查环境变量
^^^^^^^^^^^^^^

source ROS 2 setup 文件会设置运行 ROS 2 所需的若干环境变量。
如果你在查找或使用 ROS 2 包时遇到问题，请使用以下命令确认你的环境已正确设置：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ printenv | grep -i ROS

   .. group-tab:: macOS

      .. code-block:: console

        $ printenv | grep -i ROS

   .. group-tab:: Windows

      .. code-block:: console

        $ set | findstr -i ROS

检查 ``ROS_DISTRO`` 和 ``ROS_VERSION`` 等变量是否已设置。

::

  ROS_VERSION=2
  ROS_PYTHON_VERSION=3
  ROS_DISTRO={DISTRO}

如果环境变量设置不正确，请返回到你所遵循安装指南中 ROS 2 包安装的部分。
如果你需要更具体的帮助（因为环境 setup 文件可能来自不同位置），你可以 `获取答案 <https://robotics.stackexchange.com/>`__ 来向社区求助。

3.1 ``ROS_DOMAIN_ID`` 变量
~~~~~~~~~~~~~~~~~~~~~~~~~~

有关 ROS 域 ID 的详细信息，请参阅 `域 ID <../../Concepts/Intermediate/About-Domain-ID>` 文章。

一旦你为一组 ROS 2 节点确定了一个唯一的整数，就可以使用以下命令设置环境变量：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ export ROS_DOMAIN_ID=<your_domain_id>

      要在 shell 会话之间保持此设置，你可以将该命令添加到你的 shell 启动脚本中：

      .. code-block:: console

        $ echo "export ROS_DOMAIN_ID=<your_domain_id>" >> ~/.bashrc

   .. group-tab:: macOS

      .. code-block:: console

        $ export ROS_DOMAIN_ID=<your_domain_id>

      要在 shell 会话之间保持此设置，你可以将该命令添加到你的 shell 启动脚本中：

      .. code-block:: console

        $ echo "export ROS_DOMAIN_ID=<your_domain_id>" >> ~/.bash_profile

   .. group-tab:: Windows

      .. code-block:: console

        $ set ROS_DOMAIN_ID=<your_domain_id>

      如果你想在 shell 会话之间永久保持此设置，还可以运行：

      .. code-block:: console

        $ setx ROS_DOMAIN_ID <your_domain_id>

3.2 ``ROS_AUTOMATIC_DISCOVERY_RANGE`` 变量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

默认情况下，ROS 2 通信不限于 localhost。
``ROS_AUTOMATIC_DISCOVERY_RANGE`` 环境变量允许你限制 ROS 2 的发现范围。
使用 ``ROS_AUTOMATIC_DISCOVERY_RANGE`` 在某些场景下很有帮助，例如在教室里，多台机器人可能发布到同一个话题，从而导致奇怪的行为。
有关更多详细信息，请参阅 :ref:`改进的动态发现 <ImprovedDynamicDiscovery>`。

小结
----

ROS 2 开发环境在使用前需要正确配置。
这可以通过两种方式完成：要么在你打开的每个新 shell 中 source setup 文件，要么将 source 命令添加到你的启动脚本中。

如果你在使用 ROS 2 查找或使用包时遇到任何问题，你首先要做的就是检查你的环境变量，并确保它们被设置为符合你预期的版本和发行版。

下一步
------

既然你已经有了一个可用的 ROS 2 安装，并且知道如何 source 它的 setup 文件，你就可以开始通过 :doc:`turtlesim 工具 <./Introducing-Turtlesim/Introducing-Turtlesim>` 学习 ROS 2 的方方面面了。
