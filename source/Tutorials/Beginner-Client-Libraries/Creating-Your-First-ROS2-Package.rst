.. redirect-from::

    Tutorials/Creating-Your-First-ROS2-Package

.. _CreatePkg:

创建一个包
==========

**目标：** 使用 CMake 或 Python 创建一个新包，并运行其可执行文件。

**教程级别：** 入门

**时间：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

1 什么是 ROS 2 包？
^^^^^^^^^^^^^^^^^^^

包是 ROS 2 代码的组织单元。
如果你想能够安装你的代码或与他人共享它，那么你需要将其组织在一个包中。
有了包，你就可以发布你的 ROS 2 工作成果，并让其他人轻松地构建和使用它。

ROS 2 中的包创建使用 ament 作为构建系统，使用 colcon 作为构建工具。
你可以使用 CMake 或 Python 创建包，这两种方式都是官方支持的，不过也存在其他构建类型。

2 ROS 2 包由什么组成？
^^^^^^^^^^^^^^^^^^^^^^

ROS 2 Python 和 CMake 包各自有最低限度的必需内容：

.. tabs::

   .. group-tab:: CMake

      * ``CMakeLists.txt`` 文件，描述如何构建包内的代码
      * ``include/<package_name>`` 目录，包含包的公共头文件
      * ``package.xml`` 文件，包含包的元信息
      * ``src`` 目录，包含包的源代码

   .. group-tab:: Python

      * ``package.xml`` 文件，包含包的元信息
      * ``resource/<package_name>`` 包的标记文件
      * 当包有可执行文件时需要 ``setup.cfg``，这样 ``ros2 run`` 才能找到它们
      * ``setup.py``，包含如何安装包的说明
      * ``<package_name>`` - 一个与你的包同名的目录，供 ROS 2 工具查找你的包，包含 ``__init__.py``

最简单的包可能的文件结构如下：

.. tabs::

   .. group-tab:: CMake

      .. code-block:: console

        my_package/
             CMakeLists.txt
             include/my_package/
             package.xml
             src/

   .. group-tab:: Python

      .. code-block:: console

        my_package/
              package.xml
              resource/my_package
              setup.cfg
              setup.py
              my_package/


3 工作空间中的包
^^^^^^^^^^^^^^^^

单个工作空间可以包含任意数量的包，每个包都在自己的文件夹中。
你也可以在一个工作空间中拥有不同构建类型的包（CMake、Python 等）。
你不能有嵌套的包。

最佳实践是在工作空间中有一个 ``src`` 文件夹，并在其中创建你的包。
这样可以保持工作空间顶层的“整洁”。

一个简单的工作空间可能如下所示：

.. code-block:: console

  workspace_folder/
      src/
        cpp_package_1/
            CMakeLists.txt
            include/cpp_package_1/
            package.xml
            src/

        py_package_1/
            package.xml
            resource/py_package_1
            setup.cfg
            setup.py
            py_package_1/
        ...
        cpp_package_n/
            CMakeLists.txt
            include/cpp_package_n/
            package.xml
            src/


前置条件
--------

在按照 :doc:`上一个教程 <./Creating-A-Workspace/Creating-A-Workspace>` 的说明操作后，你应该已经有一个 ROS 2 工作空间。
你将在这个工作空间中创建你的包。


任务
----

1 创建一个包
^^^^^^^^^^^^

首先，:doc:`导入你的 ROS 2 安装 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`。

让我们使用你在 :ref:`上一个教程 <new-directory>` 中创建的工作空间 ``ros2_ws`` 来存放新包。

在运行包创建命令之前，请确保你位于 ``src`` 文件夹中。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ cd ~/ros2_ws/src

   .. group-tab:: macOS

     .. code-block:: console

       $ cd ~/ros2_ws/src

   .. group-tab:: Windows

     .. code-block:: console

       $ cd \ros2_ws\src

在 ROS 2 中创建新包的命令语法是：

.. tabs::

   .. group-tab:: CMake

      .. code-block:: console

        $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 <package_name>

   .. group-tab:: Python

      .. code-block:: console

        $ ros2 pkg create --build-type ament_python --license Apache-2.0 <package_name>

在本教程中，你将使用可选参数 ``--node-name`` 和 ``--license``。
``--node-name`` 选项会在包中创建一个简单的 Hello World 类型的可执行文件，而 ``--license`` 声明包的许可证信息。

在终端中输入以下命令：

.. tabs::

   .. group-tab:: CMake

      .. code-block:: console

        $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 --node-name my_node my_package

   .. group-tab:: Python

      .. code-block:: console

        $ ros2 pkg create --build-type ament_python --license Apache-2.0 --node-name my_node my_package

现在，在你的工作空间 ``src`` 目录中会有一个名为 ``my_package`` 的新文件夹。

运行命令后，你的终端将返回以下消息：

.. tabs::

   .. group-tab:: CMake

      .. code-block:: console

        going to create a new package
        package name: my_package
        destination directory: /home/user/ros2_ws/src
        package format: 3
        version: 0.0.0
        description: TODO: Package description
        maintainer: ['<name> <email>']
        licenses: ['Apache-2.0']
        build type: ament_cmake
        dependencies: []
        node_name: my_node
        creating folder ./my_package
        creating ./my_package/package.xml
        creating source and include folder
        creating folder ./my_package/src
        creating folder ./my_package/include/my_package
        creating ./my_package/CMakeLists.txt
        creating ./my_package/src/my_node.cpp

   .. group-tab:: Python

      .. code-block:: console

        going to create a new package
        package name: my_package
        destination directory: /home/user/ros2_ws/src
        package format: 3
        version: 0.0.0
        description: TODO: Package description
        maintainer: ['<name> <email>']
        licenses: ['Apache-2.0']
        build type: ament_python
        dependencies: []
        node_name: my_node
        creating folder ./my_package
        creating ./my_package/package.xml
        creating source folder
        creating folder ./my_package/my_package
        creating ./my_package/setup.py
        creating ./my_package/setup.cfg
        creating folder ./my_package/resource
        creating ./my_package/resource/my_package
        creating ./my_package/my_package/__init__.py
        creating folder ./my_package/test
        creating ./my_package/test/test_copyright.py
        creating ./my_package/test/test_flake8.py
        creating ./my_package/test/test_pep257.py
        creating ./my_package/my_package/my_node.py

你可以看到为新包自动生成的文件。

2 构建一个包
^^^^^^^^^^^^

将包放入工作空间特别有价值，因为你可以通过在工作空间根目录运行 ``colcon build`` 一次性构建许多包。
否则，你就必须逐个构建每个包。

返回到工作空间的根目录：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ cd ~/ros2_ws

   .. group-tab:: macOS

      .. code-block:: console

        $ cd ~/ros2_ws

   .. group-tab:: Windows

     .. code-block:: console

       $ cd \ros2_ws

现在你可以构建你的包了：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install

    Windows 不允许长路径，因此 ``merge-install`` 会将所有路径合并到 ``install`` 目录中。

回顾上一个教程，你的 ``ros2_ws`` 中还有 ``ros_tutorials`` 包。
你可能已经注意到，运行 ``colcon build`` 也构建了 ``turtlesim`` 包。
当你的工作空间中只有几个包时，这没什么问题，但当包很多时，``colcon build`` 可能会花费很长时间。

为了下次只构建 ``my_package`` 包，你可以运行：

.. code-block:: console

    $ colcon build --packages-select my_package

3 导入 setup 文件
^^^^^^^^^^^^^^^^^

要使用你的新包和可执行文件，首先打开一个新终端并导入你的主要 ROS 2 安装。

然后，在 ``ros2_ws`` 目录中运行以下命令来导入你的工作空间：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/local_setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/local_setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/local_setup.bat

现在你的工作空间已添加到你的路径中，你将能够使用新包的可执行文件。

4 使用包
^^^^^^^^

要运行你在创建包时使用 ``--node-name`` 参数创建的可执行文件，请输入以下命令：

.. code-block:: console

  $ ros2 run my_package my_node

这将在终端中返回一条消息：

.. tabs::

   .. group-tab:: CMake

      .. code-block:: console

        hello world my_package package

   .. group-tab:: Python

      .. code-block:: console

        Hi from my_package.

5 检查包内容
^^^^^^^^^^^^

在 ``ros2_ws/src/my_package`` 中，你将看到 ``ros2 pkg create`` 自动生成的文件和文件夹：

.. tabs::

   .. group-tab:: CMake

      .. code-block:: console

        CMakeLists.txt  include  package.xml  src

      ``my_node.cpp`` 位于 ``src`` 目录中。
      以后你所有自定义的 C++ 节点都将放在这里。

   .. group-tab:: Python

      .. code-block:: console

        my_package  package.xml  resource  setup.cfg  setup.py  test

      ``my_node.py`` 位于 ``my_package`` 目录中。
      以后你所有自定义的 Python 节点都将放在这里。

6 自定义 package.xml
^^^^^^^^^^^^^^^^^^^^

你可能已经注意到，在创建包后返回的消息中，``description`` 和 ``license`` 字段包含 ``TODO`` 注释。
这是因为包的描述和许可证声明不会自动设置，但如果你想要发布你的包，它们是必需的。
``maintainer`` 字段可能也需要填写。

从 ``ros2_ws/src/my_package`` 中，用你喜欢的文本编辑器打开 ``package.xml``：

.. tabs::

   .. group-tab:: CMake

    .. code-block:: xml

     <?xml version="1.0"?>
     <?xml-model
        href="http://download.ros.org/schema/package_format3.xsd"
        schematypens="http://www.w3.org/2001/XMLSchema"?>
     <package format="3">
      <name>my_package</name>
      <version>0.0.0</version>
      <description>TODO: Package description</description>
      <maintainer email="user@todo.todo">user</maintainer>
      <license>TODO: License declaration</license>

      <buildtool_depend>ament_cmake</buildtool_depend>

      <test_depend>ament_lint_auto</test_depend>
      <test_depend>ament_lint_common</test_depend>

      <export>
        <build_type>ament_cmake</build_type>
      </export>
     </package>

   .. group-tab:: Python

    .. code-block:: xml

     <?xml version="1.0"?>
     <?xml-model
        href="http://download.ros.org/schema/package_format3.xsd"
        schematypens="http://www.w3.org/2001/XMLSchema"?>
     <package format="3">
      <name>my_package</name>
      <version>0.0.0</version>
      <description>TODO: Package description</description>
      <maintainer email="user@todo.todo">user</maintainer>
      <license>TODO: License declaration</license>

      <test_depend>ament_copyright</test_depend>
      <test_depend>ament_flake8</test_depend>
      <test_depend>ament_pep257</test_depend>
      <test_depend>python3-pytest</test_depend>

      <export>
        <build_type>ament_python</build_type>
      </export>
     </package>

如果 ``maintainer`` 行没有自动为你填充，请填写你的姓名和电子邮件。
然后，编辑 ``description`` 行以概括该包：

.. code-block:: xml

  <description>Beginner client libraries tutorials practice package</description>

然后，更新 ``license`` 行。
你可以在 `这里 <https://opensource.org/licenses/alphabetical>`__ 阅读更多关于开源许可证的信息。
由于这个包仅用于练习，使用任何许可证都是安全的。
我们将使用 ``Apache-2.0``：

.. code-block:: xml

  <license>Apache-2.0</license>

编辑完成后别忘了保存。

在 license 标签下方，你会看到一些以 ``_depend`` 结尾的标签名。
这就是你的 ``package.xml`` 列出它对其他包的依赖项的地方，供 colcon 搜索。
``my_package`` 很简单，没有任何依赖项，但你会在接下来的教程中看到这个空间被使用。

.. tabs::

   .. group-tab:: CMake

      你现在已经完成了！

   .. group-tab:: Python

      ``setup.py`` 文件包含与 ``package.xml`` 相同的 ``description``、``maintainer`` 和 ``license`` 字段，所以你也需要设置这些字段。
      两个文件中的这些字段必须完全匹配。
      版本和名称（``package_name``）也需要完全匹配，并且应该会自动填充到两个文件中。

      用你喜欢的文本编辑器打开 ``setup.py``。

      .. code-block:: python

       from setuptools import find_packages, setup

       package_name = 'my_py_pkg'

       setup(
        name=package_name,
        version='0.0.0',
        packages=find_packages(exclude=['test']),
        data_files=[
            ('share/ament_index/resource_index/packages',
                    ['resource/' + package_name]),
            ('share/' + package_name, ['package.xml']),
          ],
        install_requires=['setuptools'],
        zip_safe=True,
        maintainer='TODO',
        maintainer_email='TODO',
        description='TODO: Package description',
        license='TODO: License declaration',
        tests_require=['pytest'],
        entry_points={
            'console_scripts': [
                    'my_node = my_py_pkg.my_node:main'
            ],
          },
       )

      编辑 ``maintainer``、``maintainer_email`` 和 ``description`` 行，使其与 ``package.xml`` 匹配。

      别忘了保存文件。


小结
----

你已经创建了一个包来组织你的代码，并让其他人可以轻松使用它。

你的包会自动填充必要的文件，然后你使用 colcon 构建它，以便在本地环境中使用它的可执行文件。

下一步
------

接下来，让我们给包添加一些有意义的内容。
你将从一个简单的发布者/订阅者系统开始，你可以选择用 :doc:`C++ <./Writing-A-Simple-Cpp-Publisher-And-Subscriber>` 或 :doc:`Python <./Writing-A-Simple-Py-Publisher-And-Subscriber>` 编写。
