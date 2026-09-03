.. redirect-from::

    Tutorials/Security/Examine-Traffic

.. _Examine-Traffic:

检查网络流量
============

**目标：** 捕获并检查原始 ROS 2 网络流量。

**教程级别：** 高级

**耗时：** 20 分钟

.. contents:: 目录
  :depth: 2
  :local:


概述
----

ROS 2 通信安全的核心是保护节点之间的通信。
前面的教程启用了安全性，但你如何能\ **真的**\ 判断流量是否被加密呢？
在本教程中，我们将看看如何捕获实时网络流量，以展示加密与未加密流量之间的区别。

.. note::

  ``rmw_fastrtps_cpp`` 默认使用 `共享内存传输 <https://fast-dds.docs.eprosima.com/en/latest/fastdds/transport/shared_memory/shared_memory.html>`_，以便在端点位于同一主机系统时提高传输层性能。
  安全 enclave 仍然会被应用，数据也会被加密。
  但是，由于数据不会经过网络接口，你无法捕获实时网络流量。
  如果你使用 ``rmw_fastrtps_cpp``，你需要要么完成本教程并在发布者和订阅者之间使用不同的主机系统，要么通过 `启用 UDP 传输 <https://fast-dds.docs.eprosima.com/en/latest/fastdds/transport/udp/udp.html#enabling-udp-transport>`_ 和 `如何设置 Fast-DDS XML 配置 <https://github.com/ros2/rmw_fastrtps#full-qos-configuration>`_ 来禁用共享内存传输。

前置条件
--------

本指南仅在 Linux 上运行，并假设你已经 :doc:`安装了 ROS 2 <../../../Installation>`。

运行演示
--------

安装 ``tcpdump``
^^^^^^^^^^^^^^^^

在一个新的终端窗口中，首先安装 `tcpdump <https://www.tcpdump.org/manpages/tcpdump.1.html>`_，这是一个用于捕获和显示网络流量的命令行工具。
虽然本教程描述的是 ``tcpdump`` 命令，但你也可以使用 `Wireshark <https://www.wireshark.org/>`_，这是一个用于捕获和分析流量的类似图形化工具。

.. code-block:: console

  $ sudo apt update
  $ sudo apt install tcpdump

通过多个 ``ssh`` 会话在单台机器上运行以下命令。

启动 talker 和 listener
^^^^^^^^^^^^^^^^^^^^^^^

再次启动 talker 和 listener，各自在自己的终端中。
未设置安全环境变量，因此这些会话未启用安全性。
在一个终端中运行：

.. code-block:: console

  $ unset ROS_SECURITY_ENABLE
  $ ros2 run demo_nodes_cpp talker --ros-args --enclave /talker_listener/talker

在另一个终端中运行：

.. code-block:: console

  $ unset ROS_SECURITY_ENABLE
  $ ros2 run demo_nodes_cpp listener --ros-args --enclave /talker_listener/listener


显示未加密的发现数据包
^^^^^^^^^^^^^^^^^^^^^^

在 talker 和 listener 运行的情况下，打开另一个终端并启动 ``tcpdump`` 来查看网络流量。
由于读取原始网络流量是一项特权操作，你需要使用 ``sudo``。

下面的命令使用 ``-X`` 选项打印数据包内容，使用 ``-i`` 选项监听任意接口上的数据包，并且仅捕获 `UDP <https://en.wikipedia.org/wiki/User_Datagram_Protocol>`_ 端口 7400 的流量。

.. code-block:: console

  $ sudo tcpdump -X -i any udp port 7400
  20:18:04.400770 IP 8_xterm.46392 > 239.255.0.1.7400: UDP, length 252
    0x0000:  4500 0118 d48b 4000 0111 7399 c0a8 8007  E.....@...s.....
    0x0010:  efff 0001 b538 1ce8 0104 31c6 5254 5053  .....8....1.RTPS
    ...
    0x00c0:  5800 0400 3f0c 3f0c 6200 1c00 1800 0000  X...?.?.b.......
    0x00d0:  2f74 616c 6b65 725f 6c69 7374 656e 6572  /talker_listener
    0x00e0:  2f74 616c 6b65 7200 2c00 2800 2100 0000  /talker.,.(.!...
    0x00f0:  656e 636c 6176 653d 2f74 616c 6b65 725f  enclave=/talker_
    0x0100:  6c69 7374 656e 6572 2f74 616c 6b65 723b  listener/talker;
    0x0110:  0000 0000 0100 0000                      ........

这是一个发现数据报——talker 在寻找订阅者。
如你所见，节点名（``/talker_listener/talker``）和 enclave（也是 ``/talker_listener/talker``）都以明文传递。
你还应该看到来自 ``listener`` 节点的类似发现数据报。
典型发现数据包的一些其他特征：

- 目标地址是 239.255.0.1，这是一个组播 IP 地址；ROS 2 默认使用组播流量进行发现。
- UDP 7400 是目标端口，遵循 `DDS-RTPS 规范 <https://www.omg.org/spec/DDSI-RTPS/About-DDSI-RTPS/>`_。
- 数据包包含 "RTPS" 标签，同样由 DDS-RTPS 规范定义。


显示未加密的数据包
^^^^^^^^^^^^^^^^^^

使用 ``tcpdump`` 通过过滤 7400 以上的 UDP 端口来捕获非发现类型的 RTPS 数据包。
你会看到几种不同类型的数据包，但请留意类似下面的内容，这明显是 talker 发送给 listener 的数据：

.. code-block:: console

  $ sudo tcpdump -i any -X udp portrange 7401-7500
  20:49:17.927303 IP localhost.46392 > localhost.7415: UDP, length 84
    0x0000:  4500 0070 5b53 4000 4011 e127 7f00 0001  E..p[S@.@..'....
    0x0010:  7f00 0001 b538 1cf7 005c fe6f 5254 5053  .....8...\.oRTPS
    0x0020:  0203 010f 010f 4874 e752 0000 0100 0000  ......Ht.R......
    0x0030:  0901 0800 cdee b760 5bf3 5aed 1505 3000  .......`[.Z...0.
    0x0040:  0000 1000 0000 1204 0000 1203 0000 0000  ................
    0x0050:  5708 0000 0001 0000 1200 0000 4865 6c6c  W...........Hell
    0x0060:  6f20 576f 726c 643a 2032 3133 3500 0000  o.World:.2135...

关于此数据包需要注意的一些特征：

- 消息内容 "Hello World: 2135" 以明文发送。
- 源和目标 IP 地址是 ``localhost``：由于两个节点都在同一台机器上运行，节点在 ``localhost`` 接口上发现了彼此。


启用加密
^^^^^^^^

停止 talker 和 listener 两个节点。
通过设置安全环境变量为两者启用加密，然后再次运行它们。

在终端 1 中：

.. code-block:: console

  $ export ROS_SECURITY_KEYSTORE=~/sros2_demo/demo_keystore
  $ export ROS_SECURITY_ENABLE=true
  $ export ROS_SECURITY_STRATEGY=Enforce
  $ ros2 run demo_nodes_cpp talker --ros-args --enclave /talker_listener/talker

在终端 2 中：

.. code-block:: console

  $ export ROS_SECURITY_KEYSTORE=~/sros2_demo/demo_keystore
  $ export ROS_SECURITY_ENABLE=true
  $ export ROS_SECURITY_STRATEGY=Enforce
  $ ros2 run demo_nodes_cpp listener --ros-args --enclave /talker_listener/listener


显示加密的发现数据包
^^^^^^^^^^^^^^^^^^^^

运行与之前相同的 ``tcpdump`` 命令，检查启用加密后发现流量的输出。
典型的发现数据包看起来大致如下：

.. code-block:: console

  $ sudo tcpdump -X -i any udp port 7400
  21:09:07.336617 IP 8_xterm.60409 > 239.255.0.1.7400: UDP, length 596
    0x0000:  4500 0270 c2f6 4000 0111 83d6 c0a8 8007  E..p..@.........
    0x0010:  efff 0001 ebf9 1ce8 025c 331e 5254 5053  .........\3.RTPS
    0x0020:  0203 010f bbdd 199c 7522 b6cb 699f 74ae  ........u"..i.t.
    ...
    0x00c0:  5800 0400 3f0c ff0f 6200 2000 1a00 0000  X...?...b.......
    0x00d0:  2f74 616c 6b65 725f 6c69 7374 656e 6572  /talker_listener
    0x00e0:  2f6c 6973 7465 6e65 7200 0000 2c00 2800  /listener...,.(.
    0x00f0:  2300 0000 656e 636c 6176 653d 2f74 616c  #...enclave=/tal
    0x0100:  6b65 725f 6c69 7374 656e 6572 2f6c 6973  ker_listener/lis
    0x0110:  7465 6e65 723b 0000 0110 c400 1400 0000  tener;..........
    0x0120:  4444 533a 4175 7468 3a50 4b49 2d44 483a  DDS:Auth:PKI-DH:
    0x0130:  312e 3000 0400 0000 0c00 0000 6464 732e  1.0.........dds.
    ...
    0x0230:  1100 0000 6464 732e 7065 726d 5f63 612e  ....dds.perm_ca.
    0x0240:  616c 676f 0000 0000 0d00 0000 4543 4453  algo........ECDS
    0x0250:  412d 5348 4132 3536 0000 0000 0000 0000  A-SHA256........
    0x0260:  0510 0800 0700 0080 0600 0080 0100 0000  ................

这个数据包要大得多，并且包含了可用于在 ROS 节点之间建立加密的信息。
我们很快就会看到，它实际上包含了一些在启用安全性时创建的安全配置文件。
想了解更多吗？
看看这篇优秀的论文 `Secure DDS 系统的网络侦察与漏洞挖掘 <https://arxiv.org/abs/1908.05310>`_，理解为什么这很重要。


显示加密的数据包
^^^^^^^^^^^^^^^^

现在使用 ``tcpdump`` 捕获数据包。
一个典型的数据包看起来如下：

.. code-block:: console

  $ sudo tcpdump -i any -X udp portrange 7401-7500
  21:18:14.531102 IP localhost.54869 > localhost.7415: UDP, length 328
    0x0000:  4500 0164 bb42 4000 4011 8044 7f00 0001  E..d.B@.@..D....
    0x0010:  7f00 0001 d655 1cf7 0150 ff63 5254 5053  .....U...P.cRTPS
    0x0020:  0203 010f daf7 10ce d977 449b bb33 f04a  .........wD..3.J
    0x0030:  3301 1400 0000 0003 492a 6066 8603 cdb5  3.......I*`f....
    0x0040:  9df6 5da6 8402 2136 0c01 1400 0000 0000  ..]...!6........
    0x0050:  0203 010f daf7 10ce d977 449b bb33 f04a  .........wD..3.J
    ...
    0x0130:  7905 d390 3201 1400 3ae5 0b60 3906 967e  y...2...:..`9..~
    0x0140:  5b17 fd42 de95 54b9 0000 0000 3401 1400  [..B..T.....4...
    0x0150:  42ae f04d 0559 84c5 7116 1c51 91ba 3799  B..M.Y..q..Q..7.
    0x0160:  0000 0000                                ....

这个 RTPS 数据包中的数据全部被加密。

除了这个数据包之外，你还应该看到带有节点名和 enclave 名的额外数据包；它们支持参数和服务等其他 ROS 特性。
这些数据包的加密选项也可以由安全策略控制。
