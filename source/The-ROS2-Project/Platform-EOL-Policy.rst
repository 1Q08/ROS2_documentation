.. _PlatformEOLPolicy:

平台 EOL 政策
=============

.. contents:: 目录
   :depth: 1
   :local:

:doc:`ROS distributions <../Releases>` 不会为已进入生命周期终止（EOL）的平台提供支持，即使该 ROS 发行版仍处于活动状态。
本文说明：

* EOL 平台用户应如何预期
* ROS Bosses 应该怎么做

政策
----

每个 ROS 发行版都会支持某些平台，例如 Windows 11 或 Ubuntu 24.04。
这些平台的供应商（如 Microsoft、Canonical）会决定平台支持期限。
当供应商决定某平台已达到 EOL 时，通常会停止发布关键缺陷修复和安全修复。
为避免可能暴露的未修补安全漏洞，我们会主动从 ROS 构建农场中移除 EOL 平台相关的作业。

如果你正在使用一个已不再被供应商支持的平台，你应该预期停止接收 ROS 包更新。
现有 ROS 包仍可用且可运行，但不再更新。
不过，在特殊情况下，ROS Bosses 也可能选择为 EOL 平台更新软件包。

面向 ROS Bosses
---------------

在目标平台达到 EOL 之前：

* 确保 ROS 发行版文档中包含任一将在 ROS 发行版之前达到 EOL 的平台的 EOL 日期。
* 至少提前 2 次同步（约 60–90 天）发布关于该平台达到 EOL 的公告，让包维护者有时间更新他们的包。
* 打开一个 `pull request 禁用该平台 buildfarm 作业 <https://github.com/ros2/ros_buildfarm_config>`_，并请 `Infrastructure PMC <https://osralliance.org/wp-content/uploads/2024/03/infrastructure_project_charter.pdf>`_ 审查。
* 对该平台最后进行一次同步。

在目标平台达到 EOL 之后：

* 更新 ROS 发行版文档，说明该平台将不再接收 ROS 包更新。
* 在 Discourse 上宣布该 ROS 发行版已经放弃对该平台的支持。
* 若符合以下条件，可考虑为该平台再发布一次版本：
    * 你此前尚未在 EOL 前进行过这次发布，且
    * 更新看起来不太可能引入回归，且
    * ROS Buildfarm 仍有该平台的运行器。
* 合并你的 PR，禁用 buildfarm 作业。
