.. redirect-from::

  Installation/Rolling/OSX-Development-Setup
  Installation/macOS-Development-Setup

macOS（源代码）
===============

.. contents:: 目录
   :depth: 2
   :local:

系统要求
--------

我们目前支持 macOS Mojave (10.14)。

系统设置
--------

安装前置条件
^^^^^^^^^^^^

你需要安装以下内容来构建 ROS 2：


#.
   **Xcode**

   * 如果你尚未安装它，请安装 `Xcode <https://apps.apple.com/app/xcode/id497799835>`_。
   * 注意：高于 11.3.1 版本的 Xcode 无法再安装到 macOS Mojave 上，因此你需要手动安装旧版本，参见：https://stackoverflow.com/a/61046761
   * 另外，如果你尚未安装命令行工具，请安装它：

     .. code-block:: console

        $ xcode-select --install
        $ sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer

   .. note::

      如果你手动安装了 Xcode.app，你需要接受 Xcode.app 的许可证。
      你可以通过打开 Xcode.app 或运行以下命令来完成：

      .. code-block:: console

         $ sudo xcodebuild -license

#.
   **brew** *（用于安装更多内容；你可能已经有了）*：


   * 按照 http://brew.sh/ 上的安装说明进行安装
   *
     *可选*：通过运行以下命令检查 ``brew`` 是否对你的系统配置满意：

     .. code-block:: console

        $ brew doctor

     修复它发现的任何问题。

#.
   使用 ``brew`` 安装更多内容：

   .. code-block:: console

      $ brew install asio assimp bison bullet cmake console_bridge cppcheck \
        cunit eigen freetype graphviz opencv openssl orocos-kdl pcre poco \
        pyqt@5 python qt@5 sip spdlog tinyxml2

#.
   设置一些环境变量：

   .. code-block:: console

      ~ Add the openssl dir for DDS-Security
      ~ if you are using BASH, then replace '.zshrc' with '.bashrc'
      $ echo "export OPENSSL_ROOT_DIR=$(brew --prefix openssl)" >> ~/.zshrc

      ~ Add the Qt directory to the PATH and CMAKE_PREFIX_PATH
      $ export CMAKE_PREFIX_PATH=$CMAKE_PREFIX_PATH:$(brew --prefix qt@5)
      $ export PATH=$PATH:$(brew --prefix qt@5)/bin

#.
   使用 ``python3 -m pip``\ （仅 ``pip`` 可能安装 Python3 或 Python2）来安装更多内容：

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
        importlib-metadata jsonschema lark==1.1.1 lxml matplotlib mock mypy==0.931 netifaces \
        nose pep8 psutil pydocstyle pydot pygraphviz pyparsing==2.4.7 \
        pytest-mock rosdep rosdistro setuptools==59.6.0 vcstool

   请确保 ``$PATH`` 环境变量包含二进制文件的安装位置（``$(brew --prefix)/bin``）

#.
   *可选*：如果你想构建 ROS 1<->2 桥接，那么你还必须安装 ROS 1：


   * 从正常的安装说明开始：http://wiki.ros.org/kinetic/Installation/OSX/Homebrew/Source
   *
     当你进行到调用 ``rosinstall_generator`` 获取源代码的步骤时，这里有一个替代调用，它只引入生成可用桥接所需的最少内容：

     .. code-block:: console

        $ rosinstall_generator catkin common_msgs roscpp rosmsg --rosdistro kinetic --deps --wet-only --tar > kinetic-ros2-bridge-deps.rosinstall
        $ wstool init -j8 src kinetic-ros2-bridge-deps.rosinstall


     否则，只需按照正常说明操作，然后在继续此处构建 ROS 2 之前 source 生成的 ``install_isolated/setup.bash``。

禁用系统完整性保护（SIP）
^^^^^^^^^^^^^^^^^^^^^^^^^

macOS/OS X 版本 >=10.11 默认启用了系统完整性保护（System Integrity Protection）。
为了不让 SIP 阻止进程继承动态链接器环境变量（例如 ``DYLD_LIBRARY_PATH``），你需要 `按照这些说明 <https://developer.apple.com/library/content/documentation/Security/Conceptual/System_Integrity_Protection_Guide/ConfiguringSystemIntegrityProtection/ConfiguringSystemIntegrityProtection.html>`__ 禁用它。

构建 ROS 2
----------

获取 ROS 2 代码
^^^^^^^^^^^^^^^

创建工作空间并克隆所有仓库：

.. code-block:: console

   $ mkdir -p ~/ros2_{DISTRO}/src
   $ cd ~/ros2_{DISTRO}
   $ vcs import --input https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos src

安装额外的 RMW 实现（可选）
^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在构建时或运行时替换。
关于如何使用多种 RMW，请参见 :doc:`指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。

构建工作空间中的代码
^^^^^^^^^^^^^^^^^^^^

运行 ``colcon`` 工具来构建所有内容（有关使用 ``colcon`` 的更多信息，请参见 :doc:`本教程 <../../Tutorials/Beginner-Client-Libraries/Colcon-Tutorial>`）：

.. code-block:: console

   $ cd ~/ros2_{DISTRO}/
   $ colcon build --symlink-install --packages-skip-by-dep python_qt_binding

注意：由于 SIP、Qt@5 和 PyQt5 存在一个未解决的问题，我们需要禁用 ``python_qt_binding`` 才能使构建成功。
该问题解决后，此限制将被移除，参见：https://github.com/ros-visualization/python_qt_binding/issues/103

设置环境
--------

source ROS 2 设置文件：

.. code-block:: console

   $ . ~/ros2_{DISTRO}/install/setup.zsh

这将自动为已构建支持的所有 DDS 供应商设置环境。

尝试一些示例
------------

在一个终端中，按上述方式设置 ROS 2 环境，然后运行一个 C++ ``talker``：

.. code-block:: console

   $ ros2 run demo_nodes_cpp talker

在另一个终端中 source 设置文件，然后运行一个 Python ``listener``：

.. code-block:: console

   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 显示它正在 ``Publishing`` 消息，而 ``listener`` 显示 ``I heard`` 那些消息。
这验证了 C++ 和 Python API 都正常工作。
太棒了！

后续步骤
--------

继续学习 `教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并学习 ROS 2 核心概念。

使用 ROS 1 桥接（可选）
-----------------------

ROS 1 桥接可以将话题从 ROS 1 连接到 ROS 2，反之亦然。
关于如何构建和使用 ROS 1 桥接，请参见专门的 `文档 <https://github.com/ros2/ros1_bridge/blob/master/README.md>`__。

保持最新
--------

参见 :doc:`../Maintaining-a-Source-Checkout` 以定期刷新你的源代码安装。

故障排查
--------

故障排查技巧可参见 :ref:`此处 <macOS-troubleshooting>`。

卸载
----

1. 如果你按照上述说明使用 colcon 安装了工作空间，那么"卸载"可能只是打开一个新终端并且不 source 工作空间的 ``setup`` 文件即可。
   这样，你的环境将表现得就像系统中没有安装 {DISTRO_TITLE} 一样。

2. 如果你还想释放空间，可以删除整个工作空间目录：

   .. code-block:: console

      $ rm -rf ~/ros2_{DISTRO}
