迁移软件包
==========

.. contents:: 目录
   :depth: 2
   :local:

软件包迁移分为两种不同的类型：

* 把现有软件包的源代码从 ROS 1 迁移到 ROS 2，并期望大部分源代码保持相同或至少相似。
  例如 `pluginlib <https://github.com/ros/pluginlib>`_，其源代码维护在同一仓库的不同分支中，必要时可以在这些分支之间移植通用的补丁。
* 为 ROS 2 实现与某个 ROS 1 软件包相同或相似的功能，但假设源代码会有显著差异。
  例如 ROS 1 中的 `roscpp <https://github.com/ros/ros_comm/tree/melodic-devel/clients/roscpp>`_ 和 ROS 2 中的 `rclcpp <https://github.com/ros2/rclcpp/tree/rolling/rclcpp>`_，它们是彼此独立的仓库，不共享任何代码。

前提条件
--------

在把 ROS 1 软件包迁移到 ROS 2 之前，必须先保证它的所有依赖项在 ROS 2 中可用。

package.xml 格式版本
--------------------

ROS 2 只支持 ``package.xml`` 格式版本 2 及更高版本。
如果你的软件包的 ``package.xml`` 使用的是格式 1，请参考 :doc:`Package.xml 格式 1 到 2 的迁移指南 <./Migrating-Package-XML>` 进行更新。

依赖项名称
----------

来自 :doc:`rosdep <../../Tutorials/Intermediate/Rosdep>` 的依赖项名称应该无需更改，因为它们在 ROS 1 和 ROS 2 中是共用的。

有些发布到 ROS 中的软件包在 ROS 2 中可能名称不同，因此依赖项可能需要相应地更新。

元软件包
--------

ROS 2 没有专门用于元软件包的软件包类型。
元软件包仍然可以作为只包含运行时依赖项的普通软件包存在。
从 ROS 1 迁移元软件包时，只需删除软件包清单中的 ``<metapackage />`` 标签。
关于元软件包/变体的更多信息，请参阅 :doc:`使用变体 <../Using-Variants>`。

许可证
------

在 ROS 1 中，我们推荐的许可证是 `3-Clause BSD License <https://opensource.org/licenses/BSD-3-Clause>`__。
在 ROS 2 中，我们推荐的许可证是 `Apache 2.0 License <https://www.apache.org/licenses/LICENSE-2.0>`__。

对于任何新项目，无论基于 ROS 1 还是 ROS 2，我们都推荐使用 Apache 2.0 许可证。

然而，在把代码从 ROS 1 迁移到 ROS 2 时，我们不能简单地更换许可证。
对于任何已有的贡献，必须保留原有的许可证。

因此，如果要迁移某个软件包，我们建议保留现有许可证，并继续以该软件包原有的 OSI 许可证（对于核心部分，我们认为应是 BSD 许可证）为其做贡献。

这样可以让事情保持清晰、易于理解。

更换许可证
^^^^^^^^^^

更换许可证是可行的，但你需要联系所有贡献者并获得许可。
对大多数软件包来说，这很可能是一项巨大的工程，并不值得考虑。
如果软件包的贡献者数量较少，那么这或许是可行的。
