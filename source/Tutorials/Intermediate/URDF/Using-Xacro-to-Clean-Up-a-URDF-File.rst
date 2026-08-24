.. redirect-from::

    Tutorials/URDF/Using-Xacro-to-Clean-Up-a-URDF-File

.. _URDFXacro:

使用 Xacro 清理你的代码
=======================

**目标：** 学习一些技巧，使用 Xacro 减少 URDF 文件中的代码量

**教程级别：** 中级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

到目前为止，如果你在家里用自己的机器人设计按这些步骤来，你可能已经厌倦了为了正确地解析非常简单的机器人描述而做各种各样的数学运算。
幸运的是，你可以使用 `xacro <https://index.ros.org/p/xacro>`_ 包让你的生活更简单。
它做了三件非常有帮助的事。

 * 常量
 * 简单数学
 * 宏

在本教程中，我们看看所有这些捷径，以帮助减少 URDF 文件的整体大小，并使其更易于阅读和维护。

使用 Xacro
----------
顾名思义，`xacro <https://index.ros.org/p/xacro>`_ 是一种用于 XML 的宏语言。
xacro 程序运行所有宏并输出结果。
典型用法看起来像这样：

.. code-block:: console

   $ xacro model.xacro > model.urdf

你也可以在 launch 文件中自动生成 urdf。
这很方便，因为它保持最新且不占用硬盘空间。
但是，生成确实需要时间，所以请注意你的 launch 文件可能需要更长时间才能启动。

要在你的 launch 文件中运行 xacro，你需要将 ``Command`` 替换作为 ``robot_state_publisher`` 的参数。

.. code-block:: python

    path_to_urdf = get_package_share_path('turtlebot3_description') / 'urdf' / 'turtlebot3_burger.urdf'
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': ParameterValue(
                Command(['xacro ', str(path_to_urdf)]), value_type=str
            )
        }]
    )

加载机器人模型的更简单方法是使用 `urdf_launch <https://github.com/ros/urdf_launch>`_ 包来自动加载 xacro/urdf。

.. literalinclude:: launch/urdf_display_launch.py
    :language: python

在 URDF 文件的顶部，你必须指定一个命名空间，文件才能正确解析。
例如，下面是一个有效的 xacro 文件的前两行：

.. code-block:: xml

    <?xml version="1.0"?>
    <robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="firefighter">

常量
----
让我们快速看看 R2D2 中的 base_link。

.. code-block:: xml

  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
      <material name="blue"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </collision>
  </link>

这里的信息有点冗余。
我们把圆柱体的长度和半径指定了两次。
更糟糕的是，如果我们想改变它，需要在两个不同的地方改。

幸运的是，xacro 允许你指定充当常量的属性。
我们可以不写上面的代码，而写这个。

.. code-block:: xml

    <xacro:property name="width" value="0.2" />
    <xacro:property name="bodylen" value="0.6" />
    <link name="base_link">
        <visual>
            <geometry>
                <cylinder radius="${width}" length="${bodylen}"/>
            </geometry>
            <material name="blue"/>
        </visual>
        <collision>
            <geometry>
                <cylinder radius="${width}" length="${bodylen}"/>
            </geometry>
        </collision>
    </link>

* 这两个值在前两行中指定。
  它们几乎可以在任何地方定义（假设是有效的 XML）、在任何层级、在使用之前或之后。
  通常它们放在顶部。
* 我们不用在 geometry 元素中指定实际半径，而是用美元符号和花括号来表示值。
* 这段代码将生成与上面相同的代码。

${} 构造的内容值随后被用来替换 ${}。
这意味着你可以将它与属性中的其他文本组合。

.. code-block:: xml

    <xacro:property name="robotname" value="marvin" />
    <link name="${robotname}s_leg" />

这将生成

.. code-block:: xml

    <link name="marvins_leg" />

然而，${} 中的内容不一定只是一个属性，这就引出了我们的下一个话题...

数学
----
你可以使用四种基本运算（+、-、\*、/）、一元负号和括号，在 ${} 构造中构建任意复杂的表达式。
示例：

.. code-block:: xml

    <cylinder radius="${wheeldiam/2}" length="0.1"/>
    <origin xyz="${reflect*(width+.02)} 0 0.25" />

你还可以使用比基本数学运算更多的东西，比如 ``sin`` 和 ``cos``。

宏
--
这是 xacro 包最大且最有用的组成部分。

简单宏
^^^^^^
让我们看一个简单无用的宏。

.. code-block:: xml

    <xacro:macro name="default_origin">
        <origin xyz="0 0 0" rpy="0 0 0"/>
    </xacro:macro>
    <xacro:default_origin />

（这没用，因为如果不指定 origin，它的值与此相同。）
这段代码将生成以下内容。

.. code-block:: xml

    <origin rpy="0 0 0" xyz="0 0 0"/>

* 名称在技术上不是必需的元素，但你需要指定它才能使用它。
* 每个 ``<xacro:$NAME />`` 实例都会被替换为 ``xacro:macro`` 标签的内容。
* 注意，即使它们不完全相同（两个属性的顺序颠倒了），生成的 XML 是等价的。
* 如果找不到指定名称的 xacro，它不会被展开，也不会生成错误。

参数化宏
^^^^^^^^
你还可以对宏进行参数化，这样它们不会每次生成完全相同的文本。
当与数学功能结合时，这会更强大。

首先，我们看一个 R2D2 中使用的简单宏的例子。

.. code-block:: xml

    <xacro:macro name="default_inertial" params="mass">
        <inertial>
                <mass value="${mass}" />
                <inertia ixx="1e-3" ixy="0.0" ixz="0.0"
                     iyy="1e-3" iyz="0.0"
                     izz="1e-3" />
        </inertial>
    </xacro:macro>

这可以与以下代码一起使用

.. code-block:: xml

    <xacro:default_inertial mass="10"/>

参数的作用和属性一样，你可以在表达式中使用它们

你也可以使用整个块作为参数。

.. code-block:: xml

    <xacro:macro name="blue_shape" params="name *shape">
        <link name="${name}">
            <visual>
                <geometry>
                    <xacro:insert_block name="shape" />
                </geometry>
                <material name="blue"/>
            </visual>
            <collision>
                <geometry>
                    <xacro:insert_block name="shape" />
                </geometry>
            </collision>
        </link>
    </xacro:macro>

    <xacro:blue_shape name="base_link">
        <cylinder radius=".42" length=".01" />
    </xacro:blue_shape>

* 要指定块参数，在参数名前加一个星号。
* 可以使用 insert_block 命令插入块
* 想插入多少次就插入多少次。

实际用法
--------
Xacro 语言在允许你做的事情上相当灵活。
除了上面展示的默认惯性宏之外，这里还有一些 xacro 在 `R2D2 模型 <https://github.com/ros/urdf_tutorial/blob/ros2/urdf/08-macroed.urdf.xacro>`_ 中使用的有用方式。

要查看 xacro 文件生成的模型，运行与之前教程相同的命令：

.. code-block:: console

  $ ros2 launch urdf_tutorial display.launch.py model:=urdf/08-macroed.urdf.xacro

（launch 文件一直都在运行 xacro 命令，但由于没有宏需要展开，所以没有影响）

腿宏
^^^^
通常你想在不同位置创建多个外观相似的对象。
你可以使用宏和一些简单的数学来减少需要编写的代码量，就像我们对 R2 的两条腿所做的那样。

.. code-block:: xml

    <xacro:macro name="leg" params="prefix reflect">
        <link name="${prefix}_leg">
            <visual>
                <geometry>
                    <box size="${leglen} 0.1 0.2"/>
                </geometry>
                <origin xyz="0 0 -${leglen/2}" rpy="0 ${pi/2} 0"/>
                <material name="white"/>
            </visual>
            <collision>
                <geometry>
                    <box size="${leglen} 0.1 0.2"/>
                </geometry>
                <origin xyz="0 0 -${leglen/2}" rpy="0 ${pi/2} 0"/>
            </collision>
            <xacro:default_inertial mass="10"/>
        </link>

        <joint name="base_to_${prefix}_leg" type="fixed">
            <parent link="base_link"/>
            <child link="${prefix}_leg"/>
            <origin xyz="0 ${reflect*(width+.02)} 0.25" />
        </joint>
        <!-- A bunch of stuff cut -->
    </xacro:macro>
    <xacro:leg prefix="right" reflect="1" />
    <xacro:leg prefix="left" reflect="-1" />

* 常见技巧 1：使用名称前缀来获得两个名称相似的对象。
* 常见技巧 2：使用数学来计算关节原点。
  在你改变机器人尺寸的情况下，更改一个属性并用一些数学来计算关节偏移会省去很多麻烦。
* 常见技巧 3：使用 reflect 参数，并将其设置为 1 或 -1。
  看看我们如何在 base_to_${prefix}_leg origin 中使用 reflect 参数将腿放在身体的两侧。
