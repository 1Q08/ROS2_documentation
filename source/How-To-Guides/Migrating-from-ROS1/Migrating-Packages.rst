迁移软件包
==========

.. contents:: 目录
   :depth: 2
   :local:

软件包迁移有两种不同的类型：

* 将现有软件包的源代码从 ROS 1 迁移到 ROS 2，其意图是源代码的
  很大一部分将保持不变或至少相似。
  一个例子是 `pluginlib <https://github.com/ros/pluginlib>`_，
  它的源代码在同一仓库的不同分支中维护，
  必要时可以在这些分支之间移植通用的补丁。
* 为 ROS 2 实现与 ROS 1 软件包相同或相似的功能，
  但假设源代码将有很大不同。
  一个例子是 ROS 1 中的 `roscpp <https://github.com/ros/ros_comm/tree/melodic-devel/clients/roscpp>`_
  和 ROS 2 中的 `rclcpp <https://github.com/ros2/rclcpp/tree/rolling/rclcpp>`_，
  它们是独立的仓库，不共享任何代码。

前提条件
--------

在能够将 ROS 1 软件包迁移到 ROS 2 之前，它的所有依赖
都必须已经在 ROS 2 中可用。

Package.xml 格式版本
--------------------

ROS 2 仅支持 ``package.xml`` 格式版本 2 及更高版本。
如果你的软件包的 ``package.xml`` 使用格式 1，
请使用 :doc:`Package.xml 格式 1 到 2 迁移指南 <./Migrating-Package-XML>` 更新它。

依赖名称
--------

来自 :doc:`rosdep <../../Tutorials/Intermediate/Rosdep>` 的依赖名称应该不需要更改，
因为这些名称在 ROS 1 和 ROS 2 之间是共享的。

一些发布到 ROS 中的软件包在 ROS 2 中可能有不同的名称，
因此依赖项可能需要相应地更新。

元包
----

ROS 2 没有针对元包的特定软件包类型。
元包仍然可以作为仅包含运行时依赖的普通软件包存在。
从 ROS 1 迁移元包时，只需移除软件包清单中的 ``<metapackage />`` 标签即可。
有关元包/变体的更多信息，请参见 :doc:`使用变体 <../Using-Variants>`。

许可协议
--------

在 ROS 1 中，我们推荐的许可是
`3-Clause BSD License <https://opensource.org/licenses/BSD-3-Clause>`__。
在 ROS 2 中，我们推荐的许可是
`Apache 2.0 License <https://www.apache.org/licenses/LICENSE-2.0>`__。

对于任何新项目，无论是 ROS 1 还是 ROS 2，我们都推荐使用 Apache 2.0 许可。

然而，在将代码从 ROS 1 迁移到 ROS 2 时，我们不能简单地更改许可。
对于任何预先存在的贡献，必须保留现有的许可。

为此，如果要迁移某个软件包，我们建议保留现有的许可，
并在现有的 OSI 许可下继续为该软件包做贡献，
对于核心元素，我们预期是 BSD 许可。

这将使事情保持清晰且易于理解。

更改许可协议
^^^^^^^^^^^^

更改许可是可能的，但你需要联系所有贡献者并获得许可。
对于大多数软件包来说，这可能是一项巨大的工作，不值得考虑。
如果软件包的贡献者人数很少，那么这或许是可行的。
