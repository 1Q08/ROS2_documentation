.. _Colcon:

.. redirect-from::

    Colcon-Tutorial
    Tutorials/Colcon-Tutorial

使用 ``colcon`` 构建包
======================

.. contents:: 目录
   :depth: 2
   :local:

**目标：** 使用 ``colcon`` 构建一个 ROS 2 工作空间。

**教程级别：** 入门

**时间：** 20 分钟

这是一个关于如何使用 ``colcon`` 创建和构建 ROS 2 工作空间的简短教程。
它是一个实用教程，并非旨在替代核心文档。

背景
----

``colcon`` 是 ROS 构建工具 ``catkin_make``、``catkin_make_isolated``、``catkin_tools`` 和 ``ament_tools`` 的迭代版本。
有关 colcon 设计的更多信息，请参阅 `此文档 <https://design.ros2.org/articles/build_tool.html>`__。

源代码可以在 `colcon GitHub 组织 <https://github.com/colcon>`__ 中找到。

前置条件
--------

安装 colcon
^^^^^^^^^^^

.. tabs::

  .. group-tab:: Ubuntu

    .. code-block:: console

        $ sudo apt install python3-colcon-common-extensions

  .. group-tab:: RHEL

    .. code-block:: console

        $ sudo dnf install python3-colcon-common-extensions

  .. group-tab:: macOS

    .. code-block:: console

        $ python3 -m pip install colcon-common-extensions

  .. group-tab:: Windows

    .. code-block:: console

        $ pip install -U colcon-common-extensions


安装 ROS 2
^^^^^^^^^^

要构建示例，你需要安装 ROS 2。

请遵循 :doc:`安装说明 <../../Installation>`。

.. attention:: 如果通过 deb 包安装，本教程需要 :ref:`桌面安装 <linux-install-debs-install-ros-2-packages>`。

基础
----

ROS 工作空间是一个具有特定结构的目录。
通常有一个 ``src`` 子目录。
该子目录是 ROS 包源代码的存放位置。
通常该目录初始为空。

colcon 执行源外构建（out-of-source builds）。
默认情况下，它会在 ``src`` 目录的同级创建以下目录：

* ``build`` 目录用于存放中间文件。
  每个包都会在其中创建一个子文件夹，例如 CMake 就是在这里被调用的。
* ``install`` 目录是每个包被安装的位置。
  默认情况下，每个包都会被安装到单独的子目录中。
* ``log`` 目录包含每次 colcon 调用的各种日志信息。

.. note:: 与 catkin 相比，这里没有 ``devel`` 目录。

创建工作空间
^^^^^^^^^^^^

首先，创建一个目录（``ros2_ws``）来容纳我们的工作空间：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

       $ mkdir -p ~/ros2_ws/src
       $ cd ~/ros2_ws

  .. group-tab:: macOS

    .. code-block:: console

       $ mkdir -p ~/ros2_ws/src
       $ cd ~/ros2_ws

  .. group-tab:: Windows

    .. code-block:: console

       $ md \dev\ros2_ws\src
       $ cd \dev\ros2_ws

此时工作空间只包含一个空的 ``src`` 目录：

添加一些源代码
^^^^^^^^^^^^^^

让我们将 `examples <https://github.com/ros2/examples>`__ 仓库克隆到工作空间的 ``src`` 目录中：

.. code-block:: console

    $ git clone https://github.com/ros2/examples src/examples -b {REPOS_FILE_BRANCH}

现在工作空间应该包含 ROS 2 示例的源代码：

.. code-block:: bash

    .
    └── src
        └── examples
            ├── CONTRIBUTING.md
            ├── LICENSE
            ├── rclcpp
            ├── rclpy
            └── README.md

    4 directories, 3 files

导入一个 underlay
^^^^^^^^^^^^^^^^^

重要的是，我们需要为现有的 ROS 2 安装导入环境，它将为示例包提供工作空间所需的构建依赖。
这是通过导入由二进制安装或源码安装提供的 setup 脚本来实现的，即另一个 colcon 工作空间（参见 :doc:`Installation <../../Installation>`）。
我们称这个环境为 **underlay**。

我们的工作空间 ``ros2_ws`` 将是现有 ROS 2 安装之上的一个 **overlay**。
通常，当你计划只对少量包进行迭代时，建议使用 overlay，而不是将所有包都放在同一个工作空间中。

构建工作空间
^^^^^^^^^^^^

.. attention::

   在 Windows 上构建包时，你需要处于 Visual Studio 环境中，详情请参阅 :ref:`构建 ROS 2 代码 <windows-dev-build-ros2>`。

在工作空间根目录下运行 ``colcon build``。
由于 ``ament_cmake`` 等构建类型不支持 ``devel`` 空间的概念，并且要求安装该包，因此 colcon 支持 ``--symlink-install`` 选项。
它允许通过修改 ``source`` 空间中的文件（例如 Python 文件或其他非编译资源）来改变已安装的文件，以便更快地迭代。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --symlink-install

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --symlink-install

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install

    Windows 不允许长路径，因此 ``merge-install`` 会将所有路径合并到 ``install`` 目录中。
    在 Windows 上，创建符号链接需要特殊权限，因此默认不使用 ``--symlink-install``。
    要使用它，你需要以管理员身份运行命令，或在系统设置中启用开发者模式。

.. tip::

   运行 ``colcon build`` 可能会使 CPU、内存和 I/O 受限的系统（如树莓派）出现屏幕和鼠标冻结，因此使用 ``--executor sequential`` 参数逐个构建包（而不是并行）可能会有所帮助。
   如需更多参数，请参阅 `colcon 文档 <https://colcon.readthedocs.io/en/released/reference/executor-arguments.html>`_。

构建完成后，我们应该看到 ``build``、``install`` 和 ``log`` 目录：

.. code-block:: bash

    .
    ├── build
    ├── install
    ├── log
    └── src

    4 directories, 0 files

.. _colcon-run-the-tests:

运行测试
^^^^^^^^

要运行我们刚构建的包的测试，请运行以下命令：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon test

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon test

  .. group-tab:: Windows

    请记住，执行以下命令时需要使用 ``x64 Native Tools Command Prompt for VS 2019``，因为我们要构建一个工作空间。

    .. code-block:: console

      $ colcon test --merge-install

    由于上面构建时使用了 ``--merge-install``，这里也需要指定它。

.. _colcon-tutorial-source-the-environment:

导入环境
^^^^^^^^

当 colcon 成功完成构建后，输出将位于 ``install`` 目录中。
在使用任何已安装的可执行文件或库之前，你需要将它们添加到路径和库路径中。
colcon 会在 ``install`` 目录中生成 bash/bat 文件来帮助设置环境。
这些文件会将所有必需的元素添加到你的路径和库路径中，并提供包导出的任何 bash 或 shell 命令。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

       $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

       $ . install/setup.bash

  .. group-tab:: Windows

    在 Windows 命令行界面中：

    .. code-block:: console

       $ call install\setup.bat

    或使用 Powershell：

    .. code-block:: console

       $ install\setup.ps1

尝试一个演示
^^^^^^^^^^^^

导入环境后，我们可以运行由 colcon 构建的可执行文件。
让我们从示例中运行一个订阅者节点：

.. code-block:: console

    $ ros2 run examples_rclcpp_minimal_subscriber subscriber_member_function

在另一个终端中，让我们运行一个发布者节点（别忘了导入 setup 脚本）：

.. code-block:: console

    $ ros2 run examples_rclcpp_minimal_publisher publisher_member_function

你应该会看到来自发布者和订阅者的消息，数字在不断递增。

创建你自己的包
--------------

colcon 使用 `REP 149 <https://reps.openrobotics.org/rep-0149/>`__ 中定义的 ``package.xml`` 规范（同时也支持 `format 2 <https://reps.openrobotics.org/rep-0140/>`__）。

colcon 支持多种构建类型。
推荐的构建类型是 ``ament_cmake`` 和 ``ament_python``。
也支持纯 ``cmake`` 包。

``ament_python`` 构建的一个示例是 `ament_index_python 包 <https://github.com/ament/ament_index/tree/{REPOS_FILE_BRANCH}/ament_index_python>`__，其中 setup.py 是构建的主要入口点。

像 `demo_nodes_cpp <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/demo_nodes_cpp>`__ 这样的包使用 ``ament_cmake`` 构建类型，并使用 CMake 作为构建工具。

为方便起见，你可以使用 ``ros2 pkg create`` 工具基于模板创建新包。
有关创建包以及如何使用 ``ros2 pkg create`` 的完整说明，请参阅后续教程 :doc:`创建包 <./Creating-Your-First-ROS2-Package>`。

.. note:: 对于 ``catkin`` 用户来说，这相当于 ``catkin_create_package``。

设置 ``colcon_cd``
------------------

``colcon_cd`` 命令允许你快速将当前 shell 的工作目录切换到某个包的目录。
例如，``colcon_cd some_ros_package`` 会快速将你带到 ``~/ros2_ws/src/some_ros_package`` 目录。
要设置 ``colcon_cd``，你需要运行以下命令来修改你的 shell 启动脚本：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc
        $ echo "export _colcon_cd_root=/opt/ros/{DISTRO}/" >> ~/.bashrc

   .. group-tab:: macOS

      .. code-block:: console

        $ echo "source /usr/local/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc
        $ echo "export _colcon_cd_root=~/ros2_install" >> ~/.bashrc

   .. group-tab:: Windows

      尚不可用

根据你安装 ``colcon_cd`` 的方式以及工作空间的位置，上述说明可能会有所不同，请参阅 `文档 <https://colcon.readthedocs.io/en/released/user/installation.html#quick-directory-changes>`__ 了解更多详情。
要在 Linux 和 macOS 中撤销此操作，请找到系统的 shell 启动脚本并删除追加的 source 和 export 命令。

设置 ``colcon`` 补全
--------------------

``colcon`` 命令支持 bash 及类 bash shell 的命令补全。
必须安装 ``colcon-argcomplete`` 包，并且可能需要进行 `一些设置 <https://colcon.readthedocs.io/en/released/user/installation.html#enable-completion>`__ 才能使其生效。

提示
----

* 如果你不想构建某个特定的包，请在该目录中放置一个名为 ``COLCON_IGNORE`` 的空文件，它就不会被索引。

* 如果你想避免在 CMake 包中配置和构建测试，可以传入：``--cmake-args -DBUILD_TESTING=0``。

* 如果你想运行某个包中的某个特定测试：

  .. code-block:: console

     $ colcon test --packages-select YOUR_PKG_NAME --ctest-args -R YOUR_TEST_IN_PKG

设置 ``colcon`` mixins
----------------------

各种命令行选项写起来繁琐，而且/或者难以记忆。

例如，要将 CMake 构建类型改为 debug，通常使用：

.. code-block:: console

    $ colcon build --cmake-args -DCMAKE_BUILD_TYPE=Debug

为了使常用的命令行选项更容易调用，本仓库提供了这些“快捷方式”。

要安装默认的 colcon mixins，请运行以下命令：

.. code-block:: console

    $ colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml
    $ colcon mixin update default

然后，尝试使用 ``debug`` mixin：

.. code-block:: console

    $ colcon build --mixin debug

更多详情，请参阅 `colcon mixin 仓库 <https://github.com/colcon/colcon-mixin-repository>`__。
