DDS 实现
========

以下是可用的 DDS 实现：

* :doc:`使用 Eclipse Cyclone DDS <DDS-Implementations/Working-with-Eclipse-CycloneDDS>` 说明如何使用 Cyclone DDS。
* :doc:`使用 eProsima Fast DDS <DDS-Implementations/Working-with-eProsima-Fast-DDS>` 说明如何使用 Fast DDS。
* :doc:`使用 RTI Connext DDS <DDS-Implementations/Working-with-RTI-Connext-DDS>` 说明如何使用 RTI Connext DDS。
* :doc:`使用 GurumNetworks GurumDDS <DDS-Implementations/Working-with-GurumNetworks-GurumDDS>` 说明如何使用 GurumDDS。

.. toctree::
   :hidden:
   :glob:

   DDS-Implementations/*

如果你想使用其他厂商之一，你需要在构建之前单独安装它们的软件。
ROS 2 构建过程会自动为那些已正确安装并加载的厂商构建支持。

一旦你安装了新的 RMW 厂商，你就可以在运行时更改所使用的厂商：:doc:`使用多个 RMW 实现 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。
