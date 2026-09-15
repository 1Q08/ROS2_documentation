.. _First-steps-with-ROS-learning-path:

ROS 入门——学习路径
==================

ROS（机器人操作系统）是一个开源生态系统，提供用于构建、部署、运行和维护机器人应用的框架、工具和库。
本页提供了一系列文章和动手实践，用于介绍 ROS 框架背后的主要概念。
完成这些内容将使您获得开始使用 ROS 开发应用所需的基本知识。

**领域：ROS 框架 | 内容类型：学习路径 | 经验水平：初级**

.. contents:: 目录
    :depth: 2
    :local:

概述
----

ROS 框架是使机器人各部分之间能够通信的“管道”。
它包括消息传递、标准接口，以及对多种编程语言和平台的支持。

在使用 ROS 开发或维护应用之前，您需要理解该框架的基本概念。
turtlesim 工具和本站的教程将帮助您快速上手。


前提条件
--------

无。
本文列出的步骤将指导您下载并安装学习 ROS 基础知识所需的一切。

步骤
----

1 了解 ROS 背后的基本概念
^^^^^^^^^^^^^^^^^^^^^^^^^

* :doc:`关于 ROS </About-ROS>`
* :doc:`/Concepts/Basic/About-Nodes`
* :doc:`/Concepts/Basic/Interfaces-Topics-Services-Actions`
* :doc:`/Concepts/Basic/About-Parameters`

2 安装 ROS 和 turtlesim
^^^^^^^^^^^^^^^^^^^^^^^

ROS 安装包含使用 ROS 所需的基本包。
如果您熟悉 Linux，我们推荐的平台是 Ubuntu（deb 包）。
否则，一个不错的备选安装平台是 Windows（二进制包）：:doc:`安装选项 </Installation>`

借助 turtlesim 这个为初学者设计的轻量级 2D 仿真工具，您可以在简单的可视化环境中学习 ROS 核心概念：:doc:`安装并设置 turtlesim </Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim>`

3 尝试使用 ROS 框架的主要通信组件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

使用 turtlesim 熟悉主要通信组件，并尝试 ROS 框架中的消息传递。

#. 完成节点教程：:doc:`/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes`
#. 完成话题教程：:doc:`/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics`
#. 完成服务教程：:doc:`/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services`
#. 完成参数教程：:doc:`/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters`
#. 完成动作教程：:doc:`/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions`

4 了解使用日志进行内省
^^^^^^^^^^^^^^^^^^^^^^

内省使您能够查看有关系统运行情况的信息。
节点使用日志以多种方式输出有关事件和状态的消息。

要实际体验通过日志进行内省，请完成 rqt_console 教程：:doc:`/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console`

5 了解如何使用启动文件
^^^^^^^^^^^^^^^^^^^^^^

启动文件允许您同时启动和配置多个包含 ROS 节点的进程，而不必打开多个终端并为每个节点重新输入配置细节。

完成启动文件教程：:doc:`/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes`

6 了解数据录制与回放
^^^^^^^^^^^^^^^^^^^^

有时回放数据很有用，可以重现测试和实验的结果、调试机器人的行为，或与他人分享您的工作。

完成录制与回放教程：:doc:`/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data`

后续步骤
--------

为了完善您对 ROS 框架的了解，我们建议您熟悉 ROS 客户端库：:doc:`/Tutorials/Beginner-Client-Libraries`
