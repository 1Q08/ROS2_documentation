.. redirect-from::

  Beta3-Overview

Beta 3 (``r2b3``)
=================

.. contents:: 目录
   :depth: 2
   :local:

支持的平台
----------

我们在三个平台上支持 ROS 2 Beta 3：Ubuntu 16.04 (Xenial)、macOS 10.12 (Sierra) 和 Windows 10。
我们为全部 3 个平台提供了二进制软件包以及从源代码编译的说明（参见 `安装说明 <../../Installation>` 以及 `文档 <https://docs.ros2.org/beta3/>`__）。

功能
----

自 Beta 2 版本以来的改进
^^^^^^^^^^^^^^^^^^^^^^^^^^

* Python 中的执行模型，修复了 Python C 扩展中内存管理的许多问题
* 实验性重写 `ros_control <https://github.com/ros2/ros2_control>`__
* 向用户公开 DDS 实现特定的符号（用于 Fast RTPS 和 Connext）（参见 `示例 <https://github.com/ros2/demos/blob/6363be2efe2fea799d92bc22a66e776b2ca9c5d0/demo_nodes_cpp_native/src/talker.cpp>`__）
* Python 中的日志 `API <https://github.com/ros2/rclpy/blob/1ef2924ef8e154c0553edf0fdba4840b08b728f8/rclpy/rclpy/logging.py>`__
* 修复了多个软件包中的若干内存泄漏和竞态条件
* 重新添加了对 PrismTech 提供的 OpenSplice 的支持（目前用于 Linux 和 Windows）
* 使用 bloom（无补丁）来制作 ROS 2 版本

新演示应用
^^^^^^^^^^

* `HSR 演示 <https://github.com/ruffsl/hsr_demo>`__

  * 使用 ROS 2 游戏手柄控制器远程控制 HSR 机器人
  * 在 HSR 上的 Docker 容器中运行 ``ros1_bridge`` （因为机器人运行的是 Ubuntu Trusty 上的 ROS 1）
  * 运行 ROS 2 开发版 `rviz <https://github.com/ros2/rviz>`__ 来可视化机器人等设备的传感器数据（参见 `视频 <https://vimeo.com/237016358>`__）

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
  * PrismTech OpenSplice：参见下方限制

* 网络事件的图 API
* 分布式发现
* 使用兼容 DDS 实现（目前仅 Connext）进行发布和订阅的实时安全代码路径

  * 支持自定义分配器

* ROS 1 <-> ROS 2 动态桥接节点
* 执行器线程模型（C++ 和 Python）
* 在编译 / 链接 / 运行时组合节点的组件模型
* 使用标准生命周期的托管组件
* 扩展的 ``.msg`` 格式，包含新功能：

  * 有界数组
  * 默认值

已知问题
--------

* 在 Windows 上，尝试使用 ``Ctrl-C`` 中止时 Python 启动文件可能会挂起（参见 `issue <https://github.com/ros2/launch/issues/64>`__）。为了继续使用被挂起命令阻塞的 shell，你可能想使用进程监视器结束挂起的 Python 进程。
* OpenSplice 支持目前不适用于 macOS。此外，`对原生句柄的访问 <https://github.com/ros2/rmw_opensplice/issues/182>`__ 尚未实现。
* 使用 Connext 时，目前不允许两个具有相同基础名称但不同命名空间的话题具有不同类型（参见 `issue <https://github.com/ros2/rmw_connext/issues/234>`__）。
