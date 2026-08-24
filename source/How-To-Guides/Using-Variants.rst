使用变体（variants）
====================

元包（metapackage）并不直接提供软件，而是依赖一组其他相关包，
为完整的一组包提供便捷的安装机制。[#]_ [#]_
变体是官方元包的列表，用于覆盖常用且有用的 ROS 包组合。

.. [#] https://wiki.debian.org/metapackage
.. [#] https://help.ubuntu.com/community/MetaPackages

ROS 2 中的不同变体在 `REP-2001 <https://reps.openrobotics.org/rep-2001/>`_ 中指定。

除了官方变体之外，还可能存在针对特定机构或机器人的元包，
如 `REP-108 <https://reps.openrobotics.org/rep-0108/#institution-specific>`_ 中所述。

添加变体
--------

对 ROS 社区有普遍用途的额外变体，可以通过
`通过拉取请求更新 REP-2001 <https://github.com/openrobotics/reps/blob/main/_posts/rep-2001.md>`_ 来提出，
其中需要描述新变体所包含的包。
机构和机器人特定的变体可以由各自的维护者直接发布，
无需更新 REP-2001。

创建项目特定的变体
------------------

如果你正在创建仅供自己项目私用的 ROS 包，你可以
以官方变体为例，创建特定于你项目的变体。
为此，你只需要创建两个文件：

#. 一个最小化的变体包被创建为一个构建类型为 ``ament_cmake`` 的包，
   包含对 ``ament_cmake`` 的 ``buildtool_depend``，
   以及针对你想要包含在变体中的每个包的 ``exec_depend`` 条目。

   .. code-block:: xml

    <?xml version="1.0"?>
    <?xml-model href="http://download.ros.org/schema/package_format2.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
    <package format="2">
      <name>my_project_variant</name>
      <version>1.0.0</version>
      <description>A package to aggregate all packages in my_project.</description>
      <maintainer email="maintainer-email">Maintainer Name</maintainer>
      <license>Apache-2.0</license>
      <!-- packages in my_project -->
      <exec_depend>my_project_msgs</exec_depend>
      <exec_depend>my_project_services</exec_depend>
      <exec_depend>my_project_examples</exec_depend>

      <export>
        <build_type>ament_cmake</build_type>
      </export>
    </package>

#. 一个最小化的 ament_cmake 包包含一个 ``CMakeLists.txt``，
   它将 package.xml 注册为一个 ament 包，以便在 ROS 2 中使用。

   .. code-block:: cmake

    cmake_minimum_required(VERSION 3.5)

    project(my_project_variant NONE)
    find_package(ament_cmake REQUIRED)
    ament_package()

然后，你可以将你的变体包与其他私有包一起构建和安装。

使用平台特定工具创建自定义变体
******************************

一些平台提供了用于创建基本包的工具，
这些工具不需要完整的 ROS 构建农场环境或等效的基础设施。
可以使用这些工具来创建平台相关的变体。
这种方法不支持 ROS 打包工具，并且依赖于平台，
但如果你创建的是现有包的集合，
而不是公共和私有 ROS 包的混合体，那么它所需的基础设施要少得多。
例如，在 Debian 或 Ubuntu 系统上，你可以使用 ``equivs`` 工具。
Debian 管理员手册中有一个
`关于元包的章节 <https://www.debian.org/doc/manuals/debian-handbook/sect.building-first-package.en.html#id-1.18.5.2>`_。
