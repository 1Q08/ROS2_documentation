.. redirect-from::

    Allocator-Template-Tutorial
    Tutorials/Allocator-Template-Tutorial

实现自定义内存分配器
====================

**目标：** 本教程将展示在编写 ROS 2 C++ 代码时如何使用自定义内存分配器。

**教程级别：** 高级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

本教程将教你如何为发布者和订阅者集成自定义分配器，使默认的堆分配器在 ROS 节点执行期间永不被调用。
本教程的代码可以在 `这里 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/topics/allocator_tutorial.cpp>`__ 找到。

背景
----

假设你想编写实时安全（real-time safe）的代码，而且你听说过在实时关键段调用 “new” 的诸多危险，因为大多数平台上的默认堆分配器是不确定的。

默认情况下，许多 C++ 标准库结构在增长时会隐式分配内存，例如 ``std::vector``。
然而，这些数据结构也接受一个 “Allocator” 模板参数。
如果你为这些数据结构之一指定了自定义分配器，它将使用该分配器而不是系统分配器来增长或缩小数据结构。
你的自定义分配器可以在栈上预先分配一块内存池，这可能更适用于实时应用。

在 ROS 2 C++ 客户端库（rclcpp）中，我们遵循与 C++ 标准库相似的哲学。
发布者、订阅者和 Executor 接受一个 Allocator 模板参数，该参数控制这些实体在执行期间进行的分配。

编写一个分配器
--------------

要编写一个与 ROS 2 分配器接口兼容的分配器，你的分配器必须与 C++ 标准库分配器接口兼容。

C++11 标准库提供了一种称为 ``allocator_traits`` 的东西。
C++11 标准规定，自定义分配器只需满足一组最低要求，就可以以标准方式分配和释放内存。
``allocator_traits`` 是一个通用结构，它会根据以最低要求编写的分配器补齐分配器的其他特性。

例如，下面这个自定义分配器的声明满足 ``allocator_traits`` （当然，你仍然需要在这个结构体中实现声明的函数）：

.. code-block:: c++

   template <class T>
   struct custom_allocator {
     using value_type = T;
     custom_allocator() noexcept;
     template <class U> custom_allocator (const custom_allocator<U>&) noexcept;
     T* allocate (std::size_t n);
     void deallocate (T* p, std::size_t n);
   };

   template <class T, class U>
   constexpr bool operator== (const custom_allocator<T>&, const custom_allocator<U>&) noexcept;

   template <class T, class U>
   constexpr bool operator!= (const custom_allocator<T>&, const custom_allocator<U>&) noexcept;

然后你就可以像这样访问由 ``allocator_traits`` 补齐的分配器的其他函数和成员：``std::allocator_traits<custom_allocator<T>>::construct(...)``

要了解 ``allocator_traits`` 的全部能力，请参见 https://en.cppreference.com/w/cpp/memory/allocator_traits 。

然而，一些只提供部分 C++11 支持的编译器（例如 GCC 4.8）仍然要求分配器实现大量样板代码才能与向量和字符串等标准库结构一起使用，因为这些结构在内部不使用 ``allocator_traits``。
因此，如果你使用的编译器只提供部分 C++11 支持，你的分配器需要看起来更像这样：

.. code-block:: c++

   template<typename T>
   struct pointer_traits {
     using reference = T &;
     using const_reference = const T &;
   };

   // Avoid declaring a reference to void with an empty specialization
   template<>
   struct pointer_traits<void> {
   };

   template<typename T = void>
   struct MyAllocator : public pointer_traits<T> {
   public:
     using value_type = T;
     using size_type = std::size_t;
     using pointer = T *;
     using const_pointer = const T *;
     using difference_type = typename std::pointer_traits<pointer>::difference_type;

     MyAllocator() noexcept;

     ~MyAllocator() noexcept;

     template<typename U>
     MyAllocator(const MyAllocator<U> &) noexcept;

     T * allocate(size_t size, const void * = 0);

     void deallocate(T * ptr, size_t size);

     template<typename U>
     struct rebind {
       typedef MyAllocator<U> other;
     };
   };

   template<typename T, typename U>
   constexpr bool operator==(const MyAllocator<T> &,
     const MyAllocator<U> &) noexcept;

   template<typename T, typename U>
   constexpr bool operator!=(const MyAllocator<T> &,
     const MyAllocator<U> &) noexcept;

编写一个示例 main
-----------------

一旦你编写好了一个有效的 C++ 分配器，你必须将它作为共享指针传递给发布者、订阅者和 executor。

.. code-block:: c++

     auto alloc = std::make_shared<MyAllocator<void>>();
     rclcpp::PublisherOptionsWithAllocator<MyAllocator<void>> publisher_options;
     publisher_options.allocator = alloc;
     auto publisher = node->create_publisher<std_msgs::msg::UInt32>(
       "allocator_tutorial", 10, publisher_options);

     rclcpp::SubscriptionOptionsWithAllocator<MyAllocator<void>> subscription_options;
     subscription_options.allocator = alloc;
     auto msg_mem_strat = std::make_shared<
       rclcpp::message_memory_strategy::MessageMemoryStrategy<
         std_msgs::msg::UInt32, MyAllocator<void>>>(alloc);
     auto subscriber = node->create_subscription<std_msgs::msg::UInt32>(
       "allocator_tutorial", 10, callback, subscription_options, msg_mem_strat);

     std::shared_ptr<rclcpp::memory_strategy::MemoryStrategy> memory_strategy =
       std::make_shared<AllocatorMemoryStrategy<MyAllocator<void>>>(alloc);
     rclcpp::ExecutorOptions options;
     options.memory_strategy = memory_strategy;
     rclcpp::executors::SingleThreadedExecutor executor(options);

你还需要使用你的分配器来分配你在执行代码路径中传递的任何消息。

.. code-block:: c++

     auto alloc = std::make_shared<MyAllocator<void>>();

一旦你实例化了节点并将 executor 添加到节点，就该 spin 了：

.. code-block:: c++

     uint32_t i = 0;
     while (rclcpp::ok()) {
       msg->data = i;
       i++;
       publisher->publish(msg);
       rclcpp::sleep_for(std::chrono::milliseconds(1));
       executor.spin_some();
     }

将分配器传递给进程内管道
------------------------

尽管我们在同一进程中实例化了发布者和订阅者，但我们还没有使用进程内（intra-process）管道。

IntraProcessManager 是一个通常对用户隐藏的类，但为了向它传递自定义分配器，我们需要通过从 rclcpp Context 获取它来暴露它。
IntraProcessManager 使用多种标准库结构，因此如果没有自定义分配器，它将调用默认的 ``new``。

.. code-block:: c++

    auto context = rclcpp::contexts::get_global_default_context();
    auto options = rclcpp::NodeOptions()
      .context(context)
      .use_intra_process_comms(true);
    auto node = rclcpp::Node::make_shared("allocator_example", options);

请确保在以此方式构造节点之后，再实例化发布者和订阅者。

测试和验证代码
--------------

你怎么知道你的自定义分配器真的被调用了呢？

显而易见的做法是统计对你的自定义分配器的 ``allocate`` 和 ``deallocate`` 函数的调用次数，并与对 ``new`` 和 ``delete`` 的调用次数进行比较。

给自定义分配器添加计数很容易：

.. code-block:: c++

     T * allocate(size_t size, const void * = 0) {
       // ...
       num_allocs++;
       // ...
     }

     void deallocate(T * ptr, size_t size) {
       // ...
       num_deallocs++;
       // ...
     }

你还可以重写全局 ``new`` 和 ``delete`` 运算符：

.. code-block:: c++

   void operator delete(void * ptr) noexcept {
     if (ptr != nullptr) {
       if (is_running) {
         global_runtime_deallocs++;
       }
       std::free(ptr);
       ptr = nullptr;
     }
   }

   void operator delete(void * ptr, size_t) noexcept {
     if (ptr != nullptr) {
       if (is_running) {
         global_runtime_deallocs++;
       }
       std::free(ptr);
       ptr = nullptr;
     }
   }

其中我们递增的变量只是全局静态整数，而 ``is_running`` 是一个全局静态布尔变量，它在调用 ``spin`` 之前被切换。

`示例可执行文件 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/topics/allocator_tutorial.cpp>`__ 会打印这些变量的值。
要运行示例可执行文件，请使用：

.. code-block:: bash

     $ ros2 run demo_nodes_cpp allocator_tutorial

或者，运行开启了进程内管道的示例：

.. code-block:: bash

     $ ros2 run demo_nodes_cpp allocator_tutorial intra
     Global new was called 15590 times during spin
     Global delete was called 15590 times during spin
     Allocator new was called 27284 times during spin
     Allocator delete was called 27281 times during spin

我们已经捕获了执行路径上发生的约 2/3 的分配/释放，但剩余 1/3 来自哪里呢？

事实上，这些分配/释放来源于本示例中使用的底层 DDS 实现。

证明这一点超出了本教程的范围，但你可以查看作为 ROS 2 持续集成测试一部分运行的分配路径测试，它通过代码回溯来确定某些函数调用是源自 rmw 实现还是 DDS 实现：

https://github.com/ros2/realtime_support/blob/{REPOS_FILE_BRANCH}/tlsf_cpp/test/test_tlsf.cpp#L41

请注意，这个测试使用的不是我们刚创建的自定义分配器，而是 TLSF 分配器（见下文）。

TLSF 分配器
-----------

ROS 2 提供对 TLSF（Two Level Segregate Fit，两级分离适配）分配器的支持，它是为满足实时要求而设计的：

https://github.com/ros2/realtime_support/tree/{REPOS_FILE_BRANCH}/tlsf_cpp

有关 TLSF 的更多信息，请参见 `瓦伦西亚理工大学提供的这个页面 <http://www.gii.upv.es/tlsf/>`_。

请注意，TLSF 分配器采用双重 GPL/LGPL 许可证。

使用 TLSF 分配器的完整可运行示例在这里：
https://github.com/ros2/realtime_support/blob/{REPOS_FILE_BRANCH}/tlsf_cpp/example/allocator_example.cpp
