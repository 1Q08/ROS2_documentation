使用自定义 Rosdistro 版本
=========================


.. contents:: 目录
    :depth: 2
    :local:


概述
----

`rosdistro <https://github.com/ros/rosdistro>`_ 包含了所有发行版的 ROS 软件包中央索引，以及用于安装打包的二进制依赖项的 ``rosdep`` 键。
当你调用 ``rosdep install ...`` 时，它会检查来自 rosdistro 的本地缓存索引（在 ``rosdep update`` 期间填充），以将 ``package.xml`` 中的键关联到要安装的 ROS 软件包、python 模块或二进制文件。
因此，该索引是 ROS 生态系统中一个重要的组成部分。

然而，有时用户希望对这一索引施加进一步的控制，以加入自己的专有键，或使用 rosdistro 的先前状态。
本指南将逐步介绍如何设置要在你的系统上使用的 rosdistro 版本。

本指南将采用的动机示例是：由于你的开发计算机或持续集成出现故障，你希望使用 Rolling 的先前版本。
在从一个操作系统过渡到另一个操作系统的期间，较旧操作系统上的 Rolling 可能因支持转移到新操作系统（即从 Ubuntu 22.04 转移到 24.04）而变得不可用。
因此，我们希望在升级到新操作系统之前，设置一个与给定操作系统上可正常工作的 Rolling 发行版相匹配的先前 rosdistro 版本，以保持系统正常运行。

重要预备知识
------------

Rosdep 默认从其 ``/etc/ros/rosdep/sources.list.d/20-default.list`` 中设置的位置填充其缓存。
在使用 ``rosdep init`` 设置 rosdep 时，它会用主要的 rosdistro URL（`来自此文件 <https://github.com/ros/rosdistro/blob/master/rosdep/sources.list.d/20-default.list>`_）填充 ``20-default.list``。
由 ``rosdep update`` 生成的缓存位于 ``~/.ros/rosdep/sources.cache``，不应手动修改。

当 rosdep 更新期间未设置 ``ROSDISTRO_INDEX_URL`` 环境变量值时，它会使用主要的公共 rosdistro 索引。
然而，当设置了该值时，你可以使用自定义的 rosdistro 索引，它可以是公共索引的快照，也可以是包含你专有软件包的完全独立的索引。

如果你想了解更多相关内容，请查阅 `ros_buildfarm 软件包中的文档 <https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/custom_rosdistro.rst>`_。

如何使用自定义 Rosdistro 版本
-----------------------------

要在你的 CI、docker 构建、本地环境、机器人或其他应用中使用自定义版本，我们首先需要确定感兴趣的 rosdistro 版本。

对于我们的动机示例，我们希望使用 ``rolling`` 在新操作系统上首次同步之前的最后一个索引状态。
在本例中，我们操作系统的最后一次同步执行于 2024 年 2 月 28 日。
幸运的是，这些同步带有标签，因此我们可以在 ``rolling/2024-02-28`` 标签分支上获取该信息。

因此，我们需要用带标签分支的值来更新 ``20-default.list``，而不是使用主仓库的当前状态。
这可以通过如下脚本完成。
如果在本地主机上运行，你可能需要加上 ``sudo``。
这会将列表更新为使用我们带标签的分支，而不是 master 分支。

.. code-block:: console

    $ sed -i "s|ros\/rosdistro\/master|ros\/rosdistro\/rolling\/2024-02-28|" /etc/ros/rosdep/sources.list.d/20-default.list

之后，我们必须更新环境变量 ``ROSDISTRO_INDEX_URL`` 以指向我们新的 rosdistro 索引。

.. code-block:: console

    $ export ROSDISTRO_INDEX_URL=https://raw.githubusercontent.com/ros/rosdistro/rolling/2024-02-28/index-v4.yaml

如果你打算在本地主机上长期使用它，那么将其加入你的 ``~/.bashrc`` 可能是明智之举，这样所有新终端都会自动执行此操作。
我们索引中的 ``v4`` 指向索引格式的新版本。
还存在一个不带 ``v4`` 的先前索引，出于历史原因和遗留系统仍然保留，但你不应使用它。

之后，你可以执行 ``rosdep update``，它现在将根据 Rolling 发行版在 2024 年 2 月 28 日（故障开始之前）的状态，利用这些更改来更新索引。
你可以在 `Nav2 的 CircleCI <https://github.com/ros-planning/navigation2/commit/80bb5bff1488c0677efcc4254b7a89908c853ba0>`_ 和 `ros_gz 的 GitHub Actions <https://github.com/gazebosim/ros_gz/pull/522/files>`_ 中看到它的实际应用，它们借此绕过了其 CI 系统中临时性的 Rolling 中断。

.. Note:: 如果你使用的是自定义 rosdistro 版本，你可以将默认列表和索引 URL 中的最终 URL 替换为你的 fork 或索引位置。
