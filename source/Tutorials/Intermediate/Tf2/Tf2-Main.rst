.. redirect-from::

    Tutorials/Tf2/Tf2-Main

.. _Tf2Main:

``tf2``
=======

许多 tf2 教程同时提供 C++ 和 Python 两个版本。
这些教程被精简为完成 C++ 路线或 Python 路线。
如果你想同时学习 C++ 和 Python，应该将教程分别过一遍，一次 C++、一次 Python。

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

工作区设置
----------

如果你还没有创建一个用于完成教程的工作区，请 :doc:`按照本教程操作 <../../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace>`。

学习 tf2
--------

#. :doc:`tf2 介绍 <./Introduction-To-Tf2>`。

   本教程将让你很好地了解 tf2 能为你做什么。
   它通过一个使用 turtlesim 的多机器人示例展示了 tf2 的一些强大功能。
   它还介绍了 ``tf2_echo``、``view_frames`` 和 ``rviz`` 的使用。

#. 编写静态广播器 :doc:`(Python) <./Writing-A-Tf2-Static-Broadcaster-Py>` :doc:`(C++) <./Writing-A-Tf2-Static-Broadcaster-Cpp>`。

   本教程教你如何将静态坐标帧广播到 tf2。

#. 编写广播器 :doc:`(Python) <./Writing-A-Tf2-Broadcaster-Py>` :doc:`(C++) <Writing-A-Tf2-Broadcaster-Cpp>`。

   本教程教你如何将机器人的状态广播到 tf2。

#. 编写监听器 :doc:`(Python) <./Writing-A-Tf2-Listener-Py>` :doc:`(C++) <./Writing-A-Tf2-Listener-Cpp>`。

   本教程教你如何使用 tf2 访问帧变换。

#. 添加帧 :doc:`(Python) <./Adding-A-Frame-Py>` :doc:`(C++) <Adding-A-Frame-Cpp>`。

   本教程教你如何向 tf2 添加一个额外的固定帧。

#. 使用时间 :doc:`(C++) <Learning-About-Tf2-And-Time-Cpp>`。

   本教程教你如何在 ``lookup_transform`` 函数中使用超时，以
   等待 tf2 树上的变换可用。

#. 时间旅行 :doc:`(C++) <./Time-Travel-With-Tf2-Cpp>`。

   本教程教你 tf2 的高级时间旅行功能。

调试 tf2
--------

#. :doc:`四元数基础 <./Quaternion-Fundamentals>`。

   本教程教你 ROS 2 中四元数使用的基础知识。

#. :doc:`调试 tf2 问题 <./Debugging-Tf2-Problems>`。

   本教程教你一种系统性的方法来调试与 tf2 相关的问题。

将传感器消息与 tf2 一起使用
---------------------------

#. :doc:`使用 tf2_ros::MessageFilter 处理带时间戳的数据类型 <./Using-Stamped-Datatypes-With-Tf2-Ros-MessageFilter>`。

   本教程教你如何使用 ``tf2_ros::MessageFilter`` 处理带时间戳的数据类型。
