.. redirect-from::

  Guides/Ament-CMake-Documentation
  Tutorials/Ament-CMake-Documentation

ament_cmake 用户文档
====================

``ament_cmake`` 是 ROS 2 中基于 CMake 的包的构建系统（特别是，它将用于大多数 C/C++ 项目）。
它是一组增强 CMake 并为包作者添加便利功能的脚本。
在使用 ``ament_cmake`` 之前，了解 `CMake <https://cmake.org/cmake/help/v3.8/>`__ 的基础知识会非常有帮助。
官方教程可以在`这里 <https://cmake.org/cmake/help/latest/guide/tutorial/index.html>`__ 找到。

.. contents:: 目录
   :depth: 2
   :local:

基础
----

基本的 CMake 大纲可以通过在命令行中使用 ``ros2 pkg create <package_name>`` 来生成。
随后，构建信息会收集在两个文件中：``package.xml`` 和 ``CMakeLists.txt``，它们必须位于同一目录中。
``package.xml`` 必须包含所有依赖项和少量元数据，以便 colcon 找到包的正确构建顺序、在 CI 中安装所需的依赖项，并为使用 ``bloom`` 发布提供信息。
``CMakeLists.txt`` 包含构建和打包可执行文件及库的命令，将是本文档的重点。

基本项目大纲
^^^^^^^^^^^^

一个 ament 包的 ``CMakeLists.txt`` 的基本大纲包含：

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.8)
    project(my_project)

    ament_package()

``project`` 的参数将是包名，并且必须与 ``package.xml`` 中的包名完全相同。

项目设置由 ``ament_package()`` 完成，并且该调用在每个包中必须恰好出现一次。
``ament_package()`` 会安装 ``package.xml``、在 ament 索引中注册该包，并为 CMake 安装配置（可能还有目标）文件，以便其他包可以通过 ``find_package`` 找到它。
由于 ``ament_package()`` 会从 ``CMakeLists.txt`` 中收集大量信息，因此它应该是你的 ``CMakeLists.txt`` 中的最后一次调用。

``ament_package`` 可以接受额外的参数：

- ``CONFIG_EXTRAS``：一个 CMake 文件列表（``.cmake`` 或由 ``configure_file()`` 展开的 ``.cmake.in`` 模板），这些文件应该可供该包的客户端使用。
  关于何时使用这些参数的示例，请参见`添加资源`_中的讨论。
  有关如何使用模板文件的更多信息，请参见`官方文档 <https://cmake.org/cmake/help/v3.8/command/configure_file.html>`__。

- ``CONFIG_EXTRAS_POST``：与 ``CONFIG_EXTRAS`` 相同，但文件被添加的顺序不同。
  ``CONFIG_EXTRAS`` 文件在针对 ``ament_export_*`` 调用生成的文件之前被包含，而 ``CONFIG_EXTRAS_POST`` 中的文件则在这些文件之后被包含。

除了添加到 ``ament_package`` 之外，你也可以添加到变量 ``${PROJECT_NAME}_CONFIG_EXTRAS`` 和 ``${PROJECT_NAME}_CONFIG_EXTRAS_POST`` 中，效果相同。
唯一的区别同样在于文件被添加的顺序，总顺序如下：

- 由 ``CONFIG_EXTRAS`` 添加的文件

- 通过追加到 ``${PROJECT_NAME}_CONFIG_EXTRAS`` 添加的文件

- 通过追加到 ``${PROJECT_NAME}_CONFIG_EXTRAS_POST`` 添加的文件

- 由 ``CONFIG_EXTRAS_POST`` 添加的文件

编译器和链接器选项
^^^^^^^^^^^^^^^^^^

ROS 2 面向符合 C++17 和 C99 标准的编译器。
未来可能会面向更新的版本，相关引用见`这里 <https://reps.openrobotics.org/rep-2000/>`__。
因此，习惯上会设置相应的 CMake 标志：

.. code-block:: cmake

    if(NOT CMAKE_C_STANDARD)
      set(CMAKE_C_STANDARD 99)
    endif()
    if(NOT CMAKE_CXX_STANDARD)
      set(CMAKE_CXX_STANDARD 17)
    endif()

为了保持代码整洁，编译器应该对有问题的代码发出警告，并且这些警告应该被修复。

建议至少覆盖以下警告级别：

- 对于 Visual Studio：默认的 ``W1`` 警告

- 对于 GCC 和 Clang：强烈推荐 ``-Wall -Wextra -Wpedantic``，建议使用 ``-Wshadow``

目前建议使用 ``add_compile_options`` 为所有目标添加这些选项。
这可以避免为所有可执行文件、库和测试杂乱的基于目标的编译选项弄乱代码：

.. code-block:: cmake

    if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
      add_compile_options(-Wall -Wextra -Wpedantic)
    endif()

查找依赖项
^^^^^^^^^^

大多数 ``ament_cmake`` 项目都会依赖其他包。
在 CMake 中，这是通过调用 ``find_package`` 实现的。
例如，如果你的包依赖于 ``rclcpp``，那么 ``CMakeLists.txt`` 文件应该包含：

.. code-block:: cmake

    find_package(rclcpp REQUIRED)

.. note::

    应该永远不需要 ``find_package`` 一个并非明确需要、但却是另一个明确需要的依赖项的依赖项的库。
    如果出现这种情况，请针对相应的包提交错误报告。

添加目标
^^^^^^^^

在 CMake 术语中，``targets`` 是该项目将要创建的产物。
可以创建库或可执行文件，单个项目可以包含零个或多个每种产物。

.. tabs::

    .. group-tab:: 库

        这些是通过调用 ``add_library`` 创建的，该调用应包含目标名称以及为创建库而需要编译的源文件。

        由于 C/C++ 中头文件与实现分离，通常不需要将头文件作为 ``add_library`` 的参数添加。

        建议以下最佳实践：

        - 将所有可供该库的客户端使用的头文件（因此必须安装）放入 ``include`` 文件夹中一个以包命名的子目录中，而所有其他文件（``.c/.cpp`` 以及不应导出的头文件）则位于 ``src`` 文件夹中

        - 在调用 ``add_library`` 时只显式引用 ``.c/.cpp`` 文件

        - 通过以下方式找到库 ``my_library`` 的头文件

        .. code-block:: cmake

            target_include_directories(my_library
              PUBLIC
                "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
                "$<INSTALL_INTERFACE:include/${PROJECT_NAME}>")

        这会在构建期间将文件夹 ``${CMAKE_CURRENT_SOURCE_DIR}/include`` 中的所有文件添加到公共接口，并在安装时将 include 文件夹（相对于 ``${CMAKE_INSTALL_DIR}``）中的所有文件添加到公共接口。

        ``ros2 pkg create`` 会创建遵循这些规则的包布局。

        .. note::

            由于 Windows 是官方支持的平台之一，为了产生最大的影响，任何包也应该能在 Windows 上构建。
            Windows 库格式强制符号可见性；也就是说，每个应被客户端使用的符号都必须由库显式导出（并且符号需要被隐式导入）。

            由于 GCC 和 Clang 构建通常不会这样做，建议使用 `GCC wiki <https://gcc.gnu.org/wiki/Visibility>`__ 中的逻辑。
            要将其用于名为 ``my_library`` 的包：

            - 将链接中的逻辑复制到一个名为 ``visibility_control.hpp`` 的头文件中。

            - 将 ``DLL`` 替换为 ``MY_LIBRARY``\ （示例请参见 `rviz_rendering <https://github.com/ros2/rviz/blob/ros2/rviz_rendering/include/rviz_rendering/visibility_control.hpp>`__ 的可见性控制）。

            - 对所有需要导出的符号（即类或函数）使用宏 "MY_LIBRARY_PUBLIC"。

            - 在项目的 ``CMakeLists.txt`` 中使用：

              .. code-block:: cmake

                  target_compile_definitions(my_library PRIVATE "MY_LIBRARY_BUILDING_LIBRARY")

            更多详情请参见 :ref:`Windows Tips and Tricks 文档中的 Windows 符号可见性 <Windows_Symbol_Visibility>`。

    .. group-tab:: 可执行文件

        这些应通过调用 ``add_executable`` 创建，该调用应包含目标名称以及为创建可执行文件而需要编译的源文件。
        可执行文件可能还需要使用 ``target_link_libraries`` 链接到本包中创建的任何库。

        由于可执行文件通常不会被客户端作为库使用，因此无需将头文件放入 ``include`` 目录中。

如果一个包同时包含库和可执行文件，请确保结合上面"库"和"可执行文件"两部分的建议。

链接到依赖项
^^^^^^^^^^^^

有两种方法可以将你的目标链接到依赖项。

第一种也是推荐的方法是使用 ament 宏 ``ament_target_dependencies``。
举例来说，假设我们想将 ``my_library`` 链接到线性代数库 Eigen3。

.. code-block:: cmake

    find_package(Eigen3 REQUIRED)
    ament_target_dependencies(my_library PUBLIC Eigen3)

它包含了必要的头文件、库及其依赖项，以便项目能够正确找到它们。

第二种方法是使用 ``target_link_libraries``。

现代 CMake 倾向于只使用目标，导出并链接到它们。
CMake 目标可以有命名空间，类似于 C++。
如果命名空间目标可用，请优先使用它们。
例如，``Eigen3`` 定义了目标 ``Eigen3::Eigen``。

在 Eigen3 的示例中，调用应该如下所示

.. code-block:: cmake

    target_link_libraries(my_library PUBLIC Eigen3::Eigen)

这同样会包含必要的头文件、库及其依赖项。
请注意，此依赖项必须之前已通过调用 ``find_package`` 被发现。

安装
^^^^

.. tabs::

    .. group-tab:: 库

        在构建可复用的库时，需要导出一些信息，以便下游包能够轻松地使用它。

        首先，安装应可供客户端使用的头文件。
        include 目录是自定义的，以支持 ``colcon`` 中的覆盖层；更多信息请参见 https://colcon.readthedocs.io/en/released/user/overriding-packages.html#install-headers-to-a-unique-include-directory。

        .. code-block:: cmake

            install(
              DIRECTORY include/
              DESTINATION include/${PROJECT_NAME}
            )

        接下来，安装目标并创建导出目标（``export_${PROJECT_NAME}``），其他代码将使用它来查找此包。
        请注意，你可以使用一次 ``install`` 调用来安装项目中的所有库。

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

        上面代码片段中发生的情况如下：

        - ``ament_export_targets`` 宏为 CMake 导出目标。
          这是必要的，以便你的库的客户端可以使用 ``target_link_libraries(client PRIVATE my_library::my_library)`` 语法。
          如果导出集包含库，请为 ``ament_export_targets`` 添加 ``HAS_LIBRARY_TARGET`` 选项，这会把潜在的库添加到环境变量中。

        - ``ament_export_dependencies`` 将依赖项导出给下游包。
          这是必要的，这样库的使用者就不必再为这些依赖项调用 ``find_package`` 了。

        .. warning::

            从 CMake 子目录调用 ``ament_export_targets``、``ament_export_dependencies`` 或其他 ament 命令将无法按预期工作。
            这是因为 CMake 子目录无法在调用 ``ament_package`` 的父作用域中设置必要的变量。

        .. note::

            Windows DLL 被视为运行时产物，会安装到 ``RUNTIME DESTINATION`` 文件夹中。
            因此，即使在基于 Unix 的系统上开发库时，也建议保留 ``RUNTIME`` 安装。

        - ``install`` 调用中的 ``EXPORT`` 表示法需要格外注意：
          它为 ``my_library`` 目标安装 CMake 文件。
          它的命名必须与 ``ament_export_targets`` 中的参数完全相同。
          为了确保它可以通过 ``ament_target_dependencies`` 使用，它不应与库名完全相同，而应带有一个类似 ``export_`` 的前缀（如上所示）。

        - 所有安装路径都相对于 ``CMAKE_INSTALL_PREFIX``，colcon/ament 已经正确设置了该变量。

        还有两个可用的附加函数，但对于基于目标的安装来说是多余的：

        .. code-block:: cmake

            ament_export_include_directories("include/${PROJECT_NAME}")
            ament_export_libraries(my_library)

        第一个宏标记导出的 include 目录的目录位置。
        第二个宏标记已安装库的位置（这是由 ``ament_export_targets`` 调用中的 ``HAS_LIBRARY_TARGET`` 参数完成的）。
        只有当下游项目不能或不想使用基于 CMake 目标的依赖项时，才应使用这些宏。

        有些宏可以为非目标导出接受不同类型的参数，但由于现代 Make 的推荐方式是使用目标，我们在此不做介绍。
        这些选项的文档可以在源代码本身中找到。

    .. group-tab:: 可执行文件

        在安装可执行文件时，以下段落*必须完全照做*，以便其余的 ROS 工具能够找到它：

        .. code-block:: cmake

            install(TARGETS my_exe
                DESTINATION lib/${PROJECT_NAME})

如果一个包同时包含库和可执行文件，请确保结合上面"库"和"可执行文件"两部分的建议。

代码检查和测试
--------------

为了将测试与使用 colcon 构建库分开，请将所有对 linter 和测试的调用包装在一个条件中：

.. code-block:: cmake

    if(BUILD_TESTING)
      find_package(ament_cmake_gtest REQUIRED)
      ament_add_gtest(<tests>)
    endif()

代码检查
^^^^^^^^

建议使用 `ament_lint_auto <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_lint_auto/doc/index.rst#ament_lint_auto>`_ 中的组合调用：

.. code-block:: cmake

    find_package(ament_lint_auto REQUIRED)
    ament_lint_auto_find_test_dependencies()

这将运行 ``package.xml`` 中定义的 linter。
建议使用 ``ament_lint_common`` 包定义的 linter 集合。
其中包含的各个 linter 及其函数可以在 `ament_lint_common 文档 <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_lint_common/doc/index.rst>`_ 中查看。

ament 提供的 linter 也可以单独添加，而不运行 ``ament_lint_auto``。
这样做的一个示例可以在 `ament_cmake_lint_cmake 文档 <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_cmake_lint_cmake/doc/index.rst>`_ 中找到。

测试
^^^^

Ament 包含用于简化 GTest 设置的 CMake 宏。
调用：

.. code-block:: cmake

    find_package(ament_cmake_gtest)
    ament_add_gtest(some_test <test_sources>)

来添加一个 GTest。
此后它就是一个常规目标，可以链接到其他库（例如项目库）。
这些宏有额外的参数：

- ``APPEND_ENV``：追加环境变量。
  例如，你可以通过以下调用添加到 ament 前缀路径：

.. code-block:: cmake

    find_package(ament_cmake_gtest REQUIRED)
    ament_add_gtest(some_test <test_sources>
      APPEND_ENV PATH=some/additional/path/for/testing/resources)

- ``APPEND_LIBRARY_DIRS``：追加库，以便链接器在运行时能够找到它们。
  这可以通过设置环境变量（如在 Windows 上设置 ``PATH``、在 Linux 上设置 ``LD_LIBRARY_PATH``）来实现，但这会使调用与平台相关。

- ``ENV``：设置环境变量（语法与 ``APPEND_ENV`` 相同）。

- ``TIMEOUT``：以秒为单位设置测试超时时间。
  GTest 的默认值为 60 秒。
  例如：

.. code-block:: cmake

    ament_add_gtest(some_test <test_sources> TIMEOUT 120)

- ``SKIP_TEST``：跳过此测试（将在控制台输出中显示为"已通过"）。

- ``SKIP_LINKING_MAIN_LIBRARIES``：不链接 GTest。

- ``WORKING_DIRECTORY``：设置测试的工作目录。

否则，默认工作目录是 ``CMAKE_CURRENT_BINARY_DIR``，这在 `CMake 文档 <https://cmake.org/cmake/help/latest/variable/CMAKE_CURRENT_BINARY_DIR.html>`_ 中有描述。

类似地，还有一个用于设置包含 GMock 的 GTest 的 CMake 宏：

.. code-block:: cmake

    find_package(ament_cmake_gmock REQUIRED)
    ament_add_gmock(some_test <test_sources>)

它的附加参数与 ``ament_add_gtest`` 相同。

扩展 ament
----------

可以向 ``ament_cmake`` 注册额外的宏/函数，并以多种方式扩展它。

向 ament 添加函数/宏
^^^^^^^^^^^^^^^^^^^^

扩展 ament 通常意味着你希望某些函数可供其他包使用。
向客户端包提供宏的最佳方式是将其注册到 ament 中。

这可以通过追加 ``${PROJECT_NAME}_CONFIG_EXTRAS`` 变量来实现，该变量由 ``ament_package()`` 通过以下方式使用：

.. code-block:: cmake

    list(APPEND ${PROJECT_NAME}_CONFIG_EXTRAS
      path/to/file.cmake"
      other/pathto/file.cmake"
    )

或者，你也可以直接将文件添加到 ``ament_package()`` 调用中：

.. code-block:: cmake

    ament_package(CONFIG_EXTRAS
      path/to/file.cmake
      other/pathto/file.cmake
    )

添加到扩展点
^^^^^^^^^^^^

除了提供包含可供其他包使用的函数的简单文件外，你还可以向 ament 添加扩展。
这些扩展是在定义扩展点的函数中被执行的脚本。
ament 扩展最常见的用例可能是注册 rosidl 消息生成器：
在编写生成器时，你通常希望用你的生成器生成所有消息和服务，而无需修改消息/服务定义包的代码。
这可以通过将生成器注册为 ``rosidl_generate_interfaces`` 的扩展来实现。

举个例子，参见

.. code-block:: cmake

    ament_register_extension(
      "rosidl_generate_interfaces"
      "rosidl_generator_cpp"
      "rosidl_generator_cpp_generate_interfaces.cmake")

它将包 ``rosidl_generator_cpp`` 的宏 ``rosidl_generator_cpp_generate_interfaces.cmake`` 注册到扩展点 ``rosidl_generate_interfaces``。
当扩展点被执行时，这将触发脚本 ``rosidl_generator_cpp_generate_interfaces.cmake`` 在此处执行。
特别是，每当函数 ``rosidl_generate_interfaces`` 被执行时，都会调用该生成器。

对生成器而言，除 ``rosidl_generate_interfaces`` 外最重要的扩展点是 ``ament_package``，它会在 ``ament_package()`` 调用时简单地执行脚本。
此扩展点在注册资源时很有用（见下文）。

``ament_register_extension`` 是一个恰好接受三个参数的函数：

- ``extension_point``：扩展点的名称（大多数情况下是 ``ament_package`` 或 ``rosidl_generate_interfaces`` 之一）

- ``package_name``：包含 CMake 文件的包的名称（即写入该文件所在项目的项目名）

- ``cmake_filename``：扩展点运行时执行的 CMake 文件

.. note::

    可以以类似于 ``ament_package`` 和 ``rosidl_generate_interfaces`` 的方式定义自定义扩展点，但这几乎不应该是必要的。

添加扩展点
^^^^^^^^^^

极少数情况下，为 ament 定义一个新的扩展点可能是有意义的。

扩展点可以在宏中注册，这样当相应的宏被调用时，所有扩展都会被执行。
要这样做：

- 为你的扩展定义并记录一个名称（例如 ``my_extension_point``），这是使用该扩展点时传给 ``ament_register_extension`` 宏的名称。

- 在应该执行扩展的宏/函数中调用：

.. code-block:: cmake

    ament_execute_extensions(my_extension_point)

Ament 扩展通过定义一个包含扩展点名称的变量，并用要执行的宏填充它来工作。
在调用 ``ament_execute_extensions`` 时，变量中定义的脚本随后会一个接一个地执行。

.. _ament-cmake-doc_adding-resources:

添加资源
--------

特别是在开发插件或允许插件的包时，从一个 ROS 包向另一个 ROS 包（例如插件）添加资源通常至关重要。
例如，使用 pluginlib 的工具的插件。

这可以通过使用 ament 索引（也称为"资源索引"）来实现。

ament 索引说明
^^^^^^^^^^^^^^

有关设计和意图的详情，请参见`这里 <https://github.com/ament/ament_cmake/blob/{REPOS_FILE_BRANCH}/ament_cmake_core/doc/resource_index.md>`__

原则上，ament 索引包含在`安装空间 <https://colcon.readthedocs.io/en/released/user/what-is-a-workspace.html#install-artifacts>`_ 内的一个文件夹中。
它包含以不同类型资源命名的浅层子文件夹。
在子文件夹中，每个提供该资源的包都通过一个"标记文件"按名称被引用。
该文件可以包含获取资源所需的任何内容，例如资源安装目录的相对路径，也可以简单地为空。

举个例子，考虑为 RViz 提供显示插件：
当在一个名为 ``my_rviz_displays`` 的项目中提供将由 pluginlib 读取的 RViz 插件时，你将提供一个 ``plugin_description.xml`` 文件，该文件将被安装并由 pluginlib 用来加载插件。
为此，通过以下方式将 plugin_description.xml 注册为 resource_index 中的资源：

.. code-block:: cmake

    pluginlib_export_plugin_description_file(rviz_common plugins_description.xml)

运行 ``colcon build`` 时，这会将一个名为 ``my_rviz_displays`` 的文件安装到 resource_index 中的一个子文件夹 ``rviz_common__pluginlib__plugin`` 中。
rviz_common 中的 pluginlib 工厂将知道从所有名为 ``rviz_common__pluginlib__plugin`` 的文件夹中收集导出插件的包的信息。
pluginlib 工厂的标记文件包含指向 ``plugins_description.xml`` 文件的安装文件夹相对路径（以及作为标记文件名的库名）。
有了这些信息，pluginlib 就可以加载库，并知道要从 ``plugin_description.xml`` 文件加载哪些插件。

作为第二个示例，考虑让你的自定义 RViz 插件使用你自己的自定义网格。
网格在启动时被加载，这样插件所有者就不必处理它，但这意味着 RViz 必须知道这些网格。
为此，RViz 提供了一个函数：

.. code-block:: cmake

    register_rviz_ogre_media_exports(DIRECTORIES <my_dirs>)

这会在 ament 索引中将目录注册为 ogre_media 资源。
简而言之，它会安装一个以调用该函数的项目命名的文件到名为 ``rviz_ogre_media_exports`` 的子文件夹中。
该文件包含宏中列出的目录的安装文件夹相对路径。
在启动时，RViz 现在可以搜索所有名为 ``rviz_ogre_media_exports`` 的文件夹，并加载所提供所有文件夹中的资源。
这些搜索使用 ``ament_index_cpp``（或用于 Python 包的 ``ament_index_py``）完成。

在接下来的部分中，我们将探讨如何将你自己的资源添加到 ament 索引，并提供这样做的最佳实践。

查询 ament 索引
^^^^^^^^^^^^^^^

如有必要，可以通过 CMake 查询 ament 索引中的资源。
为此，有三个函数：

``ament_index_has_resource``：如果资源存在，则获取该资源的前缀路径，参数如下：

- ``var``：输出参数：如果资源不存在，则将此变量填充为 FALSE，否则填充为资源的前缀路径

- ``resource_type``：资源的类型（例如 ``rviz_common__pluginlib__plugin``）

- ``resource_name``：资源的名称，通常等于添加了 resource_type 类型资源的包名（例如 ``rviz_default_plugins``）

``ament_index_get_resource``：获取特定资源的内容，即 ament 索引中标记文件的内容。

- ``var``：输出参数：如果资源标记文件存在，则填充为其内容。

- ``resource_type``：资源的类型（例如 ``rviz_common__pluginlib__plugin``）

- ``resource_name``：资源的名称，通常等于添加了 resource_type 类型资源的包名（例如 ``rviz_default_plugins``）

- ``PREFIX_PATH``：要搜索的前缀路径（通常使用默认的 ``ament_index_get_prefix_path()`` 就足够了）。

请注意，如果资源不存在，``ament_index_get_resource`` 会抛出错误，因此可能需要使用 ``ament_index_has_resource`` 进行检查。

``ament_index_get_resources``：从索引中获取注册了特定类型资源的所有包

- ``var``：输出参数：填充为注册了 resource_type 资源的所有包的名称列表

- ``resource_type``：资源的类型（例如 ``rviz_common__pluginlib__plugin``）

- ``PREFIX_PATH``：要搜索的前缀路径（通常使用默认的 ``ament_index_get_prefix_path()`` 就足够了）。

添加到 ament 索引
^^^^^^^^^^^^^^^^^

定义资源需要两方面的信息：

- 资源的名称，它必须是唯一的，

- 标记文件的布局，它可以是任何内容，也可以为空（例如，标记 ROS 2 包的 "package" 资源就是这种情况）

对于 RViz 网格资源，相应的选择是：

- 以 ``rviz_ogre_media_exports`` 作为资源的名称，

- 指向所有包含资源的文件夹的安装路径相对路径。
  这已经能让你编写在包中使用相应资源的逻辑。

为了允许用户轻松地为你的包注册资源，你最好进一步提供宏或函数，例如 pluginlib 函数或 ``rviz_ogre_media_exports`` 函数。

要注册资源，请使用 ament 函数 ``ament_index_register_resource``。
这将在 resource_index 中创建并安装标记文件。
例如，``rviz_ogre_media_exports`` 的相应调用如下：

.. code-block:: cmake

    ament_index_register_resource(rviz_ogre_media_exports CONTENT ${OGRE_MEDIA_RESOURCE_FILE})

这会安装一个以 ``${PROJECT_NAME}`` 命名的文件到 resource_index 中的 ``rviz_ogre_media_exports`` 文件夹中，其内容由变量 ``${OGRE_MEDIA_RESOURCE_FILE}`` 给出。
该宏有一些可能有用的参数：

- 第一个（未命名的）参数是资源的名称，它等于 resource_index 中文件夹的名称

- ``CONTENT``：标记文件的内容，以字符串表示。
  这可以是相对路径列表等。
  ``CONTENT`` 不能与 ``CONTENT_FILE`` 一起使用。

- ``CONTENT_FILE``：用于创建标记文件的文件的路径。
  该文件可以是普通文件，也可以是使用 ``configure_file()`` 展开的模板文件。
  ``CONTENT_FILE`` 不能与 ``CONTENT`` 一起使用。

- ``PACKAGE_NAME``：导出资源的包/库的名称，它等于标记文件的名称。
  默认为 ``${PROJECT_NAME}``。

- ``AMENT_INDEX_BINARY_DIR``：生成的 ament 索引的基路径。
  除非确实必要，否则始终使用默认值 ``${CMAKE_BINARY_DIR}/ament_cmake_index``。

- ``SKIP_INSTALL``：跳过标记文件的安装。

由于每个包只存在一个标记文件，如果 CMake 函数/宏被同一项目调用两次，通常会出问题。
不过，对于大型项目，最好将注册资源的调用拆分。

因此，最佳实践是让注册资源的宏（例如 ``register_rviz_ogre_media_exports.cmake``）只填充一些变量。
真正对 ``ament_index_register_resource`` 的调用可以添加到 ``ament_package`` 的 ament 扩展中。
由于每个项目必须且只能有一次 ``ament_package`` 调用，因此资源注册的位置始终只有一个。
对于 ``rviz_ogre_media_exports``，这相当于以下策略：

- 宏 ``register_rviz_ogre_media_exports`` 接受一个文件夹列表，并将它们追加到一个名为 ``OGRE_MEDIA_RESOURCE_FILE`` 的变量中。

- 另一个名为 ``register_rviz_ogre_media_exports_hook`` 的宏在 ``${OGRE_MEDIA_RESOURCE_FILE}`` 非空时调用 ``ament_index_register_resource``。

- ``register_rviz_ogre_media_exports_hook.cmake`` 文件在第三个文件 ``register_rviz_ogre_media_exports_hook-extras.cmake`` 中通过调用以下方式注册为 ament 扩展：

.. code-block:: cmake

    ament_register_extension("ament_package" "rviz_rendering"
      "register_rviz_ogre_media_exports_hook.cmake")

- 文件 ``register_rviz_ogre_media_exports.cmake`` 和 ``register_rviz_ogre_media_exports_hook-extra.cmake`` 通过 ``ament_package()`` 注册为 ``CONFIG_EXTRA``。

设置环境变量
------------
``ament_cmake`` 提供了一种机制，可以在 ROS 2 工作空间被 source 时自动为其设置环境变量。
这在配置以下内容时会很有用：

- RMW 实现（设置 CycloneDDS、FastDDS 等）
- Gazebo 仿真（设置插件和资源的路径）
- 其他自定义的、特定于机器人的设置配置

这可以通过 ``ament_environment_hooks`` 来实现，它允许包定义在工作空间被 source 时设置的持久环境变量。

关于环境钩子
^^^^^^^^^^^^
环境钩子是由 ROS 2 包提供的 shell 脚本。
当工作空间中的 setup 文件被 source 时，这些钩子也会被 source。
这些脚本允许你设置或扩展环境变量，而无需手动修改 ``setup.bash`` 或 ``setup.zsh`` 文件。

这些环境钩子可以通过创建两种类型的脚本文件来实现：

- ``.dsv.in`` 文件：这些是机器可读的文件，用于指定预期的环境变量更改。
  Ament 处理这些文件比传统的 shell 脚本更高效，从而提高了设置环境的性能。

- ``.sh.in`` 文件：这些是由 Linux/macOS shell（如 sh、bash 和 zsh）执行的 shell 脚本。
  它们在 source 工作空间时在运行时设置环境变量。

这些文件由 ``colcon`` 处理，以生成最终的环境钩子脚本。

``ament_environment_hooks`` 的实际实现可以在官方的 `ament-cmake 仓库 <https://github.com/ament/ament_cmake/tree/master/ament_cmake_core/cmake/environment_hooks>`__ 中找到。

通过钩子定义持久环境变量
^^^^^^^^^^^^^^^^^^^^^^^^
本节提供一个快速示例，说明如何使用环境钩子为你的 ROS 2 包配置 FastDDS XML 配置文件。

定义环境钩子时一个推荐的最佳实践是，将它们放在包工作空间内的一个专门的 ``hooks`` 目录中。

在你创建的 ``hooks`` 文件夹中，按如下方式创建一个 ``my_package.sh.in``：

.. code-block:: bash

    export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
    export RMW_FASTRTPS_USE_QOS_FROM_XML=1
    export FASTRTPS_DEFAULT_PROFILES_FILE="$COLCON_CURRENT_PREFIX/my_dds_profile.xml"

在同一个文件夹中，按如下方式创建一个 ``my_package.dsv.in`` 文件：

.. code-block:: bash

    set;RMW_IMPLEMENTATION;rmw_fastrtps_cpp
    set;RMW_FASTRTPS_USE_QOS_FROM_XML;1
    set;FASTRTPS_DEFAULT_PROFILES_FILE;my_dds_profile.xml

添加后，你可以在 ``CMakeLists.txt`` 文件中使用 ament_environment_hooks 函数注册它们：

.. code-block:: bash

    ament_environment_hooks(
      "${CMAKE_CURRENT_SOURCE_DIR}/hooks/my_package.dsv.in"
      "${CMAKE_CURRENT_SOURCE_DIR}/hooks/my_package.sh.in"
    )

另一个使用环境钩子设置 Gazebo 插件路径的示例可以在官方的 `ros_gz_project_template <https://github.com/gazebosim/ros_gz_project_template/tree/main/ros_gz_example_gazebo/hooks>`__ 中找到。

API 版本管理
------------

ROS 2 通过 ``ament_generate_version_header`` 提供自动版本头文件生成，它会创建用于 API 版本管理和特性检测的编译期宏。
这对于维护向后兼容性以及根据库版本有条件地启用特性特别有用。

.. note::

    ``ament_generate_version_header`` 功能仅适用于 C、C++ 和其他基于 C 的语言。
    它会生成带有预处理器宏的 C/C++ 头文件，不适用于 Python 或其他非基于 C 的包。

理解自动生成的版本宏
^^^^^^^^^^^^^^^^^^^^

许多 ROS 2 C/C++ 包（例如 ``rclcpp``、``rcl`` 和 ``rmw``）会自动生成版本头文件，其中包含暴露库版本信息的宏。
这些版本头文件使用 `ament_generate_version_header.cmake <https://github.com/ament/ament_cmake/blob/${ROS_DISTRO}/ament_cmake_gen_version_h/cmake/ament_generate_version_header.cmake>`__ 脚本从 ``package.xml`` 文件生成。

生成的版本宏遵循以下命名约定：

- ``<PACKAGE_NAME>_VERSION_MAJOR``：主版本号
- ``<PACKAGE_NAME>_VERSION_MINOR``：次版本号
- ``<PACKAGE_NAME>_VERSION_PATCH``：补丁版本号
- ``<PACKAGE_NAME>_VERSION``：合并后的版本，作为单个整数（major * 10000 + minor * 100 + patch）
- ``<PACKAGE_NAME>_VERSION_STR``：版本的字符串表示（例如 "1.2.3"）
- ``<PACKAGE_NAME>_VERSION_GTE(major, minor, patch)``：用于检查版本是否大于或等于指定版本的宏

例如，``rclcpp`` 提供如下宏：

- ``RCLCPP_VERSION_MAJOR``
- ``RCLCPP_VERSION_MINOR``
- ``RCLCPP_VERSION_PATCH``
- ``RCLCPP_VERSION``
- ``RCLCPP_VERSION_STR``
- ``RCLCPP_VERSION_GTE(major, minor, patch)``

为你的包生成版本头文件
^^^^^^^^^^^^^^^^^^^^^^

要为你的包生成版本头文件，请将以下内容添加到你的 ``CMakeLists.txt`` 中：

.. code-block:: cmake

    find_package(ament_cmake_gen_version_h REQUIRED)
    ament_generate_version_header(my_library)

这会在 ``<build_dir>/my_library/version.h`` 处生成一个头文件，可以包含在你的代码中：

.. code-block:: cpp

    #include "my_library/version.h"

版本信息会自动从你的 ``package.xml`` 中的 ``<version>`` 标签提取。

默认情况下，生成的头文件会放置在构建目录的 ``<package_name>/version.h`` 下。
你可以自定义输出位置：

.. code-block:: cmake

    ament_generate_version_header(my_library HEADER_PATH "my_library/my_version.h")

使用版本宏进行 API 协商
^^^^^^^^^^^^^^^^^^^^^^^

版本宏支持运行期和编译期特性检测，这对于编写跨不同 ROS 2 发行版的可移植代码至关重要。

虽然 ROS 2 保证同一发行版内的 ABI（应用程序二进制接口）兼容性，但新的接口和特性可能会被向后移植。
这意味着在单个发行版内，根据安装的补丁版本不同，可用的 API 版本可能不同。
版本宏允许开发者在用某个特性之前检查它是否可用。

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

- **在使用新特性前检查**：在使用库的旧版本中可能不可用的特性时，始终使用版本宏。
- **提供回退实现**：尽可能为旧 API 版本提供替代实现，以保持向后兼容性。
- **记录版本要求**：在包文档中清楚地记录特定特性所需的最低版本。
- **跨版本测试**：如果你的包需要支持多个 ROS 2 发行版，请针对最低支持版本进行测试。
- **使用 GTE 宏**：进行版本比较时优先使用 ``_VERSION_GTE(major, minor, patch)`` 宏，因为它比手动比较各个版本组成部分提供了更清晰、更易读的语法。
