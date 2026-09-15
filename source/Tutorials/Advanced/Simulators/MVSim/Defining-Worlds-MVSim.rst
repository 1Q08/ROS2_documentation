定义世界、机器人和传感器
========================

**目标：** 学习定义 MVSim 世界文件、添加车辆和传感器的基础知识，以及主要可用功能。

**教程级别：** 高级

**用时：** 30 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

MVSim 世界在 XML 文件（``.world.xml``）中定义。
世界文件描述了环境（地面、墙壁、障碍物）、车辆（动力学模型、形状、传感器）
以及仿真参数（物理时间步长、GUI 选项）。

MVSim 提供了一个预定义车辆和传感器定义的库，你可以通过 XML include 在自己的世界中复用。
你也可以从头开始定义所有内容，以获得完全的控制。

前置条件
--------

你应该已完成 :doc:`Getting-Started-MVSim` 教程并安装了 MVSim。

任务
----

1 最小世界文件
^^^^^^^^^^^^^^

这是一个最小世界文件，创建一个带有一个机器人的空环境：

.. code-block:: xml

    <mvsim_world version="1.0">
      <!-- Simulation settings -->
      <simul_timestep>5e-3</simul_timestep>

      <!-- GUI options -->
      <gui>
          <cam_distance>15</cam_distance>
      </gui>

      <!-- Ground plane -->
      <element class="ground_grid">
      </element>

      <!-- A differential-drive robot -->
      <vehicle name="robot1">
        <init_pose>0 0 0</init_pose>  <!-- x y yaw(deg) -->

        <!--  Dynamical model -->
        <dynamics class="differential">
            <!-- Params -->
            <l_wheel pos="0.0  0.5" mass="4.0" width="0.20" diameter="0.40" />
            <r_wheel pos="0.0 -0.5" mass="4.0" width="0.20" diameter="0.40" />

            <!-- Visual and physical shape -->
            <chassis mass="15.0" zmin="0.05" zmax="0.6">
            </chassis>

            <!--   Motor controller -->
            <controller class="twist_pid">
                <!-- Params -->
                <KP>4.1543</KP>
                <KI>1.9118</KI>
                <KD>0.0000</KD>
                <max_torque>14.44</max_torque>
                <V>0.0</V><W>0</W>
            </controller>
        </dynamics>

        <!-- Motor controller: accept twist commands, PID controller -->
        <controller class="twist_pid">
          <KP>100</KP> <KI>5</KI> <max_torque>50</max_torque>
        </controller>
      </vehicle>
    </mvsim_world>

将其保存为 ``my_world.world.xml`` 并启动它：

.. code-block:: console

    $ mvsim launch my_world.world.xml

2 使用预定义车辆和传感器
^^^^^^^^^^^^^^^^^^^^^^^^

不必从头定义车辆，你可以使用 MVSim 自带的预定义定义。
这些是 MVSim 包 ``definitions/`` 目录中的 XML 文件。

**可用车辆：**

- ``turtlebot3_burger.vehicle.xml`` -- TurtleBot3 Burger（差速驱动）
- ``jackal.vehicle.xml`` -- Clearpath Jackal UGV（4 轮差速）
- ``ackermann.vehicle.xml`` -- 通用阿克曼（类汽车）车辆
- ``pickup.vehicle.xml`` -- 皮卡（阿克曼）
- ``agricobiot2.vehicle.xml`` -- 农业机器人（阿克曼传动系）

**可用传感器：**

- ``lidar2d.sensor.xml`` -- 通用 2D 激光扫描仪
- ``rplidar-a2.sensor.xml`` -- RPLidar A2
- ``velodyne-vlp16.sensor.xml`` -- Velodyne VLP-16 3D 激光雷达
- ``ouster-os1.sensor.xml`` -- Ouster OS1 3D 激光雷达
- ``helios-32-FOV-70.sensor.xml`` -- Helios 32 线 3D 激光雷达
- ``camera.sensor.xml`` -- RGB 相机
- ``rgbd_camera.sensor.xml`` -- 深度相机（RGBD）
- ``imu.sensor.xml`` -- 惯性测量单元
- ``gnss.sensor.xml`` -- GPS/GNSS 接收器

要使用一个附带传感器的预定义车辆，请使用 XML include：

.. code-block:: xml

    <mvsim_world version="1.0">
      <simul_timestep>5e-3</simul_timestep>

      <gui>
          <cam_distance>15</cam_distance>
      </gui>

      <element class="ground_grid">
      </element>

      <!-- Include the Jackal vehicle definition -->
      <include file="$(ros2 pkg prefix mvsim)/share/mvsim/definitions/jackal.vehicle.xml"
        default_sensors="true"
        />

      <vehicle name="r1" class="jackal">
        <init_pose>0 0 170</init_pose>  <!-- In global coords: x,y, yaw(deg) -->
        <init_vel>0 0 0</init_vel>  <!-- In local coords: vx,vy, omega(deg/s) -->

        <!-- You can also attach sensors to vehicles in separate includes,
            or define them inline within the vehicle block. -->
        <!-- <include file="$(ros2 pkg prefix mvsim)/share/mvsim/definitions/lidar2d.sensor.xml" sensor_x="1.7" sensor_z="1.01" sensor_yaw="0" max_range="70.0" sensor_name="laser1" />  -->
      </vehicle>

      <variable name="WALL_THICKNESS" value="0.2"></variable>

      <!-- Wall with a single door -->
      <element class="vertical_plane">
        <x0>-10</x0> <y0>-10</y0>
        <x1>-10</x1> <y1>10</y1>
        <z>0.0</z> <height>3.0</height>
        <cull_face>NONE</cull_face>
        <texture>https://mrpt.github.io/mvsim-models/textures-cgbookcase/wall-bricks-01.png</texture>
        <texture_size_x>2.5</texture_size_x>
        <texture_size_y>2.5</texture_size_y>
        <thickness>${WALL_THICKNESS}</thickness>  <!-- Wall thickness in meters -->

        <!-- Door at 50% position (middle of wall), 1.2m wide, standard height -->
        <door>
          <position>0.5</position>  <!-- 0.0 = start point, 1.0 = end point -->
          <width>1.2</width>        <!-- meters -->
          <z_min>0.0</z_min>        <!-- bottom of door -->
          <z_max>2.1</z_max>        <!-- top of door -->
          <name>main_entrance</name>
        </door>
      </element>


    </mvsim_world>

3 世界环境元素
^^^^^^^^^^^^^^

MVSim 支持多种类型的环境元素：

**占据栅格地图** 将灰度图像加载为 2D 障碍地图，通常用于室内导航测试：

.. code-block:: xml

    <element class="occupancy_grid">
      <file>map.png</file>
      <resolution>0.05</resolution>  <!-- meters/pixel -->
    </element>

**高程地图** 根据灰度高度图图像定义地形高度，适用于户外场景：

.. code-block:: xml

    <element class="elevation_map">
      <resolution>1.0</resolution>
      <elevation_image>terrain.png</elevation_image>
      <elevation_image_min_z>0.0</elevation_image_min_z>
      <elevation_image_max_z>5.0</elevation_image_max_z>
    </element>

**带纹理平面** 添加视觉地面表面：

.. code-block:: xml

    <element class="horizontal_plane">
      <cull_face>BACK</cull_face>
      <x_min>-25</x_min> <x_max>25</x_max>
      <y_min>-25</y_min> <y_max>25</y_max>
      <z>0.0</z>
      <texture>asphalt.png</texture>
      <texture_size_x>5.0</texture_size_x>
      <texture_size_y>5.0</texture_size_y>
    </element>

**块** 是静态或动态刚体（盒子、自定义形状），用作障碍物或可操作对象：

.. code-block:: xml

    <block class="obstacle1">
      <shape_from_visual/>
      <visual>
        <model_uri>package://mvsim/models/box.dae</model_uri>
      </visual>
      <init_pose>3.0 2.0 0</init_pose>
      <mass>20</mass>
    </block>

4 车辆动力学模型
^^^^^^^^^^^^^^^^

MVSim 提供了三种主要的动力学模型：

- **差速驱动** （``class="differential"``）：像 TurtleBot3 这样的两轮机器人。
  通过线速度和角速度进行控制。

- **阿克曼** （``class="ackermann"``）：前轮转向的类汽车车辆。
  通过线速度和转向角进行控制。

- **阿克曼传动系** （``class="ackermann_drivetrain"``）：带开式或 Torsen 差速器的逼真传动系模型，
  适用于更精确的车辆行为仿真。

每辆车辆可以使用不同的电机控制器：

- ``twist_pid``：接受 ``geometry_msgs/msg/Twist`` 命令，进行 PID 速度跟踪。
  这是 ROS 2 集成最常见的选择。
- ``twist_ideal``：瞬时速度命令（无动力学延迟）。
- ``twist_front_steer_pid``：用于通过线速度和转向角控制的阿克曼车辆。
- ``raw``：直接轮扭矩控制。

5 传感器噪声与配置
^^^^^^^^^^^^^^^^^^

MVSim 中的传感器支持可配置的噪声模型。
例如，一个带噪声参数的 IMU 传感器：

.. code-block:: xml

    <sensor class="imu" name="imu1">
      <pose>0 0 0.5 0 0 0</pose>  <!-- x y z roll pitch yaw -->
      <rate_hz>100</rate_hz>

      <!-- Gyroscope noise -->
      <gyroscope_noise>
        <noise_std>1e-3</noise_std>           <!-- rad/s -->
        <bias_initial_std>1e-4</bias_initial_std>
        <bias_drift>1e-6</bias_drift>
      </gyroscope_noise>

      <!-- Accelerometer noise -->
      <accelerometer_noise>
        <noise_std>1e-2</noise_std>           <!-- m/s^2 -->
        <bias_initial_std>1e-3</bias_initial_std>
        <bias_drift>1e-5</bias_drift>
      </accelerometer_noise>
    </sensor>

激光雷达传感器支持距离、角分辨率和噪声等参数：

.. code-block:: xml

    <sensor class="laser" name="laser1">
      <pose>0.15 0 0.3 0 0 0</pose>
      <rate_hz>10</rate_hz>
      <ray_count>360</ray_count>
      <fov_degrees>360</fov_degrees>
      <range_max>20.0</range_max>
      <range_std_noise>0.01</range_std_noise>  <!-- meters -->
      <raytrace_3d>true</raytrace_3d>  <!-- use 3D collision for 2D scans -->
    </sensor>

6 其他功能
^^^^^^^^^^

**多机器人仿真：**
MVSim 原生支持在同一世界中使用多辆车辆。
每辆车辆都有自己的 ROS 2 命名空间、TF 树和话题集。
机器人可以通过传感器相互检测，并通过碰撞进行物理交互。

**属性区域：**
你可以在世界中定义具有不同物理属性的区域，例如不同的摩擦系数，
或 GNSS 传感器停止报告位置的 GPS 拒止区域。

**动画角色：**
MVSim 支持骨架动画的 3D 角色（例如行人），它们沿着航点路径移动，
适用于在动态环境中测试感知和规划。

**关节和铰接车辆：**
车辆可以使用距离关节（绳索/缆绳）或旋转关节（铰链）连接，
从而支持挂车、拖绳和铰接系统的仿真。

**XML 高级特性：**
世界文件支持 ``<include>`` 指令、变量替换、数学表达式、
``<for>`` 循环和 ``<if>`` 条件，使得程序化生成复杂环境成为可能。

**无头模式和超实时：**
MVSim 可以在没有 GUI 的情况下运行，并支持可配置的仿真速度，
这对自动化测试和强化学习工作流很有用。

与其他模拟器的比较
------------------

与其他模拟器相比，MVSim 占据了一个不同的定位：

**优势：**

- 非常轻量：CPU 和内存占用低，启动速度快。
- 专注的车辆动力学，带多种摩擦和传动系模型。
- 基于 XML 的简单世界格式，容易上手。
- 原生多机器人支持，每辆车辆有独立的 ROS 2 命名空间。
- 超实时仿真，适用于批量测试。
- 通过 XML 循环和条件实现程序化世界生成。

**局限：**

- 物理是 2D（Box2D）：没有完整的 3D 刚体动力学。
  物体不会倾倒或飞行。
  高程地图增加了地形高度，但物理本质上仍然是 2D。
- 传感器仿真不如完整的 3D 模拟器精细：相机渲染和激光雷达模型
  可用但不逼真。
- 与 Gazebo 相比，预构建模型和环境的生态系统较小。
- 专注于轮式移动机器人。

更多资源
--------

- `MVSim 文档 <https://mvsimulator.readthedocs.io/>`__
- `MVSim GitHub 仓库 <https://github.com/MRPT/mvsim>`__
- `MVSim 论文（SoftwareX） <https://doi.org/10.1016/j.softx.2023.101443>`__
