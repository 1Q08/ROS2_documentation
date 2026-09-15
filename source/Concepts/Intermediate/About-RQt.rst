.. redirect-from::

   RQt-Overview-Usage
   Tutorials/RQt-Overview-Usage
   Concepts/About-RQt

RQt 概述与使用
==============

.. contents:: 目录
   :local:

概述
----

RQt 是一个图形用户界面框架，它以插件的形式实现了各种工具和界面。
您可以在 RQt 中以可停靠窗口的形式运行所有现有的 GUI 工具。
这些工具仍然可以按传统方式独立运行，但 RQt 让您可以在单一屏幕布局中更轻松地管理各种窗口。

您可以轻松运行任何 RQt 工具/插件，方法如下：

.. code-block:: console

   $ rqt

这个 GUI 允许您选择系统上任何可用的插件。
您还可以在独立窗口中运行插件。
例如，RQt Python 控制台：

.. code-block:: console

   $ ros2 run rqt_py_console rqt_py_console

用户可以用 ``Python`` 或 ``C++`` 为 RQt 创建自己的插件。
要查看您的系统上有哪些 RQt 插件可用，请运行：

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
* *rqt_common_plugins* - 常用调试工具。

RQt 框架的优势
--------------

与从零开始构建自己的 GUI 相比：

* 标准化的 GUI 通用流程（启动-关闭钩子、恢复先前状态）。
* 可在单个窗口中停靠多个小部件。
* 轻松将您现有的 Qt 小部件转换为 RQt 插件。
* 可在 Robotics Stack Exchange（ROS 社区问答网站）获得支持，网址：https://robotics.stackexchange.com/

从系统架构的角度看：

* 支持多平台（基本上凡是能运行 ``QT`` 和 ROS 的地方）和多语言（``Python``、``C++``）。
* 生命周期易于管理：RQt 插件使用通用 API，使维护和复用更加容易。


进一步阅读
----------

* ROS 2 Discourse 上的 `移植到 ROS 2 的公告 <https://discourse.openrobotics.org/t/rqt-in-ros2/6428>`__）
* `RQt for ROS 1 文档 <https://wiki.ros.org/rqt>`__
* RQt 简介（摘自 `Willow Garage 实习生的博客文章 <http://web.archive.org/web/20130518142837/http://www.willowgarage.com/blog/2012/10/21/ros-gui>`__）
