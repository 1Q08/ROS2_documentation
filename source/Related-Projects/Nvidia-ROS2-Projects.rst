NVIDIA ROS 2 项目
=================

NVIDIA 提供了用于开发机器人 AI 应用的软件包。

ISAAC ROS 项目
--------------
* `Pre-built ROS 2 Humble support <https://nvidia-isaac-ros.github.io/getting_started/isaac_ros_buildfarm_cdn.html>`__：来自 NVIDIA 构建农场的 ROS 2 Humble 在 Ubuntu 20.04 上为 Jetson 和其他 aarch64 平台预构建的 Debian 软件包。
* `CUDA with NITROS <https://nvidia-isaac-ros.github.io/concepts/nitros/cuda_with_nitros.html>`__：这有助于用户开发自己的 CUDA 使能节点，并能与 NITROS 配合工作，NITROS 是 Isaac ROS 中类型适配与协商实现，用于加速 ROS 2 中的计算。
* `Isaac ROS NITROS Bridge <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_nitros_bridge>`__：用于把 Isaac ROS 软件包与已有 ROS 1 应用优化集成的 NITROS 桥接。
  使用它可将 ROS 应用桥接到 ROS 2，从而以比传统 ROS 桥接快超过 2 倍的速度实现加速计算。
* `Nova Carter <https://nvidia-isaac-ros.github.io/robots/nova_carter.html>`__：一个用于机器人开发与研究的参考 AMR，由 Isaac ROS 与 Nav2 驱动，并与 Open Navigation 配合用于远程操作、建图与导航。
* `Isaac ROS Nova <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_nova>`__：该仓库提供了与 Isaac Nova Orin 传感器套件接口连接的一组优化软件包。
* `Isaac ROS Pose Estimation <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_pose_estimation>`__：该仓库包含 ROS 2 软件包，用于预测对象姿态。
* `ROS2_Benchmark <https://github.com/NVIDIA-ISAAC-ROS/ros2_benchmark>`__：ros2_benchmark 提供工具，用于测量复杂图谱的吞吐量、延迟与计算利用率，而不改变待测代码。
* `Isaac ROS Benchmark <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_benchmark>`__：该软件包基于 ros2_benchmark 构建，为 Isaac ROS 图谱提供基准测试配置。
* `Isaac ROS Map Localization <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_map_localization>`__：该模块包含用于处理激光雷达并相对于地图估计位姿的 ROS 2 软件包。
  占用栅格定位器会处理平面测距扫描并估计栅格地图中的位姿；在大多数地图上，这一过程可在 1 秒内完成。
* `Isaac ROS Nitros <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_nitros>`__：用于硬件加速友好消息搬运的 Isaac Transport for ROS 软件包。
* `Isaac ROS Compression <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_compression>`__：用于压缩相机数据采集与回放、面向 AI 模型与感知功能开发的硬件加速 NITROS 软件包，能以 4x 1080p 相机 30fps（共 >120fps）压缩数据，数据占用减少约 10 倍。
* `Isaac ROS DNN Stereo Depth <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_dnn_stereo_depth>`__：DNN 立体视差包含用于预测立体输入视差的软件包。
* `Isaac ROS Depth Segmentation <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_depth_segmentation>`__：用于深度分割的硬件加速软件包。
* `Isaac ROS Nvblox <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_nvblox>`__：硬件加速 3D 场景重建与 Nav2 局部代价地图提供器，使用 nvblox。
* `Isaac ROS Object Detection <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_object_detection>`__：支持包括 DetectNet 在内的对象检测深度学习模型。
* `Isaac ROS DNN Inference <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_dnn_inference>`__：该仓库提供两个 NVIDIA GPU 加速的 ROS 2 节点，用于使用自定义模型执行深度学习推理。
  一个节点使用 TensorRT SDK，另一个节点使用 Triton SDK。
* `Isaac ROS Visual SLAM <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam>`__：该仓库提供一个 ROS 2 软件包，使用 Isaac Elbrus GPU 加速库估计立体视觉惯性里程计。
* `Isaac ROS Mission Client <http://github.com/NVIDIA-ISAAC-ROS/isaac_ros_mission_client>`__：该仓库接收来自 ROS 的状态与错误更新，并将其转换为 VDA5050 JSON 消息，再通过 ROS 2 -> MQTT 节点发送给 Mission Dispatch。
* `Isaac ROS Argus Camera <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_argus_camera>`__：该仓库提供单目和立体节点，使 ROS 开发者能够通过 CSI 接口使用连接到 Jetson 平台上的相机。
* `Isaac ROS Image Pipeline <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_image_pipeline>`__：该元软件包提供与标准 CPU 基础 image_pipeline 软件包相似的功能，但利用了 Jetson 平台的专用计算机视觉硬件。
* `Isaac ROS Common <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common>`__：Isaac ROS 通用工具集，供 Isaac ROS 套件软件包一起使用。
* `Isaac ROS AprilTag <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_apriltag>`__：ROS 2 节点使用 NVIDIA GPU 加速的 AprilTags 库检测图像中的 AprilTags，并发布其位姿、ID 与附加元数据。

附加项目
--------
* `ROS and ROS 2 DockerFiles <https://github.com/dusty-nv/jetson-containers>`__：基于 l4t 的 ROS 2 Dockerfile，允许你构建自己的 Docker 镜像。
* `ROS / ROS 2 Packages for Accelerated Deep Learning Nodes <https://github.com/dusty-nv/ros_deep_learning>`__：使用 `jetson-inference <https://github.com/dusty-nv/jetson-inference>`__ 库与 `NVIDIA Hello AI World tutorial <https://developer.nvidia.com/embedded/twodaystoademo>`__ 实现图像识别、目标检测与语义分割推理节点，以及 ROS/ROS 2 相机/视频流节点。

仿真项目
--------
* `Isaac Sim Nav2 <https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/tutorial_ros2_navigation.html>`__：在这个 ROS 2 示例中，我们演示了 Omniverse Isaac Sim 与 ROS 2 Nav2 项目集成。
* `Isaac Sim Multiple Robot ROS 2 Navigation <https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/tutorial_ros2_multi_navigation.html>`__：在这个 ROS 2 示例中，我们演示了 Omniverse Isaac Sim 与 ROS 2 Nav2 栈集成，以执行多机器人同步导航。
