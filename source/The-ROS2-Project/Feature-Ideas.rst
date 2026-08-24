.. redirect-from::

  Feature-Ideas

.. _FeatureIdeas:

功能想法
========

.. contents:: 目录
   :depth: 2
   :local:

以下是无特定顺序的功能创意。
这个列表包含我们认为很重要、适合作为对 ROS 2 良好贡献的功能。
在深入一个新功能之前，请 :doc:`先与我们联系 <../Contact>`。
我们可以提供指导，并将你与其他开发者联系起来。

设计 / 概念
-----------

* IDL 格式

  * 利用新特性，如将常量分组到枚举中
  * 将使用扩展到仅包含常量和/或声明带范围参数的 ``.idl`` 文件
  * 重新审视 IDL 接口命名的限制，参见 `ros2/design#220 <https://github.com/ros2/design/pull/220>`_

* 为 ROS 1 -> ROS 2 迁移制定迁移计划
* 节点名称的唯一性，参见 `ros2/design#187 <https://github.com/ros2/design/issues/187>`_
* 以描述性格式定义节点的特定“API”（话题 / 服务等），参见 `ros2/design#266 <https://github.com/ros2/design/pull/266>`_

基础设施和工具
--------------

* 构建

  * 合并 https://build.ros2.org 和 https://ci.ros2.org
  * 提供 macOS
  * Windows 和 macOS 包
  * 在 ``colcon`` 中支持 profiles

* 文档

  * 弃用 https://design.ros2.org。
    内容应迁移到 REP、https://github.com/ros2/ros2_documentation，或被移除。
  * 修复每个包的文档构建器，使其能够记录构建产物，即消息、服务、动作等。
  * 使 https://docs.ros.org/en/ros2_documentation 在 https://github.com/ros2/ros2_documentation 有更改时自动重新构建。
  * ``ament`` 文档
  * 添加使用 Jupyter notebook 配合 ROS 2 的文档示例。
  * 添加实现新 RMW 的文档。
  * 提供三种不同类型的内容：

    * “demos”用于展示功能并用测试覆盖它们
    * “examples”用于展示简单/极简的用法，可能有多种方式来做某事
    * “tutorials”包含更多注释和 wiki 的锚点（教授一种推荐方式）

新功能
------

末尾的星号表示粗略的工作量：1 颗星表示小，2 颗星表示中等，3 颗星表示大。


* 日志改进 [\* / \*\*]

  * 在文件中指定的配置
  * 每个 logger 的配置（例如启用 ``rqt_logger_level``）

* 时间相关

  * 支持基于时钟的速率和睡眠

* 额外的图 API 功能 [\*\* / \*\*\*]

  * 内省所有（尤其是远程）话题的 QoS 设置
  * 类似 ROS 1 Master API：https://wiki.ros.org/ROS/Master_API
  * 基于事件的通知
  * 需要了解需要扩展的 rmw 接口

* 执行器

  * 性能改进（主要围绕 waitset）
  * 确定性排序（公平调度）
  * 解耦 waitable

* 消息生成

  * 为开箱即不支持的语言补上消息生成
  * 混淆消息中的字段名以避免语言特定关键字
  * 通过在同一 Python 解释器中运行生成器来提高生成器性能

* Launch

  * 支持启动多节点可执行文件（即手动组合）
  * 扩展 launch XML/YAML 支持：事件和事件处理器、标签命名空间和别名

* Rosbag

  * 支持录制服务（和动作）

* ros1_bridge

  * 支持桥接动作

* RMW 配置

  * 统一配置中间件的标准方式

* 重映射 [\*\* / \*\*\*]

  * 通过 Service 接口进行动态重映射和别名

* 类型伪装 [\*\*\*]

  * 类似 ROS 1 的消息 traits：https://wiki.ros.org/roscpp/Overview/MessagesSerializationAndAdaptingTypes
  * 需要了解 typesupport 系统

* 扩展实时安全 [\*\*\*]

  * 用于服务、客户端和参数
  * 公开更多与实时性能相关的服务质量参数
  * 实时安全的进程内消息传递

* 多机器人支持功能和演示 [\*\*\*]

  * 不希望所有机器人上的所有节点共享相同的域（并相互发现）
  * 设计如何“分区”系统

* 支持更多 DDS / RTPS 实现：

  * RTI Connext DDS Micro（已实现，默认未启用或未官方支持）。

* 安全改进：

  * 更细粒度的安全配置（仅允许认证、认证和加密等） [\*]
  * 集成 DDS-Security 日志插件（统一聚合安全事件并通过 ROS 接口向用户报告） [\*\*]
  * 密钥存储安全（目前密钥仅存储在文件系统中） [\*\*]
  * 更友好的用户界面（使指定安全配置更容易）。
    也许是一个 Qt GUI？
    这个 GUI 还可以以某种方式协助分发密钥 [\*\*\*]
  * 一种通过某些 UI 说“请保护这个正在运行的系统”的方式，该 UI 会为当前正在运行的所有内容自动生成密钥和策略 [\*\*\*]
  * 如果有硬件特定的功能用于保护密钥或加速加密/签名消息，可以将其添加到尚未使用它的 DDS/RTPS 实现中 [\*\*\*]

减少技术债务
------------

* 修复 https://ci.ros2.org/view/nightly 上的不稳固测试。
* 能够使用工具（如 valgrind、clang-tidy、clang 静态分析 (scan-build)、ASAN、TSAN、UBSAN 等）运行（全部）单元测试。
* API 审查，特别是 rclcpp 和 rclpy 中面向用户的 API
* 将 rclcpp API 重构为专注于单一方面的独立包，之后 rclcpp 仍应提供组合的面向用户的 API
* 重新审视消息分配器，考虑使用 std::polymorphic_allocator 来解决问题
* 将 `设计文档 <https://design.ros2.org>`__ 与实现同步/协调。
* 处理 / 分类待处理工单
* 处理代码 / 文档中的 TODO
* 移除 tinyxml 依赖
