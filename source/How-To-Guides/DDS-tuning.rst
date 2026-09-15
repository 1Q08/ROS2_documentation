.. redirect-from::

  Guides/DDS-tuning
  Troubleshooting/DDS-tuning

DDS 调优信息
============

本页提供了一些参数调优指南，这些调优在真实场景中用于解决在 Linux 上使用各种 DDS 实现时遇到的问题。
我们在此记录的 Linux 上或使用某个供应商时发现的问题，也可能出现在此处未记录的其他平台和供应商上。

下面的建议只是调优的起点；它们在特定的系统和环境中行之有效，但调优结果可能因消息大小、网络拓扑等多种因素而异。
在调试时，你可能需要根据实际情况增大或减小这些数值。

需要注意的是，参数调优可能会以消耗资源为代价，并且可能影响系统中超出预期改进范围的部分。
对于每一种具体情况，都应当权衡提高可靠性所带来的收益与可能产生的负面影响。

.. _cross-vendor-tuning:

跨供应商调优
------------

**问题：** 在丢包（通常是 WiFi）连接上发送数据时，一旦某些 IP 分片被丢弃就会变得有问题，可能导致接收端的内核缓冲区被填满。

当一个 UDP 数据包缺少至少一个 IP 分片时，其余已接收的分片会填满内核缓冲区。
默认情况下，Linux 内核在尝试重组数据包分片 30 秒后会超时。
由于此时内核缓冲区已满（默认大小为 256KB），不再有新的分片能够进入，因此连接会看似长时间“挂起”。

这个问题在所有 DDS 供应商中都普遍存在，因此解决方案都涉及调整内核参数。

**解决方案：** 使用 best-effort QoS 设置，而不是 reliable。

best-effort 设置可以减少网络流量，因为 DDS 实现不必承担可靠通信的开销——在可靠通信中，发布者需要为发送给订阅者的消息获取确认，并且必须重发未被正确接收的样本。

不过，如果用于 IP 分片的内核缓冲区仍然被填满，症状还是一样（阻塞 30 秒）。
在不调整参数的情况下，该解决方案应当能在一定程度上改善此问题。

**解决方案：** 减小 ``ipfrag_time`` 参数的值。

``net.ipv4.ipfrag_time / /proc/sys/net/ipv4/ipfrag_time`` (default 30s) :
在内存中保留 IP 分片的秒数。

例如，可以通过运行以下命令将其减小为 3 秒：

.. code-block:: console

    $ sudo sysctl net.ipv4.ipfrag_time=3

减小该参数的值也会缩短接收不到任何分片的时间窗口。
该参数对所有传入分片都是全局生效的，因此需要针对每种环境评估减小其值的可行性。

**解决方案：** 增大 ``ipfrag_high_thresh`` 参数的值。

``net.ipv4.ipfrag_high_thresh / /proc/sys/net/ipv4/ipfrag_high_thresh`` (default: 262144 bytes):
用于重组 IP 分片的最大内存。

例如，可以通过运行以下命令将其增大到 128MB：

.. code-block:: console

    $ sudo sysctl net.ipv4.ipfrag_high_thresh=134217728     # (128 MB)

大幅增大该参数的值是为了尽量确保缓冲区永远不会被完全填满。
然而，假设每个 UDP 数据包都缺少一个分片，那么要容纳 ``ipfrag_time`` 时间窗口内收到的所有数据，该值可能必须非常大。

**问题：** 发送带有大量非基本类型变长数组的自定义消息会导致很高的序列化/反序列化开销和 CPU 负载。
这可能导致发布者因在 ``publish()`` 中耗费过多时间而停滞，并使 ``ros2 topic hz`` 之类的工具低报实际接收到的消息频率。
请注意，例如 ``builtin_interfaces/Time`` 也被视为非基本类型，同样会带来更高的序列化开销。
由于序列化开销增加，在把自定义消息类型从 ROS 1 直接迁移到 ROS 2 时，可以观察到严重的性能下降。

**变通方法：** 使用多个基本类型数组，而不是单个自定义类型数组，或者像 ``PointCloud2`` 消息那样打包成字节数组。
例如，不要像下面这样定义 ``FooArray`` 消息：

.. code-block:: bash

    Foo[] my_large_array

其中 ``Foo`` 定义为：

.. code-block:: bash

    uint64 foo_1
    uint32 foo_2

而应把 ``FooArray`` 定义为：

.. code-block:: bash

    uint64[] foo_1_array
    uint32[] foo_2_array

Fast RTPS 调优
--------------

**问题：** 在 WiFi 上运行时，Fast RTPS 会用大块数据或快速发布的数据淹没网络。

请参阅 :ref:`跨供应商调优 <cross-vendor-tuning>` 下的解决方案。

.. _cyclonedds-tuning:

Cyclone DDS 调优
----------------

**问题：** 尽管使用了 reliable 设置并通过有线网络传输，Cyclone DDS 仍无法可靠地投递大消息。

此问题应当会 `很快得到解决 <https://github.com/eclipse-cyclonedds/cyclonedds/issues/484>`_。
在此之前，我们想出了以下解决方案（使用 `这个测试程序 <https://github.com/jacobperron/pc_pipe>`_ 进行调试）：

**解决方案：** 增大 Linux 内核的最大接收缓冲区大小，以及 Cyclone 使用的最小套接字接收缓冲区大小。

*为处理 9MB 消息所做的调整：*

通过运行以下命令设置最大接收缓冲区大小 ``rmem_max``：

 .. code-block:: console

    $ sudo sysctl -w net.core.rmem_max=2147483647

或者通过编辑 ``/etc/sysctl.d/10-cyclone-max.conf`` 文件使其包含以下内容，从而永久设置：

 .. code-block:: bash

    net.core.rmem_max=2147483647

接下来，为了设置 Cyclone 请求的最小套接字接收缓冲区大小，请写出一个供 Cyclone 启动时使用的配置文件，如下所示：

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8" ?>
  <CycloneDDS xmlns="https://cdds.io/config" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://cdds.io/config
  https://raw.githubusercontent.com/eclipse-cyclonedds/cyclonedds/master/etc/cyclonedds.xsd">
      <Domain id="any">
          <Internal>
              <SocketReceiveBufferSize min="10MB"/>
          </Internal>
      </Domain>
  </CycloneDDS>

然后，每当你要运行节点时，设置以下环境变量：

.. code-block:: bash

    CYCLONEDDS_URI=file:///absolute/path/to/config_file.xml

RTI Connext 调优
----------------

**问题：** 尽管使用了 reliable 设置并通过有线网络传输，Connext 仍无法可靠地投递大消息。

**解决方案：** 使用这个 `Connext QoS 配置档 <https://github.com/jacobperron/pc_pipe/blob/master/etc/ROS2TEST_QOS_PROFILES.xml>`_，同时增大 ``rmem_max`` 参数。

通过运行以下命令设置最大接收缓冲区大小 ``rmem_max``：

 .. code-block:: console

    $ sudo sysctl -w net.core.rmem_max=4194304

通过在 Linux 内核中把 ``net.core.rmem_max`` 调优到 4MB，该 QoS 配置档可以实现真正可靠的行为。

此配置已被证明能够通过 SHMEM|UDPv4 可靠地投递消息，并且在一台机器上仅使用 UDPv4 时也是如此。
还测试了多机配置，``rmem_max`` 分别为 4MB 和 20MB（两台机器通过 1Gbps 以太网连接），均无消息丢失，平均消息投递时间分别为 700ms 和 371ms。

在未配置内核 ``rmem_max`` 的情况下，同一个 Connext QoS 配置档最多需要 12 秒才能完成数据投递。
不过，它至少始终能够完成投递。

**解决方案：** 使用 `Connext QoS 配置档 <https://github.com/jacobperron/pc_pipe/blob/master/etc/ROS2TEST_QOS_PROFILES.xml>`_，而 *不* 调整 ``rmem_max``。

ROS2TEST_QOS_PROFILES.xml 文件是参照 RTI 关于 `配置流控制器 <https://community.rti.com/forum-topic/transfering-large-data-over-dds>`_ 的文档配置的。
它包含慢速、中速和快速流控制器（见 Connext QoS 配置档链接）。

对于我们的场景，中速流控制器取得了最佳效果。
不过，这些控制器仍需针对其运行的具体机器/网络/环境进行调优。
Connext 流控制器可用来调优带宽及其发送数据的激进程度，不过一旦超过了某个特定设置的带宽上限，性能就会开始下降。
