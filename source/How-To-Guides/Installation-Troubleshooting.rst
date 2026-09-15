.. redirect-from::

  Guides/Installation-Troubleshooting
  Troubleshooting/Installation-Troubleshooting

安装故障排查
============

安装故障排查技巧按其适用的平台进行分类。

.. contents:: 平台
   :depth: 2
   :local:

通用
----

通用故障排查技巧适用于所有平台。

启用多播
^^^^^^^^

为了通过 DDS 成功通信，所使用的网络接口必须启用多播。
根据以往的经验，在使用回环适配器时（在 Ubuntu 或 OSX 上），它并不一定会默认启用。
请参见 `原始问题 <https://github.com/ros2/ros2/issues/552>`__ 或 `ros-answers 上的讨论 <https://answers.ros.org/question/300370/ros2-talker-cannot-communicate-with-listener/>`__。
你可以使用 ROS 2 工具验证当前配置是否允许多播：

在终端 1 中：

.. code-block:: console

   $ ros2 multicast receive

在终端 2 中：

.. code-block:: console

   $ ros2 multicast send

如果第一条命令没有返回类似下面这样的响应：

.. code-block:: bash

   Received from xx.xxx.xxx.xx:43751: 'Hello World!'

那么你需要更新防火墙配置，以通过 `ufw <https://help.ubuntu.com/community/UFW>`__ 允许多播。

.. code-block:: console

   $ sudo ufw allow in proto udp to 224.0.0.0/4
   $ sudo ufw allow in proto udp from 224.0.0.0/4


你可以使用 :code:`ifconfig` 工具检查网络接口是否启用了多播标志，也就是在 flags 部分中查找 :code:`MULTICAST`：

.. code-block:: bash

   eno1: flags=4163<...,MULTICAST>
      ...

系统上不存在相应库时导入失败
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

有时 ``rclpy`` 会导入失败，因为找不到预期的 C 扩展库。
如果出现这种情况，请将目录中存在的库与错误消息中提到的库进行对比。
假设存在一个名称相似的文件（前缀相同，如 ``_rclpy.`` ，后缀相同，如 ``.so`` ，但 Python 版本 / 架构不同），那么你使用的 Python 解释器就与构建该 C 扩展时所用的解释器并不相同。
请务必使用与构建该二进制文件时相同的 Python 解释器。

例如，在操作系统更新之后可能会出现这种不匹配的情况。
此时，重新构建工作空间或许可以解决该问题。

.. _linux-troubleshooting:

Linux
-----

内部编译器错误
^^^^^^^^^^^^^^

如果你在内存受限的平台（例如 Raspberry PI）上编译时遇到 ICE，可以尝试单线程构建（在构建命令前加上 ``MAKEFLAGS=-j1`` ）。

内存不足
^^^^^^^^

当前形式的 ``ros1_bridge`` 编译时需要 4Gb 可用内存。
如果你没有这么多可用内存，建议在该文件夹中使用 ``COLCON_IGNORE`` ，并跳过其编译。

多主机干扰
^^^^^^^^^^

如果在同一网络中运行多个实例，可能会出现干扰。
为避免这种情况，你可以将环境变量 ``ROS_DOMAIN_ID`` 设置为不同的整数，默认值为零。
这将为你的系统定义 DDS 域 ID。

source setup.bash 时出现异常
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. 仅适用于 Eloquent 和 Foxy

如果你在从源码构建后 source 环境时遇到异常，请尝试使用以下命令升级 ``colcon`` 相关软件包：

.. code-block:: console

   $ colcon version-check  # check if newer versions available
   $ sudo apt install python3-colcon* --only-upgrade  # upgrade installed colcon packages to latest version

混用 conda 与 apt 的 Python 冲突
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在使用 ROS 2 时，将用 ``apt`` 安装的软件包与用 ``conda`` 安装的软件包混用是不行的。
如果你使用 ROS 2 的官方 ``apt`` 二进制文件，请确保 ``PATH`` 环境变量中不包含任何 conda 路径。
你可能需要检查 ``.bashrc`` 中的这一行并将其注释掉。

另一方面，在 Windows 上，官方 ROS 2 安装流程通过 ``pixi`` 包管理器使用 ``conda`` 软件包，由于没有混用不同的包管理器，因此它可以正常工作。

可以为 ROS 2 构建 ``conda`` 软件包（例如社区维护的 `RoboStack <https://robostack.github.io/>`_ 项目所提供的那些），但官方并不提供 ROS 2 的 conda 软件包。

.. _macOS-troubleshooting:

macOS
-----

使用 ``pyenv`` 时出现段错误
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pyenv`` 似乎默认使用 ``.a`` 文件构建 Python，但这会导致 ``rclpy`` 出现问题，因此在使用 ``pyenv`` 时，建议在 macOS 上启用 Frameworks 来构建 Python：

https://github.com/pyenv/pyenv/wiki#how-to-build-cpython-with-framework-support-on-os-x

库未加载；找不到映像
^^^^^^^^^^^^^^^^^^^^

如果你在运行时（无论是运行测试还是运行节点）遇到库加载问题，例如下面这样：

.. code-block:: bash

   ImportError: dlopen(.../ros2_<distro>/ros2-osx/lib/python3.7/site-packages/rclpy/_rclpy.cpython-37m-darwin.so, 2): Library not loaded: @rpath/librcl_interfaces__rosidl_typesupport_c.dylib
     Referenced from: .../ros2_<distro>/ros2-osx/lib/python3.7/site-packages/rclpy/_rclpy.cpython-37m-darwin.so
     Reason: image not found

那么你很可能启用了系统完整性保护（SIP）。
请按照 `这些说明 <https://developer.apple.com/library/content/documentation/Security/Conceptual/System_Integrity_Protection_Guide/ConfiguringSystemIntegrityProtection/ConfiguringSystemIntegrityProtection.html>`__ 禁用系统完整性保护（SIP）。

Qt 构建错误：``unknown type name 'Q_ENUM'``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果你看到与 Qt 相关的构建错误，例如：

.. code-block:: bash

   In file included from /usr/local/opt/qt/lib/QtGui.framework/Headers/qguiapplication.h:46:
   /usr/local/opt/qt/lib/QtGui.framework/Headers/qinputmethod.h:87:5: error:
         unknown type name 'Q_ENUM'
       Q_ENUM(Action)
       ^

你可能使用的是 qt4 而不是 qt5：请参见 https://github.com/ros2/ros2/issues/441

使用 Homebrew 安装 opencv（以及 libjpeg、libtiff 和 libpng）时出现符号缺失
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果你安装了 opencv，可能会遇到以下情况：

.. code-block:: bash

   dyld: Symbol not found: __cg_jpeg_resync_to_restart
     Referenced from: /System/Library/Frameworks/ImageIO.framework/Versions/A/ImageIO
     Expected in: /usr/local/lib/libJPEG.dylib
    in /System/Library/Frameworks/ImageIO.framework/Versions/A/ImageIO
   /bin/sh: line 1: 25274 Trace/BPT trap: 5       /usr/local/bin/cmake

如果是这样，构建时你就需要执行以下操作：

.. code-block:: console

   $ brew unlink libpng libtiff libjpeg

但这会破坏 opencv，因此你还需要更新它才能继续正常工作：

.. code-block:: console

   $ sudo install_name_tool -change /usr/local/lib/libjpeg.8.dylib /usr/local/opt/jpeg/lib/libjpeg.8.dylib /usr/local/lib/libopencv_highgui.2.4.dylib
   $ sudo install_name_tool -change /usr/local/lib/libpng16.16.dylib /usr/local/opt/libpng/lib/libpng16.16.dylib /usr/local/lib/libopencv_highgui.2.4.dylib
   $ sudo install_name_tool -change /usr/local/lib/libtiff.5.dylib /usr/local/opt/libtiff/lib/libtiff.5.dylib /usr/local/lib/libopencv_highgui.2.4.dylib
   $ sudo install_name_tool -change /usr/local/lib/libjpeg.8.dylib /usr/local/opt/jpeg/lib/libjpeg.8.dylib /usr/local/Cellar/libtiff/4.0.4/lib/libtiff.5.dylib

第一条命令是必要的，以避免针对系统 libjpeg（等）构建的程序使用 /usr/local/lib 中的版本。
其余命令则更新由 Homebrew 构建的程序，使它们无需在 /usr/local/lib 中也能找到 libjpeg（等）的版本。

xcode-select 错误：工具 ``xcodebuild`` 需要 Xcode，但当前活动开发者目录是命令行实例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. 仅适用于 Eloquent 和 Foxy

如果你最近安装了 Xcode，可能会遇到这个错误：

.. code-block:: bash

   Xcode: xcode-select: error: tool 'xcodebuild' requires Xcode,
   but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance

要解决此错误，你需要：

1. 再次确认你已安装命令行工具：

.. code-block:: console

   $ xcode-select --install

2. 在终端中输入以下内容，以接受 Xcode 的条款和条件：

.. code-block:: console

   $ sudo xcodebuild -license accept

3. 确保 Xcode 应用位于 ``/Applications`` 目录中（而不是 ``/Users/{user}/Applications`` ）

4. 使用以下命令将 ``xcode-select`` 指向 Xcode 应用的 Developer 目录：

.. code-block:: console

   $ sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

rosdep 安装错误 ``homebrew: Failed to detect successful installation of [qt5]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
在跟随 :doc:`创建工作空间 <../Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace>` 教程时，你可能会遇到以下错误，它提示 ``rosdep`` 无法安装 Qt5。

.. code-block:: console

   $ rosdep install -i --from-path src --rosdistro {DISTRO} -y
   executing command [brew install qt5]
   Warning: qt 5.15.0 is already installed and up-to-date
   To reinstall 5.15.0, run `brew reinstall qt`
   ERROR: the following rosdeps failed to install
     homebrew: Failed to detect successful installation of [qt5]

该错误似乎源于一个 `链接问题 <https://github.com/ros-infrastructure/rosdep/issues/490#issuecomment-334959426>`__ ，可以通过运行以下命令来解决。

.. code-block:: console

   $ cd /usr/local/Cellar
   $ sudo ln -s qt qt5

现在运行 ``rosdep`` 命令应当可以正常执行：

.. code-block:: console

   $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

该命令应返回：

.. code-block:: text

   #All required rosdeps installed successfully

.. _windows-troubleshooting:

Windows
-------

系统中已存在相应库时导入仍然失败
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

有时 ``rclpy`` 会因为系统中缺少某些 DLL 而导入失败。
如果是这样，请确保安装 :ref:`安装说明 <windows-install-binary-installing-prerequisites>` 的“安装前提条件”章节中列出的所有依赖项。

如果你从二进制文件安装，可能需要更新依赖项：它们必须与构建这些二进制文件时所用的版本相同。

如果仍有问题，你可以使用 `Dependencies <https://github.com/lucasg/Dependencies>`_ 工具来确定系统中缺少哪些依赖项。
使用该工具加载相应的 ``.pyd`` 文件，它应当会报告不可用的 ``DLL`` 模块。
请确保在执行该工具之前已经 source 了当前工作空间，否则会出现未解析的 ROS DLL 文件。
利用这些信息来安装额外的依赖项，或根据需要调整你的路径。

CMake 设置修改时间错误
^^^^^^^^^^^^^^^^^^^^^^

如果你在安装文件时遇到 CMake 错误 ``file INSTALL cannot set modification time on ...`` ，很可能是有杀毒软件或 Windows Defender 干扰了构建。
例如，对于 Windows Defender，你可以将工作空间位置加入排除列表，以防止它扫描这些文件。

260 个字符的路径长度限制
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   The input line is too long.
   The syntax of the command is incorrect.

根据你的目录层次结构，在从源码构建 ROS 2 或构建你自己的库时，可能会看到路径长度限制错误。

要允许更深的路径长度：

运行 ``regedit.exe`` ，导航到 ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`` ，并将 ``LongPathsEnabled`` 设置为 0x00000001 (1)。

按 Windows 键并输入 ``Edit Group Policy`` 。
导航到 本地计算机策略 > 计算机配置 > 管理模板 > 系统 > 文件系统。
右键单击 ``Enable Win32 long paths`` ，点击“编辑”。
在对话框中，选择“已启用”并点击“确定”。

关闭并重新打开终端以重置环境，然后再次尝试构建。

CMake 软件包找不到 asio、tinyxml2、tinyxml 或 eigen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

我们发现，有时 ``asio`` 、 ``tinyxml2`` 等的 chocolatey 软件包不会添加重要的注册表项，导致 CMake 在构建 ROS 2 时无法找到它们。
我们目前还未能确定根本原因，但卸载这些 chocolatey 软件包（如果第一次卸载失败，可以加上 ``-n`` ），然后重新安装即可解决该问题。

patch.exe 会打开新的命令窗口并请求管理员权限
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

这也会导致需要使用 patch 的软件包构建失败，即使你允许它使用管理员权限。

- ``choco uninstall patch; colcon build --cmake-clean-cache`` —— 这是 `GNU Patch For Windows package <https://chocolatey.org/packages/patch>`_ 中的一个缺陷。
  如果未安装此软件包，构建过程将改用 git 附带的 Patch 版本。

无法加载 Fast RTPS 共享库
^^^^^^^^^^^^^^^^^^^^^^^^^

.. 不适用于 Crystal

Fast RTPS 需要 ``msvcr20.dll`` ，它属于 ``Visual C++ Redistributable Packages for Visual Studio 2013`` 的一部分。
尽管它通常在 Windows 10 中默认安装，但我们知道某些类 Windows 10 的版本并未默认安装它（例如：Windows Server 2019）。
如果你没有安装它，可以从 `这里 <https://www.microsoft.com/en-us/download/details.aspx?id=40784>`_ 下载。

无法创建进程
^^^^^^^^^^^^

如果运行某个 ROS 二进制文件时出现以下错误：

.. code-block::

   | failed to create process.

这很可能是找不到 Python 解释器。
对于每个可执行文件，会使用其附带脚本的 shebang（第一行），因此请确保 Python 位于预期的路径下（默认：``C:\Python38\`` ）。

二进制安装专有
^^^^^^^^^^^^^^

* 如果你的示例因为缺少 DLL 而无法启动，请确认诸如 OpenCV 之类外部依赖项的所有库都位于 ``PATH`` 变量中。
* 如果你忘记在终端中调用 ``local_setup.bat`` 文件，演示程序很可能会立即崩溃。

使用 WSL2 运行 RViz
^^^^^^^^^^^^^^^^^^^

如果你使用 `WSL2 <https://learn.microsoft.com/en-us/windows/wsl/install>`__ 在 Windows 上运行 ROS 2，可能会遇到类似下面这样的 RViz 运行问题：

.. code-block:: console

   $ rviz2
   [INFO] [1695823660.091830699] [rviz2]: Stereo is NOT SUPPORTED
   [INFO] [1695823660.091943524] [rviz2]: OpenGl version: 4.1 (GLSL 4.1)
   D3D12: Removing Device.
   Segmentation fault

一种可行的解决方案是强制 RViz 使用软件渲染：

.. code-block:: console

   $ export LIBGL_ALWAYS_SOFTWARE=true
   $ rviz2
   [INFO] [1695823660.091830699] [rviz2]: Stereo is NOT SUPPORTED
