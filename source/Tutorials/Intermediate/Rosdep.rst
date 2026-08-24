.. redirect-from::

    Tutorials/Rosdep

使用 rosdep 管理依赖
====================

.. contents:: 目录
   :depth: 2
   :local:

**目标：** 使用 ``rosdep`` 管理外部依赖。

**教程级别：** 中级

**时间：** 5 分钟

本教程将解释如何使用 ``rosdep`` 管理外部依赖。

.. warning::

   目前 rosdep 仅在 Linux 和 macOS 上可用；不支持 Windows。
   长期计划是为 https://github.com/ros-infrastructure/rosdep 添加对 Windows 的支持。

什么是 rosdep？
---------------

``rosdep`` 是一个依赖管理工具，可以与软件包和外部库协同工作。
它是一个命令行工具，用于识别和安装依赖以构建或安装软件包。
``rosdep`` 本身 *不是* 一个包管理器；它是一个元包管理器，利用自身对系统和依赖的了解，在特定平台上找到合适的软件包进行安装。
实际安装由系统包管理器完成（例如 Debian/Ubuntu 上的 ``apt``、Fedora/RHEL 上的 ``dnf`` 等）。

它最常在构建工作空间之前调用，用于安装该工作空间内软件包的依赖项。

它既可以对单个软件包工作，也可以对一个软件包目录（例如工作空间）工作。

.. note::

   尽管名称暗示它是用于 ROS 的，``rosdep`` 对 ROS 是半无关的。
   你可以通过将其作为独立 Python 软件包安装，在非 ROS 软件项目中使用这一强大工具。
   成功运行 ``rosdep`` 依赖于 ``rosdep keys`` 可用，这些 keys 可以通过几条简单命令从公共 git 仓库下载。

关于 package.xml 文件
---------------------

``package.xml`` 是你的软件中 ``rosdep`` 查找依赖集的文件。
重要的是，``package.xml`` 中的依赖列表要完整且正确，这使所有工具能够确定软件包的依赖。
缺失或不正确的依赖可能导致用户无法使用你的软件包、工作空间中的软件包构建顺序错乱，以及软件包无法发布。

``package.xml`` 文件中的依赖通常被称为“rosdep keys”。
这些依赖由软件包创建者手动填写到 ``package.xml`` 文件中，应是对其所需的任何非内置库和软件包的详尽列表。

它们在以下标签中表示（完整规范见 `REP-149 <https://reps.openrobotics.org/rep-0149/>`__）：

``<depend>``
^^^^^^^^^^^^

这些是应在软件包的构建时和运行时都提供的依赖。
对于 C++ 软件包，如有疑问，请使用此标签。
纯 Python 软件包通常没有构建阶段，因此永远不应使用此标签，而应改用 ``<exec_depend>``。

``<build_depend>``
^^^^^^^^^^^^^^^^^^

如果你仅在构建软件包时使用某个依赖，而在执行时不用，你可以使用 ``<build_depend>`` 标签。

对于这种类型的依赖，你软件包的已安装二进制文件不需要安装该特定软件包。

但是，如果你的软件包导出的头文件包含来自该依赖的头文件，这可能会造成问题。
在这种情况下，你还需要一个 ``<build_export_depend>``。

``<build_export_depend>``
^^^^^^^^^^^^^^^^^^^^^^^^^

如果你导出的头文件包含来自某个依赖的头文件，那么 ``<build_depend>`` 于你软件包的其他软件包将需要它。
这主要适用于头文件和 CMake 配置文件。
你所导出的库引用的库软件包通常应指定 ``<depend>``，因为它们在执行时也需要。

``<exec_depend>``
^^^^^^^^^^^^^^^^^

此标签声明运行你的软件包时所需的共享库、可执行文件、Python 模块、launch 脚本和其他文件的依赖。

``<test_depend>``
^^^^^^^^^^^^^^^^^

此标签声明仅测试所需的依赖。
此处的依赖 *不应* 与 ``<build_depend>``、``<exec_depend>`` 或 ``<depend>`` 指定的 keys 重复。

rosdep 如何工作？
-----------------

``rosdep`` 会检查其路径中或特定软件包中的 ``package.xml`` 文件，并找到其中存储的 rosdep keys。
然后这些 keys 会与中央索引交叉引用，以在各种包管理器中找到合适的 ROS 软件包或软件库。
最后，一旦找到这些软件包，它们就被安装并可以使用了！

``rosdep`` 通过将中央索引检索到你的本地机器来工作，这样每次运行时就不必访问网络（在 Debian/Ubuntu 上，其配置存储在 ``/etc/ros/rosdep/sources.list.d/20-default.list``）。

中央索引被称为 ``rosdistro``，`可以在线找到 <https://github.com/ros/rosdistro>`_。
我们将在下一节进一步探讨它。

我如何知道要在我的 package.xml 中放哪些 keys？
----------------------------------------------

好问题，很高兴你问了！

* 如果你想依赖的软件包是基于 ROS 的，并且已发布到 ROS 生态系统中 [1]_，例如 ``nav2_bt_navigator``，你可以直接使用该软件包的名称。
  你可以在 https://github.com/ros/rosdistro 的 ``<distro>/distribution.yaml``（例如 ``humble/distribution.yaml``）中找到你给定 ROS 发行版的所有已发布 ROS 软件包列表。
* 如果你想依赖一个非 ROS 软件包，通常称为“系统依赖”，你需要为特定库找到 keys。
  一般来说，有两个相关的文件：

  * `rosdep/base.yaml <https://github.com/ros/rosdistro/blob/master/rosdep/base.yaml>`_ 包含 ``apt`` 系统依赖
  * `rosdep/python.yaml <https://github.com/ros/rosdistro/blob/master/rosdep/python.yaml>`_ 包含 Python 依赖

要找到 key，请在这些文件中搜索你的库并找到名称。
这就是要放入 ``package.xml`` 文件的 key。

例如，假设一个软件包依赖 ``doxygen``，因为它是一款关心优质文档的优秀软件（提示提示）。
我们会在 ``rosdep/base.yaml`` 中搜索 ``doxygen`` 并找到：

.. code-block:: yaml

  doxygen:
    arch: [doxygen]
    debian: [doxygen]
    fedora: [doxygen]
    freebsd: [doxygen]
    gentoo: [app-doc/doxygen]
    macports: [doxygen]
    nixos: [doxygen]
    openembedded: [doxygen@meta-oe]
    opensuse: [doxygen]
    rhel: [doxygen]
    ubuntu: [doxygen]

这意味着我们的 rosdep key 是 ``doxygen``，它将在不同操作系统的包管理器中解析为那些不同的名称以进行安装。

如果我的库不在 rosdistro 中怎么办？
-----------------------------------

如果你的库不在 ``rosdistro`` 中，你可以体验开源软件开发的伟大之处：你可以自己添加它！
针对 rosdistro 的 pull request 通常在一周内就会被合并。

`有关如何贡献新的 rosdep keys 的详细说明可在此处找到 <https://github.com/ros/rosdistro/blob/master/CONTRIBUTING.md#rosdep-rules-contributions>`_。
如果出于某种原因这些无法公开贡献，还有其他选择：

1. fork rosdistro 并维护一个包含额外 keys 的备用索引 (:doc:`../../How-To-Guides/Using-Custom-Rosdistro`)
2. 创建一个包含自定义 keys 的新文件，并指示 ``rosdep`` 在填充本地索引时检查它 (:doc:`../Advanced/Supplementing-Custom-Rosdep-Keys`)

我如何使用 rosdep 工具？
------------------------

rosdep 安装
^^^^^^^^^^^

如果你将 ``rosdep`` 与 ROS 一起使用，它会方便地随 ROS 发行版一起打包。
这是获取 ``rosdep`` 的推荐方式。
你可以通过以下命令安装它：

.. tabs::

  .. group-tab:: Ubuntu

    .. code-block:: console

        $ sudo apt install python3-rosdep

  .. group-tab:: RHEL

    .. code-block:: console

        $ sudo dnf install python3-rosdep

.. note::

    在 Debian 和 Ubuntu 上，还有另一个名称相似的软件包，叫做 ``python3-rosdep2``。
    如果安装了该软件包，请务必在安装 ``python3-rosdep`` 之前将其删除。

如果你在 ROS 之外使用 ``rosdep``，系统软件包可能不可用。
在这种情况下，你可以直接从 https://pypi.org 安装它：

.. code-block:: console

    $ pip install rosdep

rosdep 操作
^^^^^^^^^^^

既然我们对 ``rosdep``、``package.xml`` 和 ``rosdistro`` 有了一些了解，我们就准备使用该工具本身了！
首先，如果这是第一次使用 ``rosdep``，必须通过以下命令初始化：

.. code-block:: console

    $ sudo rosdep init
    $ rosdep update

这将初始化 rosdep，``update`` 将更新本地缓存的 rosdistro 索引。
偶尔 ``update`` 一下 rosdep 以获取最新索引是个好主意。

最后，我们可以运行 ``rosdep install`` 来安装依赖。
通常，这是在一个包含许多软件包的工作空间上通过单次调用运行，以安装所有依赖。
如果位于工作空间根目录且 ``src`` 目录包含源代码，该调用如下所示。

.. code-block:: console

    $ rosdep install --from-paths src -y --ignore-src

拆解如下：

- ``--from-paths src`` 指定检查 ``package.xml`` 文件以解析 keys 的路径
- ``-y`` 表示对包管理器的所有提示默认回答 yes，以便无提示安装
- ``--ignore-src`` 表示即使存在 rosdep key，如果软件包本身也在工作空间中，也忽略安装依赖。

还有其他可用的参数和选项。
使用 ``rosdep -h`` 查看它们，或查阅 http://docs.ros.org/en/independent/api/rosdep/html/ 上更完整的 rosdep 文档。

.. [1] “已发布到 ROS 生态系统” 意味着该软件包被列在 `rosdistro 数据库 <https://github.com/ros/rosdistro>`_ 中的一个或多个 ``<distro>/distribution.yaml`` 目录中。
