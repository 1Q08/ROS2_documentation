.. redirect-from::

    Tutorials/Security/Security-on-Two

.. _Security-on-Two:

确保跨机器安全
==============

**目标：** 让两台不同的机器安全通信。

**教程级别：** 高级

**耗时：** 5 分钟

.. contents:: 目录
  :depth: 2
  :local:


背景
----

在继续之前，请确保你已完成 :doc:`Introducing-ros2-security` 教程。

前面的教程在同一台机器上使用了两个 ROS 节点，所有网络通信都通过 localhost 接口发送。
让我们将该场景扩展到涉及多台机器，因为这样身份验证和加密的好处会变得更加明显。

假设在前一个演示中创建了密钥库的机器主机名为 ``Alice``，而我们还想使用另一台主机名为 ``Bob`` 的机器来进行多机 ``talker/listener`` 演示。
我们需要将一些密钥从 ``Alice`` 移到 ``Bob``，以便 SROS 2 能够对传输进行身份验证和加密。


创建第二个密钥库
----------------

首先在 ``Bob`` 上创建一个空密钥库；密钥库实际上只是一个空目录：

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

接下来，将 ``talker`` 程序的密钥和证书从 ``Alice`` 复制到 ``Bob``。
由于密钥只是文本文件，我们可以使用 ``scp`` 来复制它们。

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

  请注意，在这种情况下，整个密钥库会在不同机器之间共享，这可能不是期望的行为，因为它可能导致安全风险。
  有关这方面的更多信息，请参阅 :doc:`Deployment-Guidelines`。

这会非常快，因为只是复制一些非常小的文本文件。
现在，我们准备好运行多机 talker/listener 演示了！


启动节点
--------

环境设置完成后，在 ``Bob`` 上运行 talker：

.. code-block:: console

  $ ros2 run demo_nodes_cpp talker --ros-args --enclave /talker_listener/talker

并在 ``Alice`` 上启动 listener：

.. code-block:: console

  $ ros2 run demo_nodes_py listener --ros-args --enclave /talker_listener/listener

现在，Alice 将收到来自 Bob 的加密消息。

在两台机器成功使用加密和身份验证通信之后，你可以使用相同的方法向 ROS 图添加更多机器。
