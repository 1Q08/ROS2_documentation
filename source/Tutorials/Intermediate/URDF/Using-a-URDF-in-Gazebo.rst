在 Gazebo 中使用 URDF
=====================

**目标：** 在 Gazebo 仿真器中仿真你的 URDF

**教程级别：** 中级

**时间：** 30 分钟

.. contents:: 目录
   :depth: 2
   :local:


本教程基于 `这个 ROS 1 教程 <http://wiki.ros.org/urdf/Tutorials/Using%20a%20URDF%20in%20Gazebo>`_。

让我们从安装演示包及其依赖项开始。

.. tabs::

   .. group-tab:: Ubuntu Packages

      .. code-block:: console

         sudo apt install ros-{DISTRO}-urdf-sim-tutorial

   .. group-tab:: RHEL Packages

      .. code-block:: console

         sudo dnf install ros-{DISTRO}-urdf-sim-tutorial

   .. group-tab:: From Source

      .. code-block:: console

         git clone https://github.com/ros/urdf_sim_tutorial.git -b ros2

无法正常工作的 Gazebo 接口
--------------------------
我们可以使用 ``gazebo.launch.py`` 把我们之前已经创建好的模型生成到 Gazebo 中

.. code-block:: console

  ros2 launch urdf_sim_tutorial gazebo.launch.py

这个 launch 文件会

 * 从 :doc:`宏教程 <Using-Xacro-to-Clean-Up-a-URDF-File>` 中加载 urdf，并将其作为话题发布（``/robot_description``）
 * 启动一个空的 Gazebo 世界
 * 运行脚本，从话题中读取 urdf 并将其生成到 Gazebo 中。
 * 默认情况下，还会显示 Gazebo 的图形界面，其外观如下：

.. image:: https://raw.githubusercontent.com/ros/urdf_sim_tutorial/ros2/doc/NonFunctional.png
  :alt: Nonfunctional robot in Gazebo


然而，它什么也不做，并且缺少 ROS 使用这个机器人所需的许多关键信息。
在 :doc:`其他 <Building-a-Visual-Robot-Model-with-URDF-from-Scratch>` :doc:`教程 <Building-a-Movable-Robot-Model-with-URDF>` 中，我们使用 `joint_state_publisher <https://index.ros.org/p/joint_state_publisher/github-ros-joint_state_publisher/>`_ 来指定每个关节的位姿。
然而，在现实世界或 Gazebo 中，机器人本身应当提供该信息。
但在没有指定这些信息的情况下，Gazebo 并不知道要发布该信息。

为了让机器人能够与你以及 ROS 进行交互，我们需要指定两样东西：插件和控制器。

旁注：配置网格
^^^^^^^^^^^^^^

.. image:: https://raw.githubusercontent.com/ros/urdf_sim_tutorial/ros2/doc/NoMesh.png
  :alt: Robot with missing meshes


如果你在家里用你自己的机器人或其他东西跟着做，那么你的模型在 Gazebo 图形界面中可能会缺少网格（也就是说，夹爪的网格不存在）。
这也可能导致 Gazebo 在启动画面出现之后还需要几秒钟才能启动，因为它正在互联网上查找缺失的模型。

这是因为你的 URDF 包需要明确告诉 Gazebo 从哪里加载网格。
为此，我们要修改存放 URDF 网格的软件包的 ``package.xml``，添加一个新的 export。

.. code-block:: xml

    <export>
      <build_type>ament_cmake</build_type>
      <gazebo_ros gazebo_model_path="${prefix}/.."/>
    </export>

``gazebo_model_path`` 属性为什么恰好取这个值，是 `另一个 issue <https://github.com/ros-simulation/gazebo_ros_pkgs/issues/1500>`_ 的问题，但可以这么说，在满足以下假设的情况下，将其设为这个值是可行的：

 * 你的网格文件名在 URDF 中使用 ``package://package_name/possible_folder/filename.ext`` 语法指定。
 * 网格通过 CMake 安装到了正确的 share 文件夹中。

Gazebo 插件
-----------
要让 ROS 2 与 Gazebo 交互，我们必须动态链接到 ROS 库，由它来告诉 Gazebo 该做什么。
理论上，这允许其他机器人操作系统以通用方式与 Gazebo 交互。
实际上，那就是 ROS。

具体来说，Gazebo / ROS 2 之间的交互全部通过链接到 ROS 2 Control 库并使用新的 URDF 标签来实现。

我们在 URDF 中 ``</robot>`` 结束标签之前指定以下内容：

.. code-block:: xml

  <ros2_control name="GazeboSystem" type="system">
    <hardware>
      <plugin>gazebo_ros2_control/GazeboSystem</plugin>
    </hardware>
    <joint name="head_swivel" />
  </ros2_control>

  <gazebo>
    <plugin filename="libgazebo_ros2_control.so" name="gazebo_ros2_control">
      <parameters>$(find urdf_sim_tutorial)/config/09a-minimal.yaml</parameters>
    </plugin>
  </gazebo>

.. note::

 * ``<gazebo>`` 和 ``<plugin>`` 标签的工作方式与它们在 ROS 1 中相同。
 * 为了让最小示例能够工作，我们必须至少指定一个关节，但稍后我们会添加更多。

最小配置文件是：

.. code-block:: yaml

  controller_manager:
    ros__parameters:
      update_rate: 100


你可以在 `09a-minimal.urdf.xacro <https://github.com/ros/urdf_sim_tutorial/blob/ros2/urdf/09a-minimal.urdf.xacro>`_ 中看到它，也可以通过运行以下命令来查看

.. code-block:: console

  ros2 launch urdf_sim_tutorial 09a-minimal.launch.py

这会启动一个带有 ``load_controller`` 服务的 ``/controller_manager`` 节点，但不会为机器人添加任何立刻有用的交互。
为此，我们需要在控制器 yaml 中指定更多信息。

生成控制器
----------
现在我们已经把 ROS 和 Gazebo 链接起来了，接下来需要指定一些我们希望在 Gazebo 内运行的 ROS 代码，我们统称它们为控制器。
现在我们可以看一个基于 `这个 yaml 文件 <https://github.com/ros/urdf_sim_tutorial/blob/ros2/config/joints.yaml>`_ 的更大示例，它指定了我们的第一个控制器。

.. code-block:: yaml

    controller_manager:
      ros__parameters:
        update_rate: 100
        use_sim_time: true

        joint_state_broadcaster:
          type: joint_state_broadcaster/JointStateBroadcaster

这个控制器位于 ``joint_state_broadcaster`` 包中，它直接从 Gazebo 把机器人关节的状态发布到 ROS 中。

在 `09-joints.launch.py <https://github.com/ros/urdf_sim_tutorial/blob/ros2/launch/09-joints.launch.py>`_ 中，我们还通过 ``ExecuteProcess`` 添加了一条 ``ros2_control`` 命令来启动这个特定的控制器。

你可以启动它，但仍然还差一点。

.. code-block:: console

  ros2 launch urdf_sim_tutorial 09-joints.launch.py

这会运行控制器，并且确实会在 ``/joint_states`` 话题上发布，但其中什么都没有。

.. code-block:: yaml

    header:
      stamp:
        sec: 13
        nanosec: 331000000
      frame_id: ''
    name: []
    position: []
    velocity: []
    effort: []

你还想让 Gazebo 做什么‽
嗯，它想要了解关于关节的更多信息。

ROS 2 Control 关节定义
----------------------
对于每一个非固定关节，我们需要在 ``ros2_control`` 标签中添加关于该关节的信息，告诉它支持哪些接口。
让我们从头部关节开始。
把 `URDF <https://github.com/ros/urdf_sim_tutorial/blob/ros2/urdf/10-firsttransmission.urdf.xacro#L241>`_ 中的关节标签修改为以下内容：

.. code-block:: xml

    <joint name="head_swivel">
      <command_interface name="position" />
      <command_interface name="velocity" />
      <state_interface name="position"/>
      <state_interface name="velocity"/>
    </joint>

 * 注意这里的关节名称与标准 URDF ``<joint>`` 标签中的关节名称一致。
 * 目前，让我们先关注 ``state_interface``，我们在其中指定要发布该关节的位置和速度。

你可以用之前的 launch 配置运行这个 URDF。

.. code-block:: console

  ros2 launch urdf_sim_tutorial 09-joints.launch.py urdf_package_path:=urdf/10-firsttransmission.urdf.xacro

现在，头部在 RViz 中显示正常了，因为头部关节已经列在 ``joint_states`` 消息中。

.. code-block:: yaml

    header:
      stamp:
        sec: 4
        nanosec: 707000000
      frame_id: ''
    name:
    - head_swivel
    position:
    - -2.9051283156888985e-08
    velocity:
    - 7.575990694887896e-06
    effort:
    - .nan


我们可以继续为所有非固定关节添加关节定义（我们也会这样做），以便所有关节都能被正确发布。
但是，生活不只是看着机器人。
我们还想要控制它们。
所以，让我们再引入一个控制器。

关节控制
--------
`这里是 <https://github.com/ros/urdf_sim_tutorial/blob/ros2/config/head.yaml>`_ 我们接下来要添加的控制器配置。

.. code-block:: yaml

    controller_manager:
      ros__parameters:
        # ... snip ...

        head_controller:
          type: position_controllers/JointGroupPositionController

    head_controller:
      ros__parameters:
        joints:
          - head_swivel
        interface_name: position


用通俗的话说，这是要添加一个名为 ``head_controller`` 的新 ``JointGroupPositionController``，然后在一个新的参数命名空间中指定包含哪些关节，以及我们发布的是位置。
我们能够这样做，是因为我们在关节标签中指定了 ``<command_interface name="position" />``。

现在我们可以像之前一样，用添加的配置和另一条 ``ros2 control`` 命令来启动它

.. code-block:: console

  ros2 launch urdf_sim_tutorial 10-head.launch.py

现在 Gazebo 订阅了一个新话题，之后你可以在 ROS 中发布一个值来控制头部的位置。

.. code-block:: console

  ros2 topic pub /head_controller/commands std_msgs/msg/Float64MultiArray "data: [-0.707]"

当这条命令发布后，位置会立即变为指定的值。

控制多个关节与模仿
------------------
我们可以用类似的方式修改夹爪关节的 URDF，但在这种情况下，我们会把多个关节关联到一个控制器上。
更新后的 `ROS 参数在这里 <https://github.com/ros/urdf_sim_tutorial/blob/ros2/config/gripper.yaml>`_。
我们还必须 `更新 URDF 以包含三个额外的关节接口 <https://github.com/ros/urdf_sim_tutorial/blob/ros2/urdf/12-gripper.urdf.xacro>`_。

要启动它，

.. code-block:: console

  ros2 launch urdf_sim_tutorial 12-gripper.launch.py

现在我们可以用一个包含三个浮点数的数组来移动夹爪。
张开并伸出：

.. code-block:: console

  ros2 topic pub /gripper_controller/commands std_msgs/msg/Float64MultiArray "data: [0.0, 0.5, 0.5]"

闭合并收回：

.. code-block:: console

  ros2 topic pub /gripper_controller/commands std_msgs/msg/Float64MultiArray "data: [-0.4, 0.0, 0.0]"

这个夹爪在设置上实际上是：我们始终希望左夹爪关节与右夹爪关节具有相同的值。
我们可以通过几个步骤把这一点写进 URDF 和控制器中。

 * 把 ``<mimic joint="left_gripper_joint"/>`` 插入到 ``right_gripper_joint`` 的 URDF 定义中（在 `这里的 xacro <https://github.com/ros/urdf_sim_tutorial/blob/ros2/urdf/12a-mimic-gripper.urdf.xacro>`_ 中做得有点取巧
 * 把 ``<param name="mimic">left_gripper_joint</param>`` 插入到 ``right_gripper_joint`` 的 ``ros2_control`` 关节接口中。
 * 在我们新的 `控制参数 <https://github.com/ros/urdf_sim_tutorial/blob/ros2/config/mimic-gripper.urdf>`_ 中，只为夹爪控制器列出这两个关节，省略 ``right_gripper_joint``。

我们可以用以下命令启动它

.. code-block:: console

  ros2 launch urdf_sim_tutorial 12-gripper.launch.py urdf_package_path:=urdf/12a-mimic-gripper.urdf.xacro

现在我们可以仅用两个值来控制它，例如

.. code-block:: console

  ros2 topic pub /gripper_controller/commands std_msgs/msg/Float64MultiArray "data: [0.0, 0.5]"

机器人的轮子转啊转
------------------
要驱动机器人四处移动，我们首先必须在 `四个轮子各自的 URDF <https://github.com/ros/urdf_sim_tutorial/blob/ros2/urdf/13-diffdrive.urdf.xacro>`_ 的 ``ros2_control`` 标签中指定更多接口，不过现在只需要速度命令接口。

我们可以为每个单独的轮子各自指定控制器，但那有什么意思呢？
相反，我们想要一起控制所有轮子。
为此，我们需要 `更多的 ROS 参数 <https://github.com/ros/urdf_sim_tutorial/blob/ros2/config/diffdrive.yaml>`_ 来使用 ``DiffDriveController``，它订阅标准的 Twist ``cmd_vel`` 消息并相应地移动机器人。

.. code-block:: console

  ros2 launch urdf_sim_tutorial 13-diffdrive.launch.py

除了加载上面的配置之外，这还会打开 ``RobotSteering`` 面板，让你可以驱动 R2D2 机器人四处移动，同时观察它在 Gazebo 中的实际行为以及它在 RViz 中的可视化行为：

.. image:: https://raw.githubusercontent.com/ros/urdf_sim_tutorial/ros2/doc/DrivingInterface.png
  :alt: Gazebo with Driving Interface


恭喜！
现在你已经在用 URDF 仿真机器人了。
