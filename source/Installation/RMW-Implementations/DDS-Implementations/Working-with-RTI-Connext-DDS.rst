RTI Connext DDS
=================

RTI Connext DDS 在全球 2000 多个要求最严苛的系统设计中备受信赖，以最高水平的性能、可靠性和安全性分发关键的实时数据。
它可免费用于原型开发、研究、非商业和学术用途。
访问 `RTI 网站 <https://www.rti.com/ros>`__ 以获取更多信息，并了解支持和商业许可证的相关选项。


先决条件
--------

安装 RTI Connext DDS
^^^^^^^^^^^^^^^^^^^^
  要构建和使用 ``rmw_connextdds``，需要与正在使用的 ROS 2 发行版兼容的 Connext DDS 版本。
  使用 apt 安装 ``rmw_connextdds`` 时会包含 Connext DDS，也可以手动安装以从源代码构建。
  下表详细列出了使用 ``apt`` 安装的 Connext DDS 版本，以及从源代码构建所需的版本：

  ==================  ===================  ====================
  ROS 2 发行版         使用 apt 安装        从源代码构建
  ==================  ===================  ====================
  rolling             n/a                  ``7.7.0``
  lyrical             ``7.7.0``            ``7.7.0``
  kilted              ``7.3.0``            ``7.3.0``
  jazzy               ``6.0.1``            ``6.0.1``
  humble              ``6.0.1``            ``6.0.1``
  ==================  ===================  ====================

RTI Connext Pro 可通过多种渠道获得：

**ROS 2 apt 软件仓库**
  ROS 2 用户可以使用以下命令，从 ROS apt 软件仓库安装适用于 x86_64 Linux 的 RTI Connext DDS 库的非商业用途版本：

  .. tabs::

     .. group-tab:: v7.3.0

        .. code-block:: console

           $ sudo apt update && sudo apt install -q -y rti-connext-dds-7.3.0-ros

     .. group-tab:: v6.0.1

        .. code-block:: console

           $ sudo apt update && sudo apt install -q -y rti-connext-dds-6.0.1

  该软件包仅包含 RTI Connext 核心 DDS 库；不包含完整的 Connext Professional 工具套件和运行时服务。
  请注意，使用 apt 安装 ``rmw_connextdds`` 时会自动安装这些 Connext 库。

**其他安装选项**
`Connext Robotics Toolkit <https://www.rti.com/developers/connext-robotics-toolkit>`__ 包含完整的 Connext 工具套件和基础设施服务。
它使用 apt 提供 ROS 和 Connext 的一步式安装。
它可免费用于原型开发、研究、非商业和学术用途。

有关在各种平台上构建和调优 RMW 及 ROS 2 应用程序，以及启用 DDS 安全性的详细说明，请参见 `RTI ROS Community <https://community.rti.com/ros>`__ 页面。


安装 rmw_connextdds 二进制软件包
--------------------------------

要从 ROS 2 apt 软件仓库安装 ``rmw_connextdds`` 和 Connext 库的二进制软件包，请使用以下命令：

.. code-block:: console

   $ sudo apt update && sudo apt install -q -y ros-{DISTRO}-rmw-connextdds


从源代码构建 rmw_connextdds
---------------------------

从源代码构建可以确保 RMW 与你的系统匹配并正确安装。
以下说明假设构建主机和目标平台为 Linux x86_64；`RTI ROS Community <https://community.rti.com/ros>`__ 页面提供了针对其他平台和目标（包括 Arm、Windows 和 macOS）的构建说明。

将 ``rmw_connextdds`` 的仓库克隆到你的 ROS 2 工作空间中，并选择与正在使用的 ROS 2 发行版匹配的分支：

.. code-block:: console

   $ mkdir -p ros2_ws/src
   $ cd ros2_ws
   $ git clone -b {DISTRO} https://github.com/ros2/rmw_connextdds src/rmw_connextdds

设置环境以帮助 colcon 发现 RTI Connext 的安装位置。
这可以通过手动将环境变量 ``NDDSHOME`` 设置为 RTI Connext 的安装位置来实现，或者使用 RTI Connext 安装自带的脚本：

.. code-block:: console

   $ source ${RTI_CONNEXT_INSTALL_LOCATION}/resource/scripts/rtisetenv_x64Linux4gcc7.3.0.bash

确保你已经设置好 ROS 2 环境：

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash

使用 colcon 构建 RMW：

.. code-block:: console

   $ colcon build --symlink-install

构建成功完成后，务必 source 工作空间的设置文件：

.. code-block:: console

   $ source install/setup.bash


使用生成的 rmw_connextdds
-------------------------

设置环境变量 ``RMW_IMPLEMENTATION`` 以告诉 ROS 2 使用哪个 RMW：

.. code-block:: console

   $ export RMW_IMPLEMENTATION=rmw_connextdds

另请参见：:doc:`使用多种 RMW 实现 <../../../How-To-Guides/Working-with-multiple-RMW-implementations>`

运行 talker 和 listener
-----------------------

现在运行 ``talker`` 和 ``listener`` 来测试 RTI Connext DDS

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp talker

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp listener
