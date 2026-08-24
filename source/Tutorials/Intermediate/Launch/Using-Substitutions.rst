.. redirect-from::

    Tutorials/Launch-Files/Using-Substitutions
    Tutorials/Launch/Using-Substitutions

使用替换
========

**目标：** 了解 ROS 2 launch 文件中的替换。

**教程级别：** 中级

**时间：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

launch 文件用于启动节点、服务并执行进程。
这组 action 可以有影响其行为的参数。
替换可以用在参数中，以在描述可复用的 launch 文件时提供更多灵活性。
替换是只在执行 launch 描述期间才被求值的变量，可用于获取特定信息，如 launch 配置、环境变量，或求值一个任意的 Python 表达式。

本教程展示了 ROS 2 launch 文件中替换的使用示例。

先决条件
--------

本教程使用 :doc:`turtlesim <../../Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim>` 包。
本教程还假设你熟悉 :doc:`创建包 <../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>`。

和往常一样，别忘了在 :doc:`你打开的每个新终端 <../../Beginner-CLI-Tools/Configuring-ROS2-Environment>` 中 source ROS 2。

使用替换
--------

1 创建和设置包
^^^^^^^^^^^^^^

首先，创建一个名为 ``launch_tutorial`` 的新包：

.. tabs::

  .. group-tab:: Python 包

    创建一个 build_type 为 ``ament_python`` 的新包：

    .. code-block:: console

      $ ros2 pkg create --build-type ament_python --license Apache-2.0 launch_tutorial

  .. group-tab:: C++ 包

    创建一个 build_type 为 ``ament_cmake`` 的新包：

    .. code-block:: console

      $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 launch_tutorial

在该包内，创建一个名为 ``launch`` 的目录：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ mkdir launch_tutorial/launch

  .. group-tab:: macOS

    .. code-block:: console

      $ mkdir launch_tutorial/launch

  .. group-tab:: Windows

    .. code-block:: console

      $ md launch_tutorial/launch

最后，确保安装 launch 文件：

.. tabs::

  .. group-tab:: Python 包

    对包的 ``setup.py`` 添加以下更改：

    .. code-block:: python

      import os
      from glob import glob
      from setuptools import find_packages, setup

      package_name = 'launch_tutorial'

      setup(
          # Other parameters ...
          data_files=[
              # ... Other data files
              # Include all launch files.
              (os.path.join('share', package_name, 'launch'), glob('launch/*'))
          ]
      )

  .. group-tab:: C++ 包

    将以下代码追加到 ``CMakeLists.txt`` 中，位置在 ``ament_package()`` 之前：

    .. code-block:: cmake

      install(DIRECTORY
              launch
              DESTINATION share/${PROJECT_NAME}/
      )



2 父 launch 文件
^^^^^^^^^^^^^^^^

让我们创建一个会调用另一个 launch 文件并向其传递参数的 launch 文件。
这个 launch 文件可以是 YAML、XML 或 Python。

为此，在 ``launch_tutorial`` 包的 ``launch`` 文件夹中创建以下文件。

.. tabs::

  .. group-tab:: XML

    将完整代码复制并粘贴到 ``launch/example_main_launch.xml`` 文件中：

    .. literalinclude:: launch/example_main_launch.xml
      :language: xml

    ``$(find-pkg-share launch_tutorial)`` 替换用于查找 ``launch_tutorial`` 包的路径。
    然后将路径替换与 ``example_substitutions_launch.xml`` 文件名拼接。

    .. literalinclude:: launch/example_main_launch.xml
      :language: xml
      :lines: 4

    带有 ``turtlesim_ns`` 和 ``use_provided_red`` 参数的 ``background_r`` 变量被传递给 ``include`` action。
    ``$(var background_r)`` 替换用于使用 ``background_r`` 变量的值来定义 ``new_background_r`` 参数。

    .. literalinclude:: launch/example_main_launch.xml
      :language: xml
      :lines: 5-7

  .. group-tab:: YAML

    将完整代码复制并粘贴到 ``launch/example_main_launch.yaml`` 文件中：

    .. literalinclude:: launch/example_main_launch.yaml
      :language: yaml

    ``$(find-pkg-share launch_tutorial)`` 替换用于查找 ``launch_tutorial`` 包的路径。
    然后将路径替换与 ``example_substitutions_launch.yaml`` 文件名拼接。

    .. literalinclude:: launch/example_main_launch.yaml
      :language: yaml
      :lines: 8

    带有 ``turtlesim_ns`` 和 ``use_provided_red`` 参数的 ``background_r`` 变量被传递给 ``include`` action。
    ``$(var background_r)`` 替换用于使用 ``background_r`` 变量的值来定义 ``new_background_r`` 参数。

    .. literalinclude:: launch/example_main_launch.yaml
      :language: yaml
      :lines: 9-15


  .. group-tab:: Python

    将完整代码复制并粘贴到 ``launch/example_main_launch.py`` 文件中：

    .. literalinclude:: launch/example_main_launch.py
      :language: python

    ``FindPackageShare`` 替换用于查找 ``launch_tutorial`` 包的路径。
    然后使用 ``PathJoinSubstitution`` 替换将该包路径与 ``example_substitutions_launch.py`` 文件名拼接。

    .. literalinclude:: launch/example_main_launch.py
      :language: python
      :lines: 14-18

    带有 ``turtlesim_ns`` 和 ``use_provided_red`` 参数的 ``launch_arguments`` 字典被传递给 ``IncludeLaunchDescription`` action。

    .. literalinclude:: launch/example_main_launch.py
      :language: python
      :lines: 19-23


3 替换示例 launch 文件
^^^^^^^^^^^^^^^^^^^^^^

现在在同一个文件夹中创建替换 launch 文件：

.. tabs::

  .. group-tab:: XML

    创建文件 ``launch/example_substitutions_launch.xml`` 并插入以下代码：

    .. literalinclude:: launch/example_substitutions_launch.xml
      :language: xml

    定义了 ``turtlesim_ns``、``use_provided_red`` 和 ``new_background_r`` launch 配置。
    它们用于将 launch 参数的值存储在上述变量中，并将它们传递给所需的 action。
    launch 配置参数之后可以在 launch 描述的任何部分使用 ``$(var <name>)`` 替换来获取 launch 参数的值。

    ``arg`` 标签用于定义可以从上面的 launch 文件或从控制台传递的 launch 参数。

    .. literalinclude:: launch/example_substitutions_launch.xml
      :language: xml
      :lines: 3-5

    定义了 ``turtlesim_node`` 节点，其 ``namespace`` 使用 ``$(var <name>)`` 替换设置为 ``turtlesim_ns`` launch 配置值。

    .. literalinclude:: launch/example_substitutions_launch.xml
      :language: xml
      :lines: 7

    之后，使用相应的 ``cmd`` 标签定义了一个 ``executable`` action。
    该命令调用 turtlesim 节点的 spawn 服务。

    此外，使用 ``$(var <name>)`` 替换获取 ``turtlesim_ns`` launch 参数的值，以构造命令字符串。

    .. literalinclude:: launch/example_substitutions_launch.xml
      :language: xml
      :lines: 8

    对于更改 turtlesim 背景红色参数的 ``ros2 param`` ``executable`` action，使用了相同的方法。
    不同之处在于，只有提供的 ``new_background_r`` 参数等于 ``200`` 且 ``use_provided_red`` launch 参数设置为 ``True`` 时，定时器内的第二个 action 才会执行。
    ``if`` 谓词的求值使用 ``$(eval <python-expression>)`` 替换完成。

    .. literalinclude:: launch/example_substitutions_launch.xml
      :language: xml
      :lines: 9-13

  .. group-tab:: YAML

    创建文件 ``launch/example_substitutions_launch.yaml`` 并插入以下代码：

    .. literalinclude:: launch/example_substitutions_launch.yaml
      :language: yaml

    定义了 ``turtlesim_ns``、``use_provided_red`` 和 ``new_background_r`` launch 配置。
    它们用于将 launch 参数的值存储在上述变量中，并将它们传递给所需的 action。
    launch 配置参数之后可以在 launch 描述的任何部分使用 ``$(var <name>)`` 替换来获取 launch 参数的值。

    ``arg`` 标签用于定义可以从上面的 launch 文件或从控制台传递的 launch 参数。

    .. literalinclude:: launch/example_substitutions_launch.yaml
      :language: yaml
      :lines: 4-12

    定义了 ``turtlesim_node`` 节点，其 ``namespace`` 使用 ``$(var <name>)`` 替换设置为 ``turtlesim_ns`` launch 配置值。

    .. literalinclude:: launch/example_substitutions_launch.yaml
      :language: yaml
      :lines: 14-18

    之后，使用相应的 ``cmd`` 标签定义了一个 ``executable`` action。
    该命令调用 turtlesim 节点的 spawn 服务。

    此外，使用 ``$(var <name>)`` 替换获取 ``turtlesim_ns`` launch 参数的值，以构造命令字符串。

    .. literalinclude:: launch/example_substitutions_launch.yaml
      :language: yaml
      :lines: 19-20

    对于更改 turtlesim 背景红色参数的 ``ros2 param`` ``executable`` action，使用了相同的方法。
    不同之处在于，只有提供的 ``new_background_r`` 参数等于 ``200`` 且 ``use_provided_red`` launch 参数设置为 ``True`` 时，定时器内的第二个 action 才会执行。
    ``if`` 谓词的求值使用 ``$(eval <python-expression>)`` 替换完成。

    .. literalinclude:: launch/example_substitutions_launch.yaml
      :language: yaml
      :lines: 21-28

  .. group-tab:: Python

    创建文件 ``launch/example_substitutions_launch.py`` 并插入以下代码：

    .. literalinclude:: launch/example_substitutions_launch.py
      :language: python

    定义了 ``turtlesim_ns``、``use_provided_red`` 和 ``new_background_r`` launch 配置。
    它们用于在上述变量中表示 launch 参数的值，并将它们传递给所需的 action。
    这些 ``LaunchConfiguration`` 替换允许我们在 launch 描述的任何部分获取 launch 参数的值。

    ``DeclareLaunchArgument`` 用于定义可以从上面的 launch 文件或从控制台传递的 launch 参数。

    .. literalinclude:: launch/example_substitutions_launch.py
      :language: python
      :lines: 14-25

    定义了 ``turtlesim_node`` 节点，其 ``namespace`` 设置为 ``turtlesim_ns`` ``LaunchConfiguration`` 替换。

    .. literalinclude:: launch/example_substitutions_launch.py
      :language: python
      :lines: 26-31

    下一个 action ``ExecuteProcess`` 使用相应的 ``cmd`` 参数定义，用于调用 turtlesim 节点的 spawn 服务。

    此外，使用 ``LaunchConfiguration`` 替换在命令字符串中提供 ``turtlesim_ns`` launch 参数的值。

    .. literalinclude:: launch/example_substitutions_launch.py
      :language: python
      :lines: 32-41

    对于更改 turtlesim 背景红色参数的 ``change_background_r`` 和 ``change_background_r_conditioned`` action，使用了相同的方法。
    不同之处在于，只有提供的 ``new_background_r`` 参数等于 ``200`` 且 ``use_provided_red`` launch 参数设置为 ``True`` 时，下一个 action 才会执行。
    ``IfCondition`` 内部的求值使用 ``PythonExpression`` 替换完成。

    .. literalinclude:: launch/example_substitutions_launch.py
      :language: python
      :lines: 51-72

4 构建包
^^^^^^^^

进入工作空间的根目录，并构建包：

.. code-block:: console

  $ colcon build

另外，请记住在构建后 source 工作空间。

启动示例
--------

现在你可以使用 ``ros2 launch`` 命令来启动。

.. tabs::

  .. group-tab:: YAML

    .. code-block:: console

        $ ros2 launch launch_tutorial example_main_launch.yaml

  .. group-tab:: XML

    .. code-block:: console

        $ ros2 launch launch_tutorial example_main_launch.xml

  .. group-tab:: Python

    .. code-block:: console

        $ ros2 launch launch_tutorial example_main_launch.py

这将执行以下操作：

#. 启动一个蓝色背景的 turtlesim 节点
#. 生成第二只乌龟
#. 将颜色改为紫色
#. 如果提供的 ``background_r`` 参数为 ``200`` 且 ``use_provided_red`` 参数为 ``True``，则在两秒后将颜色改为粉色

修改 launch 参数
----------------

.. tabs::

  .. group-tab:: YAML

    如果你想更改提供的 launch 参数，可以更新 ``example_main_launch.yaml`` 中的 ``background_r`` 变量，或使用首选参数启动 ``example_substitutions_launch.yaml``。
    要查看可以传给 launch 文件的参数，运行以下命令：

    .. code-block:: console

        $ ros2 launch launch_tutorial example_substitutions_launch.yaml --show-args

  .. group-tab:: XML

    如果你想更改提供的 launch 参数，可以更新 ``example_main_launch.xml`` 中的 ``background_r`` 变量，或使用首选参数启动 ``example_substitutions_launch.xml``。
    要查看可以传给 launch 文件的参数，运行以下命令：

    .. code-block:: console

        $ ros2 launch launch_tutorial example_substitutions_launch.xml --show-args

  .. group-tab:: Python

    如果你想更改提供的 launch 参数，可以更新 ``example_main_launch.py`` 中 ``launch_arguments`` 字典里的参数，或使用首选参数启动 ``example_substitutions_launch.py``。
    要查看可以传给 launch 文件的参数，运行以下命令：

    .. code-block:: console

        $ ros2 launch launch_tutorial example_substitutions_launch.py --show-args

这将显示可以传给 launch 文件的参数及其默认值。

.. code-block:: console

    Arguments (pass arguments as '<name>:=<value>'):

        'turtlesim_ns':
            no description given
            (default: 'turtlesim1')

        'use_provided_red':
            no description given
            (default: 'False')

        'new_background_r':
            no description given
            (default: '200')

现在你可以按如下方式将所需的参数传给 launch 文件：

.. tabs::

  .. group-tab:: YAML

    .. code-block:: console

        $ ros2 launch launch_tutorial example_substitutions_launch.yaml turtlesim_ns:='turtlesim3' use_provided_red:='True' new_background_r:=200

  .. group-tab:: XML

    .. code-block:: console

        $ ros2 launch launch_tutorial example_substitutions_launch.xml turtlesim_ns:='turtlesim3' use_provided_red:='True' new_background_r:=200

  .. group-tab:: Python

    .. code-block:: console

        $ ros2 launch launch_tutorial example_substitutions_launch.py turtlesim_ns:='turtlesim3' use_provided_red:='True' new_background_r:=200

.. _BooleanSubstitutions:

布尔替换
--------

除了 ``$(eval <python-expression>)`` 之外，还提供了一组专用的布尔替换，用于比较值并组合结果。
它们可以在允许替换的任何地方使用，包括任何 action 的 ``if`` 和 ``unless`` 属性。

.. note::

   比较是基于每个参数的字符串表示进行的。

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - XML / YAML 名称
     - Python 类
     - 描述
   * - ``$(equals A B)``
     - ``EqualsSubstitution``
     - 如果 ``A`` 等于 ``B``，则解析为 ``'true'``，否则为 ``'false'``。
   * - ``$(not-equals A B)``
     - ``NotEqualsSubstitution``
     - 如果 ``A`` 不等于 ``B``，则解析为 ``'true'``，否则为 ``'false'``。
   * - ``$(and A B)``
     - ``AndSubstitution``
     - 两个布尔替换的逻辑与。
   * - ``$(or A B)``
     - ``OrSubstitution``
     - 两个布尔替换的逻辑或。
   * - ``$(any A B ...)``
     - ``AnySubstitution``
     - 如果任一参数为真，则解析为 ``'true'``。
   * - ``$(all A B ...)``
     - ``AllSubstitution``
     - 仅当每个参数都为真时，才解析为 ``'true'``。

上一节的 ``if`` 谓词也可以使用布尔替换而不是 Python 表达式来表达：

.. tabs::

  .. group-tab:: XML

    .. code-block:: xml

      <executable cmd="ros2 param set /turtlesim background_r $(var new_background_r)"
                  if="$(and $(equals $(var new_background_r) 200) $(var use_provided_red))"/>

  .. group-tab:: YAML

    .. code-block:: yaml

      - executable:
          cmd: ros2 param set /turtlesim background_r $(var new_background_r)
          if: $(and $(equals $(var new_background_r) 200) $(var use_provided_red))

  .. group-tab:: Python

    .. code-block:: python

      from launch.conditions import IfCondition
      from launch.substitutions import AndSubstitution, EqualsSubstitution, LaunchConfiguration

      ExecuteProcess(
          cmd=[[
              FindExecutable(name='ros2'),
              ' param set ',
              '/turtlesim background_r ',
              LaunchConfiguration('new_background_r'),
          ]],
          condition=IfCondition(
              AndSubstitution(
                  EqualsSubstitution(LaunchConfiguration('new_background_r'), '200'),
                  LaunchConfiguration('use_provided_red'),
              )
          ),
      )

文档
----

`launch 文档 <https://docs.ros.org/en/{DISTRO}/p/launch/doc/source/architecture.html>`_ 提供了关于可用替换的详细信息。

总结
----

在本教程中，你学习了在 launch 文件中使用替换。
你了解了它们创建可复用 launch 文件的可能性和能力。

你现在可以进一步了解 :doc:`在 launch 文件中使用事件处理器 <./Using-Event-Handlers>`，事件处理器用于定义一组复杂的规则，可用于动态修改 launch 文件。
