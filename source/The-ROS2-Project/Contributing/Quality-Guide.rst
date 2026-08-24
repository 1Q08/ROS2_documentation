.. redirect-from::

    Quality-Guide
    Contributing/Quality-Guide

质量指南：确保代码质量
======================

.. contents:: 目录
   :depth: 2
   :local:

本页就如何改进 ROS 2 软件包的软件质量提供指导，侧重的领域比 :doc:`开发者指南 <Developer-Guide>` 的"质量实践"部分更具体。

以下各节旨在涵盖 ROS 2 核心、应用和生态软件包以及核心客户端库 C++ 和 Python。
所提出的解决方案源于设计和实现考量，旨在改进诸如"可靠性"、"安全性"、"可维护性"、"确定性"等质量属性，这些属性与非功能性需求相关。


作为 ament 软件包构建一部分的静态代码分析
-----------------------------------------

**背景**：

* 你已开发了 C++ 生产代码。
* 你已创建了一个使用 ``ament`` 构建支持的 ROS 2 软件包。

**问题**：

* 库级静态代码分析不是作为软件包构建过程的一部分运行的。
* 库级静态代码分析需要手动执行。
* 存在在构建新软件包版本前忘记执行库级静态代码分析的风险。

**解决方案**：

* 使用 ``ament`` 的集成能力，将静态代码分析作为
  软件包构建过程的一部分执行。

**实现**：

* 插入到软件包的 ``CMakeLists.txt`` 文件中。

.. code-block:: bash

   ...
   if(BUILD_TESTING)
     find_package(ament_lint_auto REQUIRED)
     ament_lint_auto_find_test_dependencies()
     ...
   endif()
   ...

* 将 ``ament_lint`` 测试依赖插入到软件包的 ``package.xml`` 文件中。

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

**结果背景**：

* ``ament`` 支持的静态代码分析工具作为软件包构建的一部分运行。
* ``ament`` 不支持的静态代码分析工具需要单独执行。

通过代码注解进行静态线程安全分析
--------------------------------

**背景：**

* 你正在开发/调试多线程 C++ 生产代码。
* 你在 C++ 代码中从多个线程访问数据。

**问题：**

* 数据竞争和死锁可能导致严重 bug。

**解决方案：**

* 通过注解线程化代码，利用 Clang 的静态 `线程安全分析 <https://clang.llvm.org/docs/ThreadSafetyAnalysis.html>`__。

**实现背景：**


要启用线程安全分析，必须对代码进行注解，让编译器了解更多代码的语义。
这些注解是 Clang 特定的属性——例如 ``__attribute__(capability()))``。
与其直接使用这些属性，ROS 2 提供了预处理器宏，在使用其他编译器时会被抹去。

这些宏可以在 `rcpputils/thread_safety_annotations.hpp <https://github.com/ros2/rcpputils/blob/{REPOS_FILE_BRANCH}/include/rcpputils/thread_safety_annotations.hpp>`__ 中找到。

线程安全分析文档指出：
  线程安全分析可以与任何线程库一起使用，但它确实要求线程 API 被包装在具有适当注解的类和方法中。

我们已经决定，我们希望 ROS 2 开发者能够直接使用 ``std::`` 线程原语进行开发。
我们不希望提供上面建议的那种自己的包装类型。

需要注意三种 C++ 标准库：

* GNU 标准库 ``libstdc++`` —— Linux 上的默认库，通过编译器选项 ``-stdlib=libstdc++`` 显式指定。
* LLVM 标准库 ``libc++`` （也称 ``libcxx``）—— macOS 上的默认库，通过编译器选项 ``-stdlib=libc++`` 显式设置。
* Windows C++ 标准库 —— 与此用例无关。

``libcxx`` 为其 ``std::mutex`` 和 ``std::lock_guard`` 实现进行了线程安全分析注解。
当使用 GNU ``libstdc++`` 时，这些注解不存在，因此无法对未包装的 ``std::`` 类型使用线程安全分析。

*因此，要直接对* ``std::`` *类型使用线程安全分析，我们必须使用* ``libcxx``。

**实现：**

这里的代码迁移建议绝非完整——在编写（或注解现有的）线程化代码时，鼓励你尽可能多地使用对你的用例合乎逻辑的注解。
不过，这个分步指南是一个很好的起点！

* 为软件包/目标启用分析

  当 C++ 编译器是 Clang 时，启用 ``-Wthread-safety`` 标志。
  以下是基于 CMake 项目的示例：

  .. code-block:: cmake

     if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
       add_compile_options(-Wthread-safety)   # for your whole package
       target_compile_options(${MY_TARGET} PUBLIC -Wthread-safety)  # for a single library or executable
     endif()

* 注解代码

  * 第 1 步——注解数据成员

    * 找出 ``std::mutex`` 用于保护某些成员数据的任何地方。
    * 将 ``RCPPUTILS_TSA_GUARDED_BY(mutex_name)`` 注解添加到受该互斥锁保护的数据上。

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
      要修复它，在返回 bar 之前先加锁。

    .. code-block:: cpp

      void get() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return bar;
      }

  * 第 3 步——（可选但推荐）将现有代码重构为私有互斥锁模式

    线程化 C++ 代码中的推荐模式是始终将你的 ``mutex`` 作为数据结构的 ``private:`` 成员。
    这让数据安全成为包含结构的责任，从结构的使用者那里卸下该责任，并最小化受影响代码的表面积。

    将你的锁设为私有可能需要重新思考你的数据接口。
    这是一个很好的练习——这里有一些需要考虑的事项：

    * 你可能希望提供专门的接口来执行需要复杂加锁逻辑的分析，例如在受互斥锁保护的 map 结构的过滤集合中计算成员数量，而不是实际将底层结构返回给消费者。
    * 在数据量小的情况下，考虑复制以避免阻塞。
      这可以让其他线程继续访问共享数据，这有可能带来更好的整体性能。

  * 第 4 步——（可选）启用负能力分析

    `负能力分析 <https://clang.llvm.org/docs/ThreadSafetyAnalysis.html#negative-capabilities>`_
    让你指定"调用此函数时不得持有此锁"。
    它可以揭示其他注解无法揭示的潜在死锁情况。

    * 在你指定 ``-Wthread-safety`` 的地方，添加额外的标志 ``-Wthread-safety-negative``。
    * 在任何获取锁的函数上，使用 ``RCPPUTILS_TSA_REQUIRES(!mutex)`` 模式。

* 如何运行分析

  * ROS CI 构建农场运行一个使用 ``libcxx`` 的夜间任务，当线程安全分析发出警告时，它会通过将 ROS 2 核心栈标记为"Unstable"来暴露任何问题。
  * 对于本地运行，你有以下选项，全部等效：

    * 使用 colcon `clang-libcxx mixin <https://github.com/colcon/colcon-mixin-repository/blob/master/clang-libcxx.mixin>`__ （关于配置 mixins，请参阅 `文档 <https://github.com/colcon/colcon-mixin-repository/blob/master/README.md>`__）
      ::

          colcon build --mixin clang-libcxx

    * 将编译器传给 CMake
      ::

          colcon build --cmake-args -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_CXX_FLAGS='-stdlib=libc++ -D_LIBCPP_ENABLE_THREAD_SAFETY_ANNOTATIONS' -DFORCE_BUILD_VENDOR_PKG=ON --no-warn-unused-cli

    * 覆盖系统编译器
      ::

          CC=clang CXX=clang++ colcon build --cmake-args -DCMAKE_CXX_FLAGS='-stdlib=libc++ -D_LIBCPP_ENABLE_THREAD_SAFETY_ANNOTATIONS' -DFORCE_BUILD_VENDOR_PKG=ON --no-warn-unused-cli

**结果背景：**

* 在使用 Clang 和 ``libcxx`` 时，潜在的死锁和竞争条件将在编译时暴露。


动态分析（数据竞争与死锁）
--------------------------

**背景：**

* 你正在开发/调试多线程 C++ 生产代码。
* 你使用 pthreads 或 C++11 线程 + llvm libc++（在使用 ThreadSanitizer 时）。
* 你不使用 Libc/libstdc++ 静态链接（在使用 ThreadSanitizer 时）。
* 你不构建非位置无关的可执行文件（在使用 ThreadSanitizer 时）。

**问题：**

* 数据竞争和死锁可能导致严重 bug。
* 数据竞争和死锁无法使用静态分析检测（原因：静态分析的局限性）。
* 数据竞争和死锁不得在开发调试/测试期间出现（原因：通常并非所有经过生产代码的可能控制路径都会被覆盖到）。

**解决方案：**

* 使用专注于发现数据竞争和死锁的动态分析工具（这里使用 clang ThreadSanitizer）。

**实现：**

* 使用 clang 编译和链接生产代码，并添加选项 ``-fsanitize=thread`` （这会对生产代码进行插桩）。
* 如果在分析期间要执行不同的生产代码，考虑条件编译，例如 `ThreadSanitizers _has_feature(thread_sanitizer) <https://clang.llvm.org/docs/ThreadSanitizer.html#has-feature-thread-sanitizer>`__。
* 如果某些代码不应被插桩，考虑 `ThreadSanitizers _/*attribute*/_((no_sanitize("thread"))) <https://clang.llvm.org/docs/ThreadSanitizer.html#attribute-no-sanitize-thread>`__。
* 如果某些文件不应被插桩，考虑文件或函数级别的排除 `ThreadSanitizers blacklisting <https://clang.llvm.org/docs/ThreadSanitizer.html#ignorelist>`__，更具体地：`ThreadSanitizers Sanitizer Special Case List <https://clang.llvm.org/docs/SanitizerSpecialCaseList.html>`__，或使用 `ThreadSanitizers no_sanitize("thread") <https://clang.llvm.org/docs/ThreadSanitizer.html#ignorelist>`__ 并使用选项 ``--fsanitize-blacklist``。

**结果背景：**

* 在部署生产代码之前，有更高几率发现其中的数据竞争和死锁。
* 分析结果可能缺乏可靠性，工具处于 beta 阶段（在使用 ThreadSanitizer 时）。
* 由于生产代码插桩而产生开销（为已插桩/未插桩的生产代码维护单独分支等）。
* 插桩代码需要更多每线程内存（在使用 ThreadSanitizer 时）。
* 插桩代码映射大量虚拟地址空间（在使用 ThreadSanitizer 时）。
