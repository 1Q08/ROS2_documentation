.. redirect-from::

  Tutorials/Launch-system
  Tutorials/Launch-Files/Launch-system
  Tutorials/Launch/Launch-system

将 launch 文件集成到 ROS 2 包中
===============================

**目标：** 向 ROS 2 包添加一个 launch 文件

**教程级别：** 中级

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

先决条件
--------

你应该已经完成了关于如何 :doc:`创建 ROS 2 包 <../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>` 的教程。

和往常一样，别忘了在 :doc:`你打开的每个新终端 <../../Beginner-CLI-Tools/Configuring-ROS2-Environment>` 中 source ROS 2。

背景
----

在 :doc:`上一个教程 <Creating-Launch-Files>` 中，我们了解了如何编写一个独立的 launch 文件。
本教程将展示如何向现有包添加 launch 文件，以及通常使用的约定。

任务
----

1 创建一个包
^^^^^^^^^^^^

为包创建一个工作空间：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ mkdir -p launch_ws/src
      $ cd launch_ws/src

  .. group-tab:: macOS

    .. code-block:: console

      $ mkdir -p launch_ws/src
      $ cd launch_ws/src

  .. group-tab:: Windows

    .. code-block:: console

      $ md launch_ws\src
      $ cd launch_ws\src

.. tabs::

  .. group-tab:: Python 包

    .. code-block:: console

      $ ros2 pkg create --build-type ament_python --license Apache-2.0 py_launch_example

  .. group-tab:: C++ 包

    .. code-block:: console

      $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 cpp_launch_example

2 创建存放 launch 文件的结构
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

按照约定，一个包的所有 launch 文件都存储在包内的 ``launch`` 目录中。
确保在你上面创建的包的顶层创建一个 ``launch`` 目录。

.. tabs::

  .. group-tab:: Python 包

    对于 Python 包，包含你的包的目录应该如下所示：

    .. code-block:: console

      src/
        py_launch_example/
          launch/
          package.xml
          py_launch_example/
          resource/
          setup.cfg
          setup.py
          test/

    为了让 colcon 能够定位和使用我们的 launch 文件，我们需要告知 Python 的 setup 工具它们的存在。
    为此，打开 ``setup.py`` 文件，在顶部添加必要的 ``import`` 语句，并将 launch 文件包含到 ``setup`` 的 ``data_files`` 参数中：

    .. code-block:: python

      import os
      from glob import glob
      # Other imports ...

      package_name = 'py_launch_example'

      setup(
          # Other parameters ...
          data_files=[
              # ... Other data files
              # Include all launch files.
              (os.path.join('share', package_name, 'launch'), glob('launch/*'))
          ]
      )

  .. group-tab:: C++ 包

    对于 C++ 包，我们只需要调整 ``CMakeLists.txt`` 文件，在文件末尾（但在 ``ament_package()`` 之前）添加：

    .. code-block:: cmake

      # Install launch files.
      install(DIRECTORY
        launch
        DESTINATION share/${PROJECT_NAME}/
      )


3 编写 launch 文件
^^^^^^^^^^^^^^^^^^

.. tabs::

  .. group-tab:: XML launch 文件

    在你的 ``launch`` 目录中，创建一个名为 ``my_script_launch.xml`` 的新 launch 文件。
    ``_launch.xml`` 是 XML launch 文件推荐（但不是必需）的文件后缀。

    .. literalinclude:: launch/my_script_launch.xml
      :language: xml

  .. group-tab:: YAML launch 文件

    在你的 ``launch`` 目录中，创建一个名为 ``my_script_launch.yaml`` 的新 launch 文件。
    ``_launch.yaml`` 是 YAML launch 文件推荐（但不是必需）的文件后缀。

    .. literalinclude:: launch/my_script_launch.yaml
      :language: yaml

  .. group-tab:: Python launch 文件

    在你的 ``launch`` 目录中，创建一个名为 ``my_script_launch.py`` 的新 launch 文件。
    ``_launch.py`` 是 Python launch 文件推荐（但不是必需）的文件后缀。
    但是，launch 文件名需要以 ``launch.py`` 结尾，才能被 ``ros2 launch`` 识别和自动补全。

    你的 launch 文件应该定义 ``generate_launch_description()`` 函数，它返回一个 ``launch.LaunchDescription()`` 供 ``ros2 launch`` 动词使用。

    .. literalinclude:: launch/my_script_launch.py
      :language: python


4 构建和运行 launch 文件
^^^^^^^^^^^^^^^^^^^^^^^^

进入工作空间的顶层，并构建它：

.. code-block:: console

  $ colcon build

在 ``colcon build`` 成功并且你已 source 工作空间之后，你应该能够按如下方式运行 launch 文件：

.. tabs::

  .. group-tab:: Python 包

    .. tabs::

      .. group-tab:: XML launch 文件

        .. code-block:: console

          $ ros2 launch py_launch_example my_script_launch.xml

      .. group-tab:: YAML launch 文件

        .. code-block:: console

          $ ros2 launch py_launch_example my_script_launch.yaml

      .. group-tab:: Python launch 文件

        .. code-block:: console

          $ ros2 launch py_launch_example my_script_launch.py

  .. group-tab:: C++ 包

    .. tabs::

      .. group-tab:: XML launch 文件

        .. code-block:: console

          $ ros2 launch cpp_launch_example my_script_launch.xml

      .. group-tab:: YAML launch 文件

        .. code-block:: console

          $ ros2 launch cpp_launch_example my_script_launch.yaml

      .. group-tab:: Python launch 文件

        .. code-block:: console

          $ ros2 launch cpp_launch_example my_script_launch.py


文档
----

`launch 文档 <https://docs.ros.org/en/{DISTRO}/p/launch/architecture.html>`__ 提供了关于 ``launch_ros`` 中同样使用的一些概念的更多细节。

关于 launch 能力的更多文档/示例即将推出。
在此期间，请参阅源代码（https://github.com/ros2/launch 和 https://github.com/ros2/launch_ros）。
