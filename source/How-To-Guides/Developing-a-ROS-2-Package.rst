.. redirect-from::

    Developing-a-ROS-2-Package
    Guides/Developing-a-ROS-2-Package
    Tutorials/Developing-a-ROS-2-Package

开发一个 ROS 2 包
#################

.. contents:: 目录
   :depth: 2
   :local:

本教程将教你如何创建你的第一个 ROS 2 应用。
它面向想要学习如何在 ROS 2 中创建自定义包的开发者，而不是想要使用 ROS 2 现有包的人。

前提条件
--------

- :doc:`安装 ROS <../../Installation>`

- `安装 colcon <https://colcon.readthedocs.io/en/released/user/installation.html>`__

- 通过 source 你的 ROS 2 安装来设置你的工作空间。

创建包
------

所有 ROS 2 包都从在你的工作空间（通常是 ``~/ros2_ws/src``）中运行以下命令开始

.. code-block:: console

   $ ros2 pkg create --license Apache-2.0 <pkg-name> --dependencies [deps]

要为特定的客户端库创建包：

.. tabs::

  .. group-tab:: C++

    .. code-block:: console

       $ ros2 pkg create  --build-type ament_cmake --license Apache-2.0 <pkg-name> --dependencies [deps]

  .. group-tab:: Python

    .. code-block:: console

       $ ros2 pkg create  --build-type ament_python --license Apache-2.0 <pkg-name> --dependencies [deps]

然后，你可以用包的依赖项、描述和作者等信息更新 ``package.xml``。

C++ 包
^^^^^^

你主要会用到 ``add_executable()`` CMake 宏，以及

.. code-block:: cmake

   ament_target_dependencies(<executable-name> [dependencies])

来创建可执行节点并链接依赖项。

要安装你的 launch 文件和节点，可以使用放在文件末尾附近、但在 ``ament_package()`` 宏之前的 ``install()`` 宏。

launch 文件和节点的示例：

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

Python 包
^^^^^^^^^

ROS 2 遵循 Python 使用 ``setuptools`` 的标准模块分发流程。
对于 Python 包，``setup.py`` 文件相当于 C++ 包的 ``CMakeLists.txt``。
有关分发的更多详情，请参见 `官方文档 <https://docs.python.org/3/distributing/index.html#distributing-index>`_。

在你的 ROS 2 包中，应该有一个如下所示的 ``setup.cfg`` 文件：

.. code-block:: ini

   [develop]
   script_dir=$base/lib/<package-name>
   [install]
   install_scripts=$base/lib/<package-name>

以及一个如下所示的 ``setup.py`` 文件：

.. code-block:: python

   import os
   from glob import glob
   from setuptools import find_packages, setup

   package_name = 'my_package'

   setup(
       name=package_name,
       version='0.0.0',
       # Packages to export
       packages=find_packages(exclude=['test']),
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


C++ 和 Python 混合包
^^^^^^^^^^^^^^^^^^^^

在编写同时包含 C++ 和 Python 代码的包时，不使用 ``setup.py`` 文件和 ``setup.cfg`` 文件。
而是使用 :doc:`ament_cmake_python <./Ament-CMake-Python-Documentation>`。
