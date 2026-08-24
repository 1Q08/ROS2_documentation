.. redirect-from::

  Guides/Ament-CMake-Python-Documentation

ament_cmake_python 用户文档
===========================

``ament_cmake_python`` 是一个包，为包含 Python 代码的 ``ament_cmake`` 构建类型的包提供 CMake 函数。
更多信息请参见 :doc:`ament_cmake 用户文档 <Ament-CMake-Documentation>`。

.. note::

   纯 Python 包在大多数情况下应使用 ``ament_python`` 构建类型。
   要创建 ``ament_python`` 包，请参见 :doc:`创建你的第一个 ROS 2 包 <../Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>`。
   ``ament_cmake_python`` 只应在无法使用上述方式的情况下使用，例如混合 C/C++ 和 Python 代码时。


.. contents:: 目录
   :depth: 2
   :local:

基础
----

基本项目大纲
^^^^^^^^^^^^

一个名为 "my_project"、使用 ``ament_cmake`` 构建类型并使用 ``ament_cmake_python`` 的包的大纲如下所示：

.. code-block::

   .
   └── my_project
       ├── CMakeLists.txt
       ├── package.xml
       └── my_project
           ├── __init__.py
           └── my_script.py

``__init__.py`` 文件可以为空，但它是必需的，用于`让 Python 将包含它的目录视为一个包 <https://docs.python.org/3/tutorial/modules.html#packages>`__。
在 ``CMakeLists.txt`` 旁边也可以有一个 ``src`` 或 ``include`` 目录，用于存放 C/C++ 代码。

使用 ament_cmake_python
^^^^^^^^^^^^^^^^^^^^^^^

该包必须在其 ``package.xml`` 中声明对 ``ament_cmake_python`` 的依赖。

.. code-block:: xml

   <buildtool_depend>ament_cmake_python</buildtool_depend>

``CMakeLists.txt`` 应包含：

.. code-block:: cmake

   find_package(ament_cmake_python REQUIRED)
   # ...
   ament_python_install_package(${PROJECT_NAME})

``ament_python_install_package()`` 的参数是 ``CMakeLists.txt`` 旁边包含 Python 文件的目录的名称。
在本例中，它是 ``my_project``，即 ``${PROJECT_NAME}``。

.. warning::

   在同一个 CMake 项目中调用 ``rosidl_generate_interfaces`` 和 ``ament_python_install_package`` 无法正常工作。
   更多信息请参见这个 `Github issue <https://github.com/ros2/rosidl_python/issues/141>`_。
   最佳实践是将消息生成分离到一个单独的包中。

然后，另一个正确依赖 ``my_project`` 的 Python 包可以将其作为普通 Python 模块使用：

.. code-block:: python

   from my_project.my_script import my_function

假设 ``my_script.py`` 包含一个名为 ``my_function()`` 的函数。

使用 ament_cmake_pytest
^^^^^^^^^^^^^^^^^^^^^^^

包 ``ament_cmake_pytest`` 用于让测试可被 ``cmake`` 发现。
该包必须在其 ``package.xml`` 中声明对 ``ament_cmake_pytest`` 的测试依赖。

.. code-block:: xml

   <test_depend>ament_cmake_pytest</test_depend>

假设该包的文件结构如下所示，测试位于 ``tests`` 文件夹中。

.. code-block::

   .
   ├── CMakeLists.txt
   ├── my_project
   │   └── my_script.py
   ├── package.xml
   └── tests
       ├── test_a.py
       └── test_b.py

``CMakeLists.txt`` 应包含：

.. code-block:: cmake

   if(BUILD_TESTING)
     find_package(ament_cmake_pytest REQUIRED)
     set(_pytest_tests
       tests/test_a.py
       tests/test_b.py
       # Add other test files here
     )
     foreach(_test_path ${_pytest_tests})
       get_filename_component(_test_name ${_test_path} NAME_WE)
       ament_add_pytest_test(${_test_name} ${_test_path}
         APPEND_ENV PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}
         TIMEOUT 60
         WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
       )
     endforeach()
   endif()

与支持自动测试发现的 ament_python 用法相比，ament_cmake_pytest 必须传入每个测试文件的路径。
超时时间可以根据需要缩短。

现在，你可以使用 :doc:`标准的 colcon 测试命令 <../Tutorials/Intermediate/Testing/CLI>` 来调用你的测试。
