.. redirect-from::

    Quality-Guide
    Contributing/Quality-Guide

质量指南：确保代码质量
======================

.. contents:: 目录
   :depth: 2
   :local:

本页给出关于如何提升 ROS 2 软件包软件质量的指导，聚焦于比 :doc:`开发者指南 <Developer-Guide>` 中“质量实践”一节更为具体的领域。

下面各节旨在覆盖 ROS 2 核心、应用与生态系统软件包，以及核心客户端库（C++ 和 Python）。
所给出的方案源于设计与实现方面的考量，用于改进“可靠性”“安全性”“可维护性”“确定性”等与非功能需求相关的质量属性。


作为 ament 软件包构建一部分的静态代码分析
-----------------------------------------

**背景**：

* 你已经开发了自己的 C++ 生产代码。
* 你已经创建了一个支持 ``ament`` 构建的 ROS 2 软件包。

**问题**：

* 库级别的静态代码分析没有作为软件包构建流程的一部分运行。
* 库级别的静态代码分析需要手动执行。
* 在构建新版本软件包之前忘记执行库级别静态代码分析的风险。

**解决方案**：

* 利用 ``ament`` 的集成能力，将静态代码分析作为软件包构建流程的一部分来执行。

**实现**：

* 在软件包的 ``CMakeLists.txt`` 文件中插入以下内容。

.. code-block:: bash

   ...
   if(BUILD_TESTING)
     find_package(ament_lint_auto REQUIRED)
     ament_lint_auto_find_test_dependencies()
     ...
   endif()
   ...

* 将 ``ament_lint`` 测试依赖插入软件包的 ``package.xml`` 文件。

.. code-block:: bash

   ...
   <package format="2">
     ...
     <test_depend>ament_lint_auto</test_depend>
     <test_depend>ament_lint_common</test_depend>
     ...
   </package>

**示例**：

* ``rclcpp``：

  * `rclcpp/rclcpp/CMakeLists.txt <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp/CMakeLists.txt>`__
  * `rclcpp/rclcpp/package.xml <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp/package.xml>`__

* ``rclcpp_lifecycle``：

  * `rclcpp/rclcpp_lifecycle/CMakeLists.txt <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp_lifecycle/CMakeLists.txt>`__
  * `rclcpp/rclcpp_lifecycle/package.xml <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp_lifecycle/package.xml>`__

**结果情况**：

* ``ament`` 所支持的静态代码分析工具会作为软件包构建的一部分运行。
* ``ament`` 不支持的静态代码分析工具需要单独执行。

通过代码注解进行静态线程安全分析
--------------------------------

**背景：**

* 你正在开发/调试自己的多线程 C++ 生产代码
* 你在 C++ 代码中从多个线程访问数据

**问题：**

* 数据竞争和死锁可能导致严重缺陷。

**解决方案：**

* 通过为多线程代码添加注解，利用 Clang 的静态 `线程安全分析 <https://clang.llvm.org/docs/ThreadSafetyAnalysis.html>`__

**实现背景：**


要启用线程安全分析，必须为代码添加注解，让编译器更了解代码的语义。
这些注解是 Clang 特有的属性——例如 ``__attribute__(capability()))``。
ROS 2 没有直接使用这些属性，而是提供了预处理器宏，它们在使用其他编译器时会被消除。

这些宏可以在 `rcpputils/thread_safety_annotations.hpp <https://github.com/ros2/rcpputils/blob/{REPOS_FILE_BRANCH}/include/rcpputils/thread_safety_annotations.hpp>`__ 中找到

线程安全分析文档指出
  线程安全分析可用于任何线程库，但它确实要求线程 API 被封装在具有适当注解的类和方法中

我们已经决定，希望 ROS 2 开发者能够在开发中直接使用 ``std::`` 线程原语。
我们不希望按上面所建议的那样提供自己的封装类型。

需要注意有三种 C++ 标准库

* GNU 标准库 ``libstdc++``——在 Linux 上是默认的，也可通过编译器选项 ``-stdlib=libstdc++`` 显式指定
* LLVM 标准库 ``libc++`` （也称为 ``libcxx``）——在 macOS 上是默认的，通过编译器选项 ``-stdlib=libc++`` 显式设置
* Windows C++ 标准库——与本用例无关

``libcxx`` 为其 ``std::mutex`` 和 ``std::lock_guard`` 实现添加了线程安全分析注解。
使用 GNU ``libstdc++`` 时不存在这些注解，因此无法对未封装的 ``std::`` 类型使用线程安全分析。

*因此，要直接对* ``std::`` *类型使用线程安全分析，我们必须使用* ``libcxx``

**实现：**

这里的代码迁移建议并不完整——在编写（或为现有代码添加注解）多线程代码时，鼓励你根据用例合理地使用尽可能多的注解。
不过，下面的分步指引是一个很好的起点！

* 为软件包/目标启用分析

  当 C++ 编译器为 Clang 时，启用 ``-Wthread-safety`` 标志。
  下面是以 CMake 为基础的项目示例

  .. code-block:: cmake

     if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
       add_compile_options(-Wthread-safety)   # for your whole package
       target_compile_options(${MY_TARGET} PUBLIC -Wthread-safety)  # for a single library or executable
     endif()

* 为代码添加注解

  * 第 1 步——为数据成员添加注解

    * 找出所有使用 ``std::mutex`` 保护某个成员数据的地方
    * 为受该互斥量保护的数据添加 ``RCPPUTILS_TSA_GUARDED_BY(mutex_name)`` 注解

    .. code-block:: cpp

      class Foo {
      public:
        void incr(int amount) {
          std::lock_guard<std::mutex> lock(mutex_);
          bar += amount;
        }

        void get() const {
          return bar;
        }

      private:
        mutable std::mutex mutex_;
        int bar RCPPUTILS_TSA_GUARDED_BY(mutex_) = 0;
      };

  * 第 2 步——修复警告

    * 在上面的示例中——``Foo::get`` 会产生编译器警告！
      要修复它，请在返回 bar 之前加锁

    .. code-block:: cpp

      void get() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return bar;
      }

  * 第 3 步——（可选但推荐）将现有代码重构为私有互斥量模式

    多线程 C++ 代码中一个推荐模式是始终把 ``mutex`` 保持为数据结构的 ``private:`` 成员。
    这让数据安全成为所属结构的关注点，把该责任从结构的使用者身上卸下，并最小化受影响的代码范围。

    将锁设为私有可能需要重新思考数据的接口。
    这是一个很好的练习——以下几点值得考虑

    * 对于需要复杂加锁逻辑的分析，你可能希望提供专门的接口，例如统计受互斥量保护的 map 结构中经过过滤的集合里的成员数量，而不是真的把底层结构返回给使用者
    * 在数据量很小时，考虑通过拷贝来避免阻塞。
      这可以让其他线程继续访问共享数据，从而有可能带来更好的整体性能。

  * 第 4 步——（可选）启用负能力分析

    `负能力分析 <https://clang.llvm.org/docs/ThreadSafetyAnalysis.html#negative-capabilities>`_
    允许你指定“调用此函数时不得持有该锁”。
    它可以揭示其他注解无法发现的潜在死锁情况。

    * 在你指定 ``-Wthread-safety`` 的地方，额外添加标志 ``-Wthread-safety-negative``
    * 在任何会获取锁的函数上，使用 ``RCPPUTILS_TSA_REQUIRES(!mutex)`` 模式

* 如何运行分析

  * ROS CI 构建农场会在 ``libcxx`` 下运行一个每夜任务，它会暴露出 ROS 2 核心栈中的任何问题——当线程安全分析产生警告时，该任务会被标记为“Unstable”
  * 对于本地运行，你有以下选项，它们都是等价的

    * 使用 colcon 的 `clang-libcxx mixin <https://github.com/colcon/colcon-mixin-repository/blob/master/clang-libcxx.mixin>`__ （关于配置 mixin 的 `文档 <https://github.com/colcon/colcon-mixin-repository/blob/master/README.md>`__）
      ::

          colcon build --mixin clang-libcxx

    * 向 CMake 传递编译器
      ::

          colcon build --cmake-args -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_CXX_FLAGS='-stdlib=libc++ -D_LIBCPP_ENABLE_THREAD_SAFETY_ANNOTATIONS' -DFORCE_BUILD_VENDOR_PKG=ON --no-warn-unused-cli

    * 覆盖系统编译器
      ::

          CC=clang CXX=clang++ colcon build --cmake-args -DCMAKE_CXX_FLAGS='-stdlib=libc++ -D_LIBCPP_ENABLE_THREAD_SAFETY_ANNOTATIONS' -DFORCE_BUILD_VENDOR_PKG=ON --no-warn-unused-cli

**结果情况：**

* 在使用 Clang 和 ``libcxx`` 时，潜在的死锁和竞态条件会在编译期暴露出来


动态分析（数据竞争与死锁）
--------------------------

**背景：**

* 你正在开发/调试自己的多线程 C++ 生产代码。
* 你使用 pthreads 或 C++11 线程 + llvm libc++（对于 ThreadSanitizer 而言）。
* 你没有使用 Libc/libstdc++ 静态链接（对于 ThreadSanitizer 而言）。
* 你没有构建非位置无关的可执行文件（对于 ThreadSanitizer 而言）。

**问题：**

* 数据竞争和死锁可能导致严重缺陷。
* 数据竞争和死锁无法通过静态分析检测出来（原因：静态分析的局限性）。
* 数据竞争和死锁在开发调试/测试期间未必会显现（原因：通常不会覆盖生产代码中所有可能的控制路径）。

**解决方案：**

* 使用专注于发现数据竞争和死锁的动态分析工具（此处为 clang ThreadSanitizer）。

**实现：**

* 使用选项 ``-fsanitize=thread`` 用 clang 编译并链接生产代码（这会对生产代码进行插桩）。
* 如果分析期间需要执行不同的生产代码，请考虑条件编译，例如 `ThreadSanitizer 的 _has_feature(thread_sanitizer) <https://clang.llvm.org/docs/ThreadSanitizer.html#has-feature-thread-sanitizer>`__。
* 如果某些代码不应被插桩，请考虑 `ThreadSanitizer 的 _/*attribute*/_((no_sanitize("thread"))) <https://clang.llvm.org/docs/ThreadSanitizer.html#attribute-no-sanitize-thread>`__。
* 如果某些文件不应被插桩，请考虑文件级或函数级排除 `ThreadSanitizer 的黑名单 <https://clang.llvm.org/docs/ThreadSanitizer.html#ignorelist>`__，更具体地说：`ThreadSanitizer 的 Sanitizer Special Case List <https://clang.llvm.org/docs/SanitizerSpecialCaseList.html>`__，或者使用 `ThreadSanitizer 的 no_sanitize("thread") <https://clang.llvm.org/docs/ThreadSanitizer.html#ignorelist>`__ 并配合选项 ``--fsanitize-blacklist``。

**结果情况：**

* 在部署生产代码之前发现数据竞争和死锁的可能性更高。
* 分析结果可能不够可靠，该工具处于 beta 阶段（对于 ThreadSanitizer 而言）。
* 由于生产代码插桩带来的开销（需要为插桩/未插桩的生产代码维护不同分支等）。
* 插桩后的代码每个线程需要更多内存（对于 ThreadSanitizer 而言）。
* 插桩后的代码会映射大量虚拟地址空间（对于 ThreadSanitizer 而言）。
