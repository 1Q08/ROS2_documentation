.. redirect-from::

  Beta1-Overview

Beta 1（``Asphalt``）
=====================

.. contents:: 目录
   :depth: 2
   :local:

支持的平台
----------

我们在三个平台上支持 ROS 2 Beta 1：Ubuntu 16.04（Xenial）、Mac OS X 10.11（El Capitan）以及 Windows 8.1 和 10。我们为全部 3 个平台同时提供二进制软件包和从源代码编译的说明。

功能
----

自 Alpha 8 发布以来的改进
^^^^^^^^^^^^^^^^^^^^^^^^^

* 支持在编译时、链接时或运行时进行节点组合。
* 受管节点的标准生命周期。
* 改进对服务质量调优和测试的支持。
* `新增和更新的设计文档 <https://design.ros2.org/>`__
* 更多的 `教程 <../../Tutorials>` 和 `示例 <https://github.com/ros2/examples>`__
* 与 ROS 1 互相桥接服务（除话题之外）

先前 Alpha 版本中的部分功能
^^^^^^^^^^^^^^^^^^^^^^^^^^^

完整列表请参见 `早期发行说明 <../index>`。


* ROS 2 客户端库的 C++ 和 Python 实现，包括以下 API：

  * 发布和订阅 ROS 话题
  * 请求和应答 ROS 服务（同步（仅 C++）和异步）
  * 获取和设置 ROS 参数（仅 C++，同步和异步）
  * 定时器回调
  * 支持多个 DDS/RTPS 实现之间的互操作
  * eProsima Fast RTPS 是我们的默认实现，并包含在二进制软件包中
  * 支持 RTI Connext：从源代码构建即可试用
  * 我们最初支持 PrismTech OpenSplice，但最终决定放弃它

* 用于网络事件的图 API
* 分布式发现
* 与兼容的 DDS 实现搭配时用于发布和订阅的实时安全代码路径（目前仅 Connext）

  * 支持自定义分配器

* ROS 1 <-> ROS 2 动态桥接节点
* C++ 中的执行器线程模型
* 扩展的 ``.msg`` 格式，新增以下功能：

  * 有界数组
  * 默认值

已知问题
^^^^^^^^

* 我们在各个仓库中跟踪问题，但主要的入口是 `ros2/ros2 issue 跟踪器 <https://github.com/ros2/ros2/issues>`__
* 我们想特别指出一个 `已知问题 <https://github.com/ros2/rmw_fastrtps/issues/81>`__，我们正与 eProsima 合作修复它，该问题会导致 FastRTPS 下大消息的性能显著下降。
  在运行一些使用较大图像分辨率的演示时会出现该问题。
