.. redirect-from::

    Tutorials/URDF/Adding-Physical-and-Collision-Properties-to-a-URDF-Model

.. _URDFProperties:

添加物理属性和碰撞属性
======================

**目标：** 学习如何为 link 添加碰撞属性和惯性属性，以及如何为 joint 添加关节动力学。

**教程级别：** 中级

**时长：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

在本教程中，我们将了解如何为 URDF 模型添加一些基本的物理属性，以及如何指定其碰撞属性。

碰撞
----

到目前为止，我们只为 link 指定了单个子元素 ``visual`` ，它定义了（一点也不意外）机器人看起来是什么样子。
然而，为了让碰撞检测正常工作或对机器人进行仿真，我们还需要定义 ``collision`` 元素。
`这里是新的 urdf <https://raw.githubusercontent.com/ros/urdf_tutorial/ros2/urdf/07-physics.urdf>`_，其中包含碰撞属性和物理属性。

下面是我们新的 base link 的代码。

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
* collision 元素定义形状的方式与 visual 元素相同，都使用 geometry 标签。
  此处 geometry 标签的格式与 visual 中完全相同。
* 你也可以像 collision 标签的子元素那样指定 origin（与 visual 一样）。

在很多情况下，你会希望碰撞几何体和原点与视觉几何体和原点完全一致。
不过，有两种主要情况并非如此：

 * **更快的处理速度** 对两个网格进行碰撞检测的计算复杂度远高于对两个简单几何体进行碰撞检测。
   因此，你可能想在 collision 元素中用更简单的几何体替换网格。
 * **安全区域** 你可能希望限制靠近敏感设备的运动。
   例如，如果我们不想让任何东西与 R2D2 的头部发生碰撞，就可以把碰撞几何体定义为一个包裹其头部的圆柱体，以防任何东西过于靠近它的头部。

物理属性
--------
为了让你的模型能正确仿真，你需要定义机器人的若干物理属性，即像 Gazebo 这样的物理引擎所需要的属性。

惯性
^^^^
每个被仿真的 link 元素都需要一个 inertial 标签。
下面是一个简单的示例。

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

* 该元素同样是 link 对象的子元素。
* 质量以千克为单位定义。
* 3x3 旋转惯性矩阵由 inertia 元素指定。
  由于它是对称的，因此可以只用 6 个元素表示，如下所示。

    +---------+---------+---------+
    | **ixx** | **ixy** | **ixz** |
    +---------+---------+---------+
    |   ixy   | **iyy** | **iyz** |
    +---------+---------+---------+
    |   ixz   |   iyz   | **izz** |
    +---------+---------+---------+

* 这些信息可以由 MeshLab 等建模程序提供。
  几何基本体（圆柱体、长方体、球体）的惯性可以使用维基百科的 `转动惯量张量列表 <https://en.wikipedia.org/wiki/List_of_moments_of_inertia#List_of_3D_inertia_tensors>`_ 计算（上面的例子中就用到了它）。
* 惯性张量同时取决于物体的质量和质量分布。
  一个好的初步近似是假设质量在物体体积内均匀分布，并根据物体的形状计算惯性张量，如上所述。
* 如果不确定该填什么，对于中等大小的 link，ixx/iyy/izz=1e-3 或更小的矩阵通常是一个合理的默认值（它对应于边长为 0.1 m、质量为 0.6 kg 的立方体）。
  单位矩阵是特别糟糕的选择，因为它通常太大了。
  （它对应于边长为 0.1 m、质量为 600 kg 的立方体！）
* 你还可以指定 origin 标签来指定重心和惯性参考系（相对于 link 的参考系）。
* 使用实时控制器时，为零（或几乎为零）的 inertia 元素会导致机器人模型在毫无警告的情况下坍塌，并且所有 link 的原点都会与世界原点重合。

接触系数
^^^^^^^^
你还可以定义 link 在彼此接触时的行为。
这通过 collision 标签中名为 contact_coefficients 的子元素来完成。
需要指定三个属性：

 * mu - `摩擦系数 <https://simple.wikipedia.org/wiki/Coefficient_of_friction>`_
 * kp - `刚度系数 <https://en.wikipedia.org/wiki/Stiffness>`_
 * kd - `阻尼系数 <https://en.wikipedia.org/wiki/Damping_ratio#Damping_ratio_definition>`_

关节动力学
^^^^^^^^^^
关节如何运动由该 joint 的 dynamics 标签定义。
这里有两个属性：

 * ``friction`` - 物理静摩擦力。
   对于移动关节，单位是牛顿。
   对于旋转关节，单位是牛顿米。
 * ``damping`` - 物理阻尼值。
   对于移动关节，单位是牛顿秒每米。
   对于旋转关节，单位是牛顿米秒每弧度。

如果未指定，这些系数默认为零。

其他标签
--------
在纯 URDF 的范畴内（即不包括 Gazebo 专用标签），还有两个有助于定义 joint 的标签：calibration 和 safety controller。
请查看 `规范 <https://wiki.ros.org/urdf/XML/joint>`_，因为它们并未包含在本教程中。

后续步骤
--------
通过 :doc:`使用 xacro <./Using-Xacro-to-Clean-Up-a-URDF-File>` 来减少你必须编写的代码量和烦人的数学计算。
