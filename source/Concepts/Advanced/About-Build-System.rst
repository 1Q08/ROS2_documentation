.. redirect-from::

   Concepts/About-Build-System

构建系统
========

.. contents:: 目录
   :local:

.. include:: ../../../global_substitutions.txt

构建系统使开发人员能够根据需要构建他们的 ROS 2 代码。
ROS 2 严重依赖于将代码划分为包，每个包都包含一个清单文件（``package.xml``）。
该清单文件包含包的基本元数据，包括它对其他包的依赖。
元构建工具的正常运行需要此清单文件。

ROS 2 构建系统由 3 个主要概念组成。

构建工具
--------

这是控制单个包编译和测试的软件。
在 ROS 2 中，C++ 通常使用 CMake，Python 使用 setuptools，但也支持其他构建工具。

构建辅助工具
------------

这些是挂接到构建工具中以改善开发人员体验的辅助函数。
ROS 2 包通常依赖 ``ament`` 系列包来实现这一点。
``ament`` 由几个重要的仓库组成，它们都位于 `GitHub 组织 <https://github.com/ament>`_ 中。

``ament_package`` 包
~~~~~~~~~~~~~~~~~~~~

位于 |GitHub|_ 上的 `ament/ament_package <https://github.com/ament/ament_package>`_，该仓库包含一个单独的 :term:`ament Python package`，它为 |ament packages| 提供各种实用工具，例如环境钩子模板。

所有 |ament packages| 无论其底层构建系统如何，都必须在包的根目录包含一个 :term:`package.xml` 文件。
:term:`package.xml`“清单”文件包含处理和操作 |package| 所需的信息。
这些 |package| 信息包括 |package| 的名称（全局唯一）以及包的依赖项。
:term:`package.xml` 文件还充当标记文件，指示 |package| 在文件系统上的位置。

:term:`package.xml` 文件的解析由 ``catkin_pkg`` 提供（与 ROS 1 相同），而通过搜索文件系统中的这些 :term:`package.xml` 文件来定位 |packages| 的功能由 ``colcon`` 等构建工具提供。

.. glossary::

   package.xml
       包清单文件，它标记 :term:`package` 的根目录，并包含关于该 :term:`package` 的元信息，包括其名称、版本、描述、维护者、许可证、依赖项等。
       清单的内容采用机器可读的 XML 格式，其内容在 |REPs| `127 <https://reps.openrobotics.org/rep-0127/>`_ 和 `140 <https://reps.openrobotics.org/rep-0140/>`_ 中描述，未来可能会在 |REPs| 中做进一步修改。

因此，每当某个 |package| 被称为 :term:`ament package` 时，就意味着它是一个单一的软件单元（源代码、构建文件、测试、文档和其他资源），并使用 :term:`package.xml` 清单文件来描述。

.. glossary::

   ament package
       任何包含 :term:`package.xml` 并遵循 ``ament`` 打包指南的 |package|，无论其底层构建系统如何。

由于 :term:`ament package` 一词与构建系统无关，因此可以有不同种类的 |ament packages|，例如 :term:`ament CMake package`、:term:`ament Python package` 等。

以下是你在此软件栈中可能遇到的常见包类型列表：

.. glossary::

    CMake package
        任何包含普通 CMake 项目和 :term:`package.xml` 清单文件的 |package|。

    ament CMake package
        同时遵循 ``ament`` 打包指南的 :term:`CMake package`。

    Python package
        任何包含基于 `setuptools <https://pypi.org/project/setuptools/>`_ 的 Python 项目和 :term:`package.xml` 清单文件的 |package|。

    ament Python package
        同时遵循 ``ament`` 打包指南的 :term:`Python package`。

``ament_cmake`` 仓库
~~~~~~~~~~~~~~~~~~~~

位于 |GitHub|_ 上的 `ament/ament_cmake <https://github.com/ament/ament_cmake>`_，该仓库包含许多“ament CMake”包和纯 CMake 包，它们提供了在 CMake 中创建“ament CMake”包所需的基础设施。
在此上下文中，“ament CMake”包意味着：使用 CMake 构建的 ``ament`` 包。
因此，该仓库中的 |packages| 提供了必要的 CMake 函数/宏和 CMake 模块，以方便创建更多“ament CMake”（或 ``ament_cmake``）包。
此类型的包通过 :term:`package.xml` 文件的 ``<export>`` 标签中的 ``<build_type>ament_cmake</build_type>`` 标签来标识。

该仓库中的 |packages| 极其模块化，但有一个单一的“瓶颈” |package| 叫做 ``ament_cmake``。
任何人都可以依赖 ``ament_cmake`` |package| 来获得该仓库中 |packages| 的全部聚合功能。
以下是该仓库中 |packages| 的列表及其简短描述：

-  ``ament_cmake``

   - 聚合该仓库中的所有其他 |packages|，用户只需依赖这一个

-  ``ament_cmake_auto``

   - 提供便捷的 CMake 函数，自动处理编写 |package| 的 ``CMakeLists.txt`` 文件中许多繁琐的部分

-  ``ament_cmake_core``

   - 提供 ``ament`` 的所有内置核心概念，例如环境钩子、资源索引、符号链接安装等

-  ``ament_cmake_gmock``

   - 添加用于创建基于 gmock 的单元测试的便捷函数

-  ``ament_cmake_gtest``

   - 添加用于创建基于 gtest 的自动化测试的便捷函数

-  ``ament_cmake_nose``

   - 添加用于创建基于 nosetests 的 Python 自动化测试的便捷函数

-  ``ament_cmake_python``

   - 为包含 Python 代码的 |packages| 提供 CMake 函数
   - 参见 :doc:`ament_cmake_python 用户文档 <../../How-To-Guides/Ament-CMake-Python-Documentation>`

-  ``ament_cmake_test``

   - 使用 `CTest <https://cmake.org/Wiki/CMake/Testing_With_CTest>`_ 将不同类型的测试（例如 gtest 和 nosetests）聚合到单个目标下

``ament_cmake_core`` |package| 包含大量 CMake 基础设施，使得使用常规接口在 |packages| 之间干净地传递信息成为可能。
这使 |packages| 与其他 |packages| 具有更解耦的构建接口，促进了它们的复用，并鼓励在不同 |packages| 的构建系统中遵循约定。
例如，它提供了一种在 |packages| 之间传递包含目录、库、定义和依赖项的标准方式，使这些信息的使用者能够以常规方式访问这些信息。

``ament_cmake_core`` |package| 还提供 ``ament`` 构建系统的功能，例如符号链接安装，它允许你将文件从源空间或构建空间符号链接到安装空间，而不是复制它们。
这允许你安装一次，然后编辑非生成的资源（如 Python 代码和配置文件），而无需重新运行安装步骤即可生效。
此功能基本上取代了 ``catkin`` 的“devel space”，因为它具有大部分优点，而几乎没有其复杂性或缺点。

``ament_cmake_core`` 提供的另一项功能是 |package| 资源索引，这是 |packages| 表明其包含某种类型资源的一种方式。
此功能的设计使回答诸如“此前缀（例如 ``/usr/local``）中有哪些 |packages|”之类的简单问题变得高效得多，因为它只需要列出该前缀下单个可能位置中的文件。
你可以在资源索引的 `设计文档 <https://github.com/ament/ament_cmake/blob/{REPOS_FILE_BRANCH}/ament_cmake_core/doc/resource_index.md>`_ 中阅读有关此功能的更多信息。

与 ``catkin`` 一样，``ament_cmake_core`` 也提供环境设置文件和 |package| 特定的环境钩子。
环境设置文件通常命名为 ``setup.bash`` 之类，是 |package| 开发人员定义使用其 |package| 所需的环境更改的地方。
开发人员可以使用“环境钩子”来实现这一点，它基本上是一段任意的 shell 代码，可以设置或修改环境变量、定义 shell 函数、设置自动补全规则等……
例如，ROS 1 就是通过此功能设置 ``ROS_DISTRO`` 环境变量的，而 ``catkin`` 对 ROS 发行版一无所知。

``ament_lint`` 仓库
~~~~~~~~~~~~~~~~~~~

位于 |GitHub|_ 上的 `ament/ament_lint <https://github.com/ament/ament_lint>`_，该仓库提供了几个 |packages|，它们以方便且一致的方式提供静态检查和测试服务。
目前有支持使用 ``uncrustify`` 进行 C++ 风格检查、使用 ``cppcheck`` 进行静态 C++ 代码检查、检查源代码中的版权、使用 ``pep8`` 进行 Python 风格检查等的 |packages|。
辅助包的列表将来可能会增长。

元构建工具
----------

这是一款知道如何对一组包进行拓扑排序，并按正确的依赖顺序构建或测试它们的软件。
该软件将调用构建工具来完成编译、测试和安装包的实际工作。

在 ROS 2 中，使用名为 `colcon <https://colcon.readthedocs.io/en/released/>`__ 的工具来完成此任务。
