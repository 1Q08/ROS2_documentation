.. redirect-from::

    Tutorials/Security/Security-on-Two

.. _Security-on-Two:

确保跨机器的安全性
==================

**目标：** 让两台不同的机器安全地通信。

**教程级别：** 高级

**时长：** 5 分钟

.. contents:: 目录
  :depth: 2
  :local:


背景
----

之前的教程在同一台机器上使用两个 ROS 节点，所有网络通信都通过 localhost 接口进行。
让我们把该场景扩展到多台机器，这样可以更明显地体现身份验证和加密带来的好处。

假设上一个演示中创建了密钥库的那台机器的主机名为 ``Alice``，而我们还想使用另一台主机名为 ``Bob`` 的机器来进行多机 ``talker/listener`` 演示。
我们需要把一些密钥从 ``Alice`` 移动到 ``Bob``，以便 SROS 2 能够对传输进行身份验证和加密。


创建第二个密钥库
----------------

先在 ``Bob`` 上创建一个空密钥库；密钥库实际上只是一个空目录：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ ssh Bob
      $ mkdir ~/sros2_demo
      $ exit

  .. group-tab:: MacOS

    .. code-block:: console

      $ ssh Bob
      $ mkdir ~/sros2_demo
      $ exit

  .. group-tab:: Windows

    .. code-block:: console

      $ ssh Bob
      $ md C:\dev\ros2\sros2_demo
      $ exit


复制文件
--------

接下来把 ``talker`` 程序的密钥和证书从 ``Alice`` 复制到 ``Bob``。
由于这些密钥只是文本文件，我们可以使用 ``scp`` 来复制它们。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ cd ~/sros2_demo/demo_keystore
      $ scp -r talker USERNAME@Bob:~/sros2_demo/demo_keystore

  .. group-tab:: MacOS

    .. code-block:: console

      $ cd ~/sros2_demo/demo_keystore
      $ scp -r talker USERNAME@Bob:~/sros2_demo/demo_keystore

  .. group-tab:: Windows

    .. code-block:: console

      $ cd C:\dev\ros2\sros2_demo\demo_keystore
      $ scp -r talker USERNAME@Bob:/dev/ros2/sros2_demo/demo_keystore

.. warning::

  请注意，在这种情况下整个密钥库会在不同机器之间共享，这可能并非你期望的行为，因为它可能带来安全风险。
  有关这方面的更多信息，请参阅 :doc:`Deployment-Guidelines`。

这会非常快，因为只是复制一些非常小的文本文件。
现在，我们准备运行多机 talker/listener 演示！


启动节点
--------

环境设置完成后，在 ``Bob`` 上运行 talker：

.. code-block:: console

  $ ros2 run demo_nodes_cpp talker --ros-args --enclave /talker_listener/talker

并在 ``Alice`` 上启动 listener：

.. code-block:: console

  $ ros2 run demo_nodes_py listener --ros-args --enclave /talker_listener/listener

现在 Alice 将从 Bob 接收加密消息。

在两台机器成功使用加密和身份验证进行通信后，你可以用同样的步骤向 ROS 图中添加更多机器。
