.. redirect-from::

    Contributing/Windows-Tips-and-Tricks

Windows 技巧与提示
==================

.. contents:: 目录
   :depth: 2
   :local:

ROS 2 将 Windows 10 支持为 Tier 1 平台，这意味着所有进入 ROS 2 核心的代码都必须支持 Windows。
对于习惯了在 Linux 或其他类 Unix 系统上做传统开发的人来说，在 Windows 上开发可能有点挑战。
本文旨在说明其中一些差异。

最大路径长度
------------
默认情况下，Windows 的 `最大路径长度 <https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation>`__ 为 260 个字符。
实际上，其中始终有 4 个字符被盘符、冒号、开头的反斜杠以及结尾的 NULL 字符占用。
这意味着路径各部分之和只有 256 个字符可用。
这对 ROS 2 有两个实际影响：

* ROS 2 内部的一些路径名相当长。
  因此，我们始终建议为 ROS 2 目录的根使用较短的路径名，例如 ``C:\dev``。
* 从源码构建 ROS 2 时，colcon 默认的隔离构建模式可能生成非常长的路径名。
  为避免这些非常长的路径名，在 Windows 上构建时请使用 ``--merge-install``。

**注意**：可以把 Windows 改为支持更长的最大路径长度。
更多信息请参见 `这篇文章 <https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=cmd#enable-long-paths-in-windows-10-version-1607-and-later>`__。

.. _Windows_Symbol_Visibility:

符号可见性
----------
Microsoft Visual C++ 编译器（MSVC）只有在动态链接库（DLL）中的符号被显式导出时才会暴露它们。
clang 和 gcc 编译器也有做同样事情的选项，但默认是关闭的。
因此，当某个原本在 Linux 上构建的库在 Windows 上构建时，其他库可能无法解析这些外部符号。
下面是可能由符号未被暴露引起的常见错误信息示例：

.. code-block:: console

   error C2448: '__attribute__': function-style initializer appears to be a function definition
   'visibility': identifier not found

.. code-block:: console

   CMake Error at C:/ws_ros2/install/random_numbers/share/random_numbers/cmake/ament_cmake_export_libraries-extras.cmake:48 (message):
      Package 'random_numbers' exports the library 'random_numbers' which
      couldn't be found

符号可见性也会影响二进制文件的加载。
如果你发现可组合节点无法运行，或者某个 Qt 可视化程序不能工作，可能是宿主进程无法从该二进制文件中找到预期的符号导出。
要在 Windows 上诊断这个问题，Windows 开发者工具中包含一个名为 Gflags 的程序，可以启用各种选项。
其中一个选项叫作 *Loader Snaps*，它使你能在调试时检测加载失败。
关于 `Gflags <https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/setting-and-clearing-image-file-flags>`__ 和 `Loaders snaps <https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/show-loader-snaps>`__ 的更多信息，请查阅 Microsoft 文档。

在 Windows 上导出符号有两种方案：可见性控制头文件（Visibility Control Headers）和 ``WINDOWS_EXPORT_ALL_SYMBOLS`` 属性。
Microsoft 建议 ROS 开发者使用可见性控制头文件来控制二进制文件中符号的导出。
可见性控制头文件对符号导出宏提供了更强的控制，并带来其他好处，包括更小的二进制体积和更短的链接时间。

可见性控制头文件
^^^^^^^^^^^^^^^^
可见性控制头文件的目的是为每个共享库定义一个宏，正确地声明符号为 dllimport 或 dllexport。
这取决于该库是被使用还是自身正在被构建。
宏中的逻辑还会考虑编译器，并包含选择合适语法的逻辑。
`GCC 可见性文档 <https://gcc.gnu.org/wiki/Visibility>`__ 包含了为库添加显式符号可见性的分步说明，这些做法“能产出质量最高的代码，并最大程度地减小二进制体积、缩短加载时间和链接时间”。
可以按下面的示例，把名为 ``visibility_control.h`` 的头文件放在每个库的 ``includes`` 文件夹中。
下面的示例展示了如何为一个名为 ``my_lib`` 的库（其中有一个名为 ``example_class`` 的类）添加可见性控制头文件。
把可见性头文件添加到该库的 include 文件夹。
样板逻辑中使用的库名用于让宏在项目中保持唯一。
在另一个库中，``MY_LIB`` 会被替换为该库的名称。

.. code-block:: c++

   #ifndef MY_LIB__VISIBILITY_CONTROL_H_
   #define MY_LIB__VISIBILITY_CONTROL_H_
   #if defined _WIN32 || defined __CYGWIN__
   #ifdef __GNUC__
      #define MY_LIB_EXPORT __attribute__ ((dllexport))
      #define MY_LIB_IMPORT __attribute__ ((dllimport))
   #else
      #define MY_LIB_EXPORT __declspec(dllexport)
      #define MY_LIB_IMPORT __declspec(dllimport)
   #endif
   #ifdef MY_LIB_BUILDING_LIBRARY
      #define MY_LIB_PUBLIC MY_LIB_EXPORT
   #else
      #define MY_LIB_PUBLIC MY_LIB_IMPORT
   #endif
   #define MY_LIB_PUBLIC_TYPE MY_LIB_PUBLIC
   #define MY_LIB_LOCAL
   #else
    // Linux visibility settings
   #define MY_LIB_PUBLIC_TYPE
   #endif
   #endif  // MY_LIB__VISIBILITY_CONTROL_H_

该头文件的完整示例，请参见 `rviz_rendering <https://github.com/ros2/rviz/blob/ros2/rviz_rendering/include/rviz_rendering/visibility_control.hpp>`__。

要使用该宏，请在需要对其他库可见的符号前添加 ``MY_LIB_PUBLIC``。
例如：

.. code-block:: c++

   Class MY_LIB_PUBLIC example_class {}

   MY_LIB_PUBLIC void example_function (){}

为了以正确导出的符号构建你的库，你需要在 CMakeLists.txt 文件中添加以下内容：

.. code-block:: cmake

  target_compile_definitions(${PROJECT_NAME}
    PRIVATE "MY_LIB_BUILDING_LIBRARY")


WINDOWS_EXPORT_ALL_SYMBOLS 目标属性
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
CMake 在 Windows 上实现了 ``WINDOWS_EXPORT_ALL_SYMBOLS`` 属性，它会自动导出函数符号。
其工作原理的更多细节可以在 `WINDOWS_EXPORT_ALL_SYMBOLS 的 CMake 文档 <https://cmake.org/cmake/help/latest/prop_tgt/WINDOWS_EXPORT_ALL_SYMBOLS.html>`__ 中找到。
通过在 CMakeLists 文件中添加以下内容即可使用该属性：

.. code-block:: cmake

   set_target_properties(${LIB_NAME} PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS TRUE)

如果一个 CMakeLists 文件中有多个库，你需要分别对每个库调用 ``set_target_properties``。

注意，Windows 上的一个二进制文件只能导出 65,536 个符号。
如果某个二进制文件导出的符号超过这个数量，就会报错，此时应使用 visibility_control 头文件。
对于全局数据符号，此方法存在例外情况。
例如，下面这样的全局静态数据成员。

.. code-block:: c++

   class Example_class
   {
   public:
   static const int Global_data_num;


在这些情况下，必须显式应用 dllimprort/dllexport。
这可以通过 generate_export_header 来实现，具体如下文所述：`Create dlls on Windows without declspec() using new CMake export all feature <https://blog.kitware.com/create-dlls-on-windows-without-declspec-using-new-cmake-export-all-feature/>`__。

最后，重要的是导出符号的头文件必须被包含到该软件包中至少一个 ``.cpp`` 文件里，这样宏才会被展开并放入生成的二进制文件中。
否则这些符号仍然无法被调用。


Debug 构建
----------
在 Windows 上以 Debug 模式构建时，有几件非常重要的事情会发生变化。
首先是所有 DLL 的库名后会自动追加 ``_d``。
因此，如果库名为 ``libfoo.dll``，在 Debug 模式下它会变成 ``libfoo_d.dll``。
Windows 上的动态链接器也知道要查找这种形式的库，所以它找不到不带 ``_d`` 后缀的库。
此外，Windows 在 Debug 模式下会启用一整套编译期和运行期检查，比 Release 构建严格得多。
出于这些原因，最好在 Windows 上运行 Debug 构建并对许多拉取请求进行测试。

正斜杠与反斜杠
--------------
在 Windows 中，默认的路径分隔符是反斜杠（``\``），这与 Linux 和 macOS 中使用正斜杠（``/``）不同。
大多数 Windows API 都能把两者都当作路径分隔符处理，但这并非普遍成立。
例如，``cmd.exe`` shell 只在使用反斜杠字符时才能进行 Tab 补全，使用正斜杠则不行。
为了在 Windows 上获得最大兼容性，在 Windows 中应始终使用反斜杠作为路径分隔符。

为 vendored 软件包打补丁
------------------------
在 ROS 2 中 vendoring 一个软件包时，经常需要应用补丁来修复缺陷、添加功能等。
通常的做法是修改 ``ExternalProject_add`` 调用，使用 ``patch`` 可执行文件添加一个 ``PATCH`` 命令。
遗憾的是，chocolatey 提供的 ``patch`` 可执行文件需要管理员权限才能运行。
变通办法是在为外部项目应用补丁时使用 ``git apply-patch``。

``git apply-patch`` 自身也有问题，它只有在应用到 git 仓库时才能正常工作。
因此，外部项目应始终使用 ``GIT`` 方法来获取项目，然后使用 ``PATCH_COMMAND`` 调用 ``git apply-patch``。

上述做法的示例用法大致如下：

.. code-block:: cmake

  ExternalProject_Add(mylibrary-${version}
    GIT_REPOSITORY https://github.com/lib/mylibrary.git
    GIT_TAG ${version}
    GIT_CONFIG advice.detachedHead=false
    # Suppress git update due to https://gitlab.kitware.com/cmake/cmake/-/issues/16419
    # See https://github.com/ament/uncrustify_vendor/pull/22 for details
    UPDATE_COMMAND ""
    TIMEOUT 600
    CMAKE_ARGS
      -DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}_install
      ${extra_cmake_args}
      -Wno-dev
    PATCH_COMMAND
      ${CMAKE_COMMAND} -E chdir <SOURCE_DIR> git apply -p1 --ignore-space-change --whitespace=nowarn ${CMAKE_CURRENT_SOURCE_DIR}/install-patch.diff
  )

Windows 上缓慢的定时器（以及整体缓慢）
--------------------------------------
在 Windows 上运行的软件总体上比在 Linux 上运行的慢得多。
这是由多种因素造成的，从默认时间片（根据 `文档 <https://docs.microsoft.com/en-us/windows/win32/procthread/multitasking>`__，为每 20 ms），到运行中的大量防病毒和反恶意软件进程，再到大量后台进程。
正因如此，测试在 Windows 上 *绝不应* 期望精确的时序。
所有测试都应有宽松的超时，并且只期望事件最终会发生（这也能防止测试在 Linux 上变得不稳定）。

Shell
-----
Windows 上有两种主要的命令行 shell：历史悠久的 ``cmd.exe`` 和 PowerShell。

``cmd.exe`` 是模拟老式 DOS shell 最接近的命令 shell，不过能力已被大大增强。
它完全基于文本，并且只理解 DOS/Windows 的 ``batch`` 文件。

PowerShell 是更新的、基于对象的 shell，Microsoft 推荐大多数新应用使用它。
它理解用于配置的 ``ps1`` 文件。

ROS 2 同时支持 ``cmd.exe`` 和 PowerShell，因此任何更改（尤其是对 ``ament`` 或 ``colcon`` 之类东西的更改）都应在两者上进行测试。
