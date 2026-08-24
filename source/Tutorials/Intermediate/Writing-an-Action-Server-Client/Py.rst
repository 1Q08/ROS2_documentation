.. redirect-from::

    Tutorials/Actions/Writing-a-Py-Action-Server-Client

.. _ActionsPy:

编写一个 action 服务器和客户端（Python）
========================================

**目标：** 用 Python 实现一个 action 服务器和客户端。

**教程级别：** 中级

**时间：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

Action 是 ROS 2 中一种异步通信的形式。
*Action 客户端* 向 *action 服务器* 发送目标请求。
*Action 服务器* 向 *action 客户端* 发送目标反馈和结果。

先决条件
--------

你需要 ``custom_action_interfaces`` 包以及在前面教程 :doc:`../Creating-an-Action` 中定义的 ``Fibonacci.action`` 接口。

任务
----

1 编写一个 action 服务器
^^^^^^^^^^^^^^^^^^^^^^^^

让我们专注于编写一个 action 服务器，它使用我们在 :doc:`../Creating-an-Action` 教程中创建的 action 来计算斐波那契数列。

到目前为止，你已经创建了包并使用 ``ros2 run`` 来运行节点。
但是，为了让本教程保持简单，我们将 action 服务器限定在单个文件中。
如果你想看看 actions 教程的完整包是什么样子，请查看
`action_tutorials <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/action_tutorials>`__。

在你的主目录中打开一个新文件，我们叫它 ``fibonacci_action_server.py``，
并添加以下代码：

.. literalinclude:: scripts/server_0.py
    :language: python

第 8 行定义了一个类 ``FibonacciActionServer``，它是 ``Node`` 的子类。
该类通过调用 ``Node`` 构造函数来初始化，将我们的节点命名为 ``fibonacci_action_server``：

.. literalinclude:: scripts/server_0.py
    :language: python
    :lines: 11

在构造函数中我们还实例化了一个新的 action 服务器：

.. literalinclude:: scripts/server_0.py
    :language: python
    :lines: 12-16

一个 action 服务器需要四个参数：

1. 一个要添加 action 服务器的 ROS 2 节点：``self``。
2. action 的类型：``Fibonacci`` （在第 5 行导入）。
3. action 名称：``'fibonacci'``。
4. 一个执行已接受目标的回调函数：``self.execute_callback``。
   这个回调 **必须** 返回一个 action 类型的结果消息。

我们还在类中定义了一个 ``execute_callback`` 方法：

.. literalinclude:: scripts/server_0.py
    :language: python
    :lines: 18-21

这就是一旦目标被接受后将被调用来执行目标的方法。

让我们尝试运行我们的 action 服务器：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ python3 fibonacci_action_server.py

  .. group-tab:: macOS

    .. code-block:: console

      $ python3 fibonacci_action_server.py

  .. group-tab:: Windows

    .. code-block:: console

      $ python fibonacci_action_server.py

在另一个终端中，我们可以使用命令行接口来发送目标：

.. code-block:: console

    $ ros2 action send_goal fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"

在运行 action 服务器的终端中，你应该会看到一条日志消息 "Executing goal..."，然后是一条警告，说明目标状态未设置。
默认情况下，如果在 execute 回调中没有设置目标句柄状态，它会假定为 *已中止* 状态。

我们可以对目标句柄调用 ``succeed()`` 来表示目标成功：

.. literalinclude:: scripts/server_1.py
    :language: python
    :lines: 18-22
    :emphasize-lines: 3

现在如果你重启 action 服务器并发送另一个目标，你应该会看到目标以状态 ``SUCCEEDED`` 完成。

现在让我们的目标执行真正计算并返回请求的斐波那契数列：

.. literalinclude:: scripts/server_2.py
    :language: python
    :lines: 18-30
    :emphasize-lines: 4-7,12

计算完序列后，我们在返回之前把它赋给结果消息字段。

再次重启 action 服务器并发送另一个目标。
你应该会看到目标以正确的结果序列完成。

1.2 发布反馈
~~~~~~~~~~~~

action 的一个优点是在目标执行期间能够向 action 客户端提供反馈。
我们可以通过调用目标句柄的 ``publish_feedback()`` 方法，让我们的 action 服务器为 action 客户端发布反馈。

我们将替换 ``sequence`` 变量，改用反馈消息来存储序列。
在 for 循环中每次更新反馈消息后，我们发布反馈消息并 sleep 一下以获得更好的效果：

.. literalinclude:: scripts/server_3.py
    :language: python
    :emphasize-lines: 1,23,24,27-31,36

重启 action 服务器后，我们可以通过使用带 ``--feedback`` 选项的命令行工具来确认反馈现在被发布了：

.. code-block:: console

    $ ros2 action send_goal --feedback fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"

2 编写一个 action 客户端
^^^^^^^^^^^^^^^^^^^^^^^^

我们也将 action 客户端限定在单个文件中。
打开一个新文件，我们叫它 ``fibonacci_action_client.py``，并添加以下样板代码：

.. literalinclude:: scripts/client_0.py
    :language: python

我们定义了一个类 ``FibonacciActionClient``，它是 ``Node`` 的子类。
该类通过调用 ``Node`` 构造函数来初始化，将我们的节点命名为 ``fibonacci_action_client``：

.. literalinclude:: scripts/client_0.py
    :language: python
    :lines: 11

同样在类构造函数中，我们使用前面教程 :doc:`../Creating-an-Action` 中的自定义 action 定义来创建一个 action 客户端：

.. literalinclude:: scripts/client_0.py
    :language: python
    :lines: 12

我们通过传递三个参数来创建一个 ``ActionClient``：

1. 一个要添加 action 客户端的 ROS 2 节点：``self``
2. action 的类型：``Fibonacci``
3. action 名称：``'fibonacci'``

我们的 action 客户端将能够与具有相同 action 名称和类型的 action 服务器通信。

我们还在 ``FibonacciActionClient`` 类中定义了一个方法 ``send_goal``：

.. literalinclude:: scripts/client_0.py
    :language: python
    :lines: 14-20

这个方法等待 action 服务器可用，然后向服务器发送一个目标。
它返回一个我们稍后可以等待的 future。

在类定义之后，我们定义了一个函数 ``main()``，它初始化 ROS 2
并创建我们 ``FibonacciActionClient`` 节点的一个实例。
然后它发送一个目标并等待该目标完成。

最后，我们在 Python 程序的入口点调用 ``main()``。

让我们先运行前面构建的 action 服务器来测试我们的 action 客户端：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ python3 fibonacci_action_server.py

  .. group-tab:: macOS

    .. code-block:: console

      $ python3 fibonacci_action_server.py

  .. group-tab:: Windows

    .. code-block:: console

      $ python fibonacci_action_server.py

在另一个终端中，运行 action 客户端。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ python3 fibonacci_action_client.py


  .. group-tab:: macOS

    .. code-block:: console

      $ python3 fibonacci_action_client.py


  .. group-tab:: Windows

    .. code-block:: console

      $ python fibonacci_action_client.py

当 action 服务器成功执行目标时，你应该会看到它打印的消息：

.. code-block:: console

    [INFO] [fibonacci_action_server]: Executing goal...
    [INFO] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1])
    [INFO] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2])
    [INFO] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2, 3])
    [INFO] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2, 3, 5])
    ~ 等等。

action 客户端应该会启动，然后很快结束。
此时，我们有了一个可用的 action 客户端，但我们看不到任何结果，也得不到任何反馈。

2.1 获取结果
~~~~~~~~~~~~

所以我们可以发送一个目标，但我们怎么知道它什么时候完成呢？
我们可以通过几个步骤获取结果信息。
首先，我们需要为我们发送的目标获取一个目标句柄。
然后，我们可以使用目标句柄来请求结果。

以下是这个例子的完整代码：

.. literalinclude:: scripts/client_1.py
    :language: python

``ActionClient.send_goal_async()`` 方法返回一个指向目标句柄的 future。
首先我们为 future 完成时注册一个回调：

.. literalinclude:: scripts/client_1.py
    :language: python
    :lines: 22

请注意，当 action 服务器接受或拒绝目标请求时，future 就会完成。
让我们更详细地看看 ``goal_response_callback``。
我们可以检查目标是否被拒绝，并提前返回，因为我们知道不会有结果：

.. literalinclude:: scripts/client_1.py
    :language: python
    :lines: 24-30

现在我们有了目标句柄，我们可以用方法 ``get_result_async()`` 来请求结果。
与发送目标类似，我们会得到一个在结果就绪时完成的 future。
让我们像为目标响应那样注册一个回调：

.. literalinclude:: scripts/client_1.py
    :language: python
    :lines: 32-33

在回调中，我们记录结果序列并关闭 ROS 2 以便干净退出：

.. literalinclude:: scripts/client_1.py
    :language: python
    :lines: 35-38

在另一个终端中运行着 action 服务器的情况下，继续尝试运行我们的 Fibonacci action 客户端吧！

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ python3 fibonacci_action_client.py

  .. group-tab:: macOS

    .. code-block:: console

      $ python3 fibonacci_action_client.py

  .. group-tab:: Windows

    .. code-block:: console

      $ python fibonacci_action_client.py

你应该会看到关于目标被接受和最终结果的日志消息。

2.2 获取反馈
~~~~~~~~~~~~

我们的 action 客户端可以发送目标。
不错！
但是如果我们能从 action 服务器获得一些关于我们发送的目标的反馈，那就更好了。

以下是这个例子的完整代码：

.. literalinclude:: scripts/client_2.py
    :language: python

下面是反馈消息的回调函数：

.. literalinclude:: scripts/client_2.py
    :language: python
    :lines: 40-42

在回调中，我们获取消息的反馈部分，并将 ``partial_sequence`` 字段打印到屏幕上。

我们需要向 action 客户端注册这个回调。
这可以通过在发送目标时额外把回调传给 action 客户端来实现：

.. literalinclude:: scripts/client_2.py
    :language: python
    :lines: 20

我们都准备好了。
如果我们运行 action 客户端，你应该会看到反馈被打印到屏幕上。

总结
----

在本教程中，你逐行组装了一个 Python action 服务器和 action 客户端，并配置它们来交换目标、反馈和结果。

相关内容
--------

* 用 Python 编写 action 服务器和客户端有多种方法；请查看 `ros2/examples <https://github.com/ros2/examples/tree/{REPOS_FILE_BRANCH}/rclpy/actions>`_ 仓库中的 ``minimal_action_server`` 和 ``minimal_action_client`` 包。

* 有关 ROS action 的更多详细信息，请参阅 `设计文章 <http://design.ros2.org/articles/actions.html>`__。
