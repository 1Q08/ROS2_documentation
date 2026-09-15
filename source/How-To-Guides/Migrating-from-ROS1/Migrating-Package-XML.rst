将 package.xml 迁移到格式 2
===========================

.. contents:: 目录
   :depth: 2
   :local:

ROS 2 要求 ``package.xml`` 文件至少使用 `格式 2 <https://reps.openrobotics.org/rep-0140/>`__。
本指南介绍如何把 ``package.xml`` 从格式 1 迁移到格式 2。

如果 ``package.xml`` 开头的 ``<package>`` 标签看起来像下面任意一种形式，那么它使用的是格式 1，你必须迁移它。

.. code-block:: xml

    <package>

.. code-block:: xml

    <package format="1">


前提条件
--------

你应该已经有一个可用的 ROS 1 安装。
这样你就可以通过构建和测试软件包来检查转换后的 ``package.xml`` 是否有效，因为 ROS 1 支持所有 ``package.xml`` 格式版本。

从格式 1 迁移到格式 2
---------------------

格式 1 与格式 2 在如何指定依赖项方面有所不同。
关于差异的概要，请阅读 `REP-0140 中的兼容性章节 <https://reps.openrobotics.org/rep-0140/#compatibility>`__。

为 ``<package>`` 添加 ``format`` 属性
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

添加或把 ``format`` 属性设置为 ``2``，以表明该 ``package.xml`` 使用格式 2。

.. code:: xml

  <package format="2">

替换 ``<run_depend>``
~~~~~~~~~~~~~~~~~~~~~

不再允许使用 ``<run_depend>`` 标签。
如果你的依赖项是这样指定的：

.. code:: xml

  <run_depend>foo</run_depend>

那么请把它替换为下面一个或两个标签：

.. code:: xml

  <build_export_depend>foo</build_export_depend>
  <exec_depend>foo</exec_depend>

如果软件包中的某些内容在执行时需要该依赖项，请使用 ``<exec_depend>`` 标签。
如果依赖你的软件包的软件包在构建时需要该依赖项，请使用 ``<build_export_depend>`` 标签。
如果不确定，请同时使用两个标签。

把某些 ``<build_depend>`` 转换为 ``<test_depend>``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在格式 1 中，``<test_depend>`` 声明的是运行软件包测试时所需的依赖项。
在格式 2 中它仍然如此，但它还额外声明构建软件包测试时所需的依赖项。

由于该标签在格式 1 中的限制，你的软件包可能以 ``<build_depend>`` 的形式指定了仅用于测试的依赖项，如下所示：

.. code:: xml

  <build_depend>testfoo</build_depend>

如果是这样，请把它改为 ``<test_depend>``。

.. code:: xml

  <test_depend>testfoo</test_depend>

.. note::

    如果你使用 CMake，请确保测试依赖项只在 ``if(BUILD_TESTING)`` 块内被引用：

    .. code:: cmake

        if (BUILD_TESTING)
            find_package(testfoo REQUIRED)
        endif()

开始使用 ``<doc_depend>``
~~~~~~~~~~~~~~~~~~~~~~~~~

使用新的 ``<doc_depend>`` 标签来声明构建软件包文档所需的依赖项。
例如，C++ 软件包可能有这个依赖项：

.. code:: xml

  <doc_depend>doxygen</doc_depend>

而 Python 软件包可能有这一个：

.. code:: xml

  <doc_depend>python3-sphinx</doc_depend>

更多信息请参阅 :doc:`关于为 ROS 2 软件包编写文档的指南 <../Documenting-a-ROS-2-Package>`。

用 ``<depend>`` 简化依赖项
~~~~~~~~~~~~~~~~~~~~~~~~~~

``<depend>`` 是一个新标签，可以让 ``package.xml`` 文件更简洁。
如果你的 ``package.xml`` 为同一个依赖项写了下面这三个标签：

.. code::

  <build_depend>foo</build_depend>
  <build_export_depend>foo</build_export_depend>
  <exec_depend>foo</exec_depend>

那么请把它们替换为单个 ``<depend>``，如下所示：

.. code:: xml

  <depend>foo</depend>

测试新的 ``package.xml``
------------------------

像平常一样使用 ``catkin_make``、``cakin_make_isolated`` 或 ``catkin`` 构建工具来构建和测试你的软件包。
如果一切成功，那么你的 ``package.xml`` 就是有效的。
