.. redirect-from::

  Beta2-Overview

Beta 2 (``r2b2``)
=================

.. contents:: 目录
   :depth: 2
   :local:

支持的平台
----------

我们在三个平台上支持 ROS 2 Beta 2：Ubuntu 16.04 (Xenial)、macOS 10.12 (Sierra) 和 Windows 10。
我们为全部 3 个平台提供了二进制软件包以及从源代码编译的说明（参见 `安装说明 <../../Installation>` 以及 `文档 <https://docs.ros2.org/beta2/>`__）。

功能
----

自 Beta 1 版本以来的改进
^^^^^^^^^^^^^^^^^^^^^^^^^^

* DDS_Security 支持（又称 SROS2，参见 `sros2 <https://github.com/ros2/sros2>`__）
* Ubuntu Xenial 的 Debian 软件包
* 类型支持已重新设计，因此你只需构建单个可执行文件，就可以通过设置环境变量选择可用的 RMW 实现之一（参见 `文档 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`）。
* 节点和话题的命名空间支持（参见 `设计文章 <https://design.ros2.org/articles/topic_and_service_names.html>`__，另见下方已知问题）。
* 一组使用可扩展 ``ros2`` 命令的命令行工具（参见 `概念文章 <../../Concepts/Basic/About-Command-Line-Tools>`）。
* 一组用于在 C / C++ 中记录日志消息的宏（参见 `rcutils <https://docs.ros2.org/beta2/api/rcutils/index.html>`__ 的 API 文档）。

新演示应用
^^^^^^^^^^

* `Turtlebot 2 演示 <https://github.com/ros2/turtlebot2_demo>`__，使用以下已（部分）转换到 ROS 2 的仓库（仅限 Linux）：

  * `ros_astra_camera <https://github.com/ros2/ros_astra_camera.git>`__
  * `depthimage_to_laserscan <https://github.com/ros2/depthimage_to_laserscan.git>`__
  * `pcl_conversions <https://github.com/ros2/pcl_conversions.git>`__
  * `cartographer <https://github.com/ros2/cartographer.git>`__
  * `cartographer_ros <https://github.com/ros2/cartographer_ros.git>`__
  * `ceres-solver <https://github.com/ros2/ceres-solver.git>`__
  * `navigation <https://github.com/ros2/navigation.git>`__
  * `teleop_twist_keyboard <https://github.com/ros2/teleop_twist_keyboard.git>`__
  * `joystick_drivers <https://github.com/ros2/joystick_drivers.git>`__
  * `teleop_twist_joy <https://github.com/ros2/teleop_twist_joy.git>`__

* `Dummy_robot 演示 <../Tutorials/Demos/dummy-robot-demo>`：

  * `robot_model <https://github.com/ros2/robot_model>`__
  * `robot_state_publisher <https://github.com/ros2/robot_state_publisher>`__

以往 Alpha/Beta 版本的部分功能
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

完整列表请参见 `早期版本说明 <../index>`。


* ROS 2 客户端库的 C++ 和 Python 实现，包括以下 API：

  * 发布和订阅 ROS 话题
  * 请求和应答 ROS 服务（同步（仅 C++）和异步）
  * 获取和设置 ROS 参数（仅 C++，同步和异步）
  * 定时器回调

* 支持多个 DDS/RTPS 实现之间的互操作性

  * eProsima Fast RTPS 是我们的默认实现，包含在二进制软件包中
  * 支持 RTI Connext：从源代码构建以试用
  * 我们最初支持 PrismTech OpenSplice，但目前对其的支持处于搁置状态

* 网络事件的图 API
* 分布式发现
* 使用兼容 DDS 实现（目前仅 Connext）进行发布和订阅的实时安全代码路径

  * 支持自定义分配器

* ROS 1 <-> ROS 2 动态桥接节点
* 执行器线程模型（仅 C++）
* 在编译 / 链接 / 运行时组合节点的组件模型
* 使用标准生命周期的托管组件
* 扩展的 ``.msg`` 格式，包含新功能：

  * 有界数组
  * 默认值

已知问题
^^^^^^^^

* 我们在各个仓库中跟踪问题，但主要入口是 `ros2/ros2 问题跟踪器 <https://github.com/ros2/ros2/issues>`__
* 我们想强调一个我们正在调查的 `已知问题 <https://github.com/ros2/rmw_connext/issues/234>`__：使用 ``rmw_connext_cpp`` 时，不允许两个具有相同基础名称但不同命名空间的话题具有不同类型。
* 响应较长的服务在 Fast-RTPS 下无法正常工作。该修复虽然不属于 beta2 的一部分，但已在上游可用，因此你可以通过使用 Fast-RTPS master 分支从源代码构建来规避此问题。
