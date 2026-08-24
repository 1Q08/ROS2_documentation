.. redirect-from::

    Contributing/Windows-Tips-and-Tricks

Windows 技巧与窍门
==================

.. contents:: 目录
   :depth: 2
   :local:

ROS 2 将 Windows 10 作为一级平台支持，这意味着所有进入 ROS 2 核心的代码都必须支持 Windows。
对于习惯在 Linux 或其他类 Unix 系统上进行传统开发的人来说，在 Windows 上开发可能会有些挑战。
本文旨在列出其中一些差异。

最大路径长度
------------
默认情况下，Windows 的 `最大路径长度 <https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation>`__ 为 260 个字符。
实际上，其中 4 个字符总是被驱动器号、冒号、开头的反斜杠和末尾的 NULL 字符占用。
这意味着路径所有部分之和只有 256 个字符可用。
这对 ROS 2 有两个实际影响：

* ROS 2 的一些内部路径名相当长。
  因此，我们始终建议为你的 ROS 2 目录根使用短路径名，例如 ``C:\dev``。
* 从源码构建 ROS 2 时，colcon 默认的隔离构建模式可能生成非常长的路径名。
  为了避免这些非常长的路径名，在 Windows 上构建时请使用 ``--merge-install``。

**注意**：可以将 Windows 更改为具有更长的最大路径长度。
有关更多信息，请参阅 `这篇文章 <https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=cmd#enable-long-paths-in-windows-10-version-1607-and-later>`__。

.. _Windows_Symbol_Visibility:

符号可见性
----------
Microsoft Visual C++ 编译器 (MSVC) 仅当符号被显式导出时才会从动态链接库 (DLL) 中暴露它们。
clang 和 gcc 编译器有同样的选项，但默认关闭。
因此，当先前在 Linux 上构建的库在 Windows 上构建时，其他库可能无法解析外部符号。
以下是由于符号未被暴露而可能导致的常见错误消息示例：

.. code-block:: console

   error C2448: '__attribute__': function-style initializer appears to be a function definition
   'visibility': identifier not found

.. code-block:: console

   CMake Error at C:/ws_ros2/install/random_numbers/share/random_numbers/cmake/ament_cmake_export_libraries-extras.cmake:48 (message):
      Package 'random_numbers' exports the library 'random_numbers' which
      couldn't be found

符号可见性也会影响二进制加载。
如果你发现某个可组合节点无法运行，或者 Qt Visualizer 无法工作，可能是因为宿主进程无法从二进制中找到预期的符号导出。
在 Windows 上诊断此问题，Windows 开发者工具包含一个名为 Gflags 的程序来启用各种选项。
其中一项选项称为 *Loader Snaps*，它让你能够在调试时检测加载失败。
有关 `Gflags <https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/setting-and-clearing-image-file-flags>`__ 和 `Loaders snaps <https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/show-loader-snaps>`__ 的更多信息，请访问 Microsoft 文档。

在 Windows 上导出符号的两种解决方案是可见性控制头文件和 ``WINDOWS_EXPORT_ALL_SYMBOLS`` 属性。
Microsoft 建议 ROS 开发者使用可见性控制头文件来控制二进制中符号的导出。
可见性控制头文件提供了对符号导出宏的更多控制，并提供其他好处，包括更小的二进制体积和更短的链接时间。

可见性控制头文件
^^^^^^^^^^^^^^^^
可见性控制头文件的目的在于为每个共享库定义一个宏，正确地将符号声明为 dllimport 或 dllexport。
这取决于该库是被消费还是被构建自身。
宏中的逻辑还会考虑编译器，并包含选择适当语法的逻辑。
`GCC 可见性文档 <https://gcc.gnu.org/wiki/Visibility>`__ 包含向库添加显式符号可见性的逐步说明，"产出最高质量的代码，并最大程度地减少二进制体积、加载时间和链接时间"。
可以在每个库的 ``includes`` 文件夹中放置一个名为 ``visibility_control.h`` 的头文件，如下面的示例所示。
下面的示例展示了如何为名为 ``my_lib`` 的库（其中有一个名为 ``example_class`` 的类）添加可见性控制头文件。
为库的 include 文件夹添加一个可见性头文件。
样板逻辑与宏中使用的库名配合，使其在项目中唯一。
在另一个库中，``MY_LIB`` 将被替换为库名。

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

有关此头文件的完整示例，请参阅 `rviz_rendering <https://github.com/ros2/rviz/blob/ros2/rviz_rendering/include/rviz_rendering/visibility_control.hpp>`__。

要使用该宏，请在需要对外部库可见的符号前添加 ``MY_LIB_PUBLIC``。
例如：

.. code-block:: c++

   Class MY_LIB_PUBLIC example_class {}

   MY_LIB_PUBLIC void example_function (){}

为了以正确导出的符号构建你的库，你需要向 CMakeLists.txt 文件添加以下内容：

.. code-block:: cmake

  target_compile_definitions(${PROJECT_NAME}
    PRIVATE "MY_LIB_BUILDING_LIBRARY")


WINDOWS_EXPORT_ALL_SYMBOLS 目标属性
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
CMake 在 Windows 上实现 ``WINDOWS_EXPORT_ALL_SYMBOLS`` 属性，该属性会使函数符号自动导出。
有关其工作原理的更多细节，可参阅 `WINDOWS_EXPORT_ALL_SYMBOLS CMake 文档 <https://cmake.org/cmake/help/latest/prop_tgt/WINDOWS_EXPORT_ALL_SYMBOLS.html>`__。
可以通过向 CMakeLists 文件添加以下内容来实现该属性：

.. code-block:: cmake

   set_target_properties(${LIB_NAME} PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS TRUE)

如果一个 CMakeLists 文件中有多个库，你需要分别对每个库调用 ``set_target_properties``。

请注意，Windows 上的二进制只能导出 65,536 个符号。
如果二进制导出的符号超过该数量，你会收到错误，应该使用 visibility_control 头文件。
在全局数据符号的情况下，此方法有一个例外。
例如，如下所示的全局静态数据成员。

.. code-block:: c++

   class Example_class
   {
   public:
   static const int Global_data_num;


在这些情况下，必须显式应用 dllimprort/dllexport。
可以使用 generate_export_header 来实现，如下文所述：`无需 declspec() 即可在 Windows 上使用新 CMake export all 功能创建 dll <https://blog.kitware.com/create-dlls-on-windows-without-declspec-using-new-cmake-export-all-feature/>`__。

最后，重要的是导出符号的头文件必须被包含到包中至少一个 ``.cpp`` 文件中，这样宏才会被展开并放入生成的二进制。
否则符号仍然无法被调用。


Debug 构建
----------
在 Windows 上以 Debug 模式构建时，有几件非常重要的事情会改变。
首先是所有 DLL 都会自动在库名后追加 ``_d``。
因此，如果库名为 ``libfoo.dll``，在 Debug 模式下它将变成 ``libfoo_d.dll``。
Windows 上的动态链接器也知道查找这种形式的库，因此它不会找到没有 ``_d`` 前缀的库。
此外，Windows 在 Debug 模式下会开启一整套编译时和运行时检查，比 Release 构建严格得多。
出于这些原因，在多个 pull request 上运行 Windows Debug 构建并测试是个好主意。

正斜杠与反斜杠
--------------
在 Windows 中，默认的路径分隔符是反斜杠（``\``），这与 Linux 和 macOS 中使用的正斜杠（``/``）不同。
大多数 Windows API 可以接受两者作为路径分隔符，但这并不是普遍成立。
例如，``cmd.exe`` shell 只能在反斜杠字符下进行制表符补全，而不能在正斜杠下。
为了在 Windows 上获得最大兼容性，在 Windows 上应始终使用反斜杠作为路径分隔符。

为 vendored 软件包打补丁
------------------------
在 ROS 2 中 vendor 一个软件包时，通常需要打补丁来修复 bug、添加功能等。
典型的做法是修改 ``ExternalProject_add`` 调用，使用 ``patch`` 可执行文件添加 ``PATCH`` 命令。
不幸的是，chocolatey 提供的 ``patch`` 可执行文件需要 Administrator 权限才能运行。
解决办法是在对外部项目打补丁时使用 ``git apply-patch``。

``git apply-patch`` 自身有一个问题，即它只在应用于 git 仓库时才能正常工作。
因此，外部项目应始终使用 ``GIT`` 方法获取项目，然后使用 ``PATCH_COMMAND`` 调用 ``git apply-patch``。

上述所有内容的示例用法大致如下：

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

Windows 慢计时器（普遍的慢）
----------------------------
在 Windows 上运行的软件通常比在 Linux 上运行的软件慢得多。
这归因于多种因素，从默认时间片（根据 `文档 <https://docs.microsoft.com/en-us/windows/win32/procthread/multitasking>`__，每 20 ms）到运行的杀毒和反恶意软件进程数量，再到运行的后台进程数量。
由于这一切，测试*永远*不应期望 Windows 上的严格计时。
所有测试都应该有宽松的超时，并且只期望事件最终发生（这也会防止测试在 Linux 上变得不稳定）。

Shell
-----
Windows 上有两个主要的命令行 shell：历史悠久的 ``cmd.exe`` 和 PowerShell。

``cmd.exe`` 是最接近模拟旧 DOS shell 的命令 shell，不过能力大大增强。
它完全基于文本，只理解 DOS/Windows 的 ``batch`` 文件。

PowerShell 是较新的、基于对象的 shell，Microsoft 推荐用于大多数新应用。
它理解 ``ps1`` 文件进行配置。

ROS 2 同时支持 ``cmd.exe`` 和 PowerShell，因此任何更改（尤其是对 ``ament`` 或 ``colcon`` 之类的更改）都应在两者上进行测试。
