.. redirect-from::

    Installation/DDS-Implementations

RMW 实现
========

默认情况下，ROS 2 使用 DDS 作为其中间件（`middleware <https://design.ros2.org/articles/ros_on_dds.html>`__）。
它与多个 DDS 或 RTPS（DDS 线协议）厂商兼容。
目前支持 eProsima 的 Fast DDS、RTI 的 Connext DDS、Eclipse Cyclone DDS 以及 GurumNetworks GurumDDS。

它还支持 Zenoh 等非 DDS 的 RMW 实现。

有关各发行版支持的 RMW 厂商，请参阅 `REP-2000 <https://reps.openrobotics.org/rep-2000/>`__。

默认的 RMW 厂商是 eProsima 的 Fast DDS。

查看所有可选方案：

.. toctree::
   :hidden:
   :glob:

   RMW-Implementations/*

* :doc:`DDS 实现 <RMW-Implementations/DDS-Implementations>` 说明如何使用 DDS。
* :doc:`非 DDS 实现 <RMW-Implementations/Non-DDS-Implementations>` 说明如何使用非 DDS 实现。
