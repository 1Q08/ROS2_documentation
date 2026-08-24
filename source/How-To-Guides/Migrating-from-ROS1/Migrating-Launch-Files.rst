.. redirect-from::

   Guides/Launch-files-migration-guide
   Tutorials/Launch-files-migration-guide
   How-To-Guides/Launch-files-migration-guide

.. _MigratingLaunch:

迁移 Launch 文件
================

.. contents:: 目录
   :depth: 2
   :local:

虽然 ROS 1 中的 launch 文件总是使用 `XML <https://wiki.ros.org/roslaunch/XML>`__ 文件来指定，但 ROS 2 同时支持 XML 和 YAML 文件。
ROS 2 还支持 Python launch 脚本以实现更大的灵活性（参见 `launch 包 <https://github.com/ros2/launch/tree/{REPOS_FILE_BRANCH}/launch>`__）。
不过，对于典型用例，应优先选择 XML 和 YAML 而不是 Python。

本指南介绍如何编写 ROS 2 XML launch 文件，以便从 ROS 1 轻松迁移。

背景
----

ROS 2 launch 系统的描述可以在 :doc:`Launch System 教程 <../../../Tutorials/Intermediate/Launch/Launch-system>` 中找到。


迁移标签
--------

launch
^^^^^^

* `在 ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/launch>`__。
* ``launch`` 是任何 ROS 2 launch XML 文件的根元素。

node
^^^^

* `在 ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/node>`__。
* 启动一个新节点。
* 与 ROS 1 的差异：

   * ``type`` 属性现在是 ``exec``。
   * ``ns`` 属性现在是 ``namespace``。
   * ``required="true"`` 现在是 ``on_exit="shutdown"``。
   * 以下属性不可用：``machine``、``respawn_delay``、``clear_params``。

示例
~~~~

.. code-block:: xml

   <launch>
      <node pkg="demo_nodes_cpp" exec="talker"/>
      <node pkg="demo_nodes_cpp" exec="listener"/>
   </launch>

param
^^^^^

* `在 ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/param>`__。
* 用于向节点传递参数。
* ROS 2 中没有全局参数的概念。
  因此，它只能嵌套在 ``node`` 标签中使用。
  以下属性在 ROS 2 中不受支持：``type``、``textfile``、``binfile``、``executable``。
* ``command`` 属性现在是 ``value="$(command '...' )"``。

示例
~~~~

.. code-block:: xml

   <launch>
      <node pkg="demo_nodes_cpp" exec="parameter_event">
         <param name="foo" value="5"/>
      </node>
   </launch>

类型推断规则
~~~~~~~~~~~~

以下是一些编写参数的示例：

.. code-block:: xml

   <node pkg="my_package" exec="my_executable" name="my_node">
      <!--值为 "1" 的字符串参数-->
      <param name="a_string" value="'1'"/>
      <!--值为 1 的整数参数-->
      <param name="an_int" value="1"/>
      <!--值为 1.0 的浮点参数-->
      <param name="a_float" value="1.0"/>
      <!--值为 "asd" 的字符串参数-->
      <param name="another_string" value="asd"/>
      <!--另一个字符串参数，值为 "asd"-->
      <param name="string_with_same_value_as_above" value="'asd'"/>
      <!--另一个字符串参数，值为 "'asd'"-->
      <param name="quoted_string" value="\'asd\'"/>
      <!--字符串列表，值为 ["asd", "bsd", "csd"]-->
      <param name="list_of_strings" value="asd, bsd, csd" value-sep=", "/>
      <!--整数列表，值为 [1, 2, 3]-->
      <param name="list_of_ints" value="1,2,3" value-sep=","/>
      <!--另一个字符串列表，值为 ["1", "2", "3"]-->
      <param name="another_list_of_strings" value="'1';'2';'3'" value-sep=";"/>
      <!--使用奇怪分隔符的字符串列表，值为 ["1", "2", "3"]-->
      <param name="strange_separator" value="'1'//'2'//'3'" value-sep="//"/>
   </node>

参数分组
~~~~~~~~

在 ROS 2 中，``param`` 标签允许嵌套。
例如：

.. code-block:: xml

   <node pkg="my_package" exec="my_executable" name="my_node" namespace="/an_absoulute_ns">
      <param name="group1">
         <param name="group2">
            <param name="my_param" value="1"/>
         </param>
         <param name="another_param" value="2"/>
      </param>
   </node>

这将创建两个参数：

* 值为 ``1`` 的 ``group1.group2.my_param``，由节点 ``/an_absolute_ns/my_node`` 承载。
* 值为 ``2`` 的 ``group1.another_param``，由节点 ``/an_absolute_ns/my_node`` 承载。

也可以使用完整的参数名称：

.. code-block:: xml

   <node pkg="my_package" exec="my_executable" name="my_node" namespace="/an_absoulute_ns">
      <param name="group1.group2.my_param" value="1"/>
      <param name="group1.another_param" value="2"/>
   </node>

rosparam
^^^^^^^^

* `在 ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/rosparam>`__。
* 从 yaml 文件加载参数。
* 它已被 ``param`` 标签中的 ``from`` 属性所取代。

示例
~~~~

.. code-block:: xml

   <node pkg="my_package" exec="my_executable" name="my_node" namespace="/an_absoulute_ns">
      <param from="/path/to/file"/>
   </node>

remap
^^^^^

* `在 ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/remap>`__。
* 用于向节点传递重映射规则。
* 它只能在 ``node`` 标签内使用。

示例
~~~~

.. code-block:: xml

   <launch>
      <node pkg="demo_nodes_cpp" exec="talker">
         <remap from="chatter" to="my_topic"/>
      </node>
      <node pkg="demo_nodes_cpp" exec="listener">
         <remap from="chatter" to="my_topic"/>
      </node>
   </launch>

include
^^^^^^^

* `在 ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/include>`__。
* 允许包含另一个 launch 文件。
* 与 ROS 1 的差异：

   * 在 ROS 1 中，被包含的内容是有作用域的。
     在 ROS 2 中则不是。
     这意味着 ``arg`` 标签的值会传播到被包含的 launch 文件中，就像在 ROS 1 中使用了 ``pass_all_args="true"`` 一样。
     但是，这种传播只适用于具有默认值的 arg（在内部/被包含的 launch 文件中）。
     必需的 arg 必须显式传递。
     将 include 嵌套在 ``group`` 标签中以限定其作用域（另请参见 ``group`` 属性 ``scoped`` 和 ``forwarding`` ）。
   * 不支持 ``ns`` 属性。
     参见 ``push_ros_namespace`` 标签的示例以获取替代方案。
   * 嵌套在 ``include`` 标签中的 ``arg`` 标签现在为 ``let``。
     不过，目前 ``arg`` 仍然受支持。
   * 嵌套在 ``include`` 标签中的 ``let`` 标签不支持条件（``if``、``unless``）或 ``description`` 属性。
   * 不支持嵌套的 ``env`` 标签。
     可以使用 ``set_env`` 和 ``unset_env`` 代替。
   * ``clear_params`` 和 ``pass_all_args`` 属性均不受支持。
     ROS 2 launch 的行为就像 ``pass_all_args`` 被设置为 true 一样（见上文）。

示例
~~~~

参见 `替换 include 标签`_。

arg
^^^

* `在 ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/arg>`__。
* ``arg`` 用于声明 launch 参数，或者在使用 ``include`` 标签时传递参数。
* 与 ROS 1 的差异：

   * 不允许使用 ``value`` 属性。
     为此请使用 ``let`` 标签。
   * ``doc`` 现在是 ``description``。
   * 当嵌套在 ``include`` 标签内时：

      * 使用 ``let`` 而不是 ``arg``。
      * 不允许使用 ``if``、``unless`` 和 ``description`` 属性。

示例
~~~~

.. code-block:: xml

   <launch>
      <arg name="topic_name" default="chatter"/>
      <node pkg="demo_nodes_cpp" exec="talker">
         <remap from="chatter" to="$(var topic_name)"/>
      </node>
      <node pkg="demo_nodes_cpp" exec="listener">
         <remap from="chatter" to="$(var topic_name)"/>
      </node>
   </launch>

向 launch 文件传递参数
~~~~~~~~~~~~~~~~~~~~~~

在上面的 XML launch 文件中，``topic_name`` 默认为名称 ``chatter``，但可以在命令行上配置。
假设上述 launch 配置位于名为 ``mylaunch.xml`` 的文件中，则可以通过以下命令启动它来使用不同的主题名称：

.. code-block:: console

   $ ros2 launch mylaunch.xml topic_name:=custom_topic_name

在 :doc:`使用替换 <../../../Tutorials/Intermediate/Launch/Using-Substitutions>` 中有一些关于传递命令行参数的附加信息。

env
^^^

* `在 ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/env>`__。
* 设置环境变量。
* 它已被 ``env``、``set_env`` 和 ``unset_env`` 取代：

   * ``env`` 只能嵌套在 ``node`` 或 ``executable`` 标签中使用。
     不支持 ``if`` 和 ``unless`` 标签。
   * ``set_env`` 可以嵌套在根标签 ``launch`` 中或在 ``group`` 标签中。
     它接受与 ``env`` 相同的属性，还支持 ``if`` 和 ``unless`` 标签。
   * ``unset_env`` 取消设置环境变量。
     它接受 ``name`` 属性和条件。

示例
~~~~

.. code-block:: xml

   <launch>
      <set_env name="MY_ENV_VAR" value="MY_VALUE" if="CONDITION_A"/>
      <set_env name="ANOTHER_ENV_VAR" value="ANOTHER_VALUE" unless="CONDITION_B"/>
      <set_env name="SOME_ENV_VAR" value="SOME_VALUE"/>
      <node pkg="MY_PACKAGE" exec="MY_EXECUTABLE" name="MY_NODE">
         <env name="NODE_ENV_VAR" value="SOME_VALUE"/>
      </node>
      <unset_env name="MY_ENV_VAR" if="CONDITION_A"/>
      <node pkg="ANOTHER_PACKAGE" exec="ANOTHER_EXECUTABLE" name="ANOTHER_NODE"/>
      <unset_env name="ANOTHER_ENV_VAR" unless="CONDITION_B"/>
      <unset_env name="SOME_ENV_VAR"/>
   </launch>


group
^^^^^

* `在 ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/group>`__。
* 允许限制 launch 配置的作用域。
  通常与 ``let``、``include`` 和 ``push_ros_namespace`` 标签一起使用。
* 与 ROS 1 的差异：

   * 没有 ``ns`` 属性。
     参见新的 ``push_ros_namespace`` 标签作为替代方案。
   * ``clear_params`` 属性不可用。
   * 它不接受 ``remap`` 或 ``param`` 标签作为子元素。
   * 它有两个新属性：``scoped`` 和 ``forwarding``（默认均为 true）。
     如果 ``scoped`` 为 false，则该组不会引入新的变量作用域，因此组内对变量所做的操作也会影响组外的变量。
     如果 ``forwarding`` 为 false，则组内无法使用外部的 launch 配置（ ``arg`` ）。
     这对于隔离被包含的 launch 文件从而防止参数名冲突非常有用。

.. _launch-prefix-example:

示例
~~~~

``launch-prefix`` 配置会影响 ``executable`` 和 ``node`` 标签的动作。
此示例将在 ``use_time_prefix_in_talker`` 参数为 ``1`` 时，仅对 talker 使用 ``time`` 作为前缀。

.. code-block:: xml

   <launch>
      <arg name="use_time_prefix_in_talker" default="0"/>
      <group>
         <let name="launch-prefix" value="time" if="$(var use_time_prefix_in_talker)"/>
         <node pkg="demo_nodes_cpp" exec="talker"/>
      </group>
      <node pkg="demo_nodes_cpp" exec="listener"/>
   </launch>

machine
^^^^^^^

目前不受支持。

test
^^^^

目前不受支持。

ROS 2 中的新标签
----------------

set_env 和 unset_env
^^^^^^^^^^^^^^^^^^^^

参见 `env`_ 标签描述。

push_ros_namespace
^^^^^^^^^^^^^^^^^^

``include`` 和 ``group`` 标签不接受 ``ns`` 属性。
此动作可以作为替代方案使用：

.. code-block:: xml

   <!-其他标签-->
   <group>
      <push_ros_namespace namespace="my_ns"/>
      <!--这里的节点命名空间为 "my_ns"。-->
      <!--如果这里有 include 动作，它的节点也会被命名空间化。-->
      <push_ros_namespace namespace="another_ns"/>
      <!--这里的节点命名空间为 "another_ns/my_ns"。-->
      <push_ros_namespace namespace="/absolute_ns"/>
      <!--这里的节点命名空间为 "/absolute_ns"。-->
      <!--下面的节点接收绝对命名空间，因此它会忽略之前压入的其他命名空间。-->
      <!--节点的完整路径将是 /asd/my_node。-->
      <node pkg="my_pkg" exec="my_executable" name="my_node" namespace="/asd"/>
   </group>
   <!--group 动作之外的节点不会被命名空间化。-->
   <!-其他标签-->

let
^^^

它是带有 value 属性的 ``arg`` 标签的替代品。

.. code-block:: xml

   <let name="foo" value="asd"/>

在 ROS 2 中，``let`` 和 ``arg`` 有两个不同的用途：

* ``let`` 设置 launch 配置值。
* ``arg`` 声明一个 launch 参数/配置，并可选地提供默认值。
  该值可以单独从 CLI 设置，或在包含给定 launch 文件时设置。
  如果未设置值，则使用提供的默认值（如果有），否则报告错误。

executable
^^^^^^^^^^

它允许运行任何可执行文件。

示例
~~~~

.. code-block:: xml

   <executable cmd="ls -las" cwd="/var/log" name="my_exec" launch-prefix="something" output="screen" shell="true">
      <env name="LD_LIBRARY" value="/lib/some.so"/>
   </executable>

替换 include 标签
-----------------

为了像 ROS 1 中那样在 **命名空间** 下包含 launch 文件，``include`` 标签必须嵌套在 ``group`` 标签中。

.. code-block:: xml

   <group>
      <include file="another_launch_file"/>
   </group>

然后，不要使用 ``ns`` 属性，而是添加 ``push_ros_namespace`` 动作标签来指定命名空间：

.. code-block:: xml

   <group>
      <push_ros_namespace namespace="my_ns"/>
      <include file="another_launch_file"/>
   </group>

只有在指定命名空间时，才需要将 ``include`` 标签嵌套在 ``group`` 标签下。

替换
----

关于 ROS 1 替换的文档可以在 `roslaunch XML wiki <https://wiki.ros.org/roslaunch/XML>`__ 中找到。
替换语法没有改变，即它仍然遵循 ``$(substitution-name arg1 arg2 ...)`` 模式。
但是，相对于 ROS 1 有一些变化：

* ``env`` 和 ``optenv`` 标签已被 ``env`` 标签取代。
  如果环境变量不存在，``$(env <NAME>)`` 将会失败。
  ``$(env <NAME> '')`` 与 ROS 1 的 ``$(optenv <NAME>)`` 相同。
  ``$(env <NAME> <DEFAULT>)`` 与 ROS 1 的 ``$(env <NAME> <DEFAULT>)`` 或 ``$(optenv <NAME> <DEFAULT>)`` 相同。
* ``find`` 已被 ``find-pkg-share`` 取代（替换为已安装包的 share 目录）。
  或者 ``find-pkg-prefix`` 将返回已安装包的根目录。
* 有一个新的 ``exec-in-pkg`` 替换。
  例如：``$(exec-in-pkg <exec_name> <package_name>)``。
* 有一个新的 ``find-exec`` 替换。
* ``arg`` 已被 ``var`` 取代。
  它会查看用 ``arg`` 或 ``let`` 标签定义的配置。
* ``eval`` 和 ``dirname`` 替换要求字符串值使用转义字符，例如 ``if="$(eval '\'$(var variable)\' == \'val1\'')"``。
  你也可以使用 HTML 转义，如 ``&quot;`` 。
* 布尔谓词也可以直接用 ``equals``、``not-equals``、``and``、``or``、``any`` 和 ``all`` 替换来表达。
  例如，``if="$(equals $(var variable) val1)"`` 等价于 ``if="$(eval '\'$(var variable)\' == \'val1\'')"``。
  详情参见 :ref:`布尔替换 <BooleanSubstitutions>`。
* ``eval`` 不会将配置（ ``arg`` ）作为局部 Python 变量传入。
  它们必须通过 ``$(var name)`` 访问。
* 在 ROS 2 中，``eval`` 的参数必须是一个带引号的字符串。
  这也是表达式内部的引号必须被转义的原因。

类型推断规则
------------

``param`` 标签的 ``类型推断规则`` 小节中展示的规则适用于任何属性。
例如：

.. code-block:: xml

   <!--给期望 int 的属性设置字符串值会引发错误。-->
   <tag1 attr-expecting-an-int="'1'"/>
   <!--正确版本。-->
   <tag1 attr-expecting-an-int="1"/>
   <!--给期望字符串的属性设置整数会引发错误。-->
   <tag2 attr-expecting-a-str="1"/>
   <!--正确版本。-->
   <tag2 attr-expecting-a-str="'1'"/>
   <!--给期望字符串的属性设置字符串列表会引发错误。-->
   <tag3 attr-expecting-a-str="asd, bsd" str-attr-sep=", "/>
   <!--正确版本。-->
   <tag3 attr-expecting-a-str="don't use a separator"/>

有些属性接受不止一种类型，例如 ``param`` 标签的 ``value`` 属性。
通常，类型为 ``int``（或 ``float``）的参数也接受 ``str``，该字符串稍后会被替换并尝试由动作转换为 ``int``（或 ``float``）。
