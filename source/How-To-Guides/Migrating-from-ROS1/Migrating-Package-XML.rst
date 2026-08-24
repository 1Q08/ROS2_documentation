将你的 package.xml 迁移到格式 2
===============================

.. contents:: 目录
   :depth: 2
   :local:

ROS 2 要求 ``package.xml`` 文件至少使用
`格式 2 <https://reps.openrobotics.org/rep-0140/>`__。
本指南展示了如何将 ``package.xml`` 从格式 1 迁移到格式 2。

如果 ``package.xml`` 开头的 ``<package>`` 标签看起来像以下两种情况之一，
那么它使用的是格式 1，你必须迁移它。

.. code-block:: xml

    <package>

.. code-block:: xml

    <package format="1">


前提条件
--------

你应该有一个可正常工作的 ROS 1 安装。
这使你能够通过构建和测试软件包来检查转换后的 ``package.xml`` 是否有效，
因为 ROS 1 支持所有 ``package.xml`` 格式版本。

从格式 1 迁移到格式 2
---------------------

格式 1 和格式 2 在指定依赖的方式上有所不同。
请阅读 `REP-0140 中的兼容性章节 <https://reps.openrobotics.org/rep-0140/#compatibility>`__，
获取差异的摘要。

为 ``<package>`` 添加 ``format`` 属性
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

添加或将 ``format`` 属性设置为 ``2``，
以表明该 ``package.xml`` 使用格式 2。

.. code:: xml

  <package format="2">

替换 ``<run_depend>``
~~~~~~~~~~~~~~~~~~~~~

``<run_depend>`` 标签不再被允许。
如果你的依赖是这样指定的：

.. code:: xml

  <run_depend>foo</run_depend>

那么用以下一个或两个标签替换它：

.. code:: xml

  <build_export_depend>foo</build_export_depend>
  <exec_depend>foo</exec_depend>

如果在你的软件包中的某些内容被执行时需要该依赖，
则使用 ``<exec_depend>`` 标签。
如果依赖你的软件包的软件包在构建时需要该依赖，
则使用 ``<build_export_depend>`` 标签。
如果不确定，就两个标签都使用。

将部分 ``<build_depend>`` 转换为 ``<test_depend>``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在格式 1 中，``<test_depend>`` 声明的是运行软件包测试时所需的依赖。
在格式 2 中它仍然如此，但此外还声明构建软件包测试时所需的依赖。

由于格式 1 中该标签的限制，你的软件包可能将仅用于测试的依赖
指定为 ``<build_depend>``，如下所示：

.. code:: xml

  <build_depend>testfoo</build_depend>

如果是这样，请将其改为 ``<test_depend>``。

.. code:: xml

  <test_depend>testfoo</test_depend>

.. note::

    如果你使用 CMake，请确保你的测试依赖只在 ``if(BUILD_TESTING)`` 块中被引用：

    .. code:: cmake

        if (BUILD_TESTING)
            find_package(testfoo REQUIRED)
        endif()

开始使用 ``<doc_depend>``
~~~~~~~~~~~~~~~~~~~~~~~~~

使用新的 ``<doc_depend>`` 标签来声明构建软件包文档所需的依赖。
例如，C++ 软件包可能有这样的依赖：

.. code:: xml

  <doc_depend>doxygen</doc_depend>

而 Python 软件包可能有这样的依赖：

.. code:: xml

  <doc_depend>python3-sphinx</doc_depend>

更多信息请参见 :doc:`记录 ROS 2 软件包的指南 <../Documenting-a-ROS-2-Package>`。

使用 ``<depend>`` 简化依赖
~~~~~~~~~~~~~~~~~~~~~~~~~~

``<depend>`` 是一个新标签，它使 ``package.xml`` 文件更加简洁。
如果你的 ``package.xml`` 针对同一个依赖有这三个标签：

.. code::

  <build_depend>foo</build_depend>
  <build_export_depend>foo</build_export_depend>
  <exec_depend>foo</exec_depend>

那么用一个 ``<depend>`` 替换它们，如下所示：

.. code:: xml

  <depend>foo</depend>

测试你的新 ``package.xml``
--------------------------

像往常一样使用 ``catkin_make``、``cakin_make_isolated`` 或 ``catkin`` 构建工具
构建和测试你的软件包。
如果一切成功，那么你的 ``package.xml`` 就是有效的。
