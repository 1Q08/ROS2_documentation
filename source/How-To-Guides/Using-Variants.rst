使用变体
========

元软件包本身并不直接提供软件，而是依赖一组其他相关软件包，从而为这整套软件包提供便捷的安装机制。
[#]_ [#]_
变体是针对常用的一系列 ROS 软件包所提供的一批官方元软件包。

.. [#] https://wiki.debian.org/metapackage
.. [#] https://help.ubuntu.com/community/MetaPackages

ROS 2 中的不同变体在 `REP-2001 <https://reps.openrobotics.org/rep-2001/>`_ 中规定。

除了官方变体之外，可能还存在针对特定机构或机器人的元软件包，如 `REP-108 <https://reps.openrobotics.org/rep-0108/#institution-specific>`_ 中所述。

添加变体
--------

可以被 ROS 社区普遍使用的其他变体，可以通过向 `REP-2001 提交拉取请求 <https://github.com/openrobotics/reps/blob/main/_posts/rep-2001.md>`_ 来描述新变体所包含的软件包，从而提出。
机构和机器人专用的变体可由各自的维护者直接发布，无需更新 REP-2001。

创建项目专用变体
----------------

如果你创建 ROS 软件包是为了在自己的项目中私下使用，你可以以官方变体为示例，创建自己项目专用的变体。
为此，你只需创建两个文件：

#. 最小变体软件包按如下方式创建：一个构建类型为 ``ament_cmake`` 的软件包，具有对 ``ament_cmake`` 的 ``buildtool_depend``，以及为你想要纳入该变体的每个软件包添加 ``exec_depend`` 条目。

   .. code-block:: xml

    <?xml version="1.0"?>
    <?xml-model href="http://download.ros.org/schema/package_format2.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
    <package format="2">
      <name>my_project_variant</name>
      <version>1.0.0</version>
      <description>A package to aggregate all packages in my_project.</description>
      <maintainer email="maintainer-email">Maintainer Name</maintainer>
      <license>Apache License 2.0</license>
      <!-- packages in my_project -->
      <exec_depend>my_project_msgs</exec_depend>
      <exec_depend>my_project_services</exec_depend>
      <exec_depend>my_project_examples</exec_depend>

      <export>
        <build_type>ament_cmake</build_type>
      </export>
    </package>

#. 一个最小的 ament_cmake 软件包包含一个 ``CMakeLists.txt``，它将 package.xml 注册为可供 ROS 2 使用的 ament 软件包。

   .. code-block:: cmake

    cmake_minimum_required(VERSION 3.5)

    project(my_project_variant NONE)
    find_package(ament_cmake REQUIRED)
    ament_package()

随后你就可以将你的变体软件包与其他私有软件包一起构建和安装。

使用平台专用工具创建自定义变体
******************************

某些平台具备用于创建基本软件包的工具，无需完整的 ROS 构建农场环境或同等基础设施。
可以使用这些工具来创建平台相关的变体。
这种方法不支持 ROS 打包工具，且与平台相关，但如果你创建的是现有软件包的集合，而不是公共和私有 ROS 软件包的混合，那么它所需的基础设施要少得多。
例如，在 Debian 或 Ubuntu 系统上你可以使用 ``equivs`` 工具。
《Debian 管理员手册》中有一 `节关于元软件包的内容 <https://www.debian.org/doc/manuals/debian-handbook/sect.building-first-package.en.html#id-1.18.5.2>`_。
