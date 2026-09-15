.. redirect-from::

    Tutorials/Tf2/Tf2-Main

.. _Tf2Main:

``tf2``
=======

许多 tf2 教程同时提供 C++ 和 Python 版本。
这些教程经过精简，可分别完成 C++ 路线或 Python 路线。
如果你想同时学习 C++ 和 Python，则应针对 C++ 和 Python 各学习一遍这些教程。

.. contents:: 目录
   :depth: 2
   :local:

.. toctree::
   :hidden:

   Introduction-To-Tf2
   Writing-A-Tf2-Static-Broadcaster-Py
   Writing-A-Tf2-Static-Broadcaster-Cpp
   Writing-A-Tf2-Broadcaster-Py
   Writing-A-Tf2-Broadcaster-Cpp
   Writing-A-Tf2-Listener-Py
   Writing-A-Tf2-Listener-Cpp
   Adding-A-Frame-Py
   Adding-A-Frame-Cpp
   Learning-About-Tf2-And-Time-Cpp
   Time-Travel-With-Tf2-Cpp
   Debugging-Tf2-Problems
   Quaternion-Fundamentals
   Using-Stamped-Datatypes-With-Tf2-Ros-MessageFilter

工作空间设置
------------

如果你还没有创建用于完成这些教程的工作空间，请 :doc:`按照本教程操作 <../../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace>`。

学习 tf2
--------

#. :doc:`tf2 简介 <./Introduction-To-Tf2>`。

   本教程将让你很好地了解 tf2 能为你做什么。
   它通过一个使用 turtlesim 的多机器人示例展示了 tf2 的部分强大功能。
   本教程还介绍了 ``tf2_echo``、``view_frames`` 和 ``rviz`` 的用法。

#. 编写静态广播器 :doc:`(Python) <./Writing-A-Tf2-Static-Broadcaster-Py>` :doc:`(C++) <./Writing-A-Tf2-Static-Broadcaster-Cpp>`。

   本教程将教你如何向 tf2 广播静态坐标系。

#. 编写广播器 :doc:`(Python) <./Writing-A-Tf2-Broadcaster-Py>` :doc:`(C++) <Writing-A-Tf2-Broadcaster-Cpp>`。

   本教程将教你如何向 tf2 广播机器人的状态。

#. 编写监听器 :doc:`(Python) <./Writing-A-Tf2-Listener-Py>` :doc:`(C++) <./Writing-A-Tf2-Listener-Cpp>`。

   本教程将教你如何使用 tf2 获取坐标变换。

#. 添加坐标系 :doc:`(Python) <./Adding-A-Frame-Py>` :doc:`(C++) <Adding-A-Frame-Cpp>`。

   本教程将教你如何向 tf2 添加一个额外的固定坐标系。

#. 使用时间 :doc:`(C++) <Learning-About-Tf2-And-Time-Cpp>`。

   本教程将教你使用 ``lookup_transform`` 函数中的超时参数，以
   等待 tf2 树上有可用的变换。

#. 时间旅行 :doc:`(C++) <./Time-Travel-With-Tf2-Cpp>`。

   本教程将介绍 tf2 的高级时间旅行功能。

调试 tf2
--------

#. :doc:`四元数基础 <./Quaternion-Fundamentals>`。

   本教程将教你 ROS 2 中四元数使用的基础知识。

#. :doc:`调试 tf2 问题 <./Debugging-Tf2-Problems>`。

   本教程将介绍一种系统化调试 tf2 相关问题的方法。

将传感器消息与 tf2 一起使用
---------------------------

#. :doc:`将带时间戳的数据类型与 tf2_ros::MessageFilter 一起使用 <./Using-Stamped-Datatypes-With-Tf2-Ros-MessageFilter>`。

   本教程将教你如何使用 ``tf2_ros::MessageFilter`` 处理带时间戳的数据类型。
