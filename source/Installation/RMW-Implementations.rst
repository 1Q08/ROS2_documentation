.. redirect-from::

    Installation/DDS-Implementations

RMW 实现
========

默认情况下，ROS 2 使用 DDS 作为其 `中间件 <https://design.ros2.org/articles/ros_on_dds.html>`__。
它与多种 DDS 或 RTPS（DDS 有线协议）供应商兼容。
目前支持 eProsima 的 Fast DDS、RTI 的 Connext DDS、Eclipse Cyclone DDS 以及 GurumNetworks GurumDDS。

它还支持 Zenoh 等非 DDS 的 RMW 实现。

关于各发行版所支持的 RMW 供应商，请参见 `REP-2000 <https://reps.openrobotics.org/rep-2000/>`__。

默认的 RMW 供应商是 eProsima 的 Fast DDS。

查看所有可能的选项：

.. toctree::
   :hidden:
   :glob:

   RMW-Implementations/*

* :doc:`DDS 实现 <RMW-Implementations/DDS-Implementations>` 介绍如何使用 DDS。
* :doc:`非 DDS 实现 <RMW-Implementations/Non-DDS-Implementations>` 介绍如何使用非 DDS 实现。
