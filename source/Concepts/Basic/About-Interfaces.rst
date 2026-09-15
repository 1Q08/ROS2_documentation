.. redirect-from::

    About-ROS-Interfaces
    Concepts/About-ROS-Interfaces

接口
====

.. contents:: 目录
   :local:

背景
----

ROS 应用通常通过三种接口之一进行通信：:doc:`主题 <About-Topics>`、:doc:`服务 <About-Services>` 或 :doc:`动作 <About-Actions>`。
ROS 2 使用一种简化的描述语言，即接口定义语言（IDL），来描述这些接口。
这种描述方式使 ROS 工具能够方便地为多种目标语言中的接口类型自动生成源代码。

本文档将描述受支持的类型：

* msg：``.msg`` 文件是描述 ROS 消息字段的纯文本文件。
  它们用于为不同语言生成消息的源代码。
* srv：``.srv`` 文件描述一个服务。
  它由两部分组成：请求和响应。
  请求和响应都是消息声明。
* action：``.action`` 文件描述动作。
  它由三部分组成：目标、结果和反馈。
  每一部分本身都是一个消息声明。

消息
----

消息是 ROS 2 节点在网络中向其他 ROS 节点发送数据的一种方式，且无需预期响应。
例如，如果一个 ROS 2 节点从传感器读取温度数据，则它可以利用 ``Temperature`` 消息将该数据发布到 ROS 2 网络。
ROS 2 网络中的其他节点可以订阅该数据并接收 ``Temperature`` 消息。

消息在 ROS 包的 ``msg/`` 目录中的 ``.msg`` 文件中被描述和定义。
``.msg`` 文件由两部分组成：字段和常量。

字段
^^^^

每个字段都由类型和名称组成，中间用空格分隔，例如：

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
* 单独定义的消息描述名称，例如 ``geometry_msgs/PoseStamped``

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

*任意内置类型都可以用于定义数组：*

.. list-table::
   :header-rows: 1

   * - 类型名称
     - `C++ <https://design.ros2.org/articles/generated_interfaces_cpp.html>`__
     - `Python <https://design.ros2.org/articles/generated_interfaces_python.html>`__
     - `DDS 类型 <https://design.ros2.org/articles/mapping_dds_types.html>`__
   * - static array
     - std::array<T, N>
     - builtins.list*
     - T[N]
   * - unbounded dynamic array
     - std::vector
     - builtins.list
     - sequence
   * - bounded dynamic array
     - custom_class<T, N>
     - builtins.list*
     - sequence<T, N>
   * - bounded string
     - std::string
     - builtins.str*
     - string

(*) 所有比其 ROS 定义更宽松的类型都将由软件强制执行 ROS 对范围和长度的约束。

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

字段名称必须仅包含小写字母数字字符，并使用下划线作为分隔符。
它们必须以字母开头，且不能以下划线结尾，也不能包含连续两个下划线。

字段默认值
~~~~~~~~~~

默认值可以设置为消息类型中的任意字段。
目前，字符串数组和复杂类型（即不在上面的内置类型表中的类型；这同样适用于所有嵌套消息）不支持默认值。

设置默认值的方法是在字段定义行中添加第三个元素，即：

.. code-block:: bash

   fieldtype fieldname fielddefaultvalue

例如：

.. code-block:: bash

   uint8 x 42
   int16 y -2000
   string full_name "John Doe"
   int32[] samples [-200, -100, 0, 100, 200]

.. note::

  * 字符串值必须使用单引号 ``'`` 或双引号 ``"`` 括起来
  * 当前字符串值不会被转义

常量
^^^^

每个常量定义都类似于带有默认值的字段描述，只是该值无法通过程序进行修改。
这个赋值使用等号 ``=`` 表示，例如：

.. code-block:: bash

   constanttype CONSTANTNAME=constantvalue

例如：

.. code-block:: bash

   int32 X=123
   int32 Y=-123
   string FOO="foo"
   string EXAMPLE='bar'

.. note::

   常量名称必须全部为大写

服务
----

服务是请求/响应式通信，其中客户端（请求方）会等待服务端（响应方）做一个简短计算并返回结果。

服务在 ROS 包的 ``srv/`` 目录中的 ``.srv`` 文件中被描述和定义。

服务描述文件由一个请求和一个响应消息类型组成，两者以 ``---`` 分隔。
任意两个按 ``---`` 连接起来的 ``.msg`` 文件都构成合法的服务描述。

下面给出一个非常简单的服务示例：它接受一个字符串并返回一个字符串：

.. code-block:: bash

   string str
   ---
   string str

当然，我们也可以构造更复杂的形式（如果你想引用同一个包中的消息，不能提到包名）：

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

不能在一个服务内部嵌套另一个服务。

动作
----

动作是一种长时间运行的请求/响应通信，其中动作客户端（请求者）等待动作服务器（响应者）执行某些动作并返回结果。
与服务相比，动作可以持续很长时间（几秒到几分钟），在执行过程中提供反馈，并且可以被中断。

动作定义的形式如下：

.. code::

   <request_type> <request_fieldname>
   ---
   <response_type> <response_fieldname>
   ---
   <feedback_type> <feedback_fieldname>

与服务类似，请求字段位于第一个三段横线（``---``）之前，响应字段位于其后。
此外，在第二个三段横线之后还有第三组字段，用于发送反馈时携带的字段。

请求字段、响应字段和反馈字段的数量都可以是任意数量（包括零）。

``<request_type>``、``<response_type>`` 和 ``<feedback_type>`` 与消息中的 ``<type>`` 遵循相同规则。
``<request_fieldname>``、``<response_fieldname>`` 和 ``<feedback_fieldname>`` 与消息中的 ``<fieldname>`` 遵循相同规则。

例如，``Fibonacci`` 动作定义如下：

.. code::

   int32 order
   ---
   int32[] sequence
   ---
   int32[] sequence

这是一个动作定义，其中动作客户端发送一个表示 Fibonacci 步骤数的单个 ``int32`` 字段，并期望动作服务器返回包含完整步骤的 ``int32`` 数组。
在此过程中，动作服务器还可能提供一个中间数组，其中包含在某个时间点之前已经完成的步骤。
