.. redirect-from::

    About-ROS-Interfaces
    Concepts/About-ROS-Interfaces

接口
====

.. contents:: 目录
   :local:

背景
----

ROS 应用通常通过以下三种类型之一的接口进行通信：:doc:`话题 <About-Topics>`、:doc:`服务 <About-Services>` 或 :doc:`动作 <About-Actions>`。
ROS 2 使用一种简化的描述语言，即接口定义语言（IDL），来描述这些接口。
这种描述让 ROS 工具能够轻松地为该接口类型自动生成多种目标语言的源代码。

在本文档中，我们将介绍受支持的类型：

* msg：``.msg`` 文件是简单的文本文件，描述 ROS 消息的字段。
  它们用于为不同语言生成消息的源代码。
* srv：``.srv`` 文件描述服务。
  它们由两部分组成：请求和响应。
  请求和响应都是消息声明。
* action：``.action`` 文件描述动作。
  它们由三部分组成：目标、结果和反馈。
  每个部分本身都是一个消息声明。

消息
----

消息是 ROS 2 节点在网络上向其他 ROS 节点发送数据的一种方式，不期望收到响应。
例如，如果某个 ROS 2 节点从传感器读取温度数据，它就可以使用 ``Temperature`` 消息在 ROS 2 网络上发布这些数据。
ROS 2 网络上的其他节点可以订阅这些数据并接收 ``Temperature`` 消息。

消息在 ROS 包 ``msg/`` 目录下的 ``.msg`` 文件中进行描述和定义。
``.msg`` 文件由两部分组成：字段和常量。

字段
^^^^

每个字段由类型和名称组成，中间用空格分隔，即：

.. code-block:: bash

   fieldtype1 fieldname1
   fieldtype2 fieldname2
   fieldtype3 fieldname3

例如：

.. code-block:: bash

   int32 my_int
   string my_string

字段类型
~~~~~~~~

字段类型可以是：

* 内置类型
* 单独定义的消息描述的名称，例如 "geometry_msgs/PoseStamped"

*当前支持的内置类型：*

.. list-table::
   :header-rows: 1

   * - 类型名称
     - `C++ <https://design.ros2.org/articles/generated_interfaces_cpp.html>`__
     - `Python <https://design.ros2.org/articles/generated_interfaces_python.html>`__
     - `DDS 类型 <https://design.ros2.org/articles/mapping_dds_types.html>`__
   * - bool
     - bool
     - builtins.bool
     - boolean
   * - byte
     - uint8_t
     - builtins.bytes*
     - octet
   * - char
     - char
     - builtins.int*
     - char
   * - float32
     - float
     - builtins.float*
     - float
   * - float64
     - double
     - builtins.float*
     - double
   * - int8
     - int8_t
     - builtins.int*
     - octet
   * - uint8
     - uint8_t
     - builtins.int*
     - octet
   * - int16
     - int16_t
     - builtins.int*
     - short
   * - uint16
     - uint16_t
     - builtins.int*
     - unsigned short
   * - int32
     - int32_t
     - builtins.int*
     - long
   * - uint32
     - uint32_t
     - builtins.int*
     - unsigned long
   * - int64
     - int64_t
     - builtins.int*
     - long long
   * - uint64
     - uint64_t
     - builtins.int*
     - unsigned long long
   * - string
     - std::string
     - builtins.str
     - string
   * - wstring
     - std::u16string
     - builtins.str
     - wstring

*每种内置类型都可以用来定义数组：*

.. list-table::
   :header-rows: 1

   * - 类型名称
     - `C++ <https://design.ros2.org/articles/generated_interfaces_cpp.html>`__
     - `Python <https://design.ros2.org/articles/generated_interfaces_python.html>`__
     - `DDS 类型 <https://design.ros2.org/articles/mapping_dds_types.html>`__
   * - 静态数组
     - std::array<T, N>
     - builtins.list*
     - T[N]
   * - 无界动态数组
     - std::vector
     - builtins.list
     - sequence
   * - 有界动态数组
     - custom_class<T, N>
     - builtins.list*
     - sequence<T, N>
   * - 有界字符串
     - std::string
     - builtins.str*
     - string

(*) 所有比其 ROS 定义更宽松的类型，都会在范围和长度上由软件强制执行 ROS 的约束。

*使用数组和有界类型的消息定义示例：*

.. code-block:: bash

   int32[] unbounded_integer_array
   int32[5] five_integers_array
   int32[<=5] up_to_five_integers_array

   string string_of_unbounded_size
   string<=10 up_to_ten_characters_string

   string[<=5] up_to_five_unbounded_strings
   string<=10[] unbounded_array_of_strings_up_to_ten_characters_each
   string<=10[<=5] up_to_five_strings_up_to_ten_characters_each

字段名称
~~~~~~~~

字段名称必须是小写字母数字字符，并用下划线分隔单词。
它们必须以字母字符开头，不得以下划线结尾，也不得包含两个连续的下划线。

字段默认值
~~~~~~~~~~

可以为消息类型中的任何字段设置默认值。
目前，字符串数组和复杂类型（即上述内置类型表中不存在的类型；这适用于所有嵌套消息）不支持默认值。

定义默认值的方法是在字段定义行中添加第三个元素，即：

.. code-block:: bash

   fieldtype fieldname fielddefaultvalue

例如：

.. code-block:: bash

   uint8 x 42
   int16 y -2000
   string full_name "John Doe"
   int32[] samples [-200, -100, 0, 100, 200]

.. note::

  * 字符串值必须用单引号 ``'`` 或双引号 ``"`` 括起来
  * 目前字符串值不会被转义

常量
^^^^

每个常量定义就像带默认值的字段描述一样，不同之处在于该值永远无法通过编程方式更改。
这种值赋值通过使用等号 ``=`` 表示，例如：

.. code-block:: bash

   constanttype CONSTANTNAME=constantvalue

例如：

.. code-block:: bash

   int32 X=123
   int32 Y=-123
   string FOO="foo"
   string EXAMPLE='bar'

.. note::

   常量名称必须是大写

服务
----

服务是一种请求/响应通信，其中客户端（请求方）等待服务器（响应方）进行简短的计算并返回结果。

服务在 ROS 包 ``srv/`` 目录下的 ``.srv`` 文件中进行描述和定义。

服务描述文件由一个请求和一个响应消息类型组成，中间用 ``---`` 分隔。
任意两个用 ``---`` 拼接的 ``.msg`` 文件都是一个合法的服务描述。

下面是一个非常简单的服务示例，它接收一个字符串并返回一个字符串：

.. code-block:: bash

   string str
   ---
   string str

当然，我们也可以变得复杂得多（如果你想引用同一包中的消息，则不得提及包名）：

.. code-block:: bash

   # request constants
   int8 FOO=1
   int8 BAR=2
   # request fields
   int8 foobar
   another_pkg/AnotherMessage msg
   ---
   # response constants
   uint32 SECRET=123456
   # response fields
   another_pkg/YetAnotherMessage val
   CustomMessageDefinedInThisPackage value
   uint32 an_integer

你不能在一个服务中嵌入另一个服务。

动作
----

动作是一种长时间运行的请求/响应通信，其中动作客户端（请求方）等待动作服务器（响应方）执行某个动作并返回结果。
与服务相比，动作可以长时间运行（几秒或几分钟），在执行过程中提供反馈，并且可以被中断。

动作定义具有以下形式：

.. code::

   <request_type> <request_fieldname>
   ---
   <response_type> <response_fieldname>
   ---
   <feedback_type> <feedback_fieldname>

与服务类似，请求字段位于第一个三连字符（``---``）之前，响应字段位于其之后。
在第二个三连字符之后还有第三组字段，即发送反馈时要发送的字段。

可以有任意数量的请求字段（包括零个）、任意数量的响应字段（包括零个）和任意数量的反馈字段（包括零个）。

``<request_type>``、``<response_type>`` 和 ``<feedback_type>`` 遵循与消息的 ``<type>`` 相同的所有规则。
``<request_fieldname>``、``<response_fieldname>`` 和 ``<feedback_fieldname>`` 遵循与消息的 ``<fieldname>`` 相同的所有规则。

例如，``Fibonacci`` 动作定义包含以下内容：

.. code::

   int32 order
   ---
   int32[] sequence
   ---
   int32[] sequence

这是一个动作定义，其中动作客户端发送一个 ``int32`` 字段，表示要计算斐波那契数列的步数，并期望动作服务器生成一个包含完整步骤的 ``int32`` 数组。
在此过程中，动作服务器还可以提供一个中间的 ``int32`` 数组，其中包含截至某个点为止已完成的步骤。
