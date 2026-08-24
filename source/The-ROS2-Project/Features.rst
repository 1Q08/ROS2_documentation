.. redirect-from::

  Features

.. _Features:

功能状态
========

以下列出的功能在当前 ROS 2 版本中可用。
除非另有说明，这些功能适用于所有受支持的平台（Ubuntu 24.04 (Noble)、Windows 10）、DDS 实现（eProsima Fast DDS、RTI Connext DDS 和 Eclipse Cyclone DDS）以及编程语言客户端库（C++ 和 Python）。
关于计划中的未来开发，请参阅 :doc:`路线图 <Roadmap>`。

.. list-table::
   :header-rows: 1

   * - 功能
     - 链接
     - 补充说明
   * - 基于 DDS 的发现、传输和序列化
     - `文章 <https://design.ros2.org/articles/ros_on_dds.html>`__
     -
   * - 支持 :doc:`多种 DDS 实现 <../Concepts/Intermediate/About-Different-Middleware-Vendors>`，在运行时选择
     - :doc:`概念 <../Concepts/Intermediate/About-Different-Middleware-Vendors>`、:doc:`How-to 指南 <../How-To-Guides/Working-with-multiple-RMW-implementations>`
     - 目前 Eclipse Cyclone DDS、eProsima Fast DDS 和 RTI Connext DDS 均得到完全支持。
   * - 由语言特定库封装而成的公共核心客户端库
     - :doc:`详情 <../Concepts/Basic/About-Client-Libraries>`
     -
   * - 基于话题的发布/订阅
     - `示例代码 <https://github.com/ros2/examples>`__\ 、`文章 <https://design.ros2.org/articles/topic_and_service_names.html>`__
     -
   * - 客户端和服务
     - `示例代码 <https://github.com/ros2/examples>`__
     -
   * - 设置/获取参数
     - `示例代码 <https://github.com/ros2/demos/tree/0.5.1/demo_nodes_cpp/src/parameters>`__
     -
   * - ROS 1 - ROS 2 通信桥
     - `教程 <https://github.com/ros2/ros1_bridge/blob/master/README.md>`__
     - 可用于话题和服务，尚不可用于动作。
   * - 用于处理非理想网络的服务质量设置
     - :doc:`演示 <../Tutorials/Demos/Quality-of-Service>`
     -
   * - 使用相同 API 的进程间和进程内通信
     - :doc:`演示 <../Tutorials/Demos/Intra-Process-Communication>`
     - 目前仅支持 C++。
   * - 在编译、链接、加载或运行时组合节点组件
     - :doc:`演示 <../Tutorials/Intermediate/Composition>`
     - 目前仅支持 C++。
   * - 同一节点中的多个执行器（在回调组级别）
     - `演示 <https://github.com/ros2/examples/tree/{DISTRO}/rclcpp/executors/cbg_executor>`__
     - 仅支持 C++。
   * - 支持具有受管理生命周期的节点
     - :doc:`演示 <../Tutorials/Demos/Managed-Nodes>`
     - 目前仅支持 C++。
   * - DDS-Security 支持
     - `演示 <https://github.com/ros2/sros2>`__
     -
   * - 使用可扩展框架的命令行内省工具
     - :doc:`概念 <../Concepts/Basic/About-Command-Line-Tools>`
     -
   * - 用于协调多个节点的启动系统
     - :doc:`教程 <../Tutorials/Intermediate/Launch/Launch-system>`
     -
   * - 节点和话题的命名空间支持
     - `文章 <https://design.ros2.org/articles/topic_and_service_names.html>`__
     -
   * - ROS 名称的静态重映射
     - :doc:`How-to 指南 <../How-To-Guides/Node-arguments>`
     -
   * - 全 ROS 2 移动机器人的演示
     - `演示 <https://github.com/ros2/turtlebot2_demo>`__
     -
   * - 实时代码的初步支持
     - :doc:`演示 <../Tutorials/Demos/Real-Time-Programming>`、:doc:`演示 <../Tutorials/Advanced/Allocator-Template-Tutorial>`
     - 仅限 Linux。
       不适用于 Fast RTPS。
   * - 对“裸金属”微控制器的初步支持
     - `Wiki <https://github.com/ros2/freertps/wiki>`__
     -
   * - 内容过滤订阅
     - :doc:`演示 <../Tutorials/Demos/Content-Filtering-Subscription>`
     - 目前仅支持 C++。
   * - 服务内省
     - :doc:`演示 <../Tutorials/Demos/Service-Introspection>`
     -

除了平台的核心功能外，ROS 最大的影响来自其可用的包。
以下是在最新版本中可用的一些高知名度包：

* `gazebo_ros_pkgs <https://index.ros.org/r/gazebo_ros_pkgs/>`__
* `image_transport <https://index.ros.org/r/image_common>`__
* `navigation2 <https://index.ros.org/r/navigation2/>`__
* `rosbag2 <https://index.ros.org/r/rosbag2/>`__
* `RQt <https://index.ros.org/r/rqt/>`__
* `RViz2 <https://index.ros.org/r/rviz/>`__
