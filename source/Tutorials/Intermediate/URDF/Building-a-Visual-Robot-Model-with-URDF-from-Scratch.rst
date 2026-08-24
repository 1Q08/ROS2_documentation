.. redirect-from::

    Tutorials/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch

.. _BuildingURDF:

从零开始构建一个视觉机器人模型
==============================

**目标：** 学习如何构建一个可以在 Rviz 中查看的机器人视觉模型

**教程级别：** 中级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

.. note:: 本教程假设你知道如何编写格式良好的 XML 代码

在本教程中，我们将构建一个看起来隐约像 R2D2 的机器人视觉模型。
在后面的教程中，你将学习如何 :doc:`连接模型 <./Building-a-Movable-Robot-Model-with-URDF>`、:doc:`添加一些物理属性 <./Adding-Physical-and-Collision-Properties-to-a-URDF-Model>`，以及 :doc:`用 xacro 生成更简洁的代码 <./Using-Xacro-to-Clean-Up-a-URDF-File>`，但现在我们先专注于让视觉几何体正确。

继续之前，请确保你已安装 `joint_state_publisher <https://index.ros.org/p/joint_state_publisher>`_ 包。
如果你安装了 `urdf_tutorial <https://index.ros.org/p/urdf_tutorial>`_ 二进制文件，这应该已经满足。
如果没有，请更新你的安装以包含该包（用 ``rosdep`` 检查）。

本教程中提到的所有机器人模型（以及源文件）都可以在 `urdf_tutorial <https://index.ros.org/p/urdf_tutorial>`_ 包中找到。

一个形状
--------

首先，我们只探索一个简单的形状。
下面是一个你能做到的最简单的 urdf。
`[源：01-myfirst.urdf] <https://github.com/ros/urdf_tutorial/blob/ros2/urdf/01-myfirst.urdf>`_

.. code-block:: xml

    <?xml version="1.0"?>
    <robot name="myfirst">
      <link name="base_link">
        <visual>
          <geometry>
            <cylinder length="0.6" radius="0.2"/>
          </geometry>
        </visual>
      </link>
    </robot>

把 XML 翻译成通俗的话，这是一个名为 ``myfirst`` 的机器人，它只包含一个 link（即部件），其视觉组件只是一个长 0.6 米、半径 0.2 米的圆柱体。
对于一个简单的 "hello world" 类型示例来说，这可能看起来有很多包裹标签。

要查看模型，启动 ``display.launch.py`` 文件：

.. code-block:: console

  $ ros2 launch urdf_tutorial display.launch.py model:=urdf/01-myfirst.urdf

这做了三件事：

 * 加载指定模型，并将其作为 ``robot_state_publisher`` 节点的参数保存。
 * 运行节点来发布 `sensor_msgs/msg/JointState <https://github.com/ros2/common_interfaces/blob/{DISTRO}/sensor_msgs/msg/JointState.msg>`_ 和变换（稍后再详细介绍）
 * 使用配置文件启动 Rviz

启动 ``display.launch.py`` 后，你应该会看到 RViz 显示如下内容：

.. image:: https://raw.githubusercontent.com/ros/urdf_tutorial/ros2/images/myfirst.png
  :width: 800
  :alt: my first image

需要注意的事项：
 * 固定坐标系是网格中心所在的变换坐标系。
   这里，它是由我们的一个 link ``base_link`` 定义的坐标系。
 * 视觉元素（圆柱体）的默认原点在其几何体的中心。
   因此，圆柱体有一半位于网格之下。

多个形状
--------

现在让我们看看如何添加多个形状/link。
如果我们只是向 urdf 添加更多 link 元素，解析器不知道把它们放在哪里。
因此，我们必须添加关节。
关节元素可以同时指柔性关节和非柔性关节。
我们将从非柔性的、即固定关节开始。
`[源：02-multipleshapes.urdf] <https://github.com/ros/urdf_tutorial/blob/ros2/urdf/02-multipleshapes.urdf>`_

.. code-block:: xml

    <?xml version="1.0"?>
    <robot name="multipleshapes">
      <link name="base_link">
        <visual>
          <geometry>
            <cylinder length="0.6" radius="0.2"/>
          </geometry>
        </visual>
      </link>

      <link name="right_leg">
        <visual>
          <geometry>
            <box size="0.6 0.1 0.2"/>
          </geometry>
        </visual>
      </link>

      <joint name="base_to_right_leg" type="fixed">
        <parent link="base_link"/>
        <child link="right_leg"/>
      </joint>

    </robot>

* 注意我们是如何定义一个 0.6m x 0.1m x 0.2m 的盒子的
* 关节是用一个父节点和一个子节点来定义的。
  URDF 最终是一个只有一个根 link 的树状结构。
  这意味着腿的位置取决于 base_link 的位置。

.. code-block:: console

  $ ros2 launch urdf_tutorial display.launch.py model:=urdf/02-multipleshapes.urdf

.. image:: https://raw.githubusercontent.com/ros/urdf_tutorial/ros2/images/multipleshapes.png
  :width: 800
  :alt: Multiple Shapes

两个形状相互重叠，因为它们共享同一个原点。
如果我们不想让它们重叠，就必须定义更多的原点。

原点
----

R2D2 的腿连接到他躯干上半部分的侧面。
所以那就是我们指定 JOINT 原点的地方。
而且，它不是连接到腿的中间，而是连接到上部，所以我们也必须为腿偏移原点。
我们还要旋转腿，使它直立。
`[源：03-origins.urdf] <https://github.com/ros/urdf_tutorial/blob/ros2/urdf/03-origins.urdf>`_

.. code-block:: xml

    <?xml version="1.0"?>
    <robot name="origins">
      <link name="base_link">
        <visual>
          <geometry>
            <cylinder length="0.6" radius="0.2"/>
          </geometry>
        </visual>
      </link>

      <link name="right_leg">
        <visual>
          <geometry>
            <box size="0.6 0.1 0.2"/>
          </geometry>
          <origin rpy="0 1.57075 0" xyz="0 0 -0.3"/>
        </visual>
      </link>

      <joint name="base_to_right_leg" type="fixed">
        <parent link="base_link"/>
        <child link="right_leg"/>
        <origin xyz="0 -0.22 0.25"/>
      </joint>

    </robot>

* 让我们先看关节的原点。
  它是相对于父节点的参考坐标系定义的。
  所以我们在 y 方向偏移 -0.22 米（在我们的左边，但相对于轴来说是右边），在 z 方向偏移 0.25 米（向上）。
  这意味着子 link 的原点将位于上方和右侧，而不管子 link 的视觉原点标签如何。
  由于我们没有指定 rpy（roll pitch yaw）属性，子坐标系默认将与父坐标系具有相同的方向。
* 现在，看腿的视觉原点，它同时有 xyz 和 rpy 偏移。
  这定义了视觉元素中心相对于其原点的位置。
  由于我们想让腿在顶部连接，我们通过将 z 偏移设为 -0.3 米来把原点向下偏移。
  而且由于我们想让腿的长边平行于 z 轴，我们将视觉部分绕 Y 轴旋转 PI/2。

.. code-block:: console

  $ ros2 launch urdf_tutorial display.launch.py model:=urdf/03-origins.urdf

.. image:: https://raw.githubusercontent.com/ros/urdf_tutorial/ros2/images/origins.png
  :width: 800
  :alt: Origins Screenshot

* 启动文件运行一些包，它们会根据你的 URDF 为模型中的每个 link 创建 TF 坐标系。
  Rviz 使用这些信息来确定在哪里显示每个形状。
* 如果某个 URDF link 不存在 TF 坐标系，那么它将被以白色放置在原点处
  （`相关问题 <http://answers.ros.org/question/207947/how-do-you-use-externally-defined-materials-in-a-urdfxacro-file/>`_）。

材料女孩
--------

"好吧，"我听到你说。
"那很可爱，但不是每个人都拥有一台 B21。
我的机器人和 R2D2 不是红色的！"
这是个好观点。
让我们看看 material 标签。
`[源：04-materials.urdf] <https://github.com/ros/urdf_tutorial/blob/ros2/urdf/04-materials.urdf>`_

.. code-block:: xml

    <?xml version="1.0"?>
    <robot name="materials">

      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>

      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>

      <link name="base_link">
        <visual>
          <geometry>
            <cylinder length="0.6" radius="0.2"/>
          </geometry>
          <material name="blue"/>
        </visual>
      </link>

      <link name="right_leg">
        <visual>
          <geometry>
            <box size="0.6 0.1 0.2"/>
          </geometry>
          <origin rpy="0 1.57075 0" xyz="0 0 -0.3"/>
          <material name="white"/>
        </visual>
      </link>

      <joint name="base_to_right_leg" type="fixed">
        <parent link="base_link"/>
        <child link="right_leg"/>
        <origin xyz="0 -0.22 0.25"/>
      </joint>

      <link name="left_leg">
        <visual>
          <geometry>
            <box size="0.6 0.1 0.2"/>
          </geometry>
          <origin rpy="0 1.57075 0" xyz="0 0 -0.3"/>
          <material name="white"/>
        </visual>
      </link>

      <joint name="base_to_left_leg" type="fixed">
        <parent link="base_link"/>
        <child link="left_leg"/>
        <origin xyz="0 0.22 0.25"/>
      </joint>

    </robot>

* 身体现在是蓝色的。
  我们定义了一个名为 "blue" 的新材料，其中红、绿、蓝和 alpha 通道分别定义为 0、0、0.8 和 1。
  所有值都可以在 [0,1] 范围内。
  然后这个材料被 base_link 的视觉元素引用。
  白色材料也是类似定义的。
* 你也可以在视觉元素内部定义 material 标签，甚至在其他 link 中引用它。
  不过，即使你重新定义它，也没有人会抱怨。
* 你还可以使用纹理来指定一个用于给对象着色的图像文件

.. code-block:: console

  $ ros2 launch urdf_tutorial display.launch.py model:=urdf/04-materials.urdf

.. image:: https://raw.githubusercontent.com/ros/urdf_tutorial/ros2/images/materials.png
  :width: 800
  :alt: Materials Screenshot

完成模型
--------

现在我们用几个更多的形状来完成模型：脚、轮子和头。
最值得注意的是，我们添加了一个球体和一些网格。
我们还会添加一些以后会用到的其他部件。
`[源：05-visual.urdf] <https://github.com/ros/urdf_tutorial/blob/ros2/urdf/05-visual.urdf>`_

.. code-block:: xml

    <?xml version="1.0"?>
    <robot name="visual">

      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>

      <link name="base_link">
        <visual>
          <geometry>
            <cylinder length="0.6" radius="0.2"/>
          </geometry>
          <material name="blue"/>
        </visual>
      </link>

      <link name="right_leg">
        <visual>
          <geometry>
            <box size="0.6 0.1 0.2"/>
          </geometry>
          <origin rpy="0 1.57075 0" xyz="0 0 -0.3"/>
          <material name="white"/>
        </visual>
      </link>

      <joint name="base_to_right_leg" type="fixed">
        <parent link="base_link"/>
        <child link="right_leg"/>
        <origin xyz="0 -0.22 0.25"/>
      </joint>

      <link name="right_base">
        <visual>
          <geometry>
            <box size="0.4 0.1 0.1"/>
          </geometry>
          <material name="white"/>
        </visual>
      </link>

      <joint name="right_base_joint" type="fixed">
        <parent link="right_leg"/>
        <child link="right_base"/>
        <origin xyz="0 0 -0.6"/>
      </joint>

      <link name="right_front_wheel">
        <visual>
          <origin rpy="1.57075 0 0" xyz="0 0 0"/>
          <geometry>
            <cylinder length="0.1" radius="0.035"/>
          </geometry>
          <material name="black"/>
        </visual>
      </link>
      <joint name="right_front_wheel_joint" type="fixed">
        <parent link="right_base"/>
        <child link="right_front_wheel"/>
        <origin rpy="0 0 0" xyz="0.133333333333 0 -0.085"/>
      </joint>

      <link name="right_back_wheel">
        <visual>
          <origin rpy="1.57075 0 0" xyz="0 0 0"/>
          <geometry>
            <cylinder length="0.1" radius="0.035"/>
          </geometry>
          <material name="black"/>
        </visual>
      </link>
      <joint name="right_back_wheel_joint" type="fixed">
        <parent link="right_base"/>
        <child link="right_back_wheel"/>
        <origin rpy="0 0 0" xyz="-0.133333333333 0 -0.085"/>
      </joint>

      <link name="left_leg">
        <visual>
          <geometry>
            <box size="0.6 0.1 0.2"/>
          </geometry>
          <origin rpy="0 1.57075 0" xyz="0 0 -0.3"/>
          <material name="white"/>
        </visual>
      </link>

      <joint name="base_to_left_leg" type="fixed">
        <parent link="base_link"/>
        <child link="left_leg"/>
        <origin xyz="0 0.22 0.25"/>
      </joint>

      <link name="left_base">
        <visual>
          <geometry>
            <box size="0.4 0.1 0.1"/>
          </geometry>
          <material name="white"/>
        </visual>
      </link>

      <joint name="left_base_joint" type="fixed">
        <parent link="left_leg"/>
        <child link="left_base"/>
        <origin xyz="0 0 -0.6"/>
      </joint>

      <link name="left_front_wheel">
        <visual>
          <origin rpy="1.57075 0 0" xyz="0 0 0"/>
          <geometry>
            <cylinder length="0.1" radius="0.035"/>
          </geometry>
          <material name="black"/>
        </visual>
      </link>
      <joint name="left_front_wheel_joint" type="fixed">
        <parent link="left_base"/>
        <child link="left_front_wheel"/>
        <origin rpy="0 0 0" xyz="0.133333333333 0 -0.085"/>
      </joint>

      <link name="left_back_wheel">
        <visual>
          <origin rpy="1.57075 0 0" xyz="0 0 0"/>
          <geometry>
            <cylinder length="0.1" radius="0.035"/>
          </geometry>
          <material name="black"/>
        </visual>
      </link>
      <joint name="left_back_wheel_joint" type="fixed">
        <parent link="left_base"/>
        <child link="left_back_wheel"/>
        <origin rpy="0 0 0" xyz="-0.133333333333 0 -0.085"/>
      </joint>

      <joint name="gripper_extension" type="fixed">
        <parent link="base_link"/>
        <child link="gripper_pole"/>
        <origin rpy="0 0 0" xyz="0.19 0 0.2"/>
      </joint>

      <link name="gripper_pole">
        <visual>
          <geometry>
            <cylinder length="0.2" radius="0.01"/>
          </geometry>
          <origin rpy="0 1.57075 0 " xyz="0.1 0 0"/>
        </visual>
      </link>

      <joint name="left_gripper_joint" type="fixed">
        <origin rpy="0 0 0" xyz="0.2 0.01 0"/>
        <parent link="gripper_pole"/>
        <child link="left_gripper"/>
      </joint>

      <link name="left_gripper">
        <visual>
          <origin rpy="0.0 0 0" xyz="0 0 0"/>
          <geometry>
            <mesh filename="package://urdf_tutorial/meshes/l_finger.dae"/>
          </geometry>
        </visual>
      </link>

      <joint name="left_tip_joint" type="fixed">
        <parent link="left_gripper"/>
        <child link="left_tip"/>
      </joint>

      <link name="left_tip">
        <visual>
          <origin rpy="0.0 0 0" xyz="0.09137 0.00495 0"/>
          <geometry>
            <mesh filename="package://urdf_tutorial/meshes/l_finger_tip.dae"/>
          </geometry>
        </visual>
      </link>
      <joint name="right_gripper_joint" type="fixed">
        <origin rpy="0 0 0" xyz="0.2 -0.01 0"/>
        <parent link="gripper_pole"/>
        <child link="right_gripper"/>
      </joint>

      <link name="right_gripper">
        <visual>
          <origin rpy="-3.1415 0 0" xyz="0 0 0"/>
          <geometry>
            <mesh filename="package://urdf_tutorial/meshes/l_finger.dae"/>
          </geometry>
        </visual>
      </link>

      <joint name="right_tip_joint" type="fixed">
        <parent link="right_gripper"/>
        <child link="right_tip"/>
      </joint>

      <link name="right_tip">
        <visual>
          <origin rpy="-3.1415 0 0" xyz="0.09137 0.00495 0"/>
          <geometry>
            <mesh filename="package://urdf_tutorial/meshes/l_finger_tip.dae"/>
          </geometry>
        </visual>
      </link>

      <link name="head">
        <visual>
          <geometry>
            <sphere radius="0.2"/>
          </geometry>
          <material name="white"/>
        </visual>
      </link>
      <joint name="head_swivel" type="fixed">
        <parent link="base_link"/>
        <child link="head"/>
        <origin xyz="0 0 0.3"/>
      </joint>

      <link name="box">
        <visual>
          <geometry>
            <box size="0.08 0.08 0.08"/>
          </geometry>
          <material name="blue"/>
        </visual>
      </link>

      <joint name="tobox" type="fixed">
        <parent link="head"/>
        <child link="box"/>
        <origin xyz="0.1814 0 0.1414"/>
      </joint>
    </robot>

.. code-block:: console

  $ ros2 launch urdf_tutorial display.launch.py model:=urdf/05-visual.urdf

.. image:: https://raw.githubusercontent.com/ros/urdf_tutorial/ros2/images/visual.png
  :width: 800
  :alt: Visual Screenshot

如何添加球体应该相当不言自明：

.. code-block:: xml

  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.2"/>
      </geometry>
      <material name="white"/>
    </visual>
  </link>

这里的网格是从 PR2 借来的。
它们是单独的文件，你必须指定路径。
你应该使用 ``package://NAME_OF_PACKAGE/path`` 表示法。
本教程的网格位于 ``urdf_tutorial`` 包中一个名为 meshes 的文件夹里。

.. code-block:: xml

  <link name="left_gripper">
    <visual>
      <origin rpy="0.0 0 0" xyz="0 0 0"/>
      <geometry>
        <mesh filename="package://urdf_tutorial/meshes/l_finger.dae"/>
      </geometry>
    </visual>
  </link>

* 网格可以以多种不同的格式导入。
  STL 相当常见，但引擎也支持 DAE，它可以有自己的颜色数据，这意味着你不必指定颜色/材料。
  这些通常位于单独的文件中。
  这些网格引用了同样位于 meshes 文件夹中的 ``.tif`` 文件。
* 网格也可以使用相对缩放参数或包围盒尺寸来调整大小。
* 我们也可以引用完全不同包中的网格。

就是这样。
一个类似 R2D2 的 URDF 模型。
现在你可以继续下一步，:doc:`让它动起来 <./Building-a-Movable-Robot-Model-with-URDF>`。
