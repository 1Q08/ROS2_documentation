.. redirect-from::

  Guides/Installation-Troubleshooting
  Troubleshooting/Installation-Troubleshooting

安装故障排查
============

安装故障排查技巧按其适用的平台分类。

.. contents:: 平台
   :depth: 2
   :local:

通用
----

通用故障排查技巧适用于所有平台。

启用组播
^^^^^^^^

为了通过 DDS 成功通信，所使用的网络接口必须启用组播（multicast）。
根据以往经验，当使用回环适配器时，这不一定默认启用（在 Ubuntu 或 OSX 上）。
请参见 `原始 issue <https://github.com/ros2/ros2/issues/552>`__ 或 `ros-answers 上的一次讨论 <https://answers.ros.org/question/300370/ros2-talker-cannot-communicate-with-listener/>`__。
你可以使用 ROS 2 工具验证当前设置是否允许组播：

在终端 1 中：

.. code-block:: console

   $ ros2 multicast receive

在终端 2 中：

.. code-block:: console

   $ ros2 multicast send

如果第一个命令没有返回类似以下的响应：

.. code-block:: bash

   Received from xx.xxx.xxx.xx:43751: 'Hello World!'

那么你需要使用 `ufw <https://help.ubuntu.com/community/UFW>`__ 更新防火墙配置以允许组播。

.. code-block:: console

   $ sudo ufw allow in proto udp to 224.0.0.0/4
   $ sudo ufw allow in proto udp from 224.0.0.0/4


你可以使用 :code:`ifconfig` 工具并查看 flags 部分中的 :code:`MULTICAST` 来检查你的网络接口是否启用了组播标志：

.. code-block:: bash

   eno1: flags=4163<...,MULTICAST>
      ...

系统上不存在库时导入失败
^^^^^^^^^^^^^^^^^^^^^^^^

有时 ``rclpy`` 导入失败，因为找不到预期的 C 扩展库。
如果是这样，请将目录中存在的库与错误消息中提到的库进行比较。
假设存在名称相似的文件（前缀相同，如 ``_rclpy.``，后缀相同，如 ``.so``，但 Python 版本/架构不同），那么你使用的 Python 解释器与用于构建 C 扩展的 Python 解释器不同。
请务必使用与构建二进制文件时相同的 Python 解释器。

例如，这种不匹配可能会在操作系统更新后出现。
此时，重新构建工作空间可能会解决该问题。

.. _linux-troubleshooting:

Linux
-----

内部编译器错误
^^^^^^^^^^^^^^

如果你在像 Raspberry PI 这样的内存受限平台上编译时遇到 ICE，你可能希望使用单线程构建（在构建命令前加上 ``MAKEFLAGS=-j1``）。

内存不足
^^^^^^^^

``ros1_bridge`` 在当前形式下需要 4Gb 的可用 RAM 才能编译。
如果你没有那么多可用 RAM，建议在该文件夹中使用 ``COLCON_IGNORE`` 并跳过其编译。

多主机干扰
^^^^^^^^^^

如果你在同一网络上运行多个实例，可能会遇到干扰。
为避免这种情况，你可以将环境变量 ``ROS_DOMAIN_ID`` 设置为不同的整数，默认值为零。
这将为你的系统定义 DDS 域 id。

source setup.bash 时出现异常
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. only relevant to Eloquent and Foxy

如果你在从源代码构建后尝试 source 环境时遇到异常，请尝试使用以下命令升级 ``colcon`` 相关包

.. code-block:: console

   $ colcon version-check  # check if newer versions available
   $ sudo apt install python3-colcon* --only-upgrade  # upgrade installed colcon packages to latest version

混用 conda 和 apt 的 Python 冲突
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在使用 ROS 2 时，将使用 ``apt`` 安装的包与使用 ``conda`` 安装的包混用是不行的。
如果你使用的是 ROS 2 的官方 ``apt`` 二进制文件，请确保你的 ``PATH`` 环境变量中没有任何 conda 路径。
你可能需要检查 ``.bashrc`` 中的这一行并将其注释掉。

另一方面，在 Windows 上，官方 ROS 2 安装流程通过 ``pixi`` 包管理器使用 ``conda`` 包，这没有问题，因为没有混用不同的包管理器。

ROS 2 的 ``conda`` 包可能会被构建（例如由社区维护的 `RoboStack <https://robostack.github.io/>`_ 项目提供的包），但官方不提供 ROS 2 的 conda 包。

无法启动 rviz2
^^^^^^^^^^^^^^

``rviz2`` 在 Wayland 显示系统上可能无法启动，并出现如下错误：

.. code-block::

   QSocketNotifier: Can only be used with threads started with QThread
   [INFO] [1714730141.758659580] [rviz2]: Stereo is NOT SUPPORTED
   [INFO] [1714730141.758813709] [rviz2]: OpenGl version: 3.1 (GLSL 1.4)
   [ERROR] [1714730141.797879232] [rviz2]: rviz::RenderSystem: error creating render window: RenderingAPIException: Invalid parentWindowHandle (wrong server or screen) in GLXWindow::create at ./.obj-aarch64-linux-gnu/ogre_vendor-prefix/src/ogre_vendor/RenderSystems/GLSupport/src/GLX/OgreGLXWindow.cpp (line 246)
   ...
   [ERROR] [1714730141.808124283] [rviz2]: Unable to create the rendering window after 100 tries
   terminate called after throwing an instance of 'std::runtime_error'
     what():  Unable to create the rendering window after 100 tries
   Aborted (core dumped)

这是由于 Wayland 与 RViz2 之间的不兼容。
你可以通过在 X11 兼容模式下运行 RViz2 来解决此问题：

.. code-block::

   QT_QPA_PLATFORM=xcb rviz2

.. _macOS-troubleshooting:

macOS
-----

使用 ``pyenv`` 时出现段错误
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pyenv`` 似乎默认使用 ``.a`` 文件构建 Python，但这会导致 ``rclpy`` 出现问题，因此建议在 macOS 上使用 ``pyenv`` 时启用 Frameworks 来构建 Python：

https://github.com/pyenv/pyenv/wiki#how-to-build-cpython-with-framework-support-on-os-x

Library not loaded; image not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果你在运行时（无论是运行测试还是运行节点）看到库加载问题，例如以下内容：

.. code-block:: bash

   ImportError: dlopen(.../ros2_<distro>/ros2-osx/lib/python3.7/site-packages/rclpy/_rclpy.cpython-37m-darwin.so, 2): Library not loaded: @rpath/librcl_interfaces__rosidl_typesupport_c.dylib
     Referenced from: .../ros2_<distro>/ros2-osx/lib/python3.7/site-packages/rclpy/_rclpy.cpython-37m-darwin.so
     Reason: image not found

那么你可能启用了系统完整性保护（System Integrity Protection）。
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

你可能使用的是 qt4 而不是 qt5：参见 https://github.com/ros2/ros2/issues/441

使用 Homebrew 安装 opencv（以及 libjpeg、libtiff 和 libpng）后出现符号缺失
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果你安装了 opencv，可能会遇到这种情况：

.. code-block:: bash

   dyld: Symbol not found: __cg_jpeg_resync_to_restart
     Referenced from: /System/Library/Frameworks/ImageIO.framework/Versions/A/ImageIO
     Expected in: /usr/local/lib/libJPEG.dylib
    in /System/Library/Frameworks/ImageIO.framework/Versions/A/ImageIO
   /bin/sh: line 1: 25274 Trace/BPT trap: 5       /usr/local/bin/cmake

如果是这样，要完成构建，你必须执行以下操作：

.. code-block:: console

   $ brew unlink libpng libtiff libjpeg

但这会破坏 opencv，因此你还需要更新它才能继续工作：

.. code-block:: console

   $ sudo install_name_tool -change /usr/local/lib/libjpeg.8.dylib /usr/local/opt/jpeg/lib/libjpeg.8.dylib /usr/local/lib/libopencv_highgui.2.4.dylib
   $ sudo install_name_tool -change /usr/local/lib/libpng16.16.dylib /usr/local/opt/libpng/lib/libpng16.16.dylib /usr/local/lib/libopencv_highgui.2.4.dylib
   $ sudo install_name_tool -change /usr/local/lib/libtiff.5.dylib /usr/local/opt/libtiff/lib/libtiff.5.dylib /usr/local/lib/libopencv_highgui.2.4.dylib
   $ sudo install_name_tool -change /usr/local/lib/libjpeg.8.dylib /usr/local/opt/jpeg/lib/libjpeg.8.dylib /usr/local/Cellar/libtiff/4.0.4/lib/libtiff.5.dylib

第一条命令是必要的，以避免针对系统 libjpeg（等）构建的组件从 /usr/local/lib 获取版本。
其余命令用于更新 Homebrew 构建的组件，使它们能够在 /usr/local/lib 中没有这些库的情况下找到 libjpeg（等）的版本。

Xcode-select 错误：工具 ``xcodebuild`` 需要 Xcode，但当前活动的开发者目录是一个命令行实例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. only relevant to Eloquent and Foxy

如果你最近安装了 Xcode，可能会遇到此错误：

.. code-block:: bash

   Xcode: xcode-select: error: tool 'xcodebuild' requires Xcode,
   but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance

要解决此错误，你需要：

1. 仔细确认你已安装命令行工具：

.. code-block:: console

   $ xcode-select --install

2. 在终端中输入以下命令接受 Xcode 的条款和条件：

.. code-block:: console

   $ sudo xcodebuild -license accept

3. 确保 Xcode 应用位于 ``/Applications`` 目录中（而不是 ``/Users/{user}/Applications``）

4. 使用以下命令将 ``xcode-select`` 指向 Xcode 应用的 Developer 目录：

.. code-block:: console

   $ sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

rosdep install 错误 ``homebrew: Failed to detect successful installation of [qt5]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
在按照 :doc:`创建工作空间 <../Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace>` 教程操作时，你可能会遇到以下错误，提示 ``rosdep`` 无法安装 Qt5。

.. code-block:: console

   $ rosdep install -i --from-path src --rosdistro {DISTRO} -y
   executing command [brew install qt5]
   Warning: qt 5.15.0 is already installed and up-to-date
   To reinstall 5.15.0, run `brew reinstall qt`
   ERROR: the following rosdeps failed to install
     homebrew: Failed to detect successful installation of [qt5]

此错误似乎源于一个 `链接问题 <https://github.com/ros-infrastructure/rosdep/issues/490#issuecomment-334959426>`__，可以通过运行以下命令解决。

.. code-block:: console

   $ cd /usr/local/Cellar
   $ sudo ln -s qt qt5

现在运行 ``rosdep`` 命令应该可以正常执行：

.. code-block:: console

   $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

该命令应返回：

.. code-block:: text

   #All required rosdeps installed successfully

.. _windows-troubleshooting:

Windows
-------

即使系统上存在库，导入仍然失败
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

有时 ``rclpy`` 导入失败，是因为你的系统上缺少某些 DLL。
如果是这样，请确保安装 :ref:`安装说明 <windows-install-binary-installing-prerequisites>` 的 "Installing prerequisites" 部分列出的所有依赖项。

如果你是从二进制文件安装的，可能需要更新依赖项：它们的版本必须与用于构建二进制文件的版本相同。

如果你仍然遇到问题，可以使用 `Dependencies <https://github.com/lucasg/Dependencies>`_ 工具来确定系统上缺少哪些依赖项。
使用该工具加载相应的 ``.pyd`` 文件，它应该会报告不可用的 ``DLL`` 模块。
在执行该工具之前，请确保当前工作空间已被 source，否则会出现无法解析的 ROS DLL 文件。
使用这些信息来安装额外的依赖项，或根据需要调整你的路径。

CMake 设置修改时间错误
^^^^^^^^^^^^^^^^^^^^^^

如果你在安装文件时遇到 CMake 错误 ``file INSTALL cannot set modification time on ...``，很可能是杀毒软件或 Windows Defender 干扰了构建。
例如，对于 Windows Defender，你可以将工作空间位置列为排除项，以防止其扫描这些文件。

260 字符路径限制
^^^^^^^^^^^^^^^^

.. code-block:: bash

   The input line is too long.
   The syntax of the command is incorrect.

根据你的目录层级，在从源代码或你自己的库构建 ROS 2 时，你可能会看到路径长度限制错误。

要允许更深的路径长度：

运行 ``regedit.exe``，导航到 ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem``，并将 ``LongPathsEnabled`` 设置为 0x00000001 (1)。

按下 Windows 键并输入 ``Edit Group Policy``。
导航到 Local Computer Policy > Computer Configuration > Administrative Templates > System > Filesystem。
右键单击 ``Enable Win32 long paths``，单击 Edit。
在对话框中，选择 Enabled 并单击 OK。

关闭并重新打开终端以重置环境，然后再次尝试构建。

CMake 包无法找到 asio、tinyxml2、tinyxml 或 eigen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

我们注意到，有时 ``asio``、``tinyxml2`` 等的 chocolatey 包不会添加重要的注册表项，导致 CMake 在构建 ROS 2 时无法找到它们。
我们尚未能确定根本原因，但卸载 chocolatey 包（如果首次卸载失败，使用 ``-n``），然后重新安装它们可以解决该问题。

patch.exe 打开新的命令窗口并要求管理员权限
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

这也会导致需要使用 patch 的包的构建失败，即使你允许它使用管理员权限。

- ``choco uninstall patch; colcon build --cmake-clean-cache`` - 这是 `GNU Patch For Windows 包 <https://chocolatey.org/packages/patch>`_ 中的一个 bug。
  如果未安装此包，构建过程将改用随 git 分发的 Patch 版本。

无法加载 Fast RTPS 共享库
^^^^^^^^^^^^^^^^^^^^^^^^^

.. does not apply to Crystal

Fast RTPS 需要 ``msvcr20.dll``，它是 ``Visual C++ Redistributable Packages for Visual Studio 2013`` 的一部分。
虽然它通常在 Windows 10 中默认安装，但我们知道某些类 Windows 10 版本默认并未安装它（例如：Windows Server 2019）。
如果你没有安装它，可以从 `这里 <https://www.microsoft.com/en-us/download/details.aspx?id=40784>`__ 下载。

无法创建进程
^^^^^^^^^^^^

如果运行 ROS 二进制文件时出现以下错误：

.. code-block::

   | failed to create process.

很可能是找不到 Python 解释器。
对于每个可执行文件，都会使用其附带脚本的 shebang（第一行），因此请确保 Python 在预期路径（默认：``C:\Python38\``）下可用。

二进制安装特定问题
^^^^^^^^^^^^^^^^^^

* 如果你的示例因缺少 DLL 而无法启动，请验证来自 OpenCV 等外部依赖项的所有库是否都在你的 ``PATH`` 变量中。
* 如果你忘记从终端调用 ``local_setup.bat`` 文件，演示程序很可能会立即崩溃。

使用 WSL2 运行 RViz
^^^^^^^^^^^^^^^^^^^

如果你使用 `WSL2 <https://learn.microsoft.com/en-us/windows/wsl/install>`__ 在 Windows 上运行 ROS 2，运行 RViz 时可能会遇到如下问题：

.. code-block:: console

   $ rviz2
   [INFO] [1695823660.091830699] [rviz2]: Stereo is NOT SUPPORTED
   [INFO] [1695823660.091943524] [rviz2]: OpenGl version: 4.1 (GLSL 4.1)
   D3D12: Removing Device.
   Segmentation fault

一种可能的解决方案是强制 RViz 使用软件渲染：

.. code-block:: console

   $ export LIBGL_ALWAYS_SOFTWARE=true
   $ rviz2
   [INFO] [1695823660.091830699] [rviz2]: Stereo is NOT SUPPORTED
