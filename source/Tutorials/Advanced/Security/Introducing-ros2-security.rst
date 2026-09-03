.. redirect-from::

    Tutorials/Security/Introducing-ros2-security

.. _sros2:
.. _ROS-2-Security-Tutorials:

设置安全性
==========

**目标：** 使用 ``sros2`` 设置安全性。

**教程级别：** 高级

**耗时：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:


背景
----

``sros2`` 包提供了在 DDS-Security 之上使用 ROS 2 的工具和说明。
这些安全特性已在多种平台（Linux、macOS 和 Windows）以及多种语言（C++ 和 Python）上经过测试。
SROS2 被设计为能与任何安全中间件配合使用，但并非所有中间件都是开源的，并且其支持程度因所使用的 ROS 发行版而异。


安装
----

通常，按照 :doc:`ROS 2 安装指南 <../../../Installation>` 和 :doc:`配置指南 <../../Beginner-CLI-Tools/Configuring-ROS2-Environment>` 安装后，安全性即可用。
但是，如果你打算从源码安装或切换中间件实现，请考虑以下注意事项：


从源码安装
^^^^^^^^^^

从源码安装之前，你需要安装一个较新版本的 openssl（1.0.2g 或更高版本）：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ sudo apt update
      $ sudo apt install libssl-dev

  .. group-tab:: MacOS

    .. code-block:: console

      $ brew install openssl

    你需要将 OpenSSL 放到库路径上才能运行 DDS-Security 演示。
    运行以下命令，并考虑将其添加到你的 ``~/.bash_profile`` 中：

    .. code-block:: console

      $ export DYLD_LIBRARY_PATH=`brew --prefix openssl`/lib:$DYLD_LIBRARY_PATH
      $ export OPENSSL_ROOT_DIR=`brew --prefix openssl`


  .. group-tab:: Windows

    如果你尚未安装 OpenSSL，请遵循 :ref:`这些说明 <windows-install-binary-installing-prerequisites>`。

Fast DDS 需要一个额外的 CMake 标志来构建安全插件，因此需要修改 colcon 调用以传入：

.. code-block:: console

  $ colcon build --symlink-install --cmake-args -DSECURITY=ON --packages-select fastrtps rmw_fastrtps_cpp rmw_fastrtps_dynamic_cpp rmw_fastrtps_shared_cpp


选择备用中间件
^^^^^^^^^^^^^^

如果你选择不使用默认的中间件实现，请务必在继续之前 :doc:`更改你的 RMW 实现 <../../../Installation/RMW-Implementations/>`。

ROS 2 允许你在运行时更改 RMW 实现。
参见 `如何使用多个 RMW 实现 <../../../How-To-Guides/Working-with-multiple-RMW-implementations>` 以探索不同的中间件实现。

请注意，不同厂商之间的安全通信不受支持。


运行演示
--------

1) 为安全文件创建一个文件夹
^^^^^^^^^^^^^^^^^^^^^^^^^^^
  首先创建一个文件夹，用于存储本演示所需的所有文件：

  .. tabs::

    .. group-tab:: Linux

      .. code-block:: console

        $ mkdir ~/sros2_demo

    .. group-tab:: MacOS

      .. code-block:: console

        $ mkdir ~/sros2_demo

    .. group-tab:: Windows

      .. code-block:: console

        $ md C:\dev\ros2\sros2_demo

2) 生成密钥库（keystore）
^^^^^^^^^^^^^^^^^^^^^^^^^

使用 ``sros2`` 工具创建密钥库。
密钥库中的文件将用于为 ROS 2 图中的所有参与者启用安全性。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ cd ~/sros2_demo
      $ ros2 security create_keystore demo_keystore

  .. group-tab:: MacOS

    .. code-block:: console

      $ cd ~/sros2_demo
      $ ros2 security create_keystore demo_keystore

  .. group-tab:: Windows

    .. code-block:: console

      $ cd sros2_demo
      $ ros2 security create_keystore demo_keystore

3) 生成密钥和证书
^^^^^^^^^^^^^^^^^

密钥库创建完成后，为每个启用安全性的节点创建密钥和证书。
对于我们的演示，这包括 talker 和 listener 节点。
此命令使用 ``create_enclave`` 功能，该功能将在下一个教程中更详细地介绍。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ ros2 security create_enclave demo_keystore /talker_listener/talker
      $ ros2 security create_enclave demo_keystore /talker_listener/listener

  .. group-tab:: MacOS

    .. code-block:: console

      $ ros2 security create_enclave demo_keystore /talker_listener/talker
      $ ros2 security create_enclave demo_keystore /talker_listener/listener

  .. group-tab:: Windows

    .. code-block:: console

      $ ros2 security create_enclave demo_keystore /talker_listener/talker
      $ ros2 security create_enclave demo_keystore /talker_listener/listener


    如果出现 ``unable to write 'random state'``，请设置环境变量 ``RANDFILE``。

    .. code-block:: console

      $ set RANDFILE=C:\dev\ros2\sros2_demo\.rnd

    然后重新运行上面的命令。


4) 配置环境变量
^^^^^^^^^^^^^^^

三个环境变量允许中间件定位加密材料，并启用（以及可能强制执行）安全性。
这些以及其他与安全相关的环境变量在 `ROS 2 DDS-Security 集成设计文档 <https://design.ros2.org/articles/ros2_dds_security.html>`_ 中有描述。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export ROS_SECURITY_KEYSTORE=~/sros2_demo/demo_keystore
      $ export ROS_SECURITY_ENABLE=true
      $ export ROS_SECURITY_STRATEGY=Enforce

  .. group-tab:: MacOS

    .. code-block:: console

      $ export ROS_SECURITY_KEYSTORE=~/sros2_demo/demo_keystore
      $ export ROS_SECURITY_ENABLE=true
      $ export ROS_SECURITY_STRATEGY=Enforce

  .. group-tab:: Windows

    .. code-block:: console

      $ set ROS_SECURITY_KEYSTORE=%cd%/demo_keystore
      $ set ROS_SECURITY_ENABLE=true
      $ set ROS_SECURITY_STRATEGY=Enforce

这些变量需要在用于演示的每个终端中定义。
为了方便，你可以将它们添加到你的启动环境中。


5) 运行 ``talker/listener`` 演示
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

通过启动 talker 节点开始演示。

.. code-block:: console

  $ ros2 run demo_nodes_cpp talker --ros-args --enclave /talker_listener/talker

在另一个终端中，同样启动 ``listener`` 节点。
此终端中的环境变量必须如上面第 4 步所述正确设置。

.. code-block:: console

  $ ros2 run demo_nodes_py listener --ros-args --enclave /talker_listener/listener

这些节点将使用身份验证和加密进行通信！
如果你查看数据包内容（例如使用 ``tcpdump`` 或 ``Wireshark``，如另一个教程所述），可以看到消息已加密。

注意：你可以在 C++（demo_nodes_cpp）和 Python（demo_nodes_py）包之间任意切换。

这些节点之所以能够通信，是因为我们为它们创建了适当的密钥和证书。

在使用 ``ros2cli`` 并回答下面的问题时，让两个节点保持运行。


6) 使用 ``ros2cli`` 配合安全性
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

要使用 ``ros2cli`` 与 ROS 2 安全网络交互，你需要通过 ``ROS_SECURITY_ENCLAVE_OVERRIDE`` 环境变量为其提供覆盖 enclave。
打开另一个终端并设置以下环境变量。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export ROS_SECURITY_KEYSTORE=~/sros2_demo/demo_keystore
      $ export ROS_SECURITY_ENABLE=true
      $ export ROS_SECURITY_STRATEGY=Enforce
      $ export ROS_SECURITY_ENCLAVE_OVERRIDE=/talker_listener/listener

  .. group-tab:: MacOS

    .. code-block:: console

      $ export ROS_SECURITY_KEYSTORE=~/sros2_demo/demo_keystore
      $ export ROS_SECURITY_ENABLE=true
      $ export ROS_SECURITY_STRATEGY=Enforce
      $ export ROS_SECURITY_ENCLAVE_OVERRIDE=/talker_listener/listener

  .. group-tab:: Windows

    .. code-block:: console

      $ set ROS_SECURITY_KEYSTORE=%cd%/demo_keystore
      $ set ROS_SECURITY_ENABLE=true
      $ set ROS_SECURITY_STRATEGY=Enforce
      $ set ROS_SECURITY_ENCLAVE_OVERRIDE=/talker_listener/listener


现在你可以使用 ``ros2cli`` 与 ROS 2 安全网络通信。

.. code-block:: console

  $ ros2 node list --no-daemon --spin-time 3
  [INFO] [1733862009.410918416] [rcl]: Found security directory: /root/ros2_ws/colcon_ws/demo_keystore/enclaves/talker_listener/talker
  /listener
  /talker

.. code-block:: console

  $ ros2 topic list --no-daemon --spin-time 3
  [INFO] [1733861998.562163611] [rcl]: Found security directory: /root/ros2_ws/colcon_ws/demo_keystore/enclaves/talker_listener/talker
  /chatter
  /parameter_events
  /rosout

.. note::

  避免使用 ros2 daemon，因为它可能没有安全 enclave；而且在 ROS 2 安全网络中应给予足够的时间进行发现。


做个测验！
----------

.. tabs::

  .. group-tab:: 问题 1

    打开另一个终端会话，但\ **不要**\ 设置环境变量，以便不启用安全性。
    启动 listener。
    你预期会发生什么？

  .. group-tab:: 答案 1

    listener 启动但不会收到任何消息。
    所有流量都已加密，未启用安全性时 listener 收不到任何内容。


.. tabs::

  .. group-tab:: 问题 2

    停止 listener，将环境变量 ``ROS_SECURITY_ENABLE`` 设置为 ``true``，然后再次启动 listener。
    这次你预期会有什么结果？

  .. group-tab:: 答案 2

    listener 仍然启动但收不到消息。
    虽然现在已经启用了安全性，但由于 ROS 无法定位密钥文件，它没有被正确配置。
    listener 会启动，但处于非安全模式，因为安全性未被强制执行；这意味着尽管配置正确的 talker 正在发送加密消息，此 listener 却无法解密它们。

.. tabs::

  .. group-tab:: 问题 3

    停止 listener，并将 ``ROS_SECURITY_STRATEGY`` 设置为 ``Enforce``。
    现在会发生什么？

  .. group-tab:: 答案 3

    listener 无法启动。
    安全性已启用且被强制执行。
    由于它仍未正确配置，因此会抛出一个错误，而不是以非安全模式启动。


了解更多！
----------

准备好进一步深入了解 ROS 安全了吗？
看看 `Secure Turtlebot2 Demo <https://github.com/ros-swg/turtlebot3_demo>`_。
你会找到一个功能完善且复杂的 ROS 2 安全实现，可以尝试你自己的自定义场景。
请务必在这里创建拉取请求和 issue，以便我们继续改进 ROS 中的安全支持！

