.. redirect-from::

   Guides/Launch-files-migration-guide
   Tutorials/Launch-files-migration-guide
   How-To-Guides/Launch-files-migration-guide

.. _MigratingLaunch:

迁移启动文件
============

.. contents:: 目录
   :depth: 2
   :local:

ROS 1 中的启动文件始终使用 `XML <https://wiki.ros.org/roslaunch/XML>`__ 文件指定，而 ROS 2 同时支持 XML 和 YAML 文件。
ROS 2 还支持 Python 启动脚本，以实现更大的灵活性（参见 `launch 软件包 <https://github.com/ros2/launch/tree/{REPOS_FILE_BRANCH}/launch>`__）。
不过对于典型用例，应优先使用 XML 和 YAML 而不是 Python。

本指南介绍如何编写 ROS 2 XML 启动文件，以便轻松地从 ROS 1 迁移过来。

背景
----

ROS 2 启动系统的说明参见 :doc:`启动系统教程 <../../../Tutorials/Intermediate/Launch/Launch-system>`。


迁移标签
--------

launch
^^^^^^

* `ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/launch>`__.
* ``launch`` 是任何 ROS 2 启动 XML 文件的根元素。

node
^^^^

* `ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/node>`__.
* 启动一个新节点。
* 与 ROS 1 的区别：

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

* `ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/param>`__.
* 用于向节点传递参数。
* ROS 2 中没有全局参数的概念。
  因此，它只能嵌套在 ``node`` 标签中使用。
  ROS 2 不支持某些属性：``type``、``textfile``、``binfile``、``executable``。
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

下面是一些如何编写参数的示例：

.. code-block:: xml

   <node pkg="my_package" exec="my_executable" name="my_node">
      <!--A string parameter with value "1"-->
      <param name="a_string" value="'1'"/>
      <!--A integer parameter with value 1-->
      <param name="an_int" value="1"/>
      <!--A float parameter with value 1.0-->
      <param name="a_float" value="1.0"/>
      <!--A string parameter with value "asd"-->
      <param name="another_string" value="asd"/>
      <!--Another string parameter, with value "asd"-->
      <param name="string_with_same_value_as_above" value="'asd'"/>
      <!--Another string parameter, with value "'asd'"-->
      <param name="quoted_string" value="\'asd\'"/>
      <!--A list of strings, with value ["asd", "bsd", "csd"]-->
      <param name="list_of_strings" value="asd, bsd, csd" value-sep=", "/>
      <!--A list of ints, with value [1, 2, 3]-->
      <param name="list_of_ints" value="1,2,3" value-sep=","/>
      <!--Another list of strings, with value ["1", "2", "3"]-->
      <param name="another_list_of_strings" value="'1';'2';'3'" value-sep=";"/>
      <!--A list of strings using an strange separator, with value ["1", "2", "3"]-->
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

这会创建两个参数：

* 一个值为 ``1`` 的 ``group1.group2.my_param``，由节点 ``/an_absolute_ns/my_node`` 承载。
* 一个值为 ``2`` 的 ``group1.another_param``，由节点 ``/an_absolute_ns/my_node`` 承载。

也可以使用完整参数名：

.. code-block:: xml

   <node pkg="my_package" exec="my_executable" name="my_node" namespace="/an_absoulute_ns">
      <param name="group1.group2.my_param" value="1"/>
      <param name="group1.another_param" value="2"/>
   </node>

rosparam
^^^^^^^^

* `ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/rosparam>`__.
* 从 yaml 文件加载参数。
* 它已被 ``param`` 标签中的 ``from`` 属性取代。

示例
~~~~

.. code-block:: xml

   <node pkg="my_package" exec="my_executable" name="my_node" namespace="/an_absoulute_ns">
      <param from="/path/to/file"/>
   </node>

remap
^^^^^

* `ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/remap>`__.
* 用于向节点传递重映射规则。
* 它只能用在 ``node`` 标签内部。

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

* `ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/include>`__.
* 允许包含另一个启动文件。
* 与 ROS 1 的区别：

   * 在 ROS 1 中，被包含的内容是有作用域的。
     在 ROS 2 中则没有。
     这意味着 ``arg`` 标签的值会被传播到被包含的启动文件中，就如同在 ROS 1 中使用了 ``pass_all_args="true"`` 一样。
     不过，这种传播只对（在内层/被包含的启动文件中）具有默认值的 arg 有效。
     必需的 arg 必须显式传递。
     把 include 嵌套在 ``group`` 标签中以限定其作用域（另见 ``group`` 的 ``scoped`` 和 ``forwarding`` 属性）。
   * 不支持 ``ns`` 属性。
     参见 ``push_ros_namespace`` 标签的示例以了解变通方法。
   * 嵌套在 ``include`` 标签中的 ``arg`` 标签现在是 ``let``。
     不过目前仍然支持 ``arg``。
   * 嵌套在 ``include`` 标签中的 ``let`` 标签不支持条件判断（``if``、``unless``）和 ``description`` 属性。
   * 不支持嵌套的 ``env`` 标签。
     可以改用 ``set_env`` 和 ``unset_env``。
   * ``clear_params`` 和 ``pass_all_args`` 两个属性都不受支持。
     ROS 2 launch 的行为就仿佛把 ``pass_all_args`` 设为 true（见上文）。

示例
~~~~

参见 `替换 include 标签`_。

arg
^^^

* `ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/arg>`__.
* ``arg`` 用于声明启动参数，或者在使用 ``include`` 标签时传递参数。
* 与 ROS 1 的区别：

   * 不允许使用 ``value`` 属性。
     请为此使用 ``let`` 标签。
   * ``doc`` 现在是 ``description``。
   * 当嵌套在 ``include`` 标签中时：

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

向启动文件传递参数
~~~~~~~~~~~~~~~~~~

在上面的 XML 启动文件中，``topic_name`` 默认为名称 ``chatter``，但可以在命令行上配置。
假设上面的启动配置位于名为 ``mylaunch.xml`` 的文件中，则可以通过如下方式启动它来使用不同的话题名称：

.. code-block:: console

   $ ros2 launch mylaunch.xml topic_name:=custom_topic_name

有关传递命令行参数的更多信息，参见 :doc:`使用替换符 <../../../Tutorials/Intermediate/Launch/Using-Substitutions>`。

env
^^^

* `ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/env>`__.
* 设置环境变量。
* 它已被 ``env``、``set_env`` 和 ``unset_env`` 取代：

   * ``env`` 只能嵌套在 ``node`` 或 ``executable`` 标签中使用。
     不支持 ``if`` 和 ``unless`` 标签。
   * ``set_env`` 可以嵌套在根标签 ``launch`` 中或 ``group`` 标签中。
     它接受与 ``env`` 相同的属性，并且还接受 ``if`` 和 ``unless`` 标签。
   * ``unset_env`` 取消设置环境变量。
     它接受 ``name`` 属性和条件判断。

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

* `ROS 1 中可用 <https://wiki.ros.org/roslaunch/XML/group>`__.
* 允许限定启动配置的作用域。
  通常与 ``let``、``include`` 和 ``push_ros_namespace`` 标签一起使用。
* 与 ROS 1 的区别：

   * 没有 ``ns`` 属性。
     可以使用新增的 ``push_ros_namespace`` 标签作为变通方法。
   * ``clear_params`` 属性不可用。
   * 它不接受 ``remap`` 和 ``param`` 作为子标签。
   * 它有两个新属性：``scoped`` 和 ``forwarding`` （默认都为 true）。
     如果 ``scoped`` 为 false，则该 group 不会引入新的变量作用域，因此对组内变量所做的操作也会影响组外的变量。
     如果 ``forwarding`` 为 false，则组内无法使用外部的启动配置（ ``arg`` ）。
     这对于隔离被包含的启动文件、从而避免参数名冲突很有用。

.. _launch-prefix-example:

示例
~~~~

``launch-prefix`` 配置会同时影响 ``executable`` 和 ``node`` 标签的动作。
本例中，如果 ``use_time_prefix_in_talker`` 参数为 ``1``，则仅对 talker 使用 ``time`` 作为前缀。

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

目前尚不支持。

test
^^^^

目前尚不支持。

ROS 2 中的新标签
----------------

set_env and unset_env
^^^^^^^^^^^^^^^^^^^^^

参见 `env`_ 标签说明。

push_ros_namespace
^^^^^^^^^^^^^^^^^^

``include`` 和 ``group`` 标签不接受 ``ns`` 属性。
可以把这个动作作为变通方法使用：

.. code-block:: xml

   <!-Other tags-->
   <group>
      <push_ros_namespace namespace="my_ns"/>
      <!--Nodes here are namespaced with "my_ns".-->
      <!--If there is an include action here, its nodes will also be namespaced.-->
      <push_ros_namespace namespace="another_ns"/>
      <!--Nodes here are namespaced with "another_ns/my_ns".-->
      <push_ros_namespace namespace="/absolute_ns"/>
      <!--Nodes here are namespaced with "/absolute_ns".-->
      <!--The following node receives an absolute namespace, so it will ignore the others previously pushed.-->
      <!--The full path of the node will be /asd/my_node.-->
      <node pkg="my_pkg" exec="my_executable" name="my_node" namespace="/asd"/>
   </group>
   <!--Nodes outside the group action won't be namespaced.-->
   <!-Other tags-->

let
^^^

它用于替代带 value 属性的 ``arg`` 标签。

.. code-block:: xml

   <let name="foo" value="asd"/>

在 ROS 2 中，``let`` 和 ``arg`` 的用途不同：

* ``let`` 设置启动配置的值。
* ``arg`` 声明一个启动参数/配置，并可选地提供默认值。
  该值可以单独从命令行设置，也可以在包含该启动文件时设置。
  如果没有设置值，则在提供了默认值时使用默认值，否则会报告错误。

executable
^^^^^^^^^^

它允许运行任意可执行文件。

示例
~~~~

.. code-block:: xml

   <executable cmd="ls -las" cwd="/var/log" name="my_exec" launch-prefix="something" output="screen" shell="true">
      <env name="LD_LIBRARY" value="/lib/some.so"/>
   </executable>

替换 include 标签
-----------------

为了像 ROS 1 那样在 **命名空间** 下包含启动文件，``include`` 标签必须嵌套在 ``group`` 标签中。

.. code-block:: xml

   <group>
      <include file="another_launch_file"/>
   </group>

然后，不再使用 ``ns`` 属性，而是添加 ``push_ros_namespace`` 动作标签来指定命名空间：

.. code-block:: xml

   <group>
      <push_ros_namespace namespace="my_ns"/>
      <include file="another_launch_file"/>
   </group>

只有在指定命名空间时，才需要把 ``include`` 标签嵌套在 ``group`` 标签下

替换符
------

关于 ROS 1 替换符的文档可以在 `roslaunch XML wiki <https://wiki.ros.org/roslaunch/XML>`__ 中找到。
替换符语法没有变化，即仍然遵循 ``$(substitution-name arg1 arg2 ...)`` 模式。
不过，相对于 ROS 1 有一些变化：

* ``env`` 和 ``optenv`` 标签已被 ``env`` 标签取代。
  如果环境变量不存在，``$(env <NAME>)`` 会失败。
  ``$(env <NAME> '')`` 的作用与 ROS 1 的 ``$(optenv <NAME>)`` 相同。
  ``$(env <NAME> <DEFAULT>)`` 的作用与 ROS 1 的 ``$(env <NAME> <DEFAULT>)`` 或 ``$(optenv <NAME> <DEFAULT>)`` 相同。
* ``find`` 已被 ``find-pkg-share`` 取代（替换为已安装软件包的 share 目录）。
  或者，``find-pkg-prefix`` 会返回已安装软件包的根目录。
* 新增了 ``exec-in-pkg`` 替换符。
  例如：``$(exec-in-pkg <exec_name> <package_name>)``。
* 新增了 ``find-exec`` 替换符。
* ``arg`` 已被 ``var`` 取代。
  它会查找由 ``arg`` 或 ``let`` 标签定义的配置。
* ``eval`` 和 ``dirname`` 替换符要求字符串值使用转义字符，例如 ``if="$(eval '\'$(var variable)\' == \'val1\'')"``。
  你也可以使用 ``&quot;`` 这样的 HTML 转义。
* ``eval`` 不会把配置（ ``arg`` ）作为局部 Python 变量传入。
  必须通过 ``$(var name)`` 访问它们。
* 在 ROS 2 中，``eval`` 的参数必须是带引号的字符串。
  这也是表达式内部的引号必须转义的原因。

类型推断规则
------------

``param`` 标签的 ``类型推断规则`` 小节中展示的规则适用于任何属性。
例如：

.. code-block:: xml

   <!--Setting a string value to an attribute expecting an int will raise an error.-->
   <tag1 attr-expecting-an-int="'1'"/>
   <!--Correct version.-->
   <tag1 attr-expecting-an-int="1"/>
   <!--Setting an integer in an attribute expecting a string will raise an error.-->
   <tag2 attr-expecting-a-str="1"/>
   <!--Correct version.-->
   <tag2 attr-expecting-a-str="'1'"/>
   <!--Setting a list of strings in an attribute expecting a string will raise an error.-->
   <tag3 attr-expecting-a-str="asd, bsd" str-attr-sep=", "/>
   <!--Correct version.-->
   <tag3 attr-expecting-a-str="don't use a separator"/>

有些属性可以接受不止一种类型，例如 ``param`` 标签的 ``value`` 属性。
通常，``int`` （或 ``float``）类型的参数也接受 ``str``，该值稍后会被替换，并由动作尝试转换为 ``int`` （或 ``float``）。
