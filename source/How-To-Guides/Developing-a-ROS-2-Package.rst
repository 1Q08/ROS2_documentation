.. redirect-from::

    Developing-a-ROS-2-Package
    Guides/Developing-a-ROS-2-Package
    Tutorials/Developing-a-ROS-2-Package

开发 ROS 2 软件包
#################

.. contents:: 目录
   :depth: 2
   :local:

本教程将教你如何创建你的第一个 ROS 2 应用程序。
它面向希望学习如何在 ROS 2 中创建自定义软件包的开发者，而不是那些想使用 ROS 2 及其现有软件包的人。

前提条件
--------

- :doc:`安装 ROS <../../Installation>`

- `安装 colcon <https://colcon.readthedocs.io/en/released/user/installation.html>`__

- 通过 source 你的 ROS 2 安装来设置工作空间。

创建软件包
----------

所有 ROS 2 软件包都从在你的工作空间（通常是 ``~/ros2_ws/src``）中运行以下命令开始

.. code-block:: console

   $ ros2 pkg create --license Apache-2.0 <pkg-name> --dependencies [deps]

要为特定的客户端库创建软件包：

.. tabs::

  .. group-tab:: C++

    .. code-block:: console

       $ ros2 pkg create  --build-type ament_cmake --license Apache-2.0 <pkg-name> --dependencies [deps]

  .. group-tab:: Python

    .. code-block:: console

       $ ros2 pkg create  --build-type ament_python --license Apache-2.0 <pkg-name> --dependencies [deps]

然后你可以更新 ``package.xml``，填入软件包信息，例如依赖项、描述和作者信息。

C++ 软件包
^^^^^^^^^^

你主要会使用 ``add_executable()`` CMake 宏以及

.. code-block:: cmake

   ament_target_dependencies(<executable-name> [dependencies])

来创建可执行节点并链接依赖项。

要安装启动文件和节点，你可以使用 ``install()`` 宏，将其放在文件末尾但在 ``ament_package()`` 宏之前。

启动文件和节点的示例：

.. code-block:: cmake

   # Install launch files
   install(
     DIRECTORY launch
     DESTINATION share/${PROJECT_NAME}
   )

   # Install nodes
   install(
     TARGETS [node-names]
     DESTINATION lib/${PROJECT_NAME}
   )

Python 软件包
^^^^^^^^^^^^^

ROS 2 遵循 Python 使用 ``setuptools`` 的标准模块分发流程。
对于 Python 软件包，``setup.py`` 文件相当于 C++ 软件包的 ``CMakeLists.txt``。
有关分发的更多细节可参阅 `官方文档 <https://docs.python.org/3/distributing/index.html#distributing-index>`_。

在你的 ROS 2 软件包中，应该有一个如下所示的 ``setup.cfg`` 文件：

.. code-block:: ini

   [develop]
   script_dir=$base/lib/<package-name>
   [install]
   install_scripts=$base/lib/<package-name>

以及一个如下所示的 ``setup.py`` 文件：

.. code-block:: python

   import os
   from glob import glob
   from setuptools import setup

   package_name = 'my_package'

   setup(
       name=package_name,
       version='0.0.0',
       # Packages to export
       packages=[package_name],
       # Files we want to install, specifically launch files
       data_files=[
           # Install marker file in the package index
           ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
           # Include our package.xml file
           (os.path.join('share', package_name), ['package.xml']),
           # Include all launch files.
           (os.path.join('share', package_name, 'launch'), glob('launch/*')),
       ],
       # This is important as well
       install_requires=['setuptools'],
       zip_safe=True,
       author='ROS 2 Developer',
       author_email='ros2@ros.com',
       maintainer='ROS 2 Developer',
       maintainer_email='ros2@ros.com',
       keywords=['foo', 'bar'],
       classifiers=[
           'Intended Audience :: Developers',
           'License :: TODO',
           'Programming Language :: Python',
           'Topic :: Software Development',
       ],
       description='My awesome package.',
       license='TODO',
       # Like the CMakeLists add_executable macro, you can add your python
       # scripts here.
       entry_points={
           'console_scripts': [
               'my_script = my_package.my_script:main'
           ],
       },
   )


C++ 与 Python 混合软件包
^^^^^^^^^^^^^^^^^^^^^^^^

编写同时包含 C++ 和 Python 代码的软件包时，不使用 ``setup.py`` 文件和 ``setup.cfg`` 文件。
而应使用 :doc:`ament_cmake_python <./Ament-CMake-Python-Documentation>`。
