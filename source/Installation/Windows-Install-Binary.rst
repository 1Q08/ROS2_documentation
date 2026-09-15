Windows（二进制）
=================

.. contents:: 目录
   :depth: 2
   :local:

本文说明如何在 Windows 上从预构建二进制包安装 ROS 2。

.. note::

    预构建二进制包不包含所有 ROS 2 软件包。
    它包含 `ROS base 变体 <https://reps.openrobotics.org/rep-2001/#ros-base>`_ 中的所有软件包，但只包含 `ROS desktop 变体 <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_ 中的一部分软件包。
    确切的软件包列表由 `此 ros2.repos 文件 <https://github.com/ros2/ros2/blob/{REPOS_FILE_BRANCH}/ros2.repos>`_ 中列出的仓库描述。

系统要求
--------

仅支持 Windows 10。

.. _windows-install-binary-installing-prerequisites:

.. include:: _Windows-Install-Prerequisites.rst

下载 ROS 2
----------

* 前往 releases 页面：https://github.com/ros2/ros2/releases
* 下载适用于 Windows 的最新软件包，例如 ``ros2-{DISTRO}-*-windows-release-amd64.zip``。

.. note::

    可能存在多个二进制下载选项，这会导致文件名有所不同。

.. note::

    若要为 ROS 2 安装调试库，请参阅 `调试相关附加内容`_。
    然后继续下载 ``ros2-package-windows-debug-AMD64.zip``。

* 将 zip 文件解压到某个位置（我们假设为 ``C:\dev\ros2_{DISTRO}``\ ）。

安装额外 DDS 实现（可选）
-------------------------

如果你想使用除默认的 Fast DDS 之外的其他 DDS 或 RTPS 厂商，可以在此处找到说明：:doc:`这里 <RMW-Implementations>`。

环境设置
--------

启动一个命令 shell，加载 ROS 2 安装脚本以配置工作空间：

.. code-block:: console

   $ call C:\dev\ros2_{DISTRO}\local_setup.bat

如果其他一切正常，上一条命令恰好输出一次 ``The system cannot find the path specified.`` 是正常的。

尝试一些示例
------------

在命令 shell 中按上述方式配置 ROS 2 环境，然后运行 C++ 的 ``talker``\ ：

.. code-block:: console

   $ ros2 run demo_nodes_cpp talker

再启动另一个命令 shell，运行 Python 的 ``listener``\ ：

.. code-block:: console

   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 输出 ``Publishing`` 消息，而 ``listener`` 输出 ``I heard`` 这些消息。
这验证了 C++ 和 Python API 都能正常工作。
太棒了！


安装后的后续步骤
----------------
继续学习 :doc:`教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并了解 ROS 2 的核心概念。

其他 RMW 实现（可选）
---------------------
ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在运行时替换。
请参阅关于如何使用多个 RMW 的 :doc:`指南 <../How-To-Guides/Working-with-multiple-RMW-implementations>`。

故障排查
--------

故障排查技巧可以在 :ref:`这里 <windows-troubleshooting>` 找到。

卸载
----

1. 如果你按上面的说明使用 colcon 安装工作空间，那么“卸载”可能只需打开一个新终端，并且不要加载该工作空间的 ``setup`` 文件。
   这样，你的环境就会表现得如同系统中没有安装 {DISTRO_TITLE}。

2. 如果你还想释放空间，可以用以下命令删除整个工作空间目录：

   .. code-block:: console

     $ rmdir /s /q \ros2_{DISTRO}

调试相关附加内容
----------------

要下载 ROS 2 调试库，你需要下载 ``ros2-{DISTRO}-*-windows-debug-AMD64.zip``。
请注意，调试库需要如下所示的更多额外配置/设置才能工作。

Python 安装可能需要修改以启用调试符号和调试版二进制文件：

* 在 Windows 的 **搜索栏** 中搜索并打开 **应用和功能**。
* 搜索已安装的 Python 版本。

* 单击“修改”。

      .. image:: images/python_installation_modify.png
         :width: 500 px

* 单击“下一步”进入 **高级选项**。

      .. image:: images/python_installation_next.png
         :width: 500 px

* 确保勾选 **Download debugging symbols** 和 **Download debug binaries**。

      .. image:: images/python_installation_enable_debug.png
         :width: 500 px

* 单击“安装”。

