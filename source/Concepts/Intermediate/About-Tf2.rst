.. redirect-from::

   Concepts/About-Tf2

Tf2
===

.. contents:: 目录
   :local:

概述
----

tf2 是一个变换库，它允许用户随着时间跟踪多个坐标系。
tf2 维护坐标系之间的关系，使用时间缓冲树结构，让用户可以在任意时刻在任意两个坐标系之间变换点、向量等。

.. image:: ../images/ros2_tf2_frames.png

tf2 的特性
----------

一个机器人系统通常有许多随时间变化的 3D 坐标系，例如世界坐标系、基座坐标系、夹爪坐标系、头部坐标系等。
tf2 会随着时间跟踪这些坐标系，并允许你提出类似以下问题：

* 5 秒前头部坐标系相对于世界坐标系的位置在哪里？
* 我的夹爪中的物体相对于基座的位姿是什么？
* 地图坐标系中基座坐标系的当前位姿是什么？

tf2 可以在分布式系统中工作。
这意味着机器人所有坐标系的相关信息可供系统中任意计算机上的所有 ROS 2 组件访问。
tf2 可以让分布式系统中的每个组件构建自己的变换信息数据库，也可以由一个中心节点收集并存储所有变换信息。

.. mermaid::

   flowchart LR
      E((Earth))
      E --> A[[Car A]]
      E --> B[[Car B]]
      E --> C{{Satellite C}}
      E --> D((Moon D))

发布变换
^^^^^^^^

在发布变换时，我们通常会把变换理解为一个坐标系到另一个坐标系的变换。
语义上的区别在于你是在转换某个坐标系中表示的数据，还是在转换坐标系本身。
这些值是互逆的。
在 ``geometry_msgs/msg/Transform`` 消息中发布的变换表示的是坐标系表述。
调试已发布变换时请牢记：它们与你按某个方向遍历变换树时查找所得到的内容互为逆值。

.. math::


   _{B}T^{data}_{A} = (_{B}T^{frame}_{A})^{-1}

TF 库会根据你遍历变换树的方向，为你自动处理这些元素的反向求解。
本文档接下来的内容会只使用 :math:`T^{data}`，其中 ``data`` 这一部分不再写出。

位置
^^^^

如果车 A 中的驱动器观测到某个物体，而地面上的人想知道它相对于自身位置的关系，就要将观测值从源坐标系变换到目标坐标系。

.. math::

   _{E}T_{A} * P_{A}^{Obs} = P_{E}^{Obs}


现在如果车 B 上的人也想知道同一个物体的位置，就可以计算得到净变换。


.. math::

   _{B}T_{E} * _{E}T_{A} * P_{A}^{Obs} = _{B}T_{A} * P_{A}^{Obs} = P_{B}^{Obs}


这正是 ``lookupTransform`` 提供的能力，其中 ``A`` 是 *源* ``frame_id``，``B`` 是 *目标* ``frame_id``。

如果可能，建议优先使用 ``transform<T>(target_frame, ...)`` 方法，因为它会从数据类型中读取 *源* ``frame_id``，并将 *目标* ``frame_id`` 写入结果数据类型中，整个数学运算在内部完成。

如果 :math:`P` 是 ``Stamped`` 数据类型，那么 :math:`_A` 就是它的 ``frame_id``。

举例来说，若根坐标系 ``A`` 在坐标系 ``B`` 下方一米，则从 ``A`` 到 ``B`` 的变换为正值。

然而当把数据从坐标系 ``B`` 转换到坐标系 ``A`` 时，必须使用该值的逆值。
这意味着在从较低参考系切换到较高参考系时，你会减少高度值。

.. math::


   _{B}T_{A} = (_{B}{Tf}_{A})^{-1}


速度
^^^^

为了表示 ``Velocity``，我们需要三类信息。
:math:`V^{moving\_frame - reference\_frame}_{observing\_frame}`
这个速度表示移动坐标系与参考坐标系之间的速度关系。
并且它在观察坐标系中表示。

例如，车 A 中的驾驶员可以报告它正在向前行驶（在 A 中观察）且速度为 1m/s（相对于地球），那就是 :math:`V_{A}^{A - E} = (1,0,0)`。
同样，若从地球视角观察（假设汽车向东行驶，地球为 NED），则可以观察到 :math:`V_{E}^{A - E} = (0, 1, 0)`。

不过变换可以说明这两者其实是相同的：

.. math::

   _{E}T_{A} * V_{A}^{A - E} = V_{E}^{A - E}


如果速度用相同坐标系（这里为 ``Obs``）表示，则它们可以相加或相减。

.. math::

   V_{Obs}^{A - C} = V_{Obs}^{A - B} + V_{Obs}^{D - C}

速度可以通过取逆来“反转”。

.. math::

   V_{Obs}^{A - C} = -(V_{Obs}^{C - A})

如果你想比较两个速度，必须先把它们变换到同一个观测坐标系中。


教程
----

我们创建了一套 :doc:`教程 <../../Tutorials/Intermediate/Tf2/Tf2-Main>`，逐步引导你使用 tf2。
你可以从 :doc:`tf2 简介 <../../Tutorials/Intermediate/Tf2/Introduction-To-Tf2>` 教程开始。
要查看所有 tf2 及相关教程的完整列表，请查看 :doc:`教程页面 <../../Tutorials/Intermediate/Tf2/Tf2-Main>`。

tf2 的主要任务本质上有两类：监听变换和广播变换。

如果你希望在坐标系之间使用 tf2 进行变换，你的节点需要监听变换。
你需要接收并缓存系统中广播的所有坐标系帧，并查询两个坐标系之间的特定变换。
请查看“编写监听器”教程 :doc:`（Python） <../../Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Py>` :doc:`（C++） <../../Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Cpp>` 以了解更多。

要扩展机器人的能力，你需要开始广播变换。
广播变换意味着向系统其余部分发送坐标系之间的相对位姿。
一个系统中可以有许多广播器，每个广播器都提供机器人不同部分的信息。
请查看“编写广播器”教程 :doc:`（Python） <../../Tutorials/Intermediate/Tf2/Writing-A-Tf2-Broadcaster-Py>` :doc:`（C++） <../../Tutorials/Intermediate/Tf2/Writing-A-Tf2-Broadcaster-Cpp>` 以了解更多。

此外，tf2 还可以广播不会随时间变化的静态变换。
这主要节省存储和查询时间，也能减少发布开销。
你应该注意到，静态变换会发布一次，并且默认不会改变，因此不会保存历史记录。
如果你想在 tf2 树中定义静态变换，请查看“编写静态广播器”教程 :doc:`（Python） <../../Tutorials/Intermediate/Tf2/Writing-A-Tf2-Static-Broadcaster-Py>` :doc:`（C++） <../../Tutorials/Intermediate/Tf2/Writing-A-Tf2-Static-Broadcaster-Cpp>`。

你还可以在“添加坐标系”教程中了解如何向 tf2 树中添加固定帧和动态帧 :doc:`（Python） <../../Tutorials/Intermediate/Tf2/Adding-A-Frame-Py>` :doc:`（C++） <../../Tutorials/Intermediate/Tf2/Adding-A-Frame-Cpp>`。

当你完成基础教程后，就可以继续学习 tf2 与时间。
tf2 与时间教程 :doc:`（C++） <../../Tutorials/Intermediate/Tf2/Learning-About-Tf2-And-Time-Cpp>` 讲解了 tf2 与时间的基本原理。
关于 tf2 与时间的高级教程 :doc:`（C++） <../../Tutorials/Intermediate/Tf2/Time-Travel-With-Tf2-Cpp>` 讲解了使用 tf2 进行时间旅行的原理。

论文
----

有一篇关于 tf2 的论文发表于 TePRA 2013：`tf：变换库 <https://ieeexplore.ieee.org/abstract/document/6556373>`_。
