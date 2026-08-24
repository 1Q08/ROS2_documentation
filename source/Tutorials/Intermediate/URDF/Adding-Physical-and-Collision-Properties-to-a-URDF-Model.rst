.. redirect-from::

    Tutorials/URDF/Adding-Physical-and-Collision-Properties-to-a-URDF-Model

.. _URDFProperties:

添加物理属性和碰撞属性
======================

**目标：** 学习如何为 link 添加碰撞和惯性属性，以及如何为 joint 添加关节动力学。

**教程级别：** 中级

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

在本教程中，我们将看看如何为你的 URDF 模型添加一些基本物理属性，以及如何指定它的碰撞属性。

碰撞
----

到目前为止，我们只用单个子元素 ``visual`` 来指定我们的 link，它（毫不意外地）定义了机器人的外观。
然而，为了让碰撞检测能够工作，或者为了模拟机器人，我们还需要定义一个 ``collision`` 元素。
`这是带有碰撞和物理属性的新 urdf <https://raw.githubusercontent.com/ros/urdf_tutorial/ros2/urdf/07-physics.urdf>`_。

这是我们新的 base link 的代码。

.. code-block:: xml

    <link name="base_link">
        <visual>
          <geometry>
            <cylinder length="0.6" radius="0.2"/>
          </geometry>
          <material name="blue">
            <color rgba="0 0 .8 1"/>
          </material>
        </visual>
        <collision>
          <geometry>
            <cylinder length="0.6" radius="0.2"/>
          </geometry>
        </collision>
      </link>

* collision 元素是 link 对象的直接子元素，与 visual 标签处于同一层级。
* collision 元素定义其形状的方式与 visual 元素相同，都是通过一个 geometry 标签。
  这里 geometry 标签的格式与 visual 中的完全相同。
* 你也可以像 visual 那样，将 origin 作为 collision 标签的子元素来指定。

在很多情况下，你会希望碰撞几何体和原点与视觉几何体和原点完全相同。
然而，有两个主要情况你不会这样做：

 * **更快的处理** 对两个网格进行碰撞检测比两个简单几何体的碰撞检测计算复杂度高得多。
   因此，你可能想在 collision 元素中用更简单的几何体替换网格。
 * **安全区域** 你可能想限制靠近敏感设备的运动。
   例如，如果我们不想让任何东西碰到 R2D2 的头，我们可以将碰撞几何体定义为一个包住他头的圆柱体，以防止任何东西太靠近他的头。

物理属性
--------
为了让你的模型能够正确模拟，你需要定义机器人的几个物理属性，即 Gazebo 等物理引擎所需的属性。

惯性
^^^^
每个被模拟的 link 元素都需要一个 inertial 标签。
下面是一个简单的例子。

.. code-block:: xml

  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 .8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
    </inertial>
  </link>

* 这个元素也是 link 对象的子元素。
* 质量以千克为单位定义。
* 3x3 的旋转惯性矩阵用 inertia 元素指定。
  由于它是对称的，因此可以只由 6 个元素来表示，如下所示。

    +---------+---------+---------+
    | **ixx** | **ixy** | **ixz** |
    +---------+---------+---------+
    |   ixy   | **iyy** | **iyz** |
    +---------+---------+---------+
    |   ixz   |   iyz   | **izz** |
    +---------+---------+---------+

* 这些信息可以由 MeshLab 等建模程序提供给你。
  几何体（圆柱体、盒子、球体）的惯性可以用维基百科的 `三维惯性张量列表 <https://en.wikipedia.org/wiki/List_of_moments_of_inertia#List_of_3D_inertia_tensors>`_ 来计算（并在上面的示例中使用）。
* 惯性张量取决于物体的质量及其质量分布。
  一个很好的初步近似是假设质量在物体体积中均匀分布，并根据物体的形状（如上所述）计算惯性张量。
* 如果不确定该填什么，一个 ixx/iyy/izz=1e-3 或更小的矩阵通常对于中等大小的 link 是一个合理的默认值（它对应边长 0.1 米、质量 0.6 kg 的盒子）。
  单位矩阵是特别糟糕的选择，因为它往往太大了。
  （它对应边长 0.1 米、质量 600 kg 的盒子！）
* 你也可以指定一个 origin 标签来指定重心和惯性参考坐标系（相对于 link 的参考坐标系）。
* 当使用实时控制器时，为零（或几乎为零）的惯性元素可能导致机器人模型毫无征兆地崩溃，所有 link 都会以它们的原点与世界原点重合的形式出现。

接触系数
^^^^^^^^
你还可以定义 link 之间相互接触时的行为。
这是通过 collision 标签的一个名为 contact_coefficients 的子元素来完成的。
有三个属性需要指定：

 * mu - `摩擦系数 <https://simple.wikipedia.org/wiki/Coefficient_of_friction>`_
 * kp - `刚度系数 <https://en.wikipedia.org/wiki/Stiffness>`_
 * kd - `阻尼系数 <https://en.wikipedia.org/wiki/Damping_ratio#Damping_ratio_definition>`_

关节动力学
^^^^^^^^^^
关节如何运动由关节的 dynamics 标签定义。
这里有两个属性：

 * ``friction`` - 物理静摩擦力。
   对于移动关节，单位是牛顿。
   对于旋转关节，单位是牛顿米。
 * ``damping`` - 物理阻尼值。
   对于移动关节，单位是牛顿秒/米。
   对于旋转关节，单位是牛顿米秒/弧度。

如果未指定，这些系数默认为零。

其他标签
--------
在纯 URDF 的领域里（即排除 Gazebo 特定标签），还有两个剩余标签可以帮助定义关节：calibration 和 safety controller。
请查看 `规范 <https://wiki.ros.org/urdf/XML/joint>`_，因为它们没有包含在本教程中。

下一步
------
通过 :doc:`使用 xacro <./Using-Xacro-to-Clean-Up-a-URDF-File>` 来减少你需要编写的代码量和令人烦恼的数学计算。
