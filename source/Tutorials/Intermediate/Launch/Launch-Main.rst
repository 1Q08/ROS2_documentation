.. redirect-from::

    Tutorials/Launch-Files/Launch-Main
    Tutorials/Launch/Launch-Main

.. _LaunchFilesMain:

启动
====

ROS 2 Launch 文件允许你同时启动和配置多个包含 ROS 2 节点的可执行文件。

.. toctree::
   :hidden:

   Creating-Launch-Files
   Launch-system
   Using-Substitutions
   Using-Event-Handlers
   Using-ROS2-Launch-For-Large-Projects

#. :doc:`创建一个 launch 文件 <./Creating-Launch-Files>`。

   了解如何创建一个能够一次性启动节点及其配置的 launch 文件。

#. :doc:`启动和监控多个节点 <./Launch-system>`。

   更深入地了解 launch 文件的工作原理。

#. :doc:`使用替换 <./Using-Substitutions>`。

   使用替换在描述可复用的 launch 文件时提供更多灵活性。

#. :doc:`使用事件处理器 <./Using-Event-Handlers>`。

   使用事件处理器来监控进程状态，或定义一套复杂的规则，用于动态修改 launch 文件。

#. :doc:`管理大型项目 <./Using-ROS2-Launch-For-Large-Projects>`。

   为大型项目组织 launch 文件，以便它们能在不同场景下尽可能复用。
   查看不同 launch 工具的用法示例，如参数、YAML 文件、remapping、命名空间、默认参数和 RViz 配置。

.. note::

   如果你来自 ROS 1，可以使用 :doc:`ROS Launch 迁移指南 <../../../How-To-Guides/Migrating-from-ROS1/Migrating-Launch-Files>` 来帮助你将 launch 文件迁移到 ROS 2。
