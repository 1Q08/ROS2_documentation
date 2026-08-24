.. redirect-from::

  Guides/Launch-file-different-formats

使用 XML、YAML 和 Python 编写 ROS 2 启动文件
============================================

.. contents:: 目录
   :depth: 2
   :local:

ROS 2 启动文件可以用 XML、YAML 和 Python 编写。
本指南展示了如何使用这些不同的格式来完成相同的任务，并讨论了一些关于何时使用每种格式的内容。

启动文件示例
------------

下面是一个分别用 XML、YAML 和 Python 实现的启动文件。
每个启动文件都执行以下操作：

* 设置带默认值的命令行参数
* 包含另一个启动文件
* 在另一个命名空间中包含另一个启动文件
* 启动一个节点并设置其命名空间
* 启动一个节点，设置其命名空间，并在该节点中设置参数（使用这些参数）
* 创建一个节点，将消息从一个话题重映射到另一个话题

.. tabs::

   .. group-tab:: XML

      .. literalinclude:: launch/different_formats_launch.xml
        :language: xml

   .. group-tab:: YAML

      .. literalinclude:: launch/different_formats_launch.yaml
        :language: yaml

   .. group-tab:: Python

      .. literalinclude:: launch/different_formats_launch.py
        :language: python


从命令行使用启动文件
--------------------

启动
^^^^

上面任何一个启动文件都可以使用 ``ros2 launch`` 运行。
要在本地尝试它们，你可以创建一个新的包并使用

.. code-block:: console

  $ ros2 launch <package_name> <launch_file_name>

或者通过指定启动文件的路径直接运行该文件

.. code-block:: console

  $ ros2 launch <path_to_launch_file>

设置参数
^^^^^^^^

要设置传递给启动文件的参数，你应该使用 ``key:=value`` 语法。
例如，你可以通过以下方式设置 ``background_r`` 的值：

.. code-block:: console

  $ ros2 launch <package_name> <launch_file_name> background_r:=255

或者

.. code-block:: console

  $ ros2 launch <path_to_launch_file> background_r:=255

控制小海龟
^^^^^^^^^^

要测试重映射是否正常工作，你可以在另一个终端中运行以下命令来控制小海龟：

.. code-block:: console

  $ ros2 run turtlesim turtle_teleop_key --ros-args --remap __ns:=/turtlesim1


.. _launch-file-different-formats-which:

XML、YAML 还是 Python：我应该使用哪一种？
-----------------------------------------

.. note::

  ROS 1 中的启动文件是用 XML 编写的，因此对于从 ROS 1 转来的用户来说，XML 可能是最熟悉的。
  要了解有哪些变化，你可以访问 :doc:`Migrating-from-ROS1/Migrating-Launch-Files`。

对于大多数应用来说，选择哪种 ROS 2 启动格式取决于开发者的偏好。
但是，如果你的启动文件需要 XML 或 YAML 无法实现的灵活性，你可以使用 Python 来编写启动文件。
使用 Python 编写 ROS 2 启动文件更灵活，原因有以下两点：

* Python 是一种脚本语言，因此你可以在启动文件中利用该语言及其库。
* `ros2/launch <https://github.com/ros2/launch>`_ （通用启动功能）和 `ros2/launch_ros <https://github.com/ros2/launch_ros>`_ （ROS 2 特定启动功能）都是用 Python 编写的，因此你可以更低层级地访问 XML 和 YAML 可能未暴露的启动功能。

话虽如此，用 Python 编写的启动文件可能比 XML 或 YAML 更复杂、更冗长。
