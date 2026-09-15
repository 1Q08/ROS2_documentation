.. redirect-from::

    DDS-and-ROS-middleware-implementations
    Concepts/About-Different-Middleware-Vendors

不同的 ROS 2 中间件供应商
=========================

.. contents:: 目录
   :local:

ROS 2 以 DDS/RTPS 作为其中间件，这种中间件提供发现、序列化与传输能力。
`这篇文章 <https://design.ros2.org/articles/ros_on_dds.html>`__ 详细解释了使用 DDS 实现以及/或 DDS 的 RTPS 线协议背后的动机。
简要地说，DDS 是一种端到端中间件，能够为 ROS 系统提供相关功能，例如分布式发现（与 ROS 1 中集中式不同）以及对运输过程中的不同「服务质量（QoS）」选项的控制。

`DDS <https://www.omg.org/omg-dds-portal>`__ 是一种行业标准，已被多家厂商实现，例如 RTI 的 `Connext DDS <https://www.rti.com/products/>`__、eProsima 的 `Fast DDS <https://fast-dds.docs.eprosima.com/>`__、Eclipse 的 `Cyclone DDS <https://projects.eclipse.org/projects/iot.cyclonedds>`__，以及 GurumNetworks 的 `GurumDDS <https://gurum.cc/index_eng>`__。
RTPS（又名 `DDSI-RTPS <https://www.omg.org/spec/DDSI-RTPS/About-DDSI-RTPS/>`__\ ）是 DDS 在网络中通信所使用的线协议。

ROS 2 支持多个 DDS/RTPS 实现，因为在选择供应商或实现时，并非“一个方案适配所有场景”。
在选择中间件实现时，您可能会考虑许多因素：例如许可证等后勤因素，或者平台可用性、计算占用等技术因素。
供应商可能提供多个 DDS 或 RTPS 实现，用于满足不同需求。
例如，RTI 的 Connext 实现就有几种变体，用于不同目的：一种专为微控制器设计，另一种面向需要特殊安全认证的应用（目前我们仅支持它们的标准桌面版本）。

要在 ROS 2 中使用 DDS/RTPS 实现，需要创建一个包含“\ **R**\ OS **M**\ iddle\ **w**\ are interface”（也就是 ``rmw`` 接口，或者直接叫 ``rmw``\ ）包，它通过 DDS 或 RTPS 实现的 API 和工具来实现抽象的 ROS 中间件接口。
为支持 DDS 实现而实现并维护 RMW 包需要大量工作，但至少支持若干实现仍很重要，因为这能确保 ROS 2 代码库不会绑定到单一实现上，用户也能依据项目需求切换实现。

支持的 RMW 实现
---------------

.. list-table::
   :header-rows: 1

   * - 产品名
     - 许可证
     - RMW 实现
     - 状态
   * - eProsima *Fast DDS*
     - Apache 2
     - ``rmw_fastrtps_cpp``
     - 完全支持。
       默认 RMW。
       随二进制发布包一起打包。
   * - Eclipse *Cyclone DDS*
     - Eclipse Public License v2.0
     - ``rmw_cyclonedds_cpp``
     - 完全支持。
       随二进制发布包一起打包。
   * - RTI *Connext DDS*
     - 商业，研究
     - ``rmw_connextdds``
     - 完全支持。
       支持包含在二进制中，但 Connext 需单独安装。
   * - GurumNetworks *GurumDDS*
     - 商业
     - ``rmw_gurumdds_cpp``
     - 社区支持。
       支持包含在二进制中，但 GurumDDS 需单独安装。

如需处理多个 RMW 实现的实用信息，请参阅 :doc:`“Working with multiple RMW implementations” <../../How-To-Guides/Working-with-multiple-RMW-implementations>` 教程。

多个 RMW 实现
-------------

当前活跃发行版的 ROS 2 二进制发布包开箱即支持多种 RMW 实现（Fast DDS、RTI Connext Pro、Eclipse Cyclone DDS、GurumNetworks GurumDDS）。
默认实现是 Fast DDS，它无需额外安装步骤，因为我们随二进制包一并分发。

如 Cyclone DDS、Connext 或 GurumDDS 之类的其他 RMW，可以通过 :doc:`安装额外包 <../../Installation/RMW-Implementations>` 来启用，而不必重建任何内容或替换已有包。

从源码构建的 ROS 2 工作区可同时构建并安装多个 RMW 实现。
在核心 ROS 2 代码编译时，只要检测到相关 DDS/RTPS 实现已正确安装并配置了相应环境变量，相关 RMW 实现也将一并构建。
例如，如果工作区中存在 `RTI Connext DDS 的 RMW 包 <https://github.com/ros2/rmw_connextdds>`__，并且也能找到 RTI 的 Connext Pro 安装环境，它就会被构建。

在许多场景中，不同 RMW 实现的节点可以相互通信，但并不是所有情况都成立。
下面列出一些厂商间通信配置不受支持的情况：

- Fast DDS <-> Connext
   - Fast DDS 发布的 ``WString`` 在 macOS 上无法被 Connext 正确接收
- Connext <-> Cyclone DDS
   - 不支持 ``WString`` 的发布/订阅通信

默认 RMW 实现
-------------

如果一个 ROS 2 工作区中安装了多个 RMW 实现，且 Fast DDS 可用，那么它会被选为默认 RMW 实现。
如果未安装 Fast DDS RMW 实现，那么将使用按 RMW 实现标识符字母顺序排列后的第一个实现。
该实现标识符是提供 RMW 实现的 ROS 包名，例如 ``rmw_cyclonedds_cpp``。
例如，如果已安装 ``rmw_cyclonedds_cpp`` 和 ``rmw_connextdds`` 两个 ROS 包，默认将是 ``rmw_connextdds``。
如果 ``rmw_fastrtps_cpp`` 被安装，那么它将成为默认实现。

参阅 :doc:`指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`，了解运行 ROS 2 示例时应指定哪种 RMW 实现。

.. _different-middleware-vendors-cross-vendor-communication:

跨厂商通信
----------

虽然不同 RMW 实现可能在有限场景下兼容，但这并不保证。
因此，建议用户确保分布式系统中的所有部分都使用相同的 ROS 版本和相同的 RMW 实现。
