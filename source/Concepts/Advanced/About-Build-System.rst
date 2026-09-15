.. redirect-from::

   Concepts/About-Build-System

构建系统
========

.. contents:: 目录
   :local:

.. include:: ../../../global_substitutions.txt

构建系统能够让开发者按需构建 ROS 2 代码。
ROS 2 在很大程度上依赖于将代码按包划分，每个包都包含一个清单文件（``package.xml``）。
这个清单文件包含有关包的必要元数据，包括它与其他包的依赖关系。
这个清单文件是元构建工具正常工作的前提。

ROS 2 构建系统由 3 个主要概念组成。

构建工具
--------

这是控制单个包编译与测试的软件。
在 ROS 2 中，通常使用 CMake 来构建 C++ 包，使用 setuptools 来构建 Python 包，但也支持其他构建工具。

构建辅助工具
------------

这些是挂接到构建工具上的辅助函数，用于改善开发者体验。
ROS 2 包通常依赖 ``ament`` 系列包来提供这些辅助能力。
``ament`` 由若干重要仓库组成，这些仓库都位于 `GitHub 组织 <https://github.com/ament>`_。

``ament_package`` 包
~~~~~~~~~~~~~~~~~~~~

位于 |GitHub|_ 上的 `ament/ament_package <https://github.com/ament/ament_package>`_ 仓库中，包含一个单独的 :term:`ament Python package`，为 |ament packages| 提供各种实用工具，例如环境钩子的模板。

所有 |ament packages| 的包根目录都必须包含一个单独的 :term:`package.xml` 文件，不论其底层构建系统为何。
:term:`package.xml` “清单”文件中包含处理和操作 |package| 必需的信息。
这些 |package| 信息包括 |package| 的全局唯一名称以及它的依赖关系。
:term:`package.xml` 文件同时也是标记 |package| 在文件系统中位置的标记文件。

:term:`package.xml` 文件的解析由 ``catkin_pkg`` 提供（与 ROS 1 一样），而通过文件系统搜索这些 :term:`package.xml` 文件来定位 |packages| 的功能，则由 ``colcon`` 这样的构建工具提供。

.. glossary::

   package.xml
       包清单文件，用于标记 :term:`package` 的根目录，并包含有关该 :term:`package` 的元信息，包括其名称、版本、描述、维护者、许可证、依赖关系等。
       清单内容采用机器可读的 XML 格式，相关内容在 |REPs| `127 <https://reps.openrobotics.org/rep-0127/>`_ 和 `140 <https://reps.openrobotics.org/rep-0140/>`_ 中有说明，未来还可能通过进一步的 |REPs| 进行修改。

因此，只要某个 |package| 被称为 :term:`ament package`，就意味着它是一个软件单元（包含源代码、构建文件、测试、文档和其他资源），并通过 :term:`package.xml` 清单文件来描述。

.. glossary::

   ament package
       任意一个包含 :term:`package.xml` 且遵循 ``ament`` 打包规范的 |package|，无论其底层构建系统是什么。

由于 :term:`ament package` 这一术语与构建系统无关，因此可能存在不同种类的 |ament packages|，例如 :term:`ament CMake package`、:term:`ament Python package` 等。

下面列出你可能会在该软件栈中遇到的常见包类型：

.. glossary::

    CMake package
        任意包含普通 CMake 项目和 :term:`package.xml` 清单文件的 |package|。

    ament CMake package
        同时遵循 ``ament`` 打包规范的 :term:`CMake package`。

    Python package
        任意包含基于 `setuptools <https://pypi.org/project/setuptools/>`_ 的 Python 项目和 :term:`package.xml` 清单文件的 |package|。

    ament Python package
        同时遵循 ``ament`` 打包规范的 :term:`Python package`。

``ament_cmake`` 仓库
~~~~~~~~~~~~~~~~~~~~

位于 |GitHub|_ 上的 `ament/ament_cmake <https://github.com/ament/ament_cmake>`_ 仓库中，包含大量“ament CMake”与纯 CMake 包，这些包提供了构建“ament CMake”包所需的 CMake 基础设施。
在这里，“ament CMake”包指的是使用 CMake 构建的 ``ament`` 包。
因此，该仓库中的 |packages| 提供了必要的 CMake 函数/宏以及 CMake 模块，用于帮助创建更多“ament CMake”（或 ``ament_cmake``）包。
这类包在 :term:`package.xml` 文件的 ``<export>`` 标签中，会通过 ``<build_type>ament_cmake</build_type>`` 标签加以标识。

该仓库中的 |packages| 非常模块化，但其中有一个单独的“瓶颈” |package|，名为 ``ament_cmake``。
任何人都可以依赖 ``ament_cmake`` |package| 来获得该仓库中其他 |packages| 的聚合功能。
下面列出该仓库中的若干 |packages| 及其简要说明：

-  ``ament_cmake``

   - 聚合该仓库中的其他所有 |packages|，用户只需依赖本包即可

-  ``ament_cmake_auto``

   - 提供便捷的 CMake 函数，自动处理编写 |package| 的 ``CMakeLists.txt`` 文件时大量繁琐细节

-  ``ament_cmake_core``

   - 提供 ``ament`` 的所有内置核心概念，例如环境钩子、资源索引、符号链接安装等

-  ``ament_cmake_gmock``

   - 添加基于 gmock 的单元测试便捷函数

-  ``ament_cmake_gtest``

   - 添加基于 gtest 的自动化测试便捷函数

-  ``ament_cmake_nose``

   - 添加基于 nosetests 的 Python 自动化测试便捷函数

-  ``ament_cmake_python``

   - 为包含 Python 代码的 |packages| 提供 CMake 函数
   - 参见 :doc:`ament_cmake_python 用户文档 <../../How-To-Guides/Ament-CMake-Python-Documentation>`

-  ``ament_cmake_test``

   - 使用 `CTest <https://cmake.org/Wiki/CMake/Testing_With_CTest>`_ 汇总不同类型测试，例如 gtest 与 nosetests，并在单个目标下运行

``ament_cmake_core`` |package| 包含大量 CMake 基础设施，使得不同 |packages| 之间能够通过约定接口清晰地传递信息。
这让 |packages| 与其他 |packages| 的构建接口耦合度更低，增强可复用性，并促进不同 |packages| 构建系统间的约定形成。
例如，它提供了一种标准方式，在 |packages| 之间传递包含目录、库、定义和依赖关系，让使用这些信息的消费者能够以一致的方式获取它们。

``ament_cmake_core`` |package| 还提供了 ``ament`` 构建系统的若干特性，例如符号链接安装，这使得你可以将文件从源空间或构建空间符号链接到安装空间，而不是复制它们。
这让你可以先安装一次，然后编辑非生成资源（如 Python 代码和配置文件），而无需重新执行安装步骤让它们生效。
这个特性本质上取代了 ``catkin`` 的“devel space”，因为它具备大多数优点，但缺点较少。

``ament_cmake_core`` 提供的另一个特性是 |package| 资源索引，用于让 |packages| 表明自己包含某种类型的资源。
该特性的设计可以更高效地回答类似“给定前缀（例如 ``/usr/local``）中有哪些 |packages|”这类简单问题，因为它只需要列出前缀中某一可能位置下的文件即可。
有关资源索引的更多信息，可阅读其 `设计文档 <https://github.com/ament/ament_cmake/blob/{REPOS_FILE_BRANCH}/ament_cmake_core/doc/resource_index.md>`_。

与 ``catkin`` 类似，``ament_cmake_core`` 还提供环境设置文件和 |package| 特定环境钩子。
环境设置文件通常命名为类似 ``setup.bash``，用于为 |package| 开发者定义利用该 |package| 所需的环境变量变更、shell 函数定义、自动补全规则设置等。
开发者能够通过“环境钩子”这种方式，在任意 shell 代码中设置或修改环境变量、定义 shell 函数、设置自动补全规则等。
例如，这正是 ROS 1 在 ``catkin`` 不知情的情况下设置 ``ROS_DISTRO`` 环境变量的方式。

``ament_lint`` 仓库
~~~~~~~~~~~~~~~~~~~

位于 |GitHub|_ 上的 `ament/ament_lint <https://github.com/ament/ament_lint>`_ 仓库中，提供了多个 |packages|，以方便、一致地提供 linting 和测试服务。
当前有 |packages| 分别支持使用 ``uncrustify`` 进行 C++ 风格检查、使用 ``cppcheck`` 进行静态 C++ 代码检查、检查源码中的版权声明、使用 ``pep8`` 进行 Python 风格检查，以及其他内容。
未来这些辅助包列表还会继续增长。

元构建工具
----------

这是一类知道如何按拓扑顺序组织一组包，并以正确的依赖顺序构建或测试它们的软件。
这类软件会调用构建工具来完成真正的编译、测试与安装工作。

在 ROS 2 中，用于此目的的工具名为 `colcon <https://colcon.readthedocs.io/en/released/>`__。
