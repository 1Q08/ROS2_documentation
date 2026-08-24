.. redirect-from::

  Beta1-Overview

Beta 1 (``Asphalt``)
====================

.. contents:: 目录
   :depth: 2
   :local:

支持的平台
----------

我们在三个平台上支持 ROS 2 Beta 1：Ubuntu 16.04 (Xenial)、Mac OS X 10.11 (El Capitan) 以及 Windows 8.1 和 10。我们为全部 3 个平台提供了二进制软件包以及从源代码编译的说明。

功能
----

自 Alpha 8 版本以来的改进
^^^^^^^^^^^^^^^^^^^^^^^^^

* 支持在编译、链接或运行时进行节点组合。
* 托管节点的标准生命周期。
* 改进了对服务质量调优和测试的支持。
* `新增和更新的设计文档 <https://design.ros2.org/>`__
* 更多 `教程 <../../Tutorials>` 和 `示例 <https://github.com/ros2/examples>`__
* 桥接 ROS 1 的往来服务（除话题外）

以往 Alpha 版本的部分功能
^^^^^^^^^^^^^^^^^^^^^^^^^

完整列表请参见 `早期版本说明 <../index>`。


* ROS 2 客户端库的 C++ 和 Python 实现，包括以下 API：

  * 发布和订阅 ROS 话题
  * 请求和应答 ROS 服务（同步（仅 C++）和异步）
  * 获取和设置 ROS 参数（仅 C++，同步和异步）
  * 定时器回调
  * 支持多个 DDS/RTPS 实现之间的互操作性
  * eProsima Fast RTPS 是我们的默认实现，包含在二进制软件包中
  * 支持 RTI Connext：从源代码构建以试用
  * 我们最初支持 PrismTech OpenSplice，但最终决定放弃它

* 网络事件的图 API
* 分布式发现
* 使用兼容 DDS 实现（目前仅 Connext）进行发布和订阅的实时安全代码路径

  * 支持自定义分配器

* ROS 1 <-> ROS 2 动态桥接节点
* C++ 中的执行器线程模型
* 扩展的 ``.msg`` 格式，包含新功能：

  * 有界数组
  * 默认值

已知问题
^^^^^^^^

* 我们在各个仓库中跟踪问题，但主要入口是 `ros2/ros2 问题跟踪器 <https://github.com/ros2/ros2/issues>`__
* 我们想强调一个 `已知问题 <https://github.com/ros2/rmw_fastrtps/issues/81>`__，我们正在与 eProsima 合作修复该问题，它会导致 FastRTPS 下大消息的性能显著下降。
  在运行某些分辨率较大的图像演示时会观察到这种情况。
