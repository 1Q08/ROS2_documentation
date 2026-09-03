.. _PlatformEOLPolicy:

平台 EOL 策略
=============

.. contents:: 目录
   :depth: 1
   :local:

:doc:`ROS 发行版 <../Releases>` 不支持已停止维护（EOL）的平台，即使该 ROS 发行版仍处于活跃状态。
本页面说明：

* EOL 平台的用户应该预期什么
* ROS Bosses 应该做什么

策略
----

每个 ROS 发行版都支持特定的\ **平台**，例如 Windows 11 或 Ubuntu 24.04。
这些平台的\ **供应商**\ （例如 Microsoft 或 Canonical）决定他们支持其平台的时长。
当供应商决定某个平台已到达 EOL 时，他们通常会停止发布关键错误和安全修复。
为了保护我们自己免受潜在未修补安全漏洞的影响，我们会主动从 ROS 构建农场移除 EOL 平台上的所有作业。

如果你正在使用一个不再受其供应商支持的平台，你应该预期不再收到更新的 ROS 包。
现有的 ROS 包仍将保持可用和正常运作，但它们将不再更新。
不过，在特殊情况下，ROS Bosses 可以选择更新 EOL 平台上的包。

面向 ROS Bosses
---------------

在目标平台到达 EOL 之前：

* 确保 ROS 发行版文档包含任何比 ROS 发行版更早到达 EOL 的平台的 EOL 日期。
* 至少提前 2 次同步（大约 60-90 天）发布关于该平台到达 EOL 的公告，以便包维护者有时间为他们的包做更新。
* 发起一个 `禁用该平台 buildfarm 作业的拉取请求 <https://github.com/ros2/ros_buildfarm_config>`_，并寻求 `Infrastructure PMC <https://osralliance.org/wp-content/uploads/2024/03/infrastructure_project_charter.pdf>`_ 的审查。
* 对该平台做最后一次同步。

在目标平台到达 EOL 之后：

* 更新 ROS 发行版文档，说明该平台将不再收到更新的 ROS 包。
* 在 Discourse 上宣布该 ROS 发行版已放弃对该平台的支持。
* 考虑在以下情况下对该平台做最后一次发布：
    * 你在 EOL 之前尚未这样做，并且
    * 这些更新似乎不太可能出现回归，并且
    * ROS Buildfarm 仍然有该平台的运行器。
* 合并你的拉取请求以禁用 buildfarm 作业。
