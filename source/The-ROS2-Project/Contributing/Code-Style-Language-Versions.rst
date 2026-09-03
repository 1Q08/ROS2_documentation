.. redirect-from::

  Contributing/Code-Style-Language-Versions

.. _CodeStyle:

代码风格与语言版本
==================

.. contents:: 目录
   :depth: 2
   :local:

为了获得外观一致的产品，我们都将遵循（如果可能）外部为每种语言定义的风格指南。
对于其他内容，例如软件包布局或文档布局，我们将需要借鉴当前流行的风格，制定自己的指南。

此外，只要有可能，开发者都应该使用集成工具，以便在他们的编辑器中检查这些指南是否被遵循。
例如，每个人都应该在编辑器中内置一个 PEP8 检查器，以减少与风格相关的审查迭代。

在可能的情况下，软件包还应将风格检查作为其单元测试的一部分，以帮助自动检测风格问题（参见 `ament_lint_auto <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_lint_auto/doc/index.rst>`__）。

C
-

标准
^^^^

我们将以 C99 为目标。

风格
^^^^

我们将使用 `Python 的 PEP7 <https://www.python.org/dev/peps/pep-0007/>`__ 作为我们的 C 风格指南，并做了一些修改和补充：

* 我们将以 C99 为目标，因为我们不需要支持 C89（正如 PEP7 所建议的）

  * 理由：除其他外，它允许我们使用 ``//`` 和 ``/* */`` 两种风格的注释
  * 理由：C99 现在几乎无处不在

* 允许使用 C++ 风格的 ``//`` 注释
* （可选）始终将字面量放在比较运算符的左侧，例如 ``0 == ret`` 而不是 ``ret == 0``

  * 理由：``ret == 0`` 太容易意外变成 ``ret = 0``
  * 可选是因为在使用 ``-Wall`` （或等效选项）时，现代编译器会在发生这种情况时发出警告

以下所有修改仅在我们不编写 Python 模块时适用：

* 不要为所有内容使用 ``Py_`` 前缀

  * 而是使用包名的 CamelCase 版本或其他适当的前缀

* 关于文档字符串的内容不适用

我们可以使用 `pep7 <https://github.com/mike-perdide/pep7>`__ python 模块进行风格检查。
编辑器集成似乎很薄弱，我们可能需要更详细地研究 C 的自动检查。

C++
---

标准
^^^^

{DISTRO_TITLE} 以 C++17 为目标。

风格
^^^^


我们将使用 `Google C++ 风格指南 <https://google.github.io/styleguide/cppguide.html>`__，并做了一些修改：

行长度
~~~~~~

* 我们的最大行长度为 100 个字符。

文件扩展名
~~~~~~~~~~

* 头文件应使用 ``.hpp`` 扩展名。

  * 理由：让工具能够确定文件内容，是 C++ 还是 C。

* 实现文件应使用 ``.cpp`` 扩展名。

  * 理由：让工具能够确定文件内容，是 C++ 还是 C。

变量命名
~~~~~~~~

* 对于全局变量，使用带下划线的小写形式，并加上 ``g_`` 前缀

  * 理由：在整个项目中保持变量命名大小写一致
  * 理由：一眼就能看出变量的作用域
  * 跨语言保持一致

* **关于命名约定的说明**：ROS 2 在若干命名方面偏离了 Google C++ 风格指南：

  * Google 风格指南建议常量使用 ``kPascalCase`` （例如 ``kDaysInAWeek``）
  * ROS 2 项目目前混合使用 ``snake_case``、``PascalCase`` 和 ``UPPER_CASE`` 命名约定
  * 这种偏离是出于历史原因，以及为了与现有 ROS 代码库保持一致
  * 对于新项目，开发者应遵循相关 ROS 2 软件包中的现有约定
  * 有疑问时，优先与周围代码保持一致，而不是严格遵循 Google 风格

函数与方法命名
~~~~~~~~~~~~~~

* Google 风格指南说使用 ``CamelCase``，但也允许 C++ 标准库的 ``snake_case`` 风格

  * 理由：ROS 2 核心软件包目前使用 ``snake_case``

    * 原因：要么是历史疏忽，要么是个人偏好，没有被 linter 检查到
    * 不更改的原因：追溯性更改会过于破坏性
  * 其他考虑：

    * ``cpplint.py`` 不检查这种情况（除了通过审查，很难强制执行）
    * ``snake_case`` 可以带来跨语言更大的统一性
  * 具体指导：

    * 对于现有项目，优先使用现有风格
    * 对于新项目，两者都可以接受，但建议优先匹配相关的现有项目
    * 最终决定始终由开发者自行裁量

      * 函数指针、可调用类型等特殊情况可能需要打破规则
    * 注意，类默认仍应使用 ``CamelCase``

访问控制
~~~~~~~~

* 取消所有类成员都必须为私有、因而需要访问器的要求

  * 理由：这对用户 API 设计过于约束
  * 我们应优先使用私有成员，仅在需要时才将它们设为公有
  * 在选择允许直接成员访问之前，我们应考虑使用访问器
  * 我们应该有充分的理由允许直接成员访问，而不能仅仅因为方便

异常
~~~~

* 允许使用异常

  * 理由：这是一个新代码库，因此遗留参数不适用于我们
  * 理由：对于面向用户的 API，使用异常是更地道的 C++
  * 应明确避免在析构函数中使用异常

* 如果我们打算将生成的 API 包装在 C 中，我们应该考虑避免使用异常

  * 理由：这样更容易包装在 C 中
  * 理由：我们打算包装在 C 中的代码里，大多数依赖本来就不使用异常

函数式对象
~~~~~~~~~~

* 对 Lambda、``std::function`` 或 ``std::bind`` 没有限制

Boost
~~~~~

* 除非绝对必要，否则应避免使用 Boost。

注释与文档注释
~~~~~~~~~~~~~~

* 将 ``///`` 和 ``/** */`` 注释用于\ *文档*\ 目的，将 ``//`` 风格注释用于说明和一般注释

  * 类和函数注释应使用 ``///`` 和 ``/** */`` 风格注释
  * 理由：这些是 C/C++ 中 Doxygen 和 Sphinx 推荐的注释
  * 理由：混合使用 ``/* */`` 和 ``//`` 便于将包含注释的代码块注释掉
  * 关于代码如何工作的描述，或类和函数内的说明，应使用 ``//`` 风格注释

指针语法对齐
~~~~~~~~~~~~

* 使用 ``char * c;`` 而不是 ``char* c;`` 或 ``char *c;``，因为有 ``char* c, *d, *e;`` 这种情况

类隐私关键字
~~~~~~~~~~~~

* 不要在 ``public:``、``private:`` 或 ``protected:`` 前放 1 个空格，让所有缩进都是 2 的倍数更一致

  * 理由：大多数编辑器不喜欢不是（软）制表符大小倍数的缩进
  * 在 ``public:``、``private:`` 或 ``protected:`` 前使用零空格，或 2 个空格
  * 如果你在前面使用 2 个空格，则其他类语句再缩进 2 个空格
  * 优先使用零空格，即 ``public:``、``private:`` 或 ``protected:`` 与类处于同一列

嵌套模板
~~~~~~~~

* 绝不在嵌套模板中添加空白

  * 优先使用 ``set<list<string>>`` （C++11 特性），而不是 ``set<list<string> >`` 或 ``set< list<string> >``

始终使用花括号
~~~~~~~~~~~~~~

* 始终在 ``if``、``else``、``do``、``while`` 和 ``for`` 后使用花括号，即使主体只有一行。

  * 理由：减少视觉歧义的机会，以及因在主体中使用宏而产生的复杂情况

开放花括号与紧贴花括号
~~~~~~~~~~~~~~~~~~~~~~

* 对 ``function``、``class``、``enum`` 和 ``struct`` 定义使用开放花括号，但在 ``if``、``else``、``while``、``for`` 等上紧贴花括号……

  * 例外：当 ``if`` （或 ``while`` 等）条件足够长以致需要换行时，则使用开放花括号（即不要紧贴）。

* 当函数调用无法放在一行时，在开放括号处换行（而不是在参数之间换行），并在下一行以 2 空格缩进开始。
  对于更多参数，在后续行继续使用 2 空格缩进。
  （注意，`Google 风格指南 <https://google.github.io/styleguide/cppguide.html#Function_Calls>`__ 在这一点上内部自相矛盾。）

  * 对于太长而无法放在一行的 ``if`` （以及 ``while`` 等）条件也是如此。

示例
~~~~

这是可以的：

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

这样\ **不**\ 行：

.. code-block:: c++

   int main(int argc, char **argv) {
     return 0;
   }

   if (this &&
       that ||
       both) {
     ...
   }


使用开放花括号而不是过度缩进，例如用于区分构造函数代码和构造函数初始化列表

这是可以的：

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

这样\ **不**\ 行，甚至很奇怪（Google 的方式？）：

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

代码检查器
~~~~~~~~~~

我们结合 Google 的 `cpplint.py <https://github.com/google/styleguide>`__ 和 `uncrustify <https://github.com/uncrustify/uncrustify>`__ 来检查这些风格。

我们提供了带自定义配置的命令行工具：

* `ament_clang_format <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_clang_format/doc/index.rst>`__：`配置 <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_clang_format/ament_clang_format/configuration/.clang-format>`__
* `ament_cpplint <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_cpplint/doc/index.rst>`__
* `ament_uncrustify <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_uncrustify/doc/index.rst>`__：`配置 <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_uncrustify/ament_uncrustify/configuration/ament_code_style.cfg>`__

一些格式化工具（如 ament_uncrustify 和 ament_clang_format）支持 ``--reformat`` 选项来就地应用更改。

我们还运行其他工具来检测和消除尽可能多的警告。
以下是我们尝试对所有软件包做的额外事情的非详尽列表：

* 使用 ``-Wall -Wextra -Wpedantic`` 等编译器标志
* 运行 ``cppcheck`` 等静态代码分析，我们已将其集成到 `ament_cppcheck <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_cppcheck/doc/index.rst>`__ 中。

Python
------

版本
^^^^

我们的开发将以 Python 3 为目标。

风格
^^^^

我们将使用 `PEP8 指南 <https://www.python.org/dev/peps/pep-0008/>`_ 进行代码格式化。

在 PEP 8 留有一些自由的地方，我们选择了以下更精确的规则：

* `我们允许每行最多 100 个字符（第五段） <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_。
* `只要不需要转义，我们选择单引号而不是双引号 <https://www.python.org/dev/peps/pep-0008/#string-quotes>`_。
* `对于续行，我们优先使用悬挂缩进 <https://www.python.org/dev/peps/pep-0008/#indentation>`_。
* `我们优先拆分，每行只有一个 import <https://peps.python.org/pep-0008/#imports>`_：

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

应在单元测试和/或编辑器集成中使用 ``(ament_)pycodestyle`` 之类的 Python 软件包来检查 Python 代码风格。

linter 中使用的 pycodestyle 配置在 `这里 <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_pycodestyle/ament_pycodestyle/configuration/ament_pycodestyle.ini>`__。

与编辑器的集成：

* `atom <https://atom.io/packages/linter-pycodestyle>`_
* `emacs <https://www.emacswiki.org/emacs/PythonProgrammingInEmacs>`_
* `Sublime Text <https://sublime.wbond.net/packages/SublimeLinter-flake8>`_
* `vim <https://github.com/nvie/vim-flake8>`_

CMake
-----

版本
^^^^

阅读 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`_ 来确定你应支持的最低 CMake 版本。
目前任何受支持的 ROS 发行版的最低版本是 **3.14.4** （macOS 上的 ROS Humble）。

风格
^^^^

由于没有现成的 CMake 风格指南，我们将定义自己的：

* 使用小写命令名（``find_package``，而不是 ``FIND_PACKAGE``）。
* 使用 ``snake_case`` 标识符（变量、函数、宏）。
* 使用空的 ``else()`` 和 ``end...()`` 命令。
* 在 ``(``\ 前不加空格。
* 使用两个空格缩进，不要使用制表符。
* 对于多行宏调用的参数，不要使用对齐缩进。
  只使用两个空格。
* 优先使用带 ``set(PARENT_SCOPE)`` 的函数而不是宏。
* 使用宏时，为局部变量加上 ``_`` 或合理的前缀。

Markdown / reStructured Text / 文档块
-------------------------------------

以下文本格式化规则旨在提高可读性以及版本管理。

任何文档类型
^^^^^^^^^^^^

* 每个句子都必须另起一行。

  * 理由：对于较长的段落，开头的一处更改会使 diff 不可读，因为它会贯穿整个段落。

* 每个句子可以选择换行以保持每行较短。
* 行末不应有任何尾随空白。

Markdown 或 RST
^^^^^^^^^^^^^^^

* 每个节标题前后各应有一个空行。

  * 理由：在浏览文档时，这有助于快速了解结构。

* 代码块前后必须各有一个空行。

  * 理由：空白仅在围栏代码块前后才重要。
    遵循这些说明将确保高亮正确且一致地工作。

* 代码块应指定一种语法（例如 ``bash``）。

仅 RST
^^^^^^

* 在 reStructured Text 中，标题应遵循 `Sphinx 风格指南 <https://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html#headings>`__ 中描述的层级：

  * 带顶线的 ``#`` （仅使用一次，用于文档标题）
  * 带顶线的 ``*``
  * ``=``
  * ``-``
  * ``^``
  * ``"``
  * 理由：一致的层级有助于在浏览文档时快速了解嵌套级别。

仅 Markdown
^^^^^^^^^^^

* 在 Markdown 中，标题应遵循 `Markdown 语法文档 <https://daringfireball.net/projects/markdown/syntax#header>`__ 中描述的 ATX 风格

  * ATX 风格标题在行首使用 1-6 个井号（``#``）来表示标题级别 1-6。
  * 井号和标题之间应有一个空格（如 ``# Heading 1``），以便在视觉上更容易区分。
  * 对 ATX 风格偏好的理由来自 `Google Markdown 风格指南 <https://github.com/google/styleguide/blob/gh-pages/docguide/style.md#atx-style-headings>`__
  * 理由：ATX 风格标题更易于搜索和维护，并使前两个标题级别与其他级别保持一致。
