非 DDS 实现
===========

* :doc:`使用 Zenoh <Non-DDS-Implementations/Working-with-Zenoh>` 说明如何使用 Zenoh。

.. toctree::
   :hidden:
   :glob:

   Non-DDS-Implementations/*

如果你想使用其他厂商之一，你需要在构建之前单独安装它们的软件。
ROS 2 构建过程会自动为那些已正确安装并加载的厂商构建支持。

一旦你安装了新的 RMW 厂商，你就可以在运行时更改所使用的厂商：:doc:`使用多个 RMW 实现 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。
