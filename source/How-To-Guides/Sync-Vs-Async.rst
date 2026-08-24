.. redirect-from::

  Guides/Sync-Vs-Async
  Tutorials/Sync-Vs-Async

.. _SyncAsync:

同步与异步服务客户端
====================

**难度：** 中级

**时长：** 10 分钟

.. contents:: Contents
   :depth: 2
   :local:


简介
----

本指南旨在提醒用户注意 Python 同步服务客户端 ``call()`` API 所带来的风险。
同步调用服务时很容易错误地导致死锁，因此我们不推荐使用 ``call()``。

我们为希望使用同步调用并且了解其中陷阱的有经验的用户提供了一个如何正确使用 ``call()`` 的示例。
我们还强调了伴随它可能出现的死锁场景。

由于我们建议避免同步调用，本指南也将讨论推荐替代方案——异步调用（``call_async()``）的特性和用法。

C++ 服务调用 API 仅提供异步形式，因此本指南中的比较和示例仅适用于 Python 服务和客户端。
这里给出的异步定义通常也适用于 C++，但有一些例外。

1 同步调用
----------

同步客户端在向服务发送请求时会阻塞调用线程，直到收到响应；在调用期间，该线程上不能发生其他任何事情。
调用可能需要任意长的时间才能完成。
完成后，响应会直接返回给客户端。

下面是一个如何从客户端节点正确执行同步服务调用的示例，类似于 :doc:`简单服务和客户端 <../Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client>` 教程中的异步节点。

.. code-block:: python

  import sys
  from threading import Thread

  from example_interfaces.srv import AddTwoInts
  import rclpy
  from rclpy.node import Node

  class MinimalClientSync(Node):

      def __init__(self):
          super().__init__('minimal_client_sync')
          self.cli = self.create_client(AddTwoInts, 'add_two_ints')
          while not self.cli.wait_for_service(timeout_sec=1.0):
              self.get_logger().info('service not available, waiting again...')
          self.req = AddTwoInts.Request()

      def send_request(self):
          self.req.a = int(sys.argv[1])
          self.req.b = int(sys.argv[2])
          return self.cli.call(self.req)
          # This only works because rclpy.spin() is called in a separate thread below.
          # Another configuration, like spinning later in main() or calling this method from a timer callback, would result in a deadlock.

  def main():
      rclpy.init()

      minimal_client = MinimalClientSync()

      spin_thread = Thread(target=rclpy.spin, args=(minimal_client,))
      spin_thread.start()

      response = minimal_client.send_request()
      minimal_client.get_logger().info(
          'Result of add_two_ints: for %d + %d = %d' %
          (minimal_client.req.a, minimal_client.req.b, response.sum))

      minimal_client.destroy_node()
      rclpy.shutdown()


  if __name__ == '__main__':
      main()

注意在 ``main()`` 中，客户端在一个单独的线程中调用 ``rclpy.spin``。
``send_request`` 和 ``rclpy.spin`` 都是阻塞的，因此它们需要位于不同的线程上。

1.1 同步死锁
------------

同步 ``call()`` API 导致死锁的方式有几种。

如上面示例的注释所述，未能创建一个单独的线程来运行 ``rclpy`` 是死锁的一个原因。
当客户端阻塞一个线程等待响应，但响应只能在该同一个线程上返回时，客户端将永远不会停止等待，其他任何事情都无法发生。

死锁的另一个原因是在订阅、定时器回调或服务回调中同步调用服务，从而阻塞 ``rclpy.spin``。
例如，如果同步客户端的 ``send_request`` 被放在一个回调中：

.. code-block:: python

  def trigger_request(msg):
      response = minimal_client.send_request()  # This will cause deadlock
      minimal_client.get_logger().info(
          'Result of add_two_ints: for %d + %d = %d' %
          (minimal_client.req.a, minimal_client.req.b, response.sum))
  subscription = minimal_client.create_subscription(String, 'trigger', trigger_request, 10)

  rclpy.spin(minimal_client)

发生死锁是因为 ``rclpy.spin`` 不会抢占带有 ``send_request`` 调用的回调。
一般来说，回调只应执行轻量且快速的操作。

.. warning::

  当发生死锁时，你不会收到任何关于服务被阻塞的提示。
  不会有警告或异常抛出，堆栈跟踪中也不会有任何指示，调用也不会失败。

2 异步调用
----------

``rclpy`` 中的异步调用是完全安全的，也是调用服务的推荐方法。
与同步调用不同，它们可以在任何地方进行，而不会有阻塞其他 ROS 和非 ROS 进程的风险。

异步客户端在向服务发送请求后会立即返回 ``future``，这是一个指示调用和响应是否已完成的值（而不是响应本身的值）。
返回的 ``future`` 可以随时被查询以获取响应。

由于发送请求不会阻塞任何东西，因此可以使用一个循环在同一个线程中既运行 ``rclpy`` 又检查 ``future``，例如：

.. code-block:: python

    while rclpy.ok():
        rclpy.spin_once(node)
        if future.done():
            #Get response

Python 的 :doc:`简单服务和客户端 <../Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client>` 教程说明了如何执行异步服务调用并使用循环检索 ``future``。

``future`` 也可以使用定时器或回调来检索，例如 `这个示例 <https://github.com/ros2/examples/blob/{REPOS_FILE_BRANCH}/rclpy/services/minimal_client/examples_rclpy_minimal_client/client_async_callback.py>`_，或使用专用线程，或其他方法。
作为调用者，由你决定如何存储 ``future``、检查其状态并检索你的响应。

总结
----

不推荐实现同步服务客户端。
它们容易发生死锁，并且在死锁发生时不会提供任何问题指示。
如果你必须使用同步调用，`1 同步调用`_ 一节中的示例是一种安全的方法。
你还应该了解 `1.1 同步死锁`_ 一节中概述的导致死锁的条件。
我们建议改用异步服务客户端。
