.. redirect-from::

    Tutorials/URDF/Building-a-Movable-Robot-Model-with-URDF

.. _MoveableURDF:

构建可移动的机器人模型
======================

**目标：** 学习如何在 URDF 中定义可移动关节。

**教程级别：** 中级

**时长：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

在本教程中，我们将在 :doc:`上一个教程 <./Building-a-Visual-Robot-Model-with-URDF-from-Scratch>` 中制作的 R2D2 模型基础上进行修改，让它带有可移动的关节。
在之前的模型中，所有关节都是固定的。
现在我们将探索另外三种重要的关节类型：连续关节（continuous）、旋转关节（revolute）和平移关节（prismatic）。

在继续之前，请确保已经安装所有前提条件。
有关所需内容的信息，请参阅 :doc:`上一个教程 <./Building-a-Visual-Robot-Model-with-URDF-from-Scratch>`。

同样，本教程中提到的所有机器人模型都可以在 `urdf_tutorial <https://index.ros.org/p/urdf_tutorial>`_ 软件包中找到。

`这里是带有柔性关节的新 urdf <https://github.com/ros/urdf_tutorial/blob/ros2/urdf/06-flexible.urdf>`_。
你可以把它与之前的版本进行对比，看看都有哪些改动，不过我们这里只关注三个示例关节。

要可视化并控制这个模型，请运行与上一个教程相同的命令：

.. code-block:: console

  $ ros2 launch urdf_tutorial display.launch.py model:=urdf/06-flexible.urdf

不过现在它还会弹出一个 GUI，让你可以控制所有非固定关节的取值。
稍微摆弄一下这个模型，看看它是如何运动的。
然后，我们再来看看我们是如何实现这一点的。

.. image:: https://raw.githubusercontent.com/ros/urdf_tutorial/ros2/images/flexible.png
  :width: 800
  :alt: 柔性模型截图

头部
----

.. code-block:: xml

  <joint name="head_swivel" type="continuous">
    <parent link="base_link"/>
    <child link="head"/>
    <axis xyz="0 0 1"/>
    <origin xyz="0 0 0.3"/>
  </joint>

机身与头部之间的连接是一个连续关节，这意味着它的角度可以取负无穷到正无穷之间的任意值。
车轮也是按这种方式建模的，因此它们可以不停地朝两个方向滚动。

我们唯一需要额外添加的信息是旋转轴，这里用 xyz 三元组来指定，它给出了头部绕其旋转的向量。
由于我们希望它绕 z 轴旋转，因此将向量指定为 "0 0 1"。

夹爪
----

.. code-block:: xml

  <joint name="left_gripper_joint" type="revolute">
    <axis xyz="0 0 1"/>
    <limit effort="1000.0" lower="0.0" upper="0.548" velocity="0.5"/>
    <origin rpy="0 0 0" xyz="0.2 0.01 0"/>
    <parent link="gripper_pole"/>
    <child link="left_gripper"/>
  </joint>

左右两个夹爪关节都被建模为旋转关节。
这意味着它们的旋转方式与连续关节相同，但有严格的限制。
因此，我们必须包含 limit 标签来指定关节的上限和下限（单位为弧度）。
我们还需要为该关节指定最大速度和力矩，不过实际数值在这里对我们来说并不重要。

夹爪臂
------

.. code-block:: xml

  <joint name="gripper_extension" type="prismatic">
    <parent link="base_link"/>
    <child link="gripper_pole"/>
    <limit effort="1000.0" lower="-0.38" upper="0" velocity="0.5"/>
    <origin rpy="0 0 0" xyz="0.19 0 0.2"/>
  </joint>

夹爪臂是一种不同类型的关节，即平移关节。
这意味着它沿轴向移动，而不是绕轴旋转。
正是这种平移运动让我们的机器人模型能够伸出和收回夹爪臂。

平移臂的限制与旋转关节的指定方式相同，只是单位是米而不是弧度。

其他类型的关节
--------------

还有另外两种可以在空间中运动的关节。
平移关节只能沿一个维度移动，而平面关节（planar）可以在一个平面内、也就是两个维度上移动。
此外，浮动关节（floating）没有约束，可以在三个维度中的任意方向上移动。
这些关节无法只用一个数值来指定，因此本教程不涉及它们。

指定姿态
--------

当你在 GUI 中拖动滑块时，模型会在 Rviz 中移动。
这是如何实现的呢？
首先，`GUI <https://index.ros.org/p/joint_state_publisher_gui>`_ 会解析 URDF，找出所有非固定关节及其限制。
然后，它使用滑块的值来发布 `sensor_msgs/msg/JointState <https://github.com/ros2/common_interfaces/blob/eloquent/sensor_msgs/msg/JointState.msg>`_ 消息。
接着，`robot_state_publisher <https://index.ros.org/p/robot_state_publisher>`_ 会使用这些消息来计算各个部件之间的所有变换。
最后，用得到的变换树在 Rviz 中显示所有形状。

后续步骤
--------

现在你已经有了一个可视化的可用模型，接下来可以 :doc:`添加一些物理属性 <./Adding-Physical-and-Collision-Properties-to-a-URDF-Model>`，或者 :doc:`开始使用 xacro 简化你的代码 <./Using-Xacro-to-Clean-Up-a-URDF-File>`。
