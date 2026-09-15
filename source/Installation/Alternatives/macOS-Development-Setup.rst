.. _macOS-latest:

macOS（源码）
=============

.. contents:: 目录
   :depth: 2
   :local:

系统要求
--------

我们目前支持 macOS Mojave（10.14）。

安装前置依赖
------------

要构建 ROS 2，你需要安装以下内容：


#.
   **Xcode**

   * 如果你还没有安装它，请安装 `Xcode <https://apps.apple.com/app/xcode/id497799835>`_。
   * 注意：晚于 11.3.1 的 Xcode 版本已无法再安装到 macOS Mojave 上，因此你需要手动安装一个较旧的版本，参见：https://stackoverflow.com/a/61046761
   * 此外，如果你还没有安装命令行工具，请安装它：

     .. code-block:: console

        $ xcode-select --install
        $ sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer

   .. note::

      如果你是手动安装的 Xcode.app，你需要接受 Xcode.app 的许可协议。
      你可以通过打开 Xcode.app 或运行以下命令来完成：

      .. code-block:: console

         $ sudo xcodebuild -license

#.
   **brew** *(用于安装更多软件；你可能已经装了它)*：


   * 按照 http://brew.sh/ 的安装说明操作
   *
     *可选*：运行以下命令，检查 ``brew`` 对你的系统配置是否满意：

     .. code-block:: console

        $ brew doctor

     修复它指出的任何问题。

#.
   使用 ``brew`` 安装更多软件：

   .. code-block:: console

      $ brew install asio assimp bison bullet cmake console_bridge cppcheck \
         cunit eigen freetype graphviz opencv openssl orocos-kdl pcre poco \
         pyqt@5 python qt@5 sip spdlog osrf/simulation/tinyxml1 tinyxml2

#.
   设置一些环境变量：

   .. code-block:: console

      ~ 为 DDS-Security 添加 openssl 目录
      ~ 如果你使用 BASH，请将 '.zshrc' 替换为 '.bashrc'
      $ echo "export OPENSSL_ROOT_DIR=$(brew --prefix openssl)" >> ~/.zshrc

      ~ 将 Qt 目录添加到 PATH 和 CMAKE_PREFIX_PATH
      $ export CMAKE_PREFIX_PATH=$CMAKE_PREFIX_PATH:$(brew --prefix qt@5)
      $ export PATH=$PATH:$(brew --prefix qt@5)/bin

#.
   使用 ``python3 -m pip`` （仅用 ``pip`` 可能会安装 Python3 或 Python2）来安装更多软件：

   .. code-block:: console

      $ python3 -m pip install --upgrade pip

      $ python3 -m pip install -U \
        --config-settings="--global-option=build_ext" \
        --config-settings="--global-option=-I$(brew --prefix graphviz)/include/" \
        --config-settings="--global-option=-L$(brew --prefix graphviz)/lib/" \
        argcomplete catkin_pkg colcon-common-extensions coverage \
        cryptography empy flake8 flake8-blind-except==0.1.1 flake8-builtins \
        flake8-class-newline flake8-comprehensions flake8-deprecated \
        flake8-docstrings flake8-import-order flake8-quotes \
        importlib-metadata lark==1.1.1 lxml matplotlib mock mypy==0.931 netifaces \
        nose pep8 psutil pydocstyle pydot pygraphviz pyparsing==2.4.7 \
        pytest-mock rosdep rosdistro setuptools==59.6.0 vcstool

   请确保 ``$PATH`` 环境变量包含这些二进制文件的安装位置（``$(brew --prefix)/bin``）

#.
   *可选*：如果你想构建 ROS 1<->2 桥接，那么你还必须安装 ROS 1：


   * 从常规安装说明开始：http://wiki.ros.org/kinetic/Installation/OSX/Homebrew/Source
   *
     当你走到调用 ``rosinstall_generator`` 获取源码的那一步时，这里有一个替代调用方式，它只引入生成一个可用桥接所需的最小内容：

     .. code-block:: console

        $ rosinstall_generator catkin common_msgs roscpp rosmsg --rosdistro kinetic --deps --wet-only --tar > kinetic-ros2-bridge-deps.rosinstall
        $ wstool init -j8 src kinetic-ros2-bridge-deps.rosinstall


     否则，只需按照常规说明操作，然后在继续此处构建 ROS 2 之前，加载生成的 ``install_isolated/setup.bash``。

禁用系统完整性保护（SIP）
-------------------------

macOS/OS X 版本 >=10.11 默认启用了系统完整性保护。
为了让 SIP 不阻止进程继承动态链接器环境变量（例如 ``DYLD_LIBRARY_PATH``），你需要 `按照这些说明 <https://developer.apple.com/library/content/documentation/Security/Conceptual/System_Integrity_Protection_Guide/ConfiguringSystemIntegrityProtection/ConfiguringSystemIntegrityProtection.html>`__ 禁用它。

获取 ROS 2 代码
---------------

创建一个工作空间并克隆所有仓库：

.. code-block:: console

   $ mkdir -p ~/ros2_{DISTRO}/src
   $ cd ~/ros2_{DISTRO}
   $ vcs import --input https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos src

安装额外 DDS 厂商（可选）
-------------------------

如果你想使用除默认外的其他 DDS 或 RTPS 厂商，可以在此处找到说明：:doc:`这里 <../RMW-Implementations>`。

构建 ROS 2 代码
---------------

运行 ``colcon`` 工具来构建所有内容（关于使用 ``colcon`` 的更多信息见 :doc:`本教程 <../../Tutorials/Beginner-Client-Libraries/Colcon-Tutorial>`）：

.. code-block:: console

   $ cd ~/ros2_{DISTRO}/
   $ colcon build --symlink-install --packages-skip-by-dep python_qt_binding

注意：由于 SIP、Qt@5 和 PyQt5 之间存在一个未解决的问题，我们需要禁用 ``python_qt_binding`` 才能让构建成功。
待该问题解决后，此项将被移除，参见：https://github.com/ros-visualization/python_qt_binding/issues/103

环境配置
--------

加载 ROS 2 安装文件：

.. code-block:: console

   $ . ~/ros2_{DISTRO}/install/setup.zsh

这将自动为所有已构建支持的 DDS 厂商配置好环境。

尝试一些示例
------------

在一个终端中，按上文所述配置好 ROS 2 环境，然后运行 C++ 的 ``talker``：

.. code-block:: console

   $ ros2 run demo_nodes_cpp talker

在另一个终端中加载安装文件，然后运行 Python 的 ``listener``：

.. code-block:: console

   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 输出 ``Publishing`` 消息，而 ``listener`` 输出 ``I heard`` 这些消息。
这验证了 C++ 和 Python API 都能正常工作。
太棒了！

安装后的后续步骤
----------------
继续学习 `教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并了解 ROS 2 的核心概念。

使用 ROS 1 桥接
---------------
ROS 1 桥接可以将话题从 ROS 1 连接到 ROS 2，反之亦然。
请参阅关于如何构建和使用 ROS 1 桥接的专门 `文档 <https://github.com/ros2/ros1_bridge/blob/master/README.md>`__。

其他 RMW 实现（可选）
---------------------
ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在运行时替换。
请参阅关于如何使用多个 RMW 的 :doc:`指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。

保持最新
--------

请参阅 :doc:`../Maintaining-a-Source-Checkout`，以定期刷新你的源码安装。

故障排查
--------

故障排查技巧可以在 :ref:`这里 <macOS-troubleshooting>` 找到。

卸载
----

1. 如果你按上面的说明使用 colcon 安装工作空间，那么“卸载”可能只需打开一个新终端，并且不要加载该工作空间的 ``setup`` 文件。
   这样，你的环境就会表现得如同系统中没有安装 {DISTRO_TITLE}。

2. 如果你还想释放空间，可以用以下命令删除整个工作空间目录：

   .. code-block:: console

      $ rm -rf ~/ros2_{DISTRO}
