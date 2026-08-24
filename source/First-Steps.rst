.. _First-steps-with-ROS-learning-path:

ROS 入门 - 学习路径
===================

ROS（Robot Operating System，机器人操作系统）是一个开源生态系统，为构建、部署、运行和维护机器人应用提供框架、工具和库。
本页提供一组文章和动手实践活动，介绍 ROS 框架背后的主要概念。
完成这些内容后，你将掌握开始使用 ROS 开发应用所必需的基础知识。

**领域：ROS 框架 | 内容类型：学习路径 | 难度：入门**

.. contents:: 目录
    :depth: 2
    :local:

概述
----

ROS 框架是使机器人不同部分之间能够相互通信的"管道"。
它包括消息传递、标准接口，以及对多种编程语言和平台的支持。

在开始使用 ROS 开发或维护应用之前，你需要理解该框架的基本概念。
turtlesim 工具和本站的教程将帮助你快速上手。

前置条件
--------

无。
本文列出的步骤将引导你下载并安装学习 ROS 基础知识所需的全部内容。

步骤
----

1 了解 ROS 背后的基本概念
^^^^^^^^^^^^^^^^^^^^^^^^^

* :doc:`关于 ROS </About-ROS>`
* :doc:`节点 </Concepts/Basic/About-Nodes>`
* :doc:`接口（话题、服务、动作） </Concepts/Basic/Interfaces-Topics-Services-Actions>`
* :doc:`参数 </Concepts/Basic/About-Parameters>`

2 安装 ROS 和 turtlesim
^^^^^^^^^^^^^^^^^^^^^^^^

ROS 的安装包含使用 ROS 所必需的核心软件包。
如果你熟悉 Linux，我们推荐的平台是 Ubuntu（deb 包）。
否则，另一个不错的替代安装平台是 Windows（二进制包）：:doc:`安装选项 </Installation>`

借助 turtlesim——一款专为初学者设计的轻量级 2D 仿真工具，你可以在简单的可视化环境中学习 ROS 的核心概念：:doc:`安装并设置 turtlesim </Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim>`

3 尝试 ROS 框架的主要通信组件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

使用 turtlesim 来熟悉主要的通信组件，并体验 ROS 框架中的消息传递。

#. 完成节点教程：:doc:`/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes`
#. 完成话题教程：:doc:`/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics`
#. 完成服务教程：:doc:`/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services`
#. 完成参数教程：:doc:`/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters`
#. 完成动作教程：:doc:`/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions`

4 学习通过日志进行内省
^^^^^^^^^^^^^^^^^^^^^^

内省（Introspection）让你能够查看系统运行状况的相关信息。
节点使用日志以多种方式输出与事件和状态相关的消息。

要实际体验通过日志进行内省，请完成 rqt_console 教程：:doc:`/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console`

5 学习使用启动文件
^^^^^^^^^^^^^^^^^^

启动文件允许你同时启动并配置多个包含 ROS 节点的进程，而无需打开多个终端并为每个节点重新输入配置信息。

请完成启动文件教程：:doc:`/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes`

6 学习数据记录与回放
^^^^^^^^^^^^^^^^^^^^

有时，回放数据有助于复现测试和实验的结果、调试机器人的行为，或与他人分享你的工作成果。

请完成记录与回放教程：:doc:`/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data`

下一步
------

为了完善你对 ROS 框架的知识，我们建议你熟悉 ROS 客户端库：:doc:`/Tutorials/Beginner-Client-Libraries`
