.. redirect-from::

    Tutorials/URDF/Building-a-Movable-Robot-Model-with-URDF

.. _MoveableURDF:

构建一个可移动的机器人模型
==========================

**目标：** 学习如何在 URDF 中定义可移动的关节。

**教程级别：** 中级

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

在本教程中，我们将修改我们在 :doc:`上一个教程 <./Building-a-Visual-Robot-Model-with-URDF-from-Scratch>` 中制作的 R2D2 模型，使它具有可移动的关节。
在上一个模型中，所有关节都是固定的。
现在我们将探索另外三种重要的关节类型：连续（continuous）、旋转（revolute）和移动（prismatic）。

继续之前，请确保你已安装所有先决条件。
请参阅 :doc:`上一个教程 <./Building-a-Visual-Robot-Model-with-URDF-from-Scratch>` 了解需要什么。

同样，本教程中提到的所有机器人模型都可以在 `urdf_tutorial <https://index.ros.org/p/urdf_tutorial>`_ 包中找到。

`这是带有柔性关节的新 urdf <https://github.com/ros/urdf_tutorial/blob/ros2/urdf/06-flexible.urdf>`_。
你可以将它与上一个版本进行比较，看看所有变化，但我们只专注于三个示例关节。

要可视化并控制这个模型，运行与上一个教程相同的命令：

.. code-block:: console

  $ ros2 launch urdf_tutorial display.launch.py model:=urdf/06-flexible.urdf

不过现在这还会弹出一个 GUI，让你控制所有非固定关节的值。
多玩玩这个模型，看看它是如何移动的。
然后，我们可以看看我们是如何实现这一点的。

.. image:: https://raw.githubusercontent.com/ros/urdf_tutorial/ros2/images/flexible.png
  :width: 800
  :alt: Screenshot of Flexible Model

头部
----

.. code-block:: xml

  <joint name="head_swivel" type="continuous">
    <parent link="base_link"/>
    <child link="head"/>
    <axis xyz="0 0 1"/>
    <origin xyz="0 0 0.3"/>
  </joint>

身体和头部之间的连接是一个连续关节，意味着它可以取从负无穷到正无穷的任意角度。
轮子也是这样建模的，这样它们就可以永远双向滚动。

我们唯一需要添加的额外信息是旋转轴，这里由一个 xyz 三元组指定，它指定了头部绕其旋转的向量。
由于我们想让它绕 z 轴旋转，我们指定向量 "0 0 1"。

夹持器
------

.. code-block:: xml

  <joint name="left_gripper_joint" type="revolute">
    <axis xyz="0 0 1"/>
    <limit effort="1000.0" lower="0.0" upper="0.548" velocity="0.5"/>
    <origin rpy="0 0 0" xyz="0.2 0.01 0"/>
    <parent link="gripper_pole"/>
    <child link="left_gripper"/>
  </joint>

右夹持器和左夹持器关节都建模为旋转关节。
这意味着它们像连续关节一样旋转，但它们有严格的限制。
因此，我们必须包含 limit 标签，指定关节的上限和下限（以弧度为单位）。
我们还必须为这个关节指定最大速度和力矩，但实际值对我们的目的来说并不重要。

夹持器臂
--------

.. code-block:: xml

  <joint name="gripper_extension" type="prismatic">
    <parent link="base_link"/>
    <child link="gripper_pole"/>
    <limit effort="1000.0" lower="-0.38" upper="0" velocity="0.5"/>
    <origin rpy="0 0 0" xyz="0.19 0 0.2"/>
  </joint>

夹持器臂是另一种关节，即移动关节。
这意味着它沿轴移动，而不是绕轴移动。
这种平移运动使我们的机器人模型能够伸出和缩回夹持器臂。

移动臂的限制的指定方式与旋转关节相同，只是单位是米而不是弧度。

其他类型的关节
--------------

还有两种在空间中移动的关节。
移动关节只能沿一个维度移动，而平面（planar）关节可以在一个平面内移动，即两个维度。
此外，浮动（floating）关节是无约束的，可以在三个维度中的任意方向移动。
这些关节无法只用单个数字指定，因此不包含在本教程中。

指定位姿
--------

当你在 GUI 中移动滑块时，模型会在 Rviz 中移动。
这是如何做到的？
首先，`GUI <https://index.ros.org/p/joint_state_publisher_gui>`_ 解析 URDF，找出所有非固定关节及其限制。
然后，它用滑块的值发布 `sensor_msgs/msg/JointState <https://github.com/ros2/common_interfaces/blob/eloquent/sensor_msgs/msg/JointState.msg>`_ 消息。
然后这些消息被 `robot_state_publisher <https://index.ros.org/p/robot_state_publisher>`_ 用来计算不同部件之间的所有变换。
得到的变换树随后被用来在 Rviz 中显示所有形状。

下一步
------

现在你有了一个视觉上可用的模型，你可以 :doc:`添加一些物理属性 <./Adding-Physical-and-Collision-Properties-to-a-URDF-Model>`，或者 :doc:`开始使用 xacro 来简化你的代码 <./Using-Xacro-to-Clean-Up-a-URDF-File>`。
