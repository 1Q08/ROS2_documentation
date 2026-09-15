.. redirect-from::

  Feature-Ideas

.. _FeatureIdeas:

功能想法
========

.. contents:: 目录
   :depth: 2
   :local:

以下是功能想法，不分先后顺序。
这个列表包含了我们认为重要、并且可以成为对 ROS 2 良好贡献的功能。
在深入开发一个新功能之前，:doc:`请先与我们联系 <../Contact>`。
我们可以提供指导，并为你对接其他开发者。

设计 / 概念
-----------

* IDL 格式

  * 利用新特性，例如把常量分组到枚举中
  * 将其用途扩展到仅含常量的 ``.idl`` 文件，和/或用范围来声明参数
  * 重新审视 IDL 接口命名的约束，参见 `ros2/design#220 <https://github.com/ros2/design/pull/220>`_

* 为 ROS 1 -> ROS 2 的过渡制定迁移计划
* 节点名称的唯一性，参见 `ros2/design#187 <https://github.com/ros2/design/issues/187>`_
* 以描述性格式给出节点在话题 / 服务 / 等方面的具体"API"，参见 `ros2/design#266 <https://github.com/ros2/design/pull/266>`_

基础设施与工具
--------------

* 构建

  * 合并 https://build.ros2.org 和 https://ci.ros2.org
  * 为 macOS 提供支持
  * Windows 和 macOS 软件包
  * 在 ``colcon`` 中支持 profiles

* 文档

  * 弃用 https://design.ros2.org。
    内容应迁移到 REP、迁移到 https://github.com/ros2/ros2_documentation，或者删除。
  * 修复按软件包划分的文档构建器，使其能够为构建产物（即消息、服务、动作等）生成文档。
  * 让 https://docs.ros.org/en/ros2_documentation 在 https://github.com/ros2/ros2_documentation 发生变更时自动重新构建。
  * ``ament`` 文档
  * 增加配合 Jupyter notebook 使用 ROS 2 的文档示例。
  * 增加实现新 RMW 的文档。
  * 提供三种不同类型的内容：

    * "demos"（演示），用于展示功能并用测试覆盖它们
    * "examples"（示例），用于展示简单/最小化的用法，可能包含多种实现方式
    * "tutorials"（教程），包含更多注释和用于维基的锚点（讲授一种推荐做法）

新功能
------

末尾的星号表示大致工作量：1 星为小，2 星为中等，3 星为大。


* 日志改进 [\* / \*\*]

  * 在文件中指定配置
  * 按记录器进行配置（例如启用 ``rqt_logger_level``）

* 时间相关

  * 基于时钟支持 rate 和 sleep

* 其他图 API 功能 [\*\* / \*\*\*]

  * 内省所有（尤其是远程）话题的 QoS 设置
  * 类似 ROS 1 Master API：https://wiki.ros.org/ROS/Master_API
  * 基于事件的通知
  * 需要了解 rmw 接口的相关知识，该接口需要扩展

* 执行器

  * 性能改进（主要围绕 waitset）
  * 确定性排序（公平调度）
  * 解耦可等待对象

* 消息生成

  * 为非开箱即用支持的语言补充消息生成
  * 对消息中的字段名进行改写，以避免语言特定的关键字
  * 通过在同一 Python 解释器中运行生成器来提升性能

* 启动

  * 支持启动多节点可执行文件（即手动组合）
  * 扩展启动 XML/YAML 支持：事件和事件处理器、标签命名空间和别名

* Rosbag

  * 支持录制服务（和动作）

* ros1_bridge

  * 支持桥接动作

* RMW 配置

  * 统一标准的中间件配置方式

* 重映射 [\*\* / \*\*\*]

  * 通过服务接口实现动态重映射和别名

* 类型伪装 [\*\*\*]

  * 类似 ROS 1 的消息 traits：https://wiki.ros.org/roscpp/Overview/MessagesSerializationAndAdaptingTypes
  * 需要了解类型支持系统

* 扩展实时安全性 [\*\*\*]

  * 面向服务、客户端和参数
  * 暴露更多与实时性能相关的服务质量参数
  * 实时安全的进程内消息传递

* 多机器人支持功能与演示 [\*\*\*]

  * 不希望所有机器人的所有节点共享同一域（并相互发现）
  * 设计如何“划分”系统

* 支持更多 DDS / RTPS 实现：

  * RTI Connext DDS Micro（已实现，但默认未启用也未官方支持）。

* 安全性改进：

  * 更细粒度的安全配置（仅允许认证、认证加加密等）[\*]
  * 集成 DDS-Security 日志插件（通过 ROS 接口统一聚合安全事件并向用户报告）[\*\*]
  * 密钥存储安全（目前密钥只是存储在文件系统中）[\*\*]
  * 更友好的用户界面（让安全配置更易指定）。
    也许是一个 Qt GUI？
    这个 GUI 还可以在某种程度上协助分发密钥 [\*\*\*]
  * 一种通过某种 UI 来表示“请保护这个正在运行的系统”的方式，自动为当前运行的所有内容生成密钥和策略 [\*\*\*]
  * 如果存在用于保护密钥或加速加密/签名消息的硬件特定功能，将其添加到尚未使用该功能的 DDS/RTPS 实现中可能会很有意思 [\*\*\*]

减少技术债务
------------

* 修复 https://ci.ros2.org/view/nightly 上不稳定的测试。
* 能够使用诸如 valgrind、clang-tidy、clang 静态分析（scan-build）、ASAN、TSAN、UBSAN 等工具运行（全部）单元测试。
* API 审查，特别是 rclcpp 和 rclpy 中面向用户的 API
* 将 rclcpp API 重构为专注于单一方面的多个独立软件包，重构后 rclcpp 仍应提供合并后的面向用户 API
* 重新审视消息分配器，考虑使用 std::polymorphic_allocator 来解决相关问题
* 将 `设计文档 <https://design.ros2.org>`__ 与实现同步 / 调和。
* 处理 / 分类待处理的工单
* 处理代码 / 文档中的 TODO
* 移除对 tinyxml 的依赖
