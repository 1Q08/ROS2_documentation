使用 ROS 2 launch 启动可组合节点
================================

.. contents:: 目录
   :depth: 1
   :local:

在 :doc:`组合教程 <../Tutorials/Intermediate/Composition>` 中，你学习了可组合节点以及如何从命令行使用它们。
在 :doc:`启动教程 <../Tutorials/Intermediate/Launch/Launch-Main>` 中，你学习了启动文件以及如何使用它们来管理多个节点。

本指南将结合上述两个主题，教你如何为可组合节点编写启动文件。

准备工作
--------

有关安装 ROS 2 的详细信息，请参见 :doc:`安装说明 <../Installation>`。

如果你通过包安装 ROS 2，请确保已安装 ``ros-{DISTRO}-image-tools``。
如果你下载了归档文件或从源代码构建 ROS 2，它已经是安装的一部分。

启动文件示例
------------

下面是一个分别用 XML、YAML 和 Python 编写、用于启动可组合节点的启动文件。
这些启动文件都执行以下操作：

* 实例化一个带有重映射、自定义参数和额外参数的 cam2image 可组合节点
* 实例化一个带有重映射、自定义参数和额外参数的 showimage 可组合节点

.. tabs::

  .. group-tab:: XML

    .. literalinclude:: launch/composition_launch.xml
      :language: xml

  .. group-tab:: YAML

    .. literalinclude:: launch/composition_launch.yaml
      :language: yaml

  .. group-tab:: Python

    .. literalinclude:: launch/composition_launch.py
      :language: python


将可组合节点加载到现有容器中
----------------------------

容器有时可以由其他启动文件或从命令行启动。
在这种情况下，你需要将你的组件添加到现有容器中。
为此，你可以使用 ``LoadComposableNodes`` 将组件加载到给定的容器中。
下面的示例启动了与上面相同的节点。

.. tabs::

  .. group-tab:: XML

    .. literalinclude:: launch/composition_load_launch.xml
      :language: xml

  .. group-tab:: YAML

    .. literalinclude:: launch/composition_load_launch.yaml
      :language: yaml

  .. group-tab:: Python

    .. literalinclude:: launch/composition_load_launch.py
      :language: python


从命令行使用启动文件
--------------------

上面任何一个启动文件都可以使用 ``ros2 launch`` 运行。
将数据复制到本地文件中，然后运行：

.. code-block:: console

  $ ros2 launch <path_to_launch_file>

进程内通信
----------

上述所有示例都使用一个额外参数来设置节点之间的进程内通信。
有关进程内通信是什么的更多信息，请参见 :doc:`进程内通信教程 <../Tutorials/Demos/Intra-Process-Communication>`。

XML、YAML 还是 Python：我应该使用哪一种？
-----------------------------------------

有关更多信息，请参见 :doc:`Launch-file-different-formats` 中的 :ref:`讨论 <launch-file-different-formats-which>`。
