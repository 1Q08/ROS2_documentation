NVIDIA ROS 2 项目
=================

NVIDIA Jetson 正致力于开发 ROS 2 包，以简化机器人 AI 应用的开发。


ROS 项目
--------
* `Isaac ROS Nvblox <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_nvblox>`__：使用 nvblox 进行硬件加速的 3D 场景重建和 Nav2 局部代价地图提供者。
* `Isaac ROS 物体检测 <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_object_detection>`__：支持包括 DetectNet 在内的物体检测深度学习模型。
* `Isaac ROS DNN 推理 <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_dnn_inference>`__：此仓库提供两个 NVIDIA GPU 加速的 ROS 2 节点，使用自定义模型执行深度学习推理。其中一个节点使用 TensorRT SDK，另一个使用 Triton SDK。
* `Isaac ROS 视觉 SLAM <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam>`__：此仓库提供一个 ROS 2 包，使用 Isaac Elbrus GPU 加速库估计双目视觉惯性里程计。
* `Isaac ROS Argus 摄像头 <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_argus_camera>`__：此仓库提供单目和双目节点，使 ROS 开发者能够通过 CSI 接口使用连接到 Jetson 平台的摄像头。
* `Isaac ROS image_pipeline <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_image_pipeline>`__：此元包提供与标准 CPU 版 image_pipeline 元包类似的功能，但利用了 Jetson 平台专用的计算机视觉硬件。
* `Isaac ROS 通用工具 <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common>`__：用于与 Isaac ROS 包套件配合使用的 Isaac ROS 通用工具。
* `Isaac ROS AprilTags <https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_apriltag>`__：ROS 2 节点使用 NVIDIA GPU 加速的 AprilTags 库在图像中检测 AprilTags，并发布其位姿、ID 和附加元数据。
* `ROS 和 ROS 2 Docker 镜像 <https://github.com/NVIDIA-AI-IOT/ros2_jetson/tree/main/docker>`__：用于在 NVIDIA Jetson 平台上轻松部署的 Docker 镜像，包含 ROS 2、PyTorch 和其他重要的机器学习库。
* `ROS 和 ROS 2 DockerFiles <https://github.com/dusty-nv/jetson-containers>`__：基于 l4t 的 ROS 2 Dockerfile，允许你构建自己的 Docker 镜像。
* `用于 PyTorch 和 TensorRT 的 ROS 2 包 <https://github.com/NVIDIA-AI-IOT/ros2_torch_trt>`__：使用 PyTorch 和 NVIDIA TensorRT 进行分类和物体检测任务的 ROS 2 包。本教程是在 NVIDIA Jetson 上将 AI 与 ROS 2 集成的良好起点。
* `用于加速深度学习节点的 ROS / ROS 2 包 <https://github.com/dusty-nv/ros_deep_learning>`__：使用 `jetson-inference <https://github.com/dusty-nv/jetson-inference>`__ 库和 `NVIDIA Hello AI World 教程 <https://developer.nvidia.com/embedded/twodaystoademo>`__ 的 ROS/ROS 2 深度学习图像识别、物体检测和语义分割推理节点，以及摄像头/视频流节点。
* `用于人体姿态估计的 ROS 2 包 <https://github.com/NVIDIA-AI-IOT/ros2_trt_pose>`__：用于人体姿态估计的 ROS 2 包。
* `用于手部姿态估计和手势分类的 ROS 2 包 <https://github.com/NVIDIA-AI-IOT/ros2_trt_pose_hand>`__：使用 TensorRT 进行实时手部姿态估计和手势分类的 ROS 2 包。
* `用于单目深度估计的 GPU 加速 ROS 2 包 <https://github.com/NVIDIA-AI-IOT/ros2_torch2trt_examples>`__：用于 NVIDIA GPU 加速 torch2trtx 示例（如单目深度估计和文本检测）的 ROS 2 包。
* `用于 Jetson 统计的 ROS 2 包 <https://github.com/NVIDIA-AI-IOT/ros2_jetson_stats>`__：用于监控和控制 NVIDIA Jetson [Xavier NX、Nano、AGX Xavier、TX1、TX2] 的 ROS 2 包。
* `用于 DeepStream SDK 的 ROS 2 包 <https://github.com/NVIDIA-AI-IOT/ros2_deepstream>`__：用于 NVIDIA DeepStream SDK 的 ROS 2 包。

仿真项目
--------
* `Isaac Sim Nav2 <https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/tutorial_ros2_navigation.html>`__：在此 ROS 2 示例中，我们演示了 Omniverse Isaac Sim 与 ROS 2 Nav2 项目的集成。
* `Isaac Sim 多机器人 ROS 2 导航 <https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/tutorial_ros2_multi_navigation.html>`__：在此 ROS 2 示例中，我们演示了 Omniverse Isaac Sim 与 ROS 2 Nav2 栈的集成，以实现多机器人同时导航。

参考资料
--------
关于 NVIDIA Jetson ROS 2 的更多更新，可以`在这里 <https://nvidia-ai-iot.github.io/ros2_jetson/>`__ 找到。
