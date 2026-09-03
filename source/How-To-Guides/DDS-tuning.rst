.. redirect-from::

  Guides/DDS-tuning
  Troubleshooting/DDS-tuning

DDS 调优信息
============

本页提供了一些参数调优指导，这些调优被发现可以解决在实际场景中于 Linux 上使用各种 DDS 实现时所遇到的问题。
我们在 Linux 上或使用某个供应商时发现的问题，也可能出现在此处未记录的其他平台和供应商上。

以下建议是调优的起点；它们适用于特定的系统和环境，但调优可能会因多种因素而有所不同。
在调试时，你可能需要根据消息大小、网络拓扑等因素增大或减小这些值。

重要的是要认识到，调优参数可能会消耗资源，并可能影响系统中超出预期改进范围的部分。
在每种情况下，都应在可靠性的提升与任何负面影响之间进行权衡。

.. _cross-vendor-tuning:

跨供应商调优
------------

**问题：** 在有损（通常是 WiFi）连接上发送数据时，如果某些 IP 分片被丢弃，可能会出现问题，可能导致接收端的内核缓冲区被填满。

当一个 UDP 数据包至少缺少一个 IP 分片时，其余已接收的分片会填满内核缓冲区。
默认情况下，Linux 内核会在尝试重组数据包分片 30 秒后超时。
由于此时内核缓冲区已满（默认大小为 256KB），新的分片无法进入，因此连接会在很长一段时间内看似"挂起"。

此问题在所有 DDS 供应商中都是通用的，因此解决方案涉及调整内核参数。

**解决方案：** 使用 best-effort QoS 设置，而不是 reliable。

Best-effort 设置可以减少网络流量，因为 DDS 实现无需承担可靠通信的开销（在可靠通信中，发布者要求对发送给订阅者的消息进行确认，并且必须重新发送未正确接收的样本）。

但是，如果 IP 分片的内核缓冲区已满，症状仍然相同（阻塞 30 秒）。
此解决方案可以在无需调整参数的情况下在一定程度上改善该问题。

**解决方案：** 减小 ``ipfrag_time`` 参数的值。

``net.ipv4.ipfrag_time / /proc/sys/net/ipv4/ipfrag_time`` （默认 30 秒）：
IP 分片在内存中保留的时间（秒）。

例如，通过运行以下命令将该值减小到 3 秒：

.. code-block:: console

    $ sudo sysctl net.ipv4.ipfrag_time=3

减小此参数的值也会缩短没有分片进入的时间窗口。
该参数对传入的所有分片全局生效，因此需要在每种环境中考虑减小其值的可行性。

**解决方案：** 增大 ``ipfrag_high_thresh`` 参数的值。

``net.ipv4.ipfrag_high_thresh / /proc/sys/net/ipv4/ipfrag_high_thresh`` （默认：262144 字节）：
用于重组 IP 分片的最大内存。

例如，通过运行以下命令将该值增大到 128MB：

.. code-block:: console

    $ sudo sysctl net.ipv4.ipfrag_high_thresh=134217728     # (128 MB)

显著增大此参数的值是为了尽量确保缓冲区永远不会被完全填满。
但是，假设每个 UDP 数据包都缺少一个分片，该值可能需要非常高才能容纳在 ``ipfrag_time`` 时间窗口内接收到的所有数据。

**问题：** 发送带有大型可变大小非原始类型数组的自定义消息会导致很高的序列化/反序列化开销和 CPU 负载。
这可能会导致发布者因在 ``publish()`` 中花费过多时间而停滞，并且诸如 ``ros2 topic hz`` 之类的工具会低估消息实际接收的频率。
请注意，例如 ``builtin_interfaces/Time`` 也被视为非原始类型，会产生更高的序列化开销。
由于序列化开销的增加，当将自定义消息类型从 ROS 1 天真地迁移到 ROS 2 时，可能会观察到严重的性能下降。

**变通方案：** 使用多个原始类型数组，而不是单个自定义类型数组，或者打包成字节数组（例如 ``PointCloud2`` 消息的做法）。
例如，不要将 ``FooArray`` 消息定义为：

.. code-block:: bash

    Foo[] my_large_array

其中 ``Foo`` 定义为：

.. code-block:: bash

    uint64 foo_1
    uint32 foo_2

而是将 ``FooArray`` 定义为：

.. code-block:: bash

    uint64[] foo_1_array
    uint32[] foo_2_array

Fast RTPS 调优
--------------

**问题：** 在 WiFi 上运行时，Fast RTPS 会用大量数据或快速发布的数据淹没网络。

请参见 :ref:`跨供应商调优 <cross-vendor-tuning>` 下的解决方案。

.. _cyclonedds-tuning:

Cyclone DDS 调优
----------------

**问题：** Cyclone DDS 无法可靠地传递大型消息，即使使用了 reliable 设置并通过有线网络传输。

此问题应该会 `很快得到解决 <https://github.com/eclipse-cyclonedds/cyclonedds/issues/484>`_。
在此之前，我们提出了以下解决方案（使用 `此测试程序 <https://github.com/jacobperron/pc_pipe>`_ 进行调试）：

**解决方案：** 增大 Linux 内核最大接收缓冲区大小以及 Cyclone 使用的最小套接字接收缓冲区大小。

*为传输 9MB 消息所做的调整：*

通过运行以下命令设置最大接收缓冲区大小 ``rmem_max``：

 .. code-block:: console

    $ sudo sysctl -w net.core.rmem_max=2147483647

或者通过编辑 ``/etc/sysctl.d/10-cyclone-max.conf`` 文件来永久设置，使其内容为：

 .. code-block:: bash

    net.core.rmem_max=2147483647

接下来，为了设置 Cyclone 请求的最小套接字接收缓冲区大小，编写一个供 Cyclone 在启动时使用的配置文件，如下所示：

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

然后，每当你运行节点时，设置以下环境变量：

.. code-block:: bash

    CYCLONEDDS_URI=file:///absolute/path/to/config_file.xml

RTI Connext 调优
----------------

**问题：** Connext 无法可靠地传递大型消息，即使使用了 reliable 设置并通过有线网络传输。

**解决方案：** 使用此 `Connext QoS 配置文件 <https://github.com/jacobperron/pc_pipe/blob/master/etc/ROS2TEST_QOS_PROFILES.xml>`_，同时增大 ``rmem_max`` 参数。

通过运行以下命令设置最大接收缓冲区大小 ``rmem_max``：

 .. code-block:: console

    $ sudo sysctl -w net.core.rmem_max=4194304

通过将 Linux 内核中的 ``net.core.rmem_max`` 调优为 4MB，该 QoS 配置文件可以产生真正可靠的行为。

此配置已被证明能够通过 SHMEM|UDPv4 可靠地传递消息，并且在单台机器上仅使用 UDPv4 也能可靠传递。
还测试了多机配置，``rmem_max`` 分别为 4MB 和 20MB（两台机器通过 1Gbps 以太网连接），没有消息丢失，平均消息传递时间分别为 700ms 和 371ms。

在不配置内核 ``rmem_max`` 的情况下，同样的 Connext QoS 配置文件需要长达 12 秒才能完成数据传递。
但是，它至少始终能够完成传递。

**解决方案：** 使用 `Connext QoS 配置文件 <https://github.com/jacobperron/pc_pipe/blob/master/etc/ROS2TEST_QOS_PROFILES.xml>`_，但\ *不*\ 调整 ``rmem_max``。

ROS2TEST_QOS_PROFILES.xml 文件是根据 RTI 关于 `配置流量控制器 <https://community.rti.com/forum-topic/transfering-large-data-over-dds>`_ 的文档配置的。
它包含慢速、中速和快速流量控制器（见 Connext QoS 配置文件链接）。

在我们的场景中，中速流量控制器产生了最佳结果。
但是，控制器仍需要针对其运行的具体机器/网络/环境进行调优。
Connext 流量控制器可用于调优带宽及其发送数据的激进程度，不过一旦超过特定设置的带宽，性能就会开始下降。
