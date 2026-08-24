.. redirect-from::

   RQt-Overview-Usage
   Tutorials/RQt-Overview-Usage
   Concepts/About-RQt

RQt 概览与用法
==============

.. contents:: 目录
   :local:

概述
----

RQt 是一个图形用户界面框架，它以插件的形式实现各种工具和接口。
可以在 RQt 中把所有现有的 GUI 工具作为可停靠窗口运行。
这些工具仍然可以以传统的独立方式运行，但 RQt 使得在单一屏幕布局中管理所有各种窗口更加容易。

你可以通过以下命令轻松运行任何 RQt 工具/插件：

.. code-block:: console

   $ rqt

这个 GUI 允许你选择系统上任何可用的插件。
你也可以在独立窗口中运行插件。
例如，RQt Python 控制台：

.. code-block:: console

   $ ros2 run rqt_py_console rqt_py_console

用户可以用 ``Python`` 或 ``C++`` 为 RQt 创建自己的插件。
要查看系统上有哪些可用的 RQt 插件，请运行：

.. code-block:: console

   $ ros2 pkg list

然后查找以 ``rqt_`` 开头的包。

系统设置
--------

从 deb 包安装
^^^^^^^^^^^^^

.. code-block:: console

   $ sudo apt install ros-{DISTRO}-rqt*


RQt 组件结构
------------

RQt 由两个元包组成：

* *rqt* - 核心基础设施模块。
* *rqt_common_plugins* - 常用的调试工具。

RQt 框架的优势
--------------

与从头构建你自己的 GUI 相比：

* 标准化的 GUI 通用流程（启动-关闭钩子、恢复先前状态）。
* 多个控件可以停靠在单个窗口中。
* 轻松地将你现有的 Qt 控件转换为 RQt 插件。
* 可在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ （ROS 社区问答网站）获得支持。

从系统架构的角度来看：

* 支持多平台（基本上只要 `QT <http://qt-project.org/>`__ 和 ROS 运行的地方）和多语言（``Python``、``C++``）。
* 可管理的生命周期：RQt 插件使用通用 API，使维护和复用更加容易。


延伸阅读
--------

* ROS 2 Discourse 上的 `移植到 ROS 2 的公告 <https://discourse.openrobotics.org/t/rqt-in-ros2/6428>`__)
* `ROS 1 的 RQt 文档 <https://wiki.ros.org/rqt>`__
* RQt 简要概述（来自 `Willow Garage 实习生的博客文章 <http://web.archive.org/web/20130518142837/http://www.willowgarage.com/blog/2012/10/21/ros-gui>`__）
