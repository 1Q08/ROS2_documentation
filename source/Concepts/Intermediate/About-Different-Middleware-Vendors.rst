.. redirect-from::

    DDS-and-ROS-middleware-implementations
    Concepts/About-Different-Middleware-Vendors

不同的 ROS 2 中间件供应商
=========================

.. contents:: 目录
   :local:

ROS 2 构建在 DDS/RTPS 之上作为其中间件，它提供发现、序列化和传输功能。
`这篇文章 <https://design.ros2.org/articles/ros_on_dds.html>`__ 详细解释了使用 DDS 实现和/或 DDS 的 RTPS 线协议背后的动机。
总之，DDS 是一种端到端的中间件，它提供与 ROS 系统相关的功能，例如分布式发现（不像 ROS 1 那样集中式）以及对传输的不同“服务质量”选项的控制。

`DDS <https://www.omg.org/omg-dds-portal>`__ 是一个由众多供应商实现的行业标准，例如 RTI 的 `Connext DDS <https://www.rti.com/products/>`__、eProsima 的 `Fast DDS <https://fast-dds.docs.eprosima.com/>`__、Eclipse 的 `Cyclone DDS <https://projects.eclipse.org/projects/iot.cyclonedds>`__ 或 GurumNetworks 的 `GurumDDS <https://gurum.cc/index_eng>`__。
RTPS（又称 `DDSI-RTPS <https://www.omg.org/spec/DDSI-RTPS/About-DDSI-RTPS/>`__\ ）是 DDS 用于在网络上通信的线协议。

ROS 2 支持多种 DDS/RTPS 实现，因为在选择供应商/实现时，并非“一刀切”。
在选择中间件实现时，你可能会考虑许多因素：诸如许可证之类的物流考虑，或诸如平台可用性或计算占用之类的技术考虑。
供应商可能会提供多个针对不同需求的 DDS 或 RTPS 实现。
例如，RTI 的 Connext 实现有几种用途不同的变体，比如一种专门针对微控制器，另一种针对需要特殊安全认证的应用（我们目前只支持他们的标准桌面版本）。

为了在 ROS 2 中使用 DDS/RTPS 实现，需要创建一个 “\ **R**\ OS **M**\ iddle\ **w**\ are interface”（又称 ``rmw`` 接口或简称 ``rmw``\ ）包，它使用 DDS 或 RTPS 实现的 API 和工具来实现抽象的 ROS 中间件接口。
实现和维护支持 DDS 实现的 RMW 包需要大量工作，但至少支持几种实现对于确保 ROS 2 代码库不绑定到任何一个特定实现非常重要，因为用户可能希望根据其项目的需要切换实现。

支持的 RMW 实现
---------------

.. list-table::
   :header-rows: 1

   * - 产品名称
     - 许可证
     - RMW 实现
     - 状态
   * - eProsima *Fast DDS*
     - Apache 2
     - ``rmw_fastrtps_cpp``
     - 完全支持。
       默认 RMW。
       随二进制发行版打包。
   * - Eclipse *Cyclone DDS*
     - Eclipse Public License v2.0
     - ``rmw_cyclonedds_cpp``
     - 完全支持。
       随二进制发行版打包。
   * - RTI *Connext DDS*
     - 商业、研究
     - ``rmw_connextdds``
     - 完全支持。
       二进制中已包含支持，但 Connext 需要单独安装。
   * - GurumNetworks *GurumDDS*
     - 商业
     - ``rmw_gurumdds_cpp``
     - 社区支持。
       二进制中已包含支持，但 GurumDDS 需要单独安装。

有关使用多种 RMW 实现的实用信息，请参阅 :doc:`“使用多种 RMW 实现” <../../How-To-Guides/Working-with-multiple-RMW-implementations>` 教程。

多种 RMW 实现
-------------

当前活跃发行版的 ROS 2 二进制发行版开箱即用地内置支持多种 RMW 实现（Fast DDS、RTI Connext Pro、Eclipse Cyclone DDS、GurumNetworks GurumDDS）。
默认是 Fast DDS，它无需任何额外安装步骤即可工作，因为我们将其随二进制包一起分发。

其他 RMW（如 Cyclone DDS、Connext 或 GurumDDS）可以通过 :doc:`安装额外的包 <../../Installation/RMW-Implementations>` 来启用，但无需重建任何内容或替换任何现有包。

从源代码构建的 ROS 2 工作空间可以同时构建和安装多种 RMW 实现。
在编译核心 ROS 2 代码时，如果相关的 DDS/RTPS 实现已正确安装并且已配置相关的环境变量，则会构建找到的任何 RMW 实现。
例如，如果 `RTI Connext DDS 的 RMW 包 <https://github.com/ros2/rmw_connextdds>`__ 的代码在工作空间中，那么如果也能找到 RTI Connext Pro 的安装，它就会被构建。

在许多情况下，你会发现使用不同 RMW 实现的节点能够相互通信，但这并非在所有情况下都成立。
以下是不受支持的跨供应商通信配置列表：

- Fast DDS <-> Connext
   - Fast DDS 发布的 ``WString`` 在 macOS 上无法被 Connext 正确接收
- Connext <-> Cyclone DDS
   - 不支持 ``WString`` 的发布/订阅通信

默认 RMW 实现
-------------

如果 ROS 2 工作空间有多种 RMW 实现，且 Fast DDS 可用，则选择 Fast DDS 作为默认 RMW 实现。
如果未安装 Fast DDS RMW 实现，则将使用按字母顺序排列的第一个 RMW 实现标识符对应的 RMW 实现。
实现标识符是提供 RMW 实现的 ROS 包的名称，例如 ``rmw_cyclonedds_cpp``。
例如，如果同时安装了 ``rmw_cyclonedds_cpp`` 和 ``rmw_connextdds`` ROS 包，则 ``rmw_connextdds`` 将成为默认实现。
如果安装了 ``rmw_fastrtps_cpp``，则它将成为默认实现。

有关如何在运行 ROS 2 示例时指定要使用的 RMW 实现，请参阅 :doc:`指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。

.. _different-middleware-vendors-cross-vendor-communication:

跨供应商通信
------------

虽然不同的 RMW 实现在有限的情况下可能兼容，但这并不能保证。
因此，建议用户确保分布式系统的所有部分都使用相同的 ROS 版本和相同的 RMW 实现。
