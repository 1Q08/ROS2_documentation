Ament Lint 命令行工具
=====================

**目标：** 学习如何使用 ``ament_lint`` 及相关工具来识别和修复代码质量问题。

**教程级别：** 高级

**预计用时：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

``ament`` 系列的 CLI 工具是用于 ROS 2 软件开发的 Python 工具。
Ament 工具可用于任何构建系统，但这些工具的一个子集——``ament_cmake`` 工具——是专门为了让基于 CMake 的开发更加容易而设计的。
Ament 附带一系列 CLI 程序，可以帮助用户编写符合 ROS 2 编码标准的代码。
使用这些工具可以极大地提高开发速度，并帮助用户编写满足 `ROS 项目编码标准 <../../The-ROS2-Project/Contributing/Code-Style-Language-Versions>` 的 ROS 应用和核心代码。
我们建议 ROS 开发者熟悉这些工具，并在提交 pull request 之前使用它们。

先决条件
--------

作为常规 ROS 2 设置的一部分，你应该已经安装了 ``ament`` 软件包。

如果你需要安装 ROS 2，请参见 :doc:`安装说明 <../../Installation>`。


Ament Lint CLI 工具
-------------------

所有 ament lint 工具都使用类似的 CLI 模式。
它们接收一个目录、一个目录列表、文件或文件列表，分析输入文件并生成报告。
所有 ament lint 工具都有以下内置选项。
**对于某个给定的 ament 工具，最新、最准确的文档可以通过使用该工具内置的** ``--help`` **功能找到。**

* ``-h, --help`` - 显示帮助消息并退出。
  内置的帮助消息通常包含该工具最准确、最新的文档。
* ``--exclude [filename ...]`` - 要从分析中排除的文件名，支持通配符。
* ``--xunit-file XUNIT_FILE`` - 生成一个 `xunit <https://xunit.net/>`_ 兼容的 XML 文件。
  这些文件最常被 IDE 和 CI 用于自动化收集测试结果。



1 ``ament_copyright``
^^^^^^^^^^^^^^^^^^^^^

``ament_copyright`` CLI 可用于检查和更新 ROS 源代码中的版权声明。
这个工具还可以用于检查源代码中是否存在合适的软件许可证、版权年份和版权持有者。
``ament_copyright`` 工具相对于调用它的目录工作，它会遍历子目录并检查目录内的每个源文件。
你可以使用 ``ament_copyright`` 检查你的 ROS 包、ROS 工作区、目录或单个源文件，只需切换到相应的根目录并调用该命令即可。
``ament_copyright`` 还可以用于自动为缺少版权和许可证的源代码文件添加版权和许可证。


1.1 ``ament_copyright`` 参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

默认情况下，``ament_copyright`` 遍历调用它的目录（包括子目录），并返回一份报告，列出所有缺少版权声明的文件。
该程序接受一个可选参数，即需要扫描以生成报告的目录列表。
例如，如果你只想扫描源文件和头文件的版权声明，可以调用：``ament_copyright ./src ./include``。

1.2 ``ament_copyright`` 选项
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ament_copyright`` 支持以下选项：

* ``--add-missing COPYRIGHT_NAME LICENSE`` - 使用传入的版权持有者和许可证来添加缺失的版权声明和许可证信息。
  传给该选项的 ``LICENSE`` 是要使用的许可证名称。
  可用许可证的完整列表可以通过调用 ``ament_copyright --list-licenses`` 找到。
* ``--add-copyright-year`` - 将当前年份添加到现有版权声明中。
* ``--list-copyright-names`` - 列出已知版权持有者的名称。
* ``--list-licenses`` - 列出已知许可证的名称。
* ``--verbose`` - 显示所有文件，而不只是有错误/修改的文件。

1.3 ``ament_copyright`` 示例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

要检查你的 ROS 包是否有合适的版权和许可证文件，只需不带参数调用 ``ament_copyright``。
使用 ``--verbose`` 选项将列出所有被检查的文件。

.. code-block:: console

  $ ament_copyright --verbose
  my_package/src/new_file.cpp: could not find copyright notice
  my_package/src/old_file.cpp: copyright=Open Source Robotics Foundation, Inc. (2023), license=apache2
  my_package/include/new_file.h: could not find copyright notice
  my_package/include/old_file.h: copyright=Open Source Robotics Foundation, Inc. (2023), license=apache2


2 ``ament_cppcheck``
^^^^^^^^^^^^^^^^^^^^

``ament_cppcheck`` 命令行工具可用于对 C++ 源代码文件执行静态分析。
`静态分析 <https://en.wikipedia.org/wiki/Static_program_analysis>`_ 是自动审查源代码文件、找出那些在编译后常常会引发问题的模式的过程。
``ament_cppcheck`` 使用的底层工具 `cppcheck <https://github.com/danmar/cppcheck>`__ 的某些版本可能相当慢。
因此，``ament_cppcheck`` 可能在某些系统上被禁用。
要启用它，你只需要设置 ``AMENT_CPPCHECK_ALLOW_SLOW_VERSIONS`` 环境变量。


2.1 ``ament_cppcheck`` 参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~

默认情况下，``ament_cppcheck`` 遍历调用它的目录（包括子目录），并返回一份报告，列出源文件中所有潜在的问题。
该程序接受一个可选参数，即需要扫描以生成报告的目录列表。
例如，如果你只想扫描一个最近修改的文件，可以调用 ``ament_cppcheck ./src/my_cpp_file.cpp``。

2.2 ``ament_cppcheck`` 选项
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ament_cppcheck`` 支持以下选项：

* ``--libraries [LIBRARIES ...]`` - 除了 C 和 C++ 标准库之外要加载的库配置。
  每个库都以 '--library=<library_name>' 的形式传给 cppcheck。
* ``--include_dirs [INCLUDE_DIRS ...]`` - 被检查的 C/C++ 文件的包含目录。
  每个目录都以 '-I <include_dir>' 的形式传给 cppcheck（默认：None）
* ``--cppcheck-version`` - 获取 cppcheck 版本、打印它，然后退出。

2.3 ``ament_cppcheck`` 示例
~~~~~~~~~~~~~~~~~~~~~~~~~~~

在一个名为 ``example.cpp`` 的文件中创建下面这个简单的 C++ 程序。

.. code-block:: cpp

  int main()
  {
      char a[10];
      a[10] = 0;
      return 0;
  }


这个简单的程序访问了已分配数组越界的内存。
在包含该文件的目录中运行 ``ament_cppcheck`` 会产生以下结果：

.. code-block:: console

   $ ament_cppcheck
   [example.cpp:4]: (error: arrayIndexOutOfBounds) Array 'a[10]' accessed at index 10, which is out of bounds.


3 ``ament_cpplint``
^^^^^^^^^^^^^^^^^^^

``ament_cpplint`` 可用于使用 `cpplint <https://github.com/cpplint/cpplint?tab=readme-ov-file>`_ 对照 `Google 风格规范 <https://google.github.io/styleguide/cppguide.html>`_ 检查你的 C++ 代码。
``ament_cpplint`` 会扫描当前目录和子目录中所有 C++ 头文件和源文件，对文件应用 CppLint 并返回结果。
目前 ``ament_cpplint`` 无法自动解决它发现的问题；如果你想自动修复格式问题，请参见 ``ament_uncrustify``。


3.1 ``ament_cpplint`` 参数
~~~~~~~~~~~~~~~~~~~~~~~~~~
该程序接受一个可选参数，即需要扫描以生成报告的目录列表。
例如，如果你只想扫描源文件和头文件的版权声明，可以调用：``ament_copyright ./src ./include``。


3.2 ``ament_cpplint`` 选项
~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``--filters FILTER,FILTER,...`` - 要应用的类别过滤器列表，以逗号分隔。
* ``--linelength N`` - 最大行长度（默认：100）。
* ``--root ROOT`` - 传给 cpplint 的 --root 选项。


3.3 ``ament_cpplint`` 示例
~~~~~~~~~~~~~~~~~~~~~~~~~~

让我们创建一个名为 ``example.cpp`` 的简单 C++ 程序。
我们将添加几行违反编码标准的代码：

.. code-block:: cpp

  int main()
  {
    int a = 10;
    int b = 10;
    int c = 0;/*<trailing whitespace>*/
    if( a == b)  {/*<tab>*/      c=a;}/*<trailing whitespace>*/
    return 0;
  }


对这个文件应用 ``ament_cpplint`` 会产生以下错误：

.. code-block:: console

  example.cpp:0:  No copyright message found.  You should have a line: "Copyright [year] <Copyright Owner>"  [legal/copyright] [5]
  example.cpp:6:  Line ends in whitespace.  Consider deleting these extra spaces.  [whitespace/end_of_line] [4]
  example.cpp:6:  Tab found; better to use spaces  [whitespace/tab] [1]
  example.cpp:6:  Line ends in whitespace.  Consider deleting these extra spaces.  [whitespace/end_of_line] [4]
  example.cpp:6:  Missing spaces around =  [whitespace/operators] [4]


4 ``ament_flake8``
^^^^^^^^^^^^^^^^^^

`Flake8 <https://pypi.org/project/flake8/>`_ 是一个用于 lint 和风格强制的 Python 工具。
``ament_flake8`` 命令行工具可用于使用 `Flake8 <https://pypi.org/project/flake8/>`_ 快速对 Python 源代码文件执行 lint。
这个工具将帮助你找出 ROS Python 程序中的小错误和风格问题，例如行尾空白、过长的代码行、函数参数间距不当等等！
不过请注意，``flake8`` 和 ``ament_flake8`` 不能自动重新格式化代码来修复这些问题。

4.1 ``ament_flake8`` 参数
~~~~~~~~~~~~~~~~~~~~~~~~~

该程序接受一个可选参数，即需要扫描以生成报告的目录列表。
例如，如果你只想扫描工作区中的一个包，可以直接在该包的工作目录中调用 ``ament_flake8``，或者传给它一个目录路径。


4.2 ``ament_flake8`` 选项
~~~~~~~~~~~~~~~~~~~~~~~~~

* ``--config path`` - 要使用的配置文件。
  默认配置文件可以在你安装目录的 site packages 目录中找到。
  我们不建议更改默认设置。
* ``--linelength N`` - 手动设置最大行长度。

4.3 ``ament_flake8`` 示例
~~~~~~~~~~~~~~~~~~~~~~~~~

在一个名为 ``example.py`` 的文件中创建下面这个简单的 Python 程序。

.. code-block:: python

  def uglyPythonFunction(a,b,  c):
      if a != b:
          print("A does not match b")
      thisIsAVariableNameThatIsWayTooLongLongLong = 2
      extra_long =(thisIsAVariableNameThatIsWayTooLongLongLong*thisIsAVariableNameThatIsWayTooLongLongLong )
      return(c)

对这个文件应用 ``ament_flake8`` 会产生以下错误。

.. code-block:: console

  example.py:1:25: E231 missing whitespace after ','
  def uglyPythonFunction(a,b,  c):

  example.py:5:5: F841 local variable 'extra_long' is assigned to but never used
      extra_long =(thisIsAVariableNameThatIsWayTooLongLongLong*thisIsAVariableNameThatIsWayTooLongLongLong )
      ^

  example.py:5:17: E225 missing whitespace around operator
      extra_long =(thisIsAVariableNameThatIsWayTooLongLongLong*thisIsAVariableNameThatIsWayTooLongLongLong )
                  ^

  example.py:5:100: E501 line too long (106 > 99 characters)
      extra_long =(thisIsAVariableNameThatIsWayTooLongLongLong*thisIsAVariableNameThatIsWayTooLongLongLong )
                                                                                                     ^

  example.py:5:105: E202 whitespace before ')'
      extra_long =(thisIsAVariableNameThatIsWayTooLongLongLong*thisIsAVariableNameThatIsWayTooLongLongLong )
                                                                                                          ^

  1     E202 whitespace before ')'
  1     E225 missing whitespace around operator
  1     E231 missing whitespace after ','
  1     E501 line too long (106 > 99 characters)
  1     F841 local variable 'extra_long' is assigned to but never used

  1 files checked
  5 errors

  'E'-type errors: 4
  'F'-type errors: 1

  Checked files:

  * example.py


5 ``ament_uncrustify``
^^^^^^^^^^^^^^^^^^^^^^

`Uncrustify <https://github.com/uncrustify/uncrustify>`_ 是一种 C++ lint 工具，与 ``ament_cpplint`` 类似，但它的优点是能够\ **自动修复**\ 它发现的问题！
这个工具将帮助你找出并修复 C++ ROS 程序中的小错误和风格问题，例如行尾空白、过长的代码行、函数参数间距不当等等！


5.1 ``ament_uncrustify`` 参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

该程序接受一个可选参数，即需要扫描以生成报告的目录列表。
例如，如果你只想扫描工作区中的一个包，可以直接在该包的工作目录中调用 ``ament_uncrustify``，或者传给它一个目录路径。


5.2 ``ament_uncrustify`` 选项
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``-c CFG`` - 如果你更想使用自己的设置，Uncrustify 应使用的配置文件。
  我们建议你使用默认设置。
* ``--linelength N`` - 最大行长度。
* ``--language`` - {C,C++,CPP} 之一，以 ``-l <language>`` 的形式传给 uncrustify，强制指定一种语言，而不是根据文件扩展名选择。
* ``--reformat`` - 就地重新格式化文件，即修复遇到的格式错误。
  **我们建议你在运行** ``ament_uncrustify`` **时使用这个选项，因为它能帮你节省不少时间！**

5.3 ``ament_uncrustify`` 示例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


让我们回到那个名为 ``example.cpp`` 的简单 C++ 程序。

.. code-block:: cpp

  int main()
  {
       int a = 10;
       int b = 10;
       int c = 0;<trailing whitespace>
       if( a == b)<trailing whitespace>{
    <tab>      c=a;}<trailing whitespace>
       return 0;
   }


对这个文件应用 ``ament_uncrustify example.cpp`` 会产生以下输出。

.. code-block:: diff

  --- example.cpp
  +++ example.cpp.uncrustify
  @@ -1,9 +1,10 @@
  -  int main()
  -  {
  -       int a = 10;
  -       int b = 10;
  -       int c = 0;<trailing whitespace>
  -       if( a == b)<trailing whitespace>{
  - <tab>       c=a;}<trailing whitespace>
  -       return 0;
  -   }
  +int main()
  +{
  +  int a = 10;
  +  int b = 10;
  +  int c = 0;
  +  if (a == b) {
  +    c = a;
  +  }
  +  return 0;
  +}
  1 files with code style divergence

要将这些更改应用到文件，我们可以带 ``--reformat`` 标志运行 ``ament_uncrustify``。
**指定了这个选项后，uncrustify 会在原地应用必要的更改，为我们节省大量时间，尤其是在处理较大的代码库时！**

6 其他值得注意的 Ament 工具
^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS Desktop Full 附带了一些值得注意的 ament 开发工具。
下面列出了其中几个工具。

* ``ament_lint_cmake`` - 对照风格规范检查 CMake 文件。
* ``ament_xmllint`` - 使用 xmllint 检查 XML 标记，例如 XML launch 文件。
* ``ament_pep257`` - 对照 `PEP 257 <https://peps.python.org/pep-0257/>`_ 中的风格规范检查 Python 文档字符串。

Ament 具有高度可扩展性，我们鼓励 ROS 用户构建和使用能让它们更高效的 ament 工具。
你可以通过使用 ``apt search`` 或在 `ROS Index 上搜索 ament <https://index.ros.org/?pkgs=ament&search_packages=true>`_ 来搜索其他社区贡献的 ament lint 工具。
