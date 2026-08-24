.. redirect-from::

    Allocator-Template-Tutorial
    Tutorials/Allocator-Template-Tutorial

实现自定义内存分配器
====================

**目标：** 本教程将展示在编写 ROS 2 C++ 代码时如何使用自定义内存分配器。

**教程级别：** 高级

**预计用时：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

本教程将教你如何为发布者和订阅者集成自定义分配器，使默认的堆分配器在 ROS 节点执行期间永不被调用。
本教程的代码可以在 `这里 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/topics/allocator_tutorial_pmr.cpp>`__ 找到。

背景
----

假设你想编写实时安全（real-time safe）的代码，而且你听说过在实时关键段调用 ``new`` 的诸多危险，因为大多数平台上的默认堆分配器是不确定的。

默认情况下，许多 C++ 标准库结构在增长时会隐式分配内存，例如 ``std::vector``。
然而，这些数据结构也接受一个 “Allocator” 模板参数。
如果你为这些数据结构之一指定了自定义分配器，它将使用该分配器而不是系统分配器来增长或缩小数据结构。
你的自定义分配器可以在栈上预先分配一块内存池，这可能更适用于实时应用。

在 ROS 2 C++ 客户端库（rclcpp）中，我们遵循与 C++ 标准库相似的哲学。
发布者、订阅者和 Executor 接受一个 Allocator 模板参数，该参数控制这些实体在执行期间进行的分配。

编写一个分配器
--------------

要编写一个与 ROS 2 分配器接口兼容的分配器，你的分配器必须与 C++ 标准库分配器接口兼容。

自 C++17 起，标准库提供了一种称为 ``std::pmr::memory_resource`` 的东西。
这是一个可以被继承的类，用于创建满足一组最低要求的自定义分配器。

例如，下面这个自定义内存资源的声明满足了这些要求（当然，你仍然需要在这个类中实现声明的函数）：

.. code-block:: c++

    class CustomMemoryResource : public std::pmr::memory_resource
    {
    private:
      void * do_allocate(std::size_t bytes, std::size_t alignment) override;

      void do_deallocate(
        void * p, std::size_t bytes,
        std::size_t alignment) override;

      bool do_is_equal(
        const std::pmr::memory_resource & other) const noexcept override;
    };

要了解 ``std::pmr::memory_resource`` 的全部能力，请参见 https://en.cppreference.com/w/cpp/memory/memory_resource。

本教程中自定义分配器的完整实现在 https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/topics/allocator_tutorial_pmr.cpp。

编写一个示例 main
-----------------

一旦你编写好了一个有效的 C++ 分配器，你必须将它作为共享指针传递给发布者、订阅者和 executor。
但首先，我们声明几个别名以缩短名称。

.. code-block:: c++

     using rclcpp::memory_strategies::allocator_memory_strategy::AllocatorMemoryStrategy;
     using Alloc = std::pmr::polymorphic_allocator<void>;
     using MessageAllocTraits =
       rclcpp::allocator::AllocRebind<std_msgs::msg::UInt32, Alloc>;
     using MessageAlloc = MessageAllocTraits::allocator_type;
     using MessageDeleter = rclcpp::allocator::Deleter<MessageAlloc, std_msgs::msg::UInt32>;
     using MessageUniquePtr = std::unique_ptr<std_msgs::msg::UInt32, MessageDeleter>;

现在我们可以使用自定义分配器创建我们的资源：

.. code-block:: c++

     CustomMemoryResource mem_resource{};
     auto alloc = std::make_shared<Alloc>(&mem_resource);
     rclcpp::PublisherOptionsWithAllocator<Alloc> publisher_options;
     publisher_options.allocator = alloc;
     auto publisher = node->create_publisher<std_msgs::msg::UInt32>(
       "allocator_tutorial", 10, publisher_options);

     rclcpp::SubscriptionOptionsWithAllocator<Alloc> subscription_options;
     subscription_options.allocator = alloc;
     auto msg_mem_strat = std::make_shared<
       rclcpp::message_memory_strategy::MessageMemoryStrategy<
         std_msgs::msg::UInt32, Alloc>>(alloc);
     auto subscriber = node->create_subscription<std_msgs::msg::UInt32>(
       "allocator_tutorial", 10, callback, subscription_options, msg_mem_strat);

     std::shared_ptr<rclcpp::memory_strategy::MemoryStrategy> memory_strategy =
       std::make_shared<AllocatorMemoryStrategy<Alloc>>(alloc);

     rclcpp::ExecutorOptions options;
     options.memory_strategy = memory_strategy;
     rclcpp::executors::SingleThreadedExecutor executor(options);

你还需要实例化一个自定义 deleter 和 allocator，用于分配消息时使用：

.. code-block:: c++

     MessageDeleter message_deleter;
     MessageAlloc message_alloc = *alloc;
     rclcpp::allocator::set_allocator_for_deleter(&message_deleter, &message_alloc);

一旦你把节点添加到 executor，就该 spin 了。
我们将使用自定义分配器来分配每条消息：

.. code-block:: c++

     uint32_t i = 0;
     while (rclcpp::ok()) {
       auto ptr = MessageAllocTraits::allocate(message_alloc, 1);
       MessageAllocTraits::construct(message_alloc, ptr);
       MessageUniquePtr msg(ptr, message_deleter);
       msg->data = i;
       ++i;
       publisher->publish(std::move(msg));
       rclcpp::sleep_for(10ms);
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

     void * do_allocate(std::size_t size, std::size_t alignment) override
     {
       // ...
       num_allocs++;
       // ...
     }

     void do_deallocate(
       void * p, std::size_t bytes,
       std::size_t alignment) override
     {
       // ...
       num_deallocs++;
       // ...
     }

你还可以重写全局 ``new`` 和 ``delete`` 运算符：

.. code-block:: c++

     void * operator new(std::size_t size)
     {
       if (is_running) {
         global_runtime_allocs++;
       }
       return std::malloc(size);
     }

     void operator delete(void * ptr, size_t) noexcept
     {
       if (ptr != nullptr) {
         if (is_running) {
           global_runtime_deallocs++;
         }
         std::free(ptr);
       }
     }

     void operator delete(void * ptr) noexcept
     {
       if (ptr != nullptr) {
         if (is_running) {
           global_runtime_deallocs++;
         }
         std::free(ptr);
       }
     }

其中我们递增的变量只是全局静态整数，而 ``is_running`` 是一个全局静态布尔变量，它在调用 ``spin`` 之前被切换。

`示例可执行文件 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/topics/allocator_tutorial_pmr.cpp>`__ 会打印这些变量的值。
要运行示例可执行文件，请使用：

.. code-block:: console

     $ ros2 run demo_nodes_cpp allocator_tutorial

或者，运行开启了进程内管道的示例：

.. code-block:: console

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
