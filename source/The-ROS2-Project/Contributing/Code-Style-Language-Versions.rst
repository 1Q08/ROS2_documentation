.. redirect-from::

  Contributing/Code-Style-Language-Versions

.. _CodeStyle:

代码风格与语言版本
==================

.. contents:: 目录
   :depth: 2
   :local:

为了得到外观一致的产品，我们将全部遵循（如有可能）外部定义的、针对各语言的风格指南。
对于软件包布局或文档布局之类的其他事项，我们需要自行制定指南，并借鉴目前流行的风格。

此外，在可能的情况下，开发者应使用集成工具，以便在编辑器中检查是否遵循了这些指南。
例如，每个人都应在自己的编辑器中内置 PEP8 检查器，以减少与风格相关的评审迭代次数。

同样，在可能的情况下，软件包应把风格检查作为其单元测试的一部分，以帮助自动发现风格问题（参见 `ament_lint_auto <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_lint_auto/doc/index.rst>`__）。

C
-

标准
^^^^

我们将以 C99 为目标。

风格
^^^^

我们的 C 风格指南将采用 `Python 的 PEP7 <https://www.python.org/dev/peps/pep-0007/>`__，并做一些修改和补充：

* 我们将以 C99 为目标，因为我们不需要支持 C89（尽管 PEP7 建议支持）

  * 理由：除其他外，它允许我们同时使用 ``//`` 和 ``/* */`` 风格注释
  * 理由：C99 如今几乎无处不在

* 允许使用 C++ 风格的 ``//`` 注释
* （可选）始终把字面量放在比较运算符的左侧，例如写 ``0 == ret`` 而不是 ``ret == 0``

  * 理由：``ret == 0`` 太容易因疏忽而写成 ``ret = 0``
  * 之所以是可选的，是因为在使用 ``-Wall`` （或等价选项）时，现代编译器会对此给出警告

以下所有修改仅在我们不是在编写 Python 模块时适用：

* 不要给所有东西都加上 ``Py_`` 前缀

  * 应使用包名的驼峰式版本或其他合适的前缀

* 关于文档字符串的那些内容不适用

我们可以使用 `pep7 <https://github.com/mike-perdide/pep7>`__ Python 模块进行风格检查。
其编辑器集成似乎比较薄弱，我们可能需要更深入地研究 C 的自动检查方案。

C++
---

标准
^^^^

{DISTRO_TITLE} 以 C++17 为目标。

风格
^^^^


我们将采用 `Google C++ 风格指南 <https://google.github.io/styleguide/cppguide.html>`__，并做一些修改：

行长
~~~~

* 我们的最大行长为 100 个字符。

文件扩展名
~~~~~~~~~~

* 头文件应使用 ``.hpp`` 扩展名。

  * 理由：让工具能够判断文件内容是 C++ 还是 C。

* 实现文件应使用 ``.cpp`` 扩展名。

  * 理由：让工具能够判断文件内容是 C++ 还是 C。

变量命名
~~~~~~~~

* 对于全局变量，使用小写加下划线，并以 ``g_`` 作为前缀

  * 理由：保持整个项目的变量命名大小写风格一致
  * 理由：一眼就能看出变量的作用域
  * 保持各语言之间的一致性

* **关于命名约定的说明**：ROS 2 在若干命名方面偏离了 Google C++ 风格指南：

  * Google 风格指南建议常量使用 ``kPascalCase`` （例如 ``kDaysInAWeek``）
  * ROS 2 项目目前混用 ``snake_case``、``PascalCase`` 和 ``UPPER_CASE`` 命名约定
  * 这种偏离是出于历史原因以及与既有 ROS 代码库保持一致
  * 对于新项目，开发者应遵循相关 ROS 2 软件包中已有的约定
  * 如有疑问，优先与周围代码保持一致，而不是严格遵循 Google 风格

函数与方法命名
~~~~~~~~~~~~~~

* Google 风格指南要求 ``CamelCase``，但也允许 C++ 标准库风格的 ``snake_case``

  * 理由：ROS 2 核心软件包目前使用 ``snake_case``

    * 原因：要么是历史上的疏忽，要么是个人偏好未被 linter 检查出来
    * 不修改的原因：追溯性地修改会造成太大破坏
  * 其他考虑：

    * ``cpplint.py`` 不检查这种情况（除人工评审外很难强制执行）
    * ``snake_case`` 可以让各语言之间更一致
  * 具体指导：

    * 对于现有项目，优先使用既有风格
    * 对于新项目，两种都可以接受，但建议优先与相关的现有项目保持一致
    * 最终决定始终由开发者自行判断

      * 函数指针、可调用类型等特殊情形可能需要变通规则
    * 注意，类默认仍应使用 ``CamelCase``

访问控制
~~~~~~~~

* 取消“所有类成员都必须是私有的、因而都需要访问器”的要求

  * 理由：这对用户 API 设计限制过强
  * 我们应优先使用私有成员，只在需要时才把它们设为公有
  * 在决定允许直接访问成员之前，应先考虑使用访问器
  * 允许直接访问成员应有充分的理由，而不能仅仅因为对我们方便

异常
~~~~

* 允许使用异常

  * 理由：这是一个新的代码库，所以遗留问题的理由对我们不适用
  * 理由：对于面向用户的 API 来说，使用异常更符合 C++ 惯例
  * 应明确避免在析构函数中抛出异常

* 如果我们打算把最终的 API 用 C 封装，就应考虑避免使用异常

  * 理由：这样更容易用 C 封装
  * 理由：我们打算用 C 封装的代码中，大多数依赖本身都不使用异常

函数式对象
~~~~~~~~~~

* 对 Lambda、``std::function`` 或 ``std::bind`` 没有限制

Boost
~~~~~

* 除非绝对必要，否则应避免使用 Boost。

注释与文档注释
~~~~~~~~~~~~~~

* *文档* 用途使用 ``///`` 和 ``/** */`` 注释，笔记和一般性说明使用 ``//`` 风格注释

  * 类和函数的注释应使用 ``///`` 和 ``/** */`` 风格注释
  * 理由：在 C/C++ 中，Doxygen 和 Sphinx 推荐这样使用
  * 理由：混用 ``/* */`` 和 ``//`` 便于用块注释注释掉本身含有注释的代码
  * 关于代码如何工作的描述，或类和函数内部的笔记，应使用 ``//`` 风格注释

指针语法对齐
~~~~~~~~~~~~

* 使用 ``char * c;`` 而不是 ``char* c;`` 或 ``char *c;``，因为存在这种情形：``char* c, *d, *e;``

类访问关键字
~~~~~~~~~~~~

* 不要在 ``public:``、``private:`` 或 ``protected:`` 前加 1 个空格，所有缩进都是 2 的倍数会更为一致

  * 理由：大多数编辑器不喜欢不是（软）制表符宽度倍数的缩进
  * 在 ``public:``、``private:`` 或 ``protected:`` 前使用零个空格或 2 个空格
  * 如果你在前面使用 2 个空格，就把其他类语句再额外缩进 2 个空格
  * 优先使用零个空格，即让 ``public:``、``private:`` 或 ``protected:`` 与 class 位于同一列

嵌套模板
~~~~~~~~

* 绝不要在嵌套模板中添加空白

  * 优先使用 ``set<list<string>>`` （C++11 特性），而不是 ``set<list<string> >`` 或 ``set< list<string> >``

始终使用花括号
~~~~~~~~~~~~~~

* 在 ``if``、``else``、``do``、``while`` 和 ``for`` 之后始终使用花括号，即使函数体只有一行。

  * 理由：减少视觉歧义的机会，也减少因函数体中使用宏而产生的复杂情况

开放花括号与紧凑花括号
~~~~~~~~~~~~~~~~~~~~~~

* ``function``、``class``、``enum`` 和 ``struct`` 定义使用开放花括号，而在 ``if``、``else``、``while``、``for`` 等之后使用紧凑花括号……

  * 例外：当 ``if`` （或 ``while`` 等）的条件长到需要换行时，就使用开放花括号（即不要紧凑）。

* 当函数调用无法放入一行时，在左圆括号处换行（而不是在参数之间），并在下一行以 2 空格缩进开始。
  后续更多参数的行继续使用 2 空格缩进。
  （注意，`Google 风格指南 <https://google.github.io/styleguide/cppguide.html#Function_Calls>`__ 在这一点上自相矛盾。）

  * 对于无法放入一行的 ``if`` （以及 ``while`` 等）条件也是如此。

示例
~~~~

下面是正确的：

.. code-block:: c++

   int main(int argc, char **argv)
   {
     if (condition) {
       return 0;
     } else {
       return 1;
     }
   }

   if (this && that || both) {
     ...
   }

   // Long condition; open brace
   if (
     this && that || both && this && that || both && this && that || both && this && that)
   {
     ...
   }

   // Short function call
   call_func(foo, bar);

   // Long function call; wrap at the open parenthesis
   call_func(
     foo, bar, foo, bar, foo, bar, foo, bar, foo, bar, foo, bar, foo, bar, foo, bar, foo, bar,
     foo, bar, foo, bar, foo, bar, foo, bar, foo, bar, foo, bar, foo, bar, foo, bar, foo, bar);

   // Very long function argument; separate it for readability
   call_func(
     bang,
     fooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo,
     bar, bat);

下面 **不** 正确：

.. code-block:: c++

   int main(int argc, char **argv) {
     return 0;
   }

   if (this &&
       that ||
       both) {
     ...
   }


应使用开放花括号而不是过度缩进，例如用于区分构造函数代码和构造函数初始化列表

下面是正确的：

.. code-block:: c++

   ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
     Type par_name1,  // 2 space indent
     Type par_name2,
     Type par_name3)
   {
     DoSomething();  // 2 space indent
     ...
   }

   MyClass::MyClass(int var)
   : some_var_(var),
     some_other_var_(var + 1)
   {
     ...
     DoSomething();
     ...
   }

下面 **不** 正确，甚至很怪（Google 的方式？）：

.. code-block:: c++

   ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
       Type par_name1,  // 4 space indent
       Type par_name2,
       Type par_name3) {
     DoSomething();  // 2 space indent
     ...
   }

   MyClass::MyClass(int var)
       : some_var_(var),             // 4 space indent
         some_other_var_(var + 1) {  // lined up
     ...
     DoSomething();
     ...
   }

Linter
~~~~~~

我们用 Google 的 `cpplint.py <https://github.com/google/styleguide>`__ 和 `uncrustify <https://github.com/uncrustify/uncrustify>`__ 的组合来检查这些风格。

我们提供带有自定义配置的命令行工具：

* `ament_clang_format <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_clang_format/doc/index.rst>`__：`配置 <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_clang_format/ament_clang_format/configuration/.clang-format>`__
* `ament_cpplint <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_cpplint/doc/index.rst>`__
* `ament_uncrustify <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_uncrustify/doc/index.rst>`__：`配置 <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_uncrustify/ament_uncrustify/configuration/ament_code_style.cfg>`__

某些格式化工具（例如 ament_uncrustify 和 ament_clang_format）支持 ``--reformat`` 选项，用于就地应用更改。

我们还会运行其他工具来检测并尽可能消除警告。
下面是我们尽量对所有软件包执行的其他事项的非穷尽列表：

* 使用 ``-Wall -Wextra -Wpedantic`` 之类的编译器标志
* 运行静态代码分析，例如 ``cppcheck``，我们已把它集成到 `ament_cppcheck <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_cppcheck/doc/index.rst>`__ 中。

Python
------

版本
^^^^

我们的开发将以 Python 3 为目标。

风格
^^^^

代码格式将采用 `PEP8 指南 <https://www.python.org/dev/peps/pep-0008/>`_。

在 PEP 8 留有自由的地方，我们选择了以下更精确的规则：

* `我们允许每行最多 100 个字符（第五段） <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_。
* `只要不需要转义，我们选择单引号而不是双引号 <https://www.python.org/dev/peps/pep-0008/#string-quotes>`_。
* `续行我们优先使用悬挂缩进 <https://www.python.org/dev/peps/pep-0008/#indentation>`_。
* `我们更倾向于每行只有一个 import <https://peps.python.org/pep-0008/#imports>`_：

  .. code-block:: python

    # This is preferred
    from typing import Dict
    from typing import List

    # over these
    from typing import Dict, List
    from typing import (
      Dict,
      List,
    )

在单元测试和/或编辑器集成中，应使用 ``(ament_)pycodestyle`` Python 包之类的工具来检查 Python 代码风格。

linter 中使用的 pycodestyle 配置见 `此处 <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_pycodestyle/ament_pycodestyle/configuration/ament_pycodestyle.ini>`__。

与编辑器集成：

* `atom <https://atom.io/packages/linter-pycodestyle>`_
* `emacs <https://www.emacswiki.org/emacs/PythonProgrammingInEmacs>`_
* `Sublime Text <https://sublime.wbond.net/packages/SublimeLinter-flake8>`_
* `vim <https://github.com/nvie/vim-flake8>`_

CMake
-----

版本
^^^^

请阅读 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`_ 以确定你应支持的最低 CMake 版本。
目前所有受支持 ROS 发行版的最低版本是 **3.14.4** （macOS 上的 ROS Humble）。

风格
^^^^

由于没有现成的 CMake 风格指南，我们将定义自己的：

* 命令名使用小写（``find_package``，而不是 ``FIND_PACKAGE``）。
* 标识符（变量、函数、宏）使用 ``snake_case``。
* 使用空的 ``else()`` 和 ``end...()`` 命令。
* ``(`` 前不加空白。
* 使用两个空格缩进，不要使用制表符。
* 多行宏调用时，参数不要使用对齐缩进。
  只使用两个空格。
* 优先使用带 ``set(PARENT_SCOPE)`` 的函数，而不是宏。
* 使用宏时，给局部变量加上 ``_`` 或合理的前缀。

Markdown / reStructured Text / 文档块
-------------------------------------

以下文本格式规则旨在提升可读性以及版本管理效果。

任何文档类型
^^^^^^^^^^^^

* 每个句子都必须另起一行。

  * 理由：对于较长的段落，开头的单个改动会让 diff 无法阅读，因为它会贯穿整个段落。

* 每个句子可以选择性地换行以保持每行较短。
* 各行不应有行尾空白。

Markdown 或 RST
^^^^^^^^^^^^^^^

* 每个节标题前应有一个空行，后也应有一个空行。

  * 理由：这有助于快速浏览文档结构、获得整体印象。

* 代码块前后必须有空行。

  * 理由：空白只对围栏代码块的正前方和正后方有影响。
    遵循这些说明可确保高亮正常且一致地工作。

* 代码块应指定语言（例如 ``bash``）。

仅限 RST
^^^^^^^^

* 在 reStructured Text 中，标题应遵循 `Sphinx 风格指南 <https://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html#headings>`__ 中描述的层级：

  * 带上下划线的 ``#`` （仅用一次，用于文档标题）
  * 带上下划线的 ``*``
  * ``=``
  * ``-``
  * ``^``
  * ``"``
  * 理由：一致的层级有助于在浏览文档时快速了解嵌套层级。

仅限 Markdown
^^^^^^^^^^^^^

* 在 Markdown 中，标题应遵循 `Markdown 语法文档 <https://daringfireball.net/projects/markdown/syntax#header>`__ 中描述的 ATX 风格

  * ATX 风格标题在行首使用 1-6 个井号字符（``#``）来表示 1-6 级标题。
  * 井号与标题文字之间应加一个空格（例如 ``# Heading 1``），以便更便于在视觉上区分它们。
  * 偏好 ATX 风格的理由来自 `Google Markdown 风格指南 <https://github.com/google/styleguide/blob/gh-pages/docguide/style.md#atx-style-headings>`__
  * 理由：ATX 风格标题更易于搜索和维护，并使前两级标题与其他级别的标题保持一致。
