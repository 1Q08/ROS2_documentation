使用自定义的 Rosdistro 版本
===========================


.. contents:: Contents
    :depth: 2
    :local:


概述
----

`rosdistro <https://github.com/ros/rosdistro>`_ 包含所有发行版 ROS 软件包的中央索引，
以及用于安装打包二进制依赖的 ``rosdep`` 键。
当你调用 ``rosdep install ...`` 时，它会检查 rosdistro 的本地缓存索引
（在 ``rosdep update`` 期间填充），以将 ``package.xml`` 中的键关联到
要安装的 ROS 软件包、Python 模块或二进制文件。
因此，该索引是 ROS 生态的重要组成部分。

然而，有时用户希望对这一索引施加进一步的控制，
以加入他们自己的专有键，或者使用 rosdistro 的某个先前状态。
本指南将介绍如何设置系统上要使用的 rosdistro 版本。

本指南使用的动机示例是：由于你的开发计算机或持续集成
出现故障，你希望使用 Rolling 的某个先前版本。
有可能在从一个操作系统过渡到另一个操作系统的时期，
由于支持转移到新的操作系统（即从 Ubuntu 22.04 迁移到 24.04），
旧操作系统上的 Rolling 可能变得不可用。
因此，我们希望设置一个与给定操作系统上可正常工作的
Rolling 发行版相匹配的先前版本的 rosdistro，以便在升级到
新操作系统之前保持我们的系统正常运转。

重要的预备知识
--------------

默认情况下，Rosdep 会从 ``/etc/ros/rosdep/sources.list.d/20-default.list``
中设置的位置填充其缓存。
当使用 ``rosdep init`` 设置 rosdep 时，它会用主要的 rosdistro URL
（`来自此文件 <https://github.com/ros/rosdistro/blob/master/rosdep/sources.list.d/20-default.list>`_）填充 ``20-default.list``。
``rosdep update`` 生成的缓存位于 ``~/.ros/rosdep/sources.cache``，
不应手动修改。

当 rosdep update 期间未设置 ``ROSDISTRO_INDEX_URL`` 环境变量值时，
它会使用主要的公共 rosdistro 索引。
然而，当设置了该值时，你可以使用自定义的 rosdistro 索引，
它可以是公共索引的快照，也可以是填充了你专有软件包的完全独立的索引。

如果你想了解更多相关信息，请查看 `ros_buildfarm 软件包中的文档 <https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/custom_rosdistro.rst>`_。

如何使用自定义的 Rosdistro 版本
-------------------------------

要在你的 CI、docker 构建、本地环境、机器人或其他应用中使用
自定义版本，我们首先需要确定感兴趣的 rosdistro 版本。

对于我们的动机示例，我们希望使用新操作系统上第一次同步 ``rolling``
之前的最后一个索引状态。
在这种情况下，我们操作系统的最后一次同步是在 2024 年 2 月 28 日执行的。
方便的是，这些同步都打了标签，因此我们可以在
``rolling/2024-02-28`` 标签分支上获取该信息。

因此，我们需要用打标签的分支值更新 ``20-default.list``，
而不是使用主仓库的当前状态。
这可以通过如下脚本完成。
如果在本地主机上运行，你可能需要加上 ``sudo``。
这会把列表更新为使用我们的标签分支，而不是 master 分支。

.. code-block:: console

    $ sed -i "s|ros\/rosdistro\/master|ros\/rosdistro\/rolling\/2024-02-28|" /etc/ros/rosdep/sources.list.d/20-default.list

之后，我们现在必须更新环境变量 ``ROSDISTRO_INDEX_URL``，
使其指向我们新的 rosdistro 索引。

.. code-block:: console

    $ export ROSDISTRO_INDEX_URL=https://raw.githubusercontent.com/ros/rosdistro/rolling/2024-02-28/index-v4.yaml

如果你打算在本地主机上长期使用它，将其包含在 ``~/.bashrc`` 中
可能是明智之举，这样所有新终端都会自动执行此操作。
索引中的 ``v4`` 指向索引格式的新版本。
还存在一个不带 ``v4`` 的先前索引，它出于历史原因和旧系统而被保留，
但你不应该使用它。

之后，你可以执行 ``rosdep update``，现在它将使用这些更改，
按照 2024 年 2 月 28 日故障开始之前的 Rolling 发行版状态来更新索引。
你可以在 `Nav2 的 CircleCI <https://github.com/ros-planning/navigation2/commit/80bb5bff1488c0677efcc4254b7a89908c853ba0>`_ 和
`ros_gz 的 GitHub Actions <https://github.com/gazebosim/ros_gz/pull/522/files>`_ 中看到其实际应用，
它们以此绕过各自 CI 系统中临时的 Rolling 故障。

.. Note:: 如果你正在使用自定义的 rosdistro 版本，你可以用你的 fork 或索引位置替换默认列表和索引 URL 中的最终 URL。
