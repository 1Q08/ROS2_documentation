.. redirect-from::

  Guides/Ament-CMake-Documentation
  Tutorials/Ament-CMake-Documentation

ament_cmake 用户文档
====================

``ament_cmake`` 是 ROS 2 中基于 CMake 的软件包的构建系统（尤其是大多数 C/C++ 项目都会使用它）。
它是一组增强 CMake 并为软件包作者提供便利功能的脚本。
在使用 ``ament_cmake`` 之前，了解 `CMake <https://cmake.org/cmake/help/v3.8/>`__ 的基础知识会非常有帮助。
可以在 `这里 <https://cmake.org/cmake/help/latest/guide/tutorial/index.html>`__ 找到官方教程。

.. contents:: 目录
   :depth: 2
   :local:

基础
----

在命令行中使用 ``ros2 pkg create <package_name>`` 可以生成基本的 CMake 框架。
构建信息随后会被收集到两个文件中：``package.xml`` 与 ``CMakeLists.txt``，它们必须位于同一目录下。
``package.xml`` 必须包含所有依赖项以及一些元数据，以便 colcon 为你的软件包确定正确的构建顺序、在 CI 中安装所需的依赖项，并为使用 ``bloom`` 发布提供信息。
``CMakeLists.txt`` 包含构建和打包可执行文件与库的命令，将是本文档的重点。

基本项目框架
^^^^^^^^^^^^

ament 软件包的 ``CMakeLists.txt`` 基本框架包含以下内容：

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.8)
    project(my_project)

    ament_package()

传给 ``project`` 的参数将是软件包名称，并且必须与 ``package.xml`` 中的软件包名称完全相同。

项目设置由 ``ament_package()`` 完成，并且每个软件包只能调用它一次。
``ament_package()`` 会安装 ``package.xml``、将该软件包注册到 ament 索引中，并安装供 CMake 使用的配置文件（可能还有目标文件），以便其他软件包能通过 ``find_package`` 找到它。
由于 ``ament_package()`` 会从 ``CMakeLists.txt`` 中收集大量信息，它应当是你 ``CMakeLists.txt`` 中的最后一次调用。

``ament_package`` 还可以接受额外的参数：

- ``CONFIG_EXTRAS``：一个 CMake 文件（``.cmake`` 或由 ``configure_file()`` 展开的 ``.cmake.in`` 模板）列表，这些文件应当对该软件包的客户端可用。
  关于何时使用这些参数的示例，请参阅 `添加资源`_ 中的讨论。
  有关如何使用模板文件的更多信息，请参阅 `官方文档 <https://cmake.org/cmake/help/v3.8/command/configure_file.html>`__。

- ``CONFIG_EXTRAS_POST``：与 ``CONFIG_EXTRAS`` 相同，但文件的添加顺序不同。
  对 ``ament_export_*`` 调用所生成的文件会在 ``CONFIG_EXTRAS`` 文件之后被包含，而来自 ``CONFIG_EXTRAS_POST`` 的文件则在其后被包含。

除了添加到 ``ament_package``，你也可以添加到变量 ``${PROJECT_NAME}_CONFIG_EXTRAS`` 和 ``${PROJECT_NAME}_CONFIG_EXTRAS_POST``，效果相同。
唯一的区别同样是文件的添加顺序，其总顺序如下：

- 由 ``CONFIG_EXTRAS`` 添加的文件

- 通过追加到 ``${PROJECT_NAME}_CONFIG_EXTRAS`` 添加的文件

- 通过追加到 ``${PROJECT_NAME}_CONFIG_EXTRAS_POST`` 添加的文件

- 由 ``CONFIG_EXTRAS_POST`` 添加的文件

编译器与链接器选项
^^^^^^^^^^^^^^^^^^

ROS 2 面向符合 C++17 和 C99 标准的编译器。
未来可能会面向更新的版本，相关说明参见 `这里 <https://reps.openrobotics.org/rep-2000/>`__。
因此，通常会设置相应的 CMake 标志：

.. code-block:: cmake

    if(NOT CMAKE_C_STANDARD)
      set(CMAKE_C_STANDARD 99)
    endif()
    if(NOT CMAKE_CXX_STANDARD)
      set(CMAKE_CXX_STANDARD 17)
    endif()

为保持代码整洁，编译器应当对可疑代码发出警告，并且应当修复这些警告。

建议至少覆盖以下警告级别：

- 对于 Visual Studio：默认的 ``W1`` 警告

- 对于 GCC 和 Clang：强烈建议使用 ``-Wall -Wextra -Wpedantic``，并建议使用 ``-Wshadow``

目前建议使用 ``add_compile_options`` 为所有目标添加这些选项。
这样可以避免为所有可执行文件、库和测试使用基于目标的编译选项而使代码变得杂乱：

.. code-block:: cmake

    if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
      add_compile_options(-Wall -Wextra -Wpedantic)
    endif()

查找依赖项
^^^^^^^^^^

大多数 ``ament_cmake`` 项目都会依赖其他软件包。
在 CMake 中，这通过调用 ``find_package`` 来完成。
例如，如果你的软件包依赖 ``rclcpp``，那么 ``CMakeLists.txt`` 文件应当包含：

.. code-block:: cmake

    find_package(rclcpp REQUIRED)

.. note::

    绝不应需要 ``find_package`` 某个库——它并非显式需要的，而只是某个显式需要的依赖项所依赖的库。
    如果出现这种情况，请针对相应的软件包提交缺陷报告。

添加目标
^^^^^^^^

在 CMake 术语中，``targets`` 指的是该项目将要创建的产物。
既可以创建库，也可以创建可执行文件，并且单个项目可以包含零个或多个其中的任意一种。

.. tabs::

    .. group-tab:: Libraries

        它们通过调用 ``add_library`` 创建，该调用应同时包含目标的名称以及为创建该库而需要编译的源文件。

        由于 C/C++ 中头文件与实现是分离的，通常不必把头文件作为参数传给 ``add_library``。

        建议采用以下最佳实践：

        - 把所有应能被该库的客户端使用（因而必须安装）的头文件放到 ``include`` 文件夹下与软件包同名的子目录中，而所有其他文件（``.c/.cpp`` 以及不应导出的头文件）则放在 ``src`` 文件夹内

        - 在调用 ``add_library`` 时只显式引用 ``.c/.cpp`` 文件

        - 通过以下方式查找你的库 ``my_library`` 的头文件

        .. code-block:: cmake

            target_include_directories(my_library
              PUBLIC
                "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
                "$<INSTALL_INTERFACE:include/${PROJECT_NAME}>")

        这会在构建时把 ``${CMAKE_CURRENT_SOURCE_DIR}/include`` 文件夹中的所有文件加入公共接口，并在安装时把 include 文件夹（相对于 ``${CMAKE_INSTALL_DIR}``）中的所有文件加入。

        ``ros2 pkg create`` 创建的软件包布局遵循这些规则。

        .. note::

            由于 Windows 是官方支持的平台之一，为了获得最大的影响，任何软件包都应当也能在 Windows 上构建。
            Windows 的库格式强制要求符号可见性；也就是说，每个要从客户端使用的符号都必须由该库显式导出（而符号需要被隐式导入）。

            由于 GCC 和 Clang 构建通常不会这样做，建议采用 `GCC wiki <https://gcc.gnu.org/wiki/Visibility>`__ 中的逻辑。
            要对名为 ``my_library`` 的软件包使用它：

            - 把链接中的逻辑复制到名为 ``visibility_control.hpp`` 的头文件中。

            - 把 ``DLL`` 替换为 ``MY_LIBRARY`` （示例参见 `rviz_rendering <https://github.com/ros2/rviz/blob/ros2/rviz_rendering/include/rviz_rendering/visibility_control.hpp>`__ 的可见性控制）。

            - 对所有需要导出的符号（即类或函数）使用宏 "MY_LIBRARY_PUBLIC"。

            - 在项目的 ``CMakeLists.txt`` 中使用：

              .. code-block:: cmake

                  target_compile_definitions(my_library PRIVATE "MY_LIBRARY_BUILDING_LIBRARY")

            更多细节参见 :ref:`Windows 技巧与提示文档中的 Windows 符号可见性 <Windows_Symbol_Visibility>`。

    .. group-tab:: Executables

        它们应通过调用 ``add_executable`` 创建，该调用应同时包含目标的名称以及为创建该可执行文件而需要编译的源文件。
        该可执行文件可能还需要通过 ``target_link_libraries`` 与本软件包中创建的任何库进行链接。

        由于可执行文件通常不会被客户端当作库使用，因此不需要把任何头文件放入 ``include`` 目录。

如果软件包同时包含库和可执行文件，请务必结合上面 "Libraries" 和 "Executables" 两部分的建议。

链接到依赖项
^^^^^^^^^^^^

把目标链接到依赖项有两种方式。

第一种也是推荐的方式是使用 ament 宏 ``ament_target_dependencies``。
例如，假设我们想把 ``my_library`` 链接到线性代数库 Eigen3。

.. code-block:: cmake

    find_package(Eigen3 REQUIRED)
    ament_target_dependencies(my_library PUBLIC Eigen3)

它会包含必要的头文件和库及其依赖项，以便项目能够正确找到它们。

第二种方式是使用 ``target_link_libraries``。

现代 CMake 更倾向于只使用目标，导出并链接到这些目标。
CMake 目标可以像 C++ 那样带有命名空间。
如果可用的目标带有命名空间，请优先使用它们。
例如，``Eigen3`` 定义了目标 ``Eigen3::Eigen``。

在 Eigen3 的例子中，该调用应当如下所示

.. code-block:: cmake

    target_link_libraries(my_library PUBLIC Eigen3::Eigen)

这同样会包含必要的头文件、库及其依赖项。
注意，该依赖项必须已通过调用 ``find_package`` 被发现。

安装
^^^^

.. tabs::

    .. group-tab:: Libraries

        在构建可复用的库时，需要导出一些信息，以便下游软件包能轻松使用它。

        首先，安装应当对客户端可用的头文件。
        该 include 目录是自定义的，以支持 ``colcon`` 中的覆盖层；更多信息参见 https://colcon.readthedocs.io/en/released/user/overriding-packages.html#install-headers-to-a-unique-include-directory 。

        .. code-block:: cmake

            install(
              DIRECTORY include/
              DESTINATION include/${PROJECT_NAME}
            )

        接下来，安装目标并创建导出目标（``export_${PROJECT_NAME}``），其他代码将使用它来查找此软件包。
        注意，你可以使用单次 ``install`` 调用来安装项目中的所有库。

        .. code-block:: cmake

            install(
              TARGETS my_library
              EXPORT export_${PROJECT_NAME}
              LIBRARY DESTINATION lib
              ARCHIVE DESTINATION lib
              RUNTIME DESTINATION bin
            )

            ament_export_targets(export_${PROJECT_NAME} HAS_LIBRARY_TARGET)
            ament_export_dependencies(some_dependency)

        上面代码片段中发生的事情如下：

        - ``ament_export_targets`` 宏会为 CMake 导出这些目标。
          这对于让你库的客户端能够使用 ``target_link_libraries(client PRIVATE my_library::my_library)`` 语法是必要的。
          如果导出集合中包含库，请给 ``ament_export_targets`` 加上 ``HAS_LIBRARY_TARGET`` 选项，它会把可能的库添加到环境变量中。

        - ``ament_export_dependencies`` 会把依赖项导出给下游软件包。
          这样库的使用者就不必再为那些依赖项调用 ``find_package``。

        .. warning::

            从 CMake 子目录中调用 ``ament_export_targets``、``ament_export_dependencies`` 或其他 ament 命令将无法按预期工作。
            这是因为 CMake 子目录无法在调用 ``ament_package`` 的父作用域中设置必要的变量。

        .. note::

            Windows DLL 被视为运行时产物，会被安装到 ``RUNTIME DESTINATION`` 文件夹中。
            因此，即使在基于 Unix 的系统上开发库，也建议保留 ``RUNTIME`` 安装。

        - ``install`` 调用的 ``EXPORT`` 写法需要额外注意：
          它会安装 ``my_library`` 目标的 CMake 文件。
          其名称必须与 ``ament_export_targets`` 中的参数完全一致。
          为确保它能通过 ``ament_target_dependencies`` 使用，其名称不应与库名完全相同，而应像上面所示那样带有 ``export_`` 之类的前缀。

        - 所有安装路径都相对于 ``CMAKE_INSTALL_PREFIX``，colcon/ament 已经正确设置了该变量。

        另有两个可用的函数，但对于基于目标的安装来说是多余的：

        .. code-block:: cmake

            ament_export_include_directories("include/${PROJECT_NAME}")
            ament_export_libraries(my_library)

        第一个宏标记所导出 include 目录的位置。
        第二个宏标记已安装库的位置（这由调用 ``ament_export_targets`` 时的 ``HAS_LIBRARY_TARGET`` 参数完成）。
        只有当下游项目无法或不想使用基于 CMake 目标的依赖项时，才应使用它们。

        其中一些宏可以为非目标导出接受不同类型的参数，但由于现代 CMake 的推荐做法是使用目标，我们在此不再赘述。
        这些选项的文档可以在源代码本身中找到。

    .. group-tab:: Executables

        在安装可执行文件时 *必须严格照搬* 下面的内容，其余 ROS 工具才能找到它：

        .. code-block:: cmake

            install(TARGETS my_exe
                DESTINATION lib/${PROJECT_NAME})

如果软件包同时包含库和可执行文件，请务必结合上面 "Libraries" 和 "Executables" 两部分的建议。

代码检查与测试
--------------

为了在使用 colcon 构建库时把测试分离出来，请把所有对代码检查工具和测试的调用都放在一个条件块中：

.. code-block:: cmake

    if(BUILD_TESTING)
      find_package(ament_cmake_gtest REQUIRED)
      ament_add_gtest(<tests>)
    endif()

代码检查
^^^^^^^^

建议使用 `ament_lint_auto <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_lint_auto/doc/index.rst#ament_lint_auto>`_ 提供的合并调用：

.. code-block:: cmake

    find_package(ament_lint_auto REQUIRED)
    ament_lint_auto_find_test_dependencies()

这会运行 ``package.xml`` 中定义的代码检查工具。
建议使用 ``ament_lint_common`` 软件包所定义的代码检查工具集合。
其中包含的各个代码检查工具及其功能可以在 `ament_lint_common 文档 <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_lint_common/doc/index.rst>`_ 中查看。

ament 提供的代码检查工具也可以单独添加，而不必运行 ``ament_lint_auto``。
关于如何做到这一点的一个示例可以在 `ament_cmake_lint_cmake 文档 <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_cmake_lint_cmake/doc/index.rst>`_ 中找到。

测试
^^^^

Ament 包含用于简化 GTest 设置的 CMake 宏。
调用：

.. code-block:: cmake

    find_package(ament_cmake_gtest)
    ament_add_gtest(some_test <test_sources>)

即可添加一个 GTest。
这样它就是一个常规目标，可以与其他库（例如项目库）进行链接。
这些宏还有额外的参数：

- ``APPEND_ENV``：追加环境变量。
  例如，你可以通过调用以下内容来添加到 ament 前缀路径：

.. code-block:: cmake

    find_package(ament_cmake_gtest REQUIRED)
    ament_add_gtest(some_test <test_sources>
      APPEND_ENV PATH=some/additional/path/for/testing/resources)

- ``APPEND_LIBRARY_DIRS``：追加库，以便链接器在运行时能够找到它们。
  这可以通过设置环境变量来实现，例如 Windows 上的 ``PATH`` 和 Linux 上的 ``LD_LIBRARY_PATH``，但这会使该调用与平台相关。

- ``ENV``：设置环境变量（语法与 ``APPEND_ENV`` 相同）。

- ``TIMEOUT``：以秒为单位设置测试超时时间。
  GTest 的默认值为 60 秒。
  例如：

.. code-block:: cmake

    ament_add_gtest(some_test <test_sources> TIMEOUT 120)

- ``SKIP_TEST``：跳过此测试（在控制台输出中将显示为 "passed"）。

- ``SKIP_LINKING_MAIN_LIBRARIES``：不链接 GTest。

- ``WORKING_DIRECTORY``：设置测试的工作目录。

否则，默认工作目录为 ``CMAKE_CURRENT_BINARY_DIR``，其说明见 `CMake 文档 <https://cmake.org/cmake/help/latest/variable/CMAKE_CURRENT_BINARY_DIR.html>`_。

类似地，还有一个用于设置包含 GMock 的 GTest 的 CMake 宏：

.. code-block:: cmake

    find_package(ament_cmake_gmock REQUIRED)
    ament_add_gmock(some_test <test_sources>)

它的额外参数与 ``ament_add_gtest`` 相同。

扩展 ament
----------

可以向 ``ament_cmake`` 注册额外的宏/函数，并以多种方式扩展它。

向 ament 添加函数/宏
^^^^^^^^^^^^^^^^^^^^

扩展 ament 通常意味着你希望某些函数对其他软件包可用。
向客户端软件包提供该宏的最佳方式是把它注册到 ament。

这可以通过追加 ``${PROJECT_NAME}_CONFIG_EXTRAS`` 变量来实现，``ament_package()`` 会通过以下方式使用它

.. code-block:: cmake

    list(APPEND ${PROJECT_NAME}_CONFIG_EXTRAS
      path/to/file.cmake"
      other/pathto/file.cmake"
    )

或者，你也可以把这些文件直接添加到 ``ament_package()`` 调用中：

.. code-block:: cmake

    ament_package(CONFIG_EXTRAS
      path/to/file.cmake
      other/pathto/file.cmake
    )

向扩展点添加内容
^^^^^^^^^^^^^^^^

除了提供可在其他软件包中使用的函数的简单文件之外，你还可以向 ament 添加扩展。
这些扩展是脚本，它们会与定义扩展点的函数一起被执行。
ament 扩展最常见的用例大概就是注册 rosidl 消息生成器：
在编写生成器时，通常希望无需修改消息/服务定义软件包的代码，就能用你的生成器生成所有消息和服务。
这可以通过把该生成器注册为 ``rosidl_generate_interfaces`` 的扩展来实现。

例如，参见

.. code-block:: cmake

    ament_register_extension(
      "rosidl_generate_interfaces"
      "rosidl_generator_cpp"
      "rosidl_generator_cpp_generate_interfaces.cmake")

它把软件包 ``rosidl_generator_cpp`` 的宏 ``rosidl_generator_cpp_generate_interfaces.cmake`` 注册到扩展点 ``rosidl_generate_interfaces``。
当该扩展点被执行时，就会触发执行这里的脚本 ``rosidl_generator_cpp_generate_interfaces.cmake``。
具体而言，每当函数 ``rosidl_generate_interfaces`` 被执行时，它都会调用该生成器。

对生成器而言，除 ``rosidl_generate_interfaces`` 之外最重要的扩展点就是 ``ament_package``，它会通过 ``ament_package()`` 调用直接执行脚本。
在注册资源（见下文）时，这个扩展点很有用。

``ament_register_extension`` 是一个恰好接受三个参数的函数：

- ``extension_point``：扩展点的名称（大多数情况下会是 ``ament_package`` 或 ``rosidl_generate_interfaces`` 之一）

- ``package_name``：包含该 CMake 文件的软件包名称（即写入该文件的项目的项目名）

- ``cmake_filename``：扩展点运行时执行的 CMake 文件

.. note::

    可以以类似 ``ament_package`` 和 ``rosidl_generate_interfaces`` 的方式定义自定义扩展点，但这几乎是不必要的。

添加扩展点
^^^^^^^^^^

在极少情况下，为 ament 定义新的扩展点可能会很有意义。

扩展点可以在宏内部注册，这样当相应的宏被调用时，所有扩展都会被执行。
要实现这一点：

- 为你的扩展定义并记录一个名称（例如 ``my_extension_point``），这就是在使用该扩展点时传给 ``ament_register_extension`` 宏的名称。

- 在应当执行这些扩展的宏/函数中调用：

.. code-block:: cmake

    ament_execute_extensions(my_extension_point)

ament 扩展的工作方式是：定义一个包含扩展点名称的变量，并用要执行的宏来填充它。
调用 ``ament_execute_extensions`` 时，该变量中定义的脚本就会依次被执行。

.. _ament-cmake-doc_adding-resources:

添加资源
--------

特别是在开发插件或允许插件的软件包时，往往需要从一个 ROS 软件包向另一个软件包（例如插件）添加资源。
示例可以是使用 pluginlib 的工具的插件。

这可以使用 ament 索引（也称为“资源索引”）来实现。

ament 索引详解
^^^^^^^^^^^^^^

关于其设计与意图的细节，参见 `这里 <https://github.com/ament/ament_cmake/blob/{REPOS_FILE_BRANCH}/ament_cmake_core/doc/resource_index.md>`__

原则上，ament 索引包含在 `安装空间 <https://colcon.readthedocs.io/en/released/user/what-is-a-workspace.html#install-artifacts>`_ 中的一个文件夹里。
它包含以不同资源类型命名的浅层子文件夹。
在该子文件夹内，每个提供上述资源的软件包都通过一个“标记文件”按名称被引用。
该文件可以包含获取资源所需的任何内容，例如指向资源安装目录的相对路径，也可以简单地是空文件。

举例来说，假设要为 RViz 提供显示插件：
在名为 ``my_rviz_displays`` 的项目中提供将被 pluginlib 读取的 RViz 插件时，你会提供一个 ``plugin_description.xml`` 文件，它会被安装并由 pluginlib 用来加载插件。
为此，通过以下方式把 plugin_description.xml 注册为 resource_index 中的一个资源

.. code-block:: cmake

    pluginlib_export_plugin_description_file(rviz_common plugins_description.xml)

运行 ``colcon build`` 时，这会把一个名为 ``my_rviz_displays`` 的文件安装到 resource_index 中名为 ``rviz_common__pluginlib__plugin`` 的子文件夹里。
rviz_common 中的 pluginlib 工厂会知道要从所有名为 ``rviz_common__pluginlib__plugin`` 的文件夹中为导出插件的软件包收集信息。
pluginlib 工厂的标记文件包含指向 ``plugins_description.xml`` 文件的、相对于安装文件夹的路径（以及作为标记文件名的库名）。
有了这些信息，pluginlib 就能加载该库，并知道要从 ``plugin_description.xml`` 文件中加载哪些插件。

作为第二个例子，考虑让你自己的 RViz 插件使用你自己自定义网格的可能性。
网格会在启动时被加载，这样插件所有者就不必处理它，但这意味着 RViz 必须知道这些网格。
为此，RViz 提供了一个函数：

.. code-block:: cmake

    register_rviz_ogre_media_exports(DIRECTORIES <my_dirs>)

这会把这些目录作为 ogre_media 资源注册到 ament 索引中。
简而言之，它会把一个以调用该函数的项目命名的文件安装到名为 ``rviz_ogre_media_exports`` 的子文件夹中。
该文件包含指向宏中所列目录的、相对于安装文件夹的路径。
在启动时，RViz 现在可以搜索所有名为 ``rviz_ogre_media_exports`` 的文件夹，并加载所提供的所有文件夹中的资源。
这些搜索使用 ``ament_index_cpp`` （Python 软件包则使用 ``ament_index_py``）完成。

以下各节将探讨如何把自己的资源添加到 ament 索引中，并提供相应的最佳实践。

查询 ament 索引
^^^^^^^^^^^^^^^

如有必要，可以通过 CMake 查询 ament 索引中的资源。
为此，有三个函数：

``ament_index_has_resource``：如果资源存在，则获取指向该资源的前缀路径，参数如下：

- ``var``：输出参数：如果资源不存在，则把这个变量填为 FALSE，否则填入指向该资源的前缀路径

- ``resource_type``：资源的类型（例如 ``rviz_common__pluginlib__plugin``）

- ``resource_name``：资源的名称，通常就是添加了 resource_type 类型资源的软件包名称（例如 ``rviz_default_plugins``）

``ament_index_get_resource``：获取特定资源的内容，即 ament 索引中标记文件的内容。

- ``var``：输出参数：如果资源标记文件存在，则填入其内容。

- ``resource_type``：资源的类型（例如 ``rviz_common__pluginlib__plugin``）

- ``resource_name``：资源的名称，通常就是添加了 resource_type 类型资源的软件包名称（例如 ``rviz_default_plugins``）

- ``PREFIX_PATH``：要搜索的前缀路径（通常默认的 ``ament_index_get_prefix_path()`` 就足够了）。

注意，如果资源不存在，``ament_index_get_resource`` 会抛出错误，因此可能需要用 ``ament_index_has_resource`` 进行检查。

``ament_index_get_resources``：从索引中获取所有注册了某一特定类型资源的软件包

- ``var``：输出参数：填入所有注册了 resource_type 类型资源的软件包名称列表

- ``resource_type``：资源的类型（例如 ``rviz_common__pluginlib__plugin``）

- ``PREFIX_PATH``：要搜索的前缀路径（通常默认的 ``ament_index_get_prefix_path()`` 就足够了）。

向 ament 索引添加内容
^^^^^^^^^^^^^^^^^^^^^

定义资源需要两部分信息：

- 资源的名称，它必须是唯一的，

- 标记文件的布局，它可以是任何内容，也可以是空的（例如标记 ROS 2 软件包的 "package" 资源就是如此）

对于 RViz 网格资源，相应的选择是：

- 资源名称使用 ``rviz_ogre_media_exports``，

- 使用指向所有包含资源的文件夹的、相对于安装路径的相对路径。
  这样你就已经可以在软件包中编写使用相应资源的逻辑了。

为了使用户能轻松为你的软件包注册资源，你还应提供宏或函数，例如 pluginlib 函数或 ``rviz_ogre_media_exports`` 函数。

要注册资源，请使用 ament 函数 ``ament_index_register_resource``。
它会在 resource_index 中创建并安装标记文件。
例如，``rviz_ogre_media_exports`` 对应的调用如下：

.. code-block:: cmake

    ament_index_register_resource(rviz_ogre_media_exports CONTENT ${OGRE_MEDIA_RESOURCE_FILE})

这会把一个名为 ``${PROJECT_NAME}`` 的文件安装到 resource_index 中的 ``rviz_ogre_media_exports`` 文件夹里，其内容由变量 ``${OGRE_MEDIA_RESOURCE_FILE}`` 给出。
该宏有一些可能有用的参数：

- 第一个（未命名的）参数是资源的名称，也就是 resource_index 中文件夹的名称

- ``CONTENT``：标记文件的内容，以字符串形式给出。
  这可以是相对路径列表等。
  ``CONTENT`` 不能与 ``CONTENT_FILE`` 一起使用。

- ``CONTENT_FILE``：用于创建标记文件的文件路径。
  该文件可以是普通文件，也可以是用 ``configure_file()`` 展开的模板文件。
  ``CONTENT_FILE`` 不能与 ``CONTENT`` 一起使用。

- ``PACKAGE_NAME``：导出该资源的软件包/库的名称，也就是标记文件的名称。
  默认为 ``${PROJECT_NAME}``。

- ``AMENT_INDEX_BINARY_DIR``：所生成 ament 索引的基础路径。
  除非确实必要，否则请始终使用默认值 ``${CMAKE_BINARY_DIR}/ament_cmake_index``。

- ``SKIP_INSTALL``：跳过安装标记文件。

由于每个软件包只存在一个标记文件，因此如果同一个项目两次调用该 CMake 函数/宏，通常会有问题。
不过，对于大型项目而言，最好把注册资源的调用拆分到多处。

因此，最佳实践是让诸如 ``register_rviz_ogre_media_exports.cmake`` 这样注册资源的宏只填充一些变量。
真正对 ``ament_index_register_resource`` 的调用则可以放在 ``ament_package`` 的一个 ament 扩展中。
由于每个项目只能有一次对 ``ament_package`` 的调用，因此注册资源的地方始终只有一个。
就 ``rviz_ogre_media_exports`` 而言，这对应以下策略：

- 宏 ``register_rviz_ogre_media_exports`` 接收一个文件夹列表，并把它们追加到名为 ``OGRE_MEDIA_RESOURCE_FILE`` 的变量中。

- 另一个名为 ``register_rviz_ogre_media_exports_hook`` 的宏会在 ``${OGRE_MEDIA_RESOURCE_FILE}`` 非空时调用 ``ament_index_register_resource``。

- ``register_rviz_ogre_media_exports_hook.cmake`` 文件通过调用以下内容，在第三个文件 ``register_rviz_ogre_media_exports_hook-extras.cmake`` 中被注册为 ament 扩展

.. code-block:: cmake

    ament_register_extension("ament_package" "rviz_rendering"
      "register_rviz_ogre_media_exports_hook.cmake")

- ``register_rviz_ogre_media_exports.cmake`` 和 ``register_rviz_ogre_media_exports_hook-extra.cmake`` 文件通过 ``ament_package()`` 被注册为 ``CONFIG_EXTRA``。

设置环境变量
------------
``ament_cmake`` 提供了一种机制，可以在 source 某个 ROS 2 工作空间时自动为其设置环境变量。
这在配置以下内容时很有用：

- RMW 实现（设置 CycloneDDS、FastDDS 等）
- Gazebo 仿真（设置插件和资源的路径）
- 其他机器人特定的自定义设置配置

这可以通过 ``ament_environment_hooks`` 来实现，它允许软件包定义在 source 工作空间时设置的持久环境变量。

关于环境钩子
^^^^^^^^^^^^
环境钩子是 ROS 2 软件包提供的 shell 脚本。
当 source 工作空间中的 setup 文件时，这些钩子也会被 source。
这些脚本让你无需手动修改 ``setup.bash`` 或 ``setup.zsh`` 文件，就能设置或扩展环境变量。

这些环境钩子可以通过创建两类脚本文件来实现：

- ``.dsv.in`` 文件：这些是机器可读的文件，用于指定期望的环境变量变更。
  Ament 处理这些文件比处理传统 shell 脚本更高效，从而提升了设置环境时的性能。

- ``.sh.in`` 文件：这些是由 Linux/macOS shell（如 sh、bash 和 zsh）执行的 shell 脚本。
  它们在 source 工作空间时于运行时设置环境变量。

这些文件由 ``colcon`` 处理，以生成最终的环境钩子脚本。

``ament_environment_hooks`` 的实际实现可以在官方 `ament-cmake 仓库 <https://github.com/ament/ament_cmake/tree/master/ament_cmake_core/cmake/environment_hooks>`__ 中找到。

通过钩子定义持久环境变量
^^^^^^^^^^^^^^^^^^^^^^^^
本节提供一个快速示例，说明如何使用环境钩子为你的 ROS 2 软件包配置 FastDDS XML 配置档。

定义环境钩子时推荐的最佳实践是把它们放在软件包工作空间内专门的 ``hooks`` 目录中。

在你创建的 ``hooks`` 文件夹中，创建一个 ``my_package.sh.in``，内容如下：

.. code-block:: bash

    export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
    export RMW_FASTRTPS_USE_QOS_FROM_XML=1
    export FASTRTPS_DEFAULT_PROFILES_FILE="$COLCON_CURRENT_PREFIX/my_dds_profile.xml"

在同一文件夹中，创建一个 ``my_package.dsv.in`` 文件，内容如下：

.. code-block:: bash

    set;RMW_IMPLEMENTATION;rmw_fastrtps_cpp
    set;RMW_FASTRTPS_USE_QOS_FROM_XML;1
    set;FASTRTPS_DEFAULT_PROFILES_FILE;my_dds_profile.xml

添加之后，你可以在 ``CMakeLists.txt`` 文件中使用 ament_environment_hooks 函数注册它们：

.. code-block:: bash

    ament_environment_hooks(
      "${CMAKE_CURRENT_SOURCE_DIR}/hooks/my_package.dsv.in"
      "${CMAKE_CURRENT_SOURCE_DIR}/hooks/my_package.sh.in"
    )

另一个针对 Gazebo 插件路径使用环境钩子的示例可以在官方 `ros_gz_project_template <https://github.com/gazebosim/ros_gz_project_template/tree/main/ros_gz_example_gazebo/hooks>`__ 中找到。

API 版本管理
------------

ROS 2 通过 ``ament_generate_version_header`` 提供自动的版本头文件生成，它会为 API 版本管理和特性检测创建编译期宏。
这对于保持向后兼容性以及根据库版本有条件地启用特性特别有用。

.. note::

    ``ament_generate_version_header`` 功能仅适用于 C、C++ 以及其他基于 C 的语言。
    它生成带有预处理宏的 C/C++ 头文件，不适用于 Python 或其他不基于 C 的软件包。

理解自动生成的版本宏
^^^^^^^^^^^^^^^^^^^^

许多 ROS 2 C/C++ 软件包（例如 ``rclcpp``、``rcl`` 和 ``rmw``）都会自动生成版本头文件，其中包含暴露库版本信息的宏。
这些版本头文件是使用 `ament_generate_version_header.cmake <https://github.com/ament/ament_cmake/blob/${ROS_DISTRO}/ament_cmake_gen_version_h/cmake/ament_generate_version_header.cmake>`__ 脚本从 ``package.xml`` 文件生成的。

生成的版本宏遵循以下命名约定：

- ``<PACKAGE_NAME>_VERSION_MAJOR``：主版本号
- ``<PACKAGE_NAME>_VERSION_MINOR``：次版本号
- ``<PACKAGE_NAME>_VERSION_PATCH``：补丁版本号
- ``<PACKAGE_NAME>_VERSION``：合并为单个整数的版本号（major * 10000 + minor * 100 + patch）
- ``<PACKAGE_NAME>_VERSION_STR``：版本的字符串表示（例如 "1.2.3"）
- ``<PACKAGE_NAME>_VERSION_GTE(major, minor, patch)``：用于检查版本是否大于或等于指定版本的宏

例如，``rclcpp`` 提供了如下宏：

- ``RCLCPP_VERSION_MAJOR``
- ``RCLCPP_VERSION_MINOR``
- ``RCLCPP_VERSION_PATCH``
- ``RCLCPP_VERSION``
- ``RCLCPP_VERSION_STR``
- ``RCLCPP_VERSION_GTE(major, minor, patch)``

为你的软件包生成版本头文件
^^^^^^^^^^^^^^^^^^^^^^^^^^

要为你自己的软件包生成版本头文件，请在 ``CMakeLists.txt`` 中添加以下内容：

.. code-block:: cmake

    find_package(ament_cmake_gen_version_h REQUIRED)
    ament_generate_version_header(my_library)

这会在 ``<build_dir>/my_library/version.h`` 处生成一个头文件，可以在你的代码中包含它：

.. code-block:: cpp

    #include "my_library/version.h"

版本信息会自动从你的 ``package.xml`` 中的 ``<version>`` 标签提取。

默认情况下，生成的头文件会放在构建目录下 ``<package_name>/version.h`` 中。
你可以自定义输出位置：

.. code-block:: cmake

    ament_generate_version_header(my_library HEADER_PATH "my_library/my_version.h")

使用版本宏进行 API 协商
^^^^^^^^^^^^^^^^^^^^^^^

版本宏支持运行时和编译期的特性检测，这对于编写可跨不同 ROS 2 发行版移植的代码至关重要。

虽然 ROS 2 保证同一发行版内的 ABI（应用程序二进制接口）兼容性，但新的接口和特性可能会被向后移植。
这意味着在单个发行版内，可用的 API 版本可能因所安装的补丁发行版不同而不同。
版本宏让开发者可以在使用某个特定特性之前检查它是否可用。

示例：版本检查
~~~~~~~~~~~~~~

.. code-block:: cpp

    #include "rclcpp/version.h"

    // Check if new feature is available
    #if RCLCPP_VERSION_GTE(28, 3, 0)
      use_new_api_with_feature();
    #else
      use_old_api_without_feature();
    #endif

最佳实践
~~~~~~~~

- **使用新特性前先检查**：在使用旧版本库中可能不可用的特性时，请始终使用版本宏。
- **提供回退实现**：在可能的情况下，为较旧的 API 版本提供替代实现，以保持向后兼容性。
- **记录版本要求**：在软件包文档中清楚地记录特定特性所需的最低版本。
- **跨版本测试**：如果你的软件包需要支持多个 ROS 2 发行版，请针对最低支持的版本进行测试。
- **使用 GTE 宏**：在进行版本比较时，优先使用 ``_VERSION_GTE(major, minor, patch)`` 宏，因为它比手动比较各个版本组成部分提供了更简洁、更易读的语法。
