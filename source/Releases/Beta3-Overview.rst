.. redirect-from::

  Beta3-Overview

Beta 3（``r2b3``）
==================

.. contents:: 目录
   :depth: 2
   :local:

支持的平台
----------

我们在三个平台上支持 ROS 2 Beta 3：Ubuntu 16.04（Xenial）、macOS 10.12（Sierra）和 Windows 10。
对于全部 3 个平台，我们既提供二进制软件包，也提供从源代码编译的说明（参见 `安装说明 <../../Installation>` 以及 `文档 <https://docs.ros2.org/beta3/>`__）。

功能
----

自 Beta 2 发布以来的改进
^^^^^^^^^^^^^^^^^^^^^^^^

* Python 中的执行模型，以及 Python C 扩展中内存管理的诸多修复
* `ros_control <https://github.com/ros2/ros2_control>`__ 的实验性重写
* 向用户暴露特定于 DDS 实现的符号（针对 Fast RTPS 和 Connext）（参见 `示例 <https://github.com/ros2/demos/blob/6363be2efe2fea799d92bc22a66e776b2ca9c5d0/demo_nodes_cpp_native/src/talker.cpp>`__）
* Python 中的日志 `API <https://github.com/ros2/rclpy/blob/1ef2924ef8e154c0553edf0fdba4840b08b728f8/rclpy/rclpy/logging.py>`__
* 修复了各个软件包中的若干内存泄漏和竞态条件
* 重新加入了由 PrismTech 提供的 OpenSplice 支持（目前支持 Linux 和 Windows）
* 使用 bloom（无需打补丁）来制作 ROS 2 发行版

新的演示应用
^^^^^^^^^^^^

* `HSR 演示 <https://github.com/ruffsl/hsr_demo>`__

  * 使用 ROS 2 手柄控制器远程操控 HSR 机器人
  * 在 HSR 上的 Docker 容器中运行 ``ros1_bridge`` （因为该机器人运行的是 Ubuntu Trusty 上的 ROS 1）
  * 运行 ROS 2 开发版的 `rviz <https://github.com/ros2/rviz>`__ 以可视化来自机器人的传感器数据等（参见 `视频 <https://vimeo.com/237016358>`__）

先前 Alpha/Beta 发行版中的部分功能
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

完整列表请参见 `早期发行说明 <../index>`。

* ROS 2 客户端库的 C++ 和 Python 实现，包括以下 API：

  * 发布和订阅 ROS 话题
  * 请求和回复 ROS 服务（同步（仅 C++）和异步）
  * 获取和设置 ROS 参数（仅 C++，同步和异步）
  * 定时器回调

* 支持多种 DDS/RTPS 实现之间的互操作性

  * eProsima Fast RTPS 是我们的默认实现，并包含在二进制软件包中
  * 支持 RTI Connext：从源代码构建即可试用
  * PrismTech OpenSplice：参见下文的限制

* 用于网络事件的计算图 API
* 分布式发现
* 在兼容的 DDS 实现（目前仅 Connext）下，发布和订阅的实时安全代码路径

  * 支持自定义分配器

* ROS 1 <-> ROS 2 动态桥接节点
* 执行器线程模型（C++ 和 Python）
* 组件模型，可在编译 / 链接 / 运行时组合节点
* 使用标准生命周期的受管组件
* 扩展的 ``.msg`` 格式，新增以下功能：

  * 有界数组
  * 默认值

已知问题
--------

* 在 Windows 上，使用 ``Ctrl-C`` 尝试中止时，Python 启动文件可能会挂起（参见 `issue <https://github.com/ros2/launch/issues/64>`__）。为了继续使用被挂起命令阻塞的 shell，你可以使用进程监视器结束挂起的 Python 进程。
* 目前 macOS 上不支持 OpenSplice。此外，`对原生句柄的访问 <https://github.com/ros2/rmw_opensplice/issues/182>`__ 尚未实现。
* 在使用 Connext 时，目前不允许基名相同但命名空间不同的两个话题具有不同的类型（参见 `issue <https://github.com/ros2/rmw_connext/issues/234>`__）。
