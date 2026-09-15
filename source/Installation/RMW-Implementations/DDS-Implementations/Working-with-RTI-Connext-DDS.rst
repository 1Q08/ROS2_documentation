RTI Connext DDS
===============

RTI Connext DDS 在全球 2000 多个要求最为严苛的系统设计中广受信赖，能够以最高水平的性能、可靠性和安全性来分发关键的实时数据。
它对于原型开发、研究、非商业用途和学术用途是免费的。
请访问 `RTI 官网 <https://www.rti.com/ros>`__ 了解更多信息，并了解支持与商业许可的相关选项。


前置条件
--------

安装 RTI Connext DDS
^^^^^^^^^^^^^^^^^^^^
  要构建和使用 ``rmw_connextdds``，需要一个与所用 ROS 2 发行版兼容的 Connext DDS 版本。
  使用 apt 安装 ``rmw_connextdds`` 时会同时包含 Connext DDS，或者也可以手动安装以便从源码构建。
  下表详细列出了使用 ``apt`` 安装的 Connext DDS 版本，以及从源码构建所需的版本：

  ==================  ===================  ====================
  ROS 2 发行版         apt 安装版本          从源码构建所需版本
  ==================  ===================  ====================
  rolling             n/a                  ``7.7.0``
  lyrical             ``7.7.0``            ``7.7.0``
  kilted              ``7.3.0``            ``7.3.0``
  jazzy               ``6.0.1``            ``6.0.1``
  humble              ``6.0.1``            ``6.0.1``
  ==================  ===================  ====================

RTI Connext Pro 可通过多种渠道获取：

**ROS 2 apt 仓库**
  ROS 2 用户可以使用以下命令，从 ROS apt 仓库为 x86_64 Linux 安装非商业用途版本的 RTI Connext DDS 库：

  .. tabs::

     .. group-tab:: v7.3.0

        .. code-block:: console

           $ sudo apt update && sudo apt install -q -y rti-connext-dds-7.3.0-ros

     .. group-tab:: v6.0.1

        .. code-block:: console

           $ sudo apt update && sudo apt install -q -y rti-connext-dds-6.0.1

  此软件包仅包含 RTI Connext 核心 DDS 库；不包含完整的 Connext Professional 工具套件和运行时服务。
  请注意，使用 apt 安装 ``rmw_connextdds`` 时会自动安装这些 Connext 库。

**其他安装选项**
`Connext Robotics Toolkit <https://www.rti.com/developers/connext-robotics-toolkit>`__ 包含完整的 Connext 工具套件和基础设施服务。
它提供了使用 apt 一步安装 ROS 和 Connext 的方式。
它对于原型开发、研究、非商业用途和学术用途是免费的。

有关为各种平台构建和调优 RMW 及 ROS 2 应用，以及启用 DDS 安全特性的详细说明，请参见 `RTI ROS 社区 <https://community.rti.com/ros>`__ 页面。


安装 rmw_connextdds 二进制软件包
--------------------------------

要从 ROS 2 apt 仓库安装 ``rmw_connextdds`` 及 Connext 库的二进制软件包，请使用以下命令：

.. code-block:: console

   $ sudo apt update && sudo apt install -q -y ros-{DISTRO}-rmw-connextdds


从源码构建 rmw_connextdds
-------------------------

从源码构建可以确保 RMW 与你的系统相匹配并正确安装。
以下说明假定构建主机与目标均为 Linux x86_64；`RTI ROS 社区 <https://community.rti.com/ros>`__
页面提供了为其他平台和目标（包括 Arm、Windows 和 macOS）构建的说明。

将 ``rmw_connextdds`` 的仓库克隆到你的 ROS 2 工作空间，并选择与所用 ROS 2 发行版相匹配的分支：

.. code-block:: console

   $ mkdir -p ros2_ws/src
   $ cd ros2_ws
   $ git clone -b {DISTRO} https://github.com/ros2/rmw_connextdds src/rmw_connextdds

设置环境以帮助 colcon 发现 RTI Connext 的安装位置。
可以通过手动将环境变量 ``NDDSHOME`` 设置为 RTI Connext 安装位置来完成，或者使用 RTI Connext 安装自带的脚本：

.. code-block:: console

   $ source ${RTI_CONNEXT_INSTALL_LOCATION}/resource/scripts/rtisetenv_x64Linux4gcc7.3.0.bash

确保已设置好 ROS 2 环境：

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash

使用 colcon 构建 RMW：

.. code-block:: console

   $ colcon build --symlink-install

构建成功完成后，请务必加载工作空间的 setup 文件：

.. code-block:: console

   $ source install/setup.bash


使用构建生成的 rmw_connextdds
-----------------------------

设置环境变量 ``RMW_IMPLEMENTATION`` 以告诉 ROS 2 使用哪个 RMW：

.. code-block:: console

   $ export RMW_IMPLEMENTATION=rmw_connextdds

另请参见：:doc:`使用多个 RMW 实现 <../../../How-To-Guides/Working-with-multiple-RMW-implementations>`

运行 talker 和 listener
-----------------------

现在运行 ``talker`` 和 ``listener`` 来测试 RTI Connext DDS

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp talker

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp listener
