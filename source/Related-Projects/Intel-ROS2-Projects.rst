.. redirect-from::

  Intel-ROS2-Projects

Intel ROS 2 项目
================

Intel® 机器人开源项目（Intel® ROS 项目）旨在借助各类 Intel 技术与平台——包括 CPU、GPU、`Intel® Movidius™ NCS <https://www.intel.com/content/www/us/en/developer/tools/neural-compute-stick/overview.html>`__ 优化的深度学习后端、FPGA、`Intel® RealSense™ <https://www.intel.com/content/www/us/en/architecture-and-technology/realsense-overview.html>`__ 摄像头等——实现物体检测/定位/跟踪、人员检测、车辆检测以及工业机械臂抓取点分析。

关键项目
--------

我们正在开发以下 ROS 2 项目，并逐步通过 https://github.com/intel/ 或 ROS 2 GitHub 仓库发布源代码。

* `ROS2 OpenVINO <https://github.com/intel/ros2_openvino_toolkit>`__：用于 Intel® 视觉推理与神经网络优化工具包的 ROS 2 包，用于开发跨平台计算机视觉解决方案。
* `ROS2 RealSense 摄像头 <https://github.com/IntelRealSense/realsense-ros>`__：用于 Intel® RealSense™ D400 系列摄像头的 ROS 2 包
* `ROS2 Movidius NCS <https://github.com/intel/ros2_intel_movidius_ncs>`__：使用 Intel® Movidius™ 神经计算棒（NCS）进行物体检测的 ROS 2 包。
* `ROS2 对象消息 <https://github.com/intel/ros2_object_msgs>`__：用于对象的 ROS 2 消息。
* `ROS2 对象分析 <https://github.com/intel/ros2_object_analytics>`__：用于物体检测、跟踪和 2D/3D 定位的 ROS 2 包。
* `ROS2 消息过滤器 <https://github.com/ros2/message_filters>`__：用于带时间戳消息同步的 ROS 2 包。
* `ROS2 CV Bridge <https://github.com/ros-perception/vision_opencv/tree/ros2/cv_bridge>`__：用于桥接 openCV 的 ROS 2 包。
* `ROS2 对象地图 <https://github.com/intel/ros2_object_map>`__：基于 ROS 2 对象分析提供的信息，在 SLAM 过程中于地图上标记对象标签的 ROS 2 包。
* `ROS2 运动对象 <https://github.com/intel/ros2_moving_object>`__：基于 ROS 2 对象分析提供的信息，提供对象运动信息（例如对象在 x、y、z 轴上的速度）的 ROS 2 包。
* `ROS2 抓取库 <https://github.com/intel/ros2_grasp_library>`__：用于抓取位置分析的 ROS 2 包，并与 `MoveIt <https://github.com/ros-planning/moveit2.git>`__ 抓取接口兼容。
* `ROS2 导航 <https://github.com/ros-planning/navigation2>`__：用于机器人导航的 ROS 2 包，已集成到 ROS 2 Crystal 发行版中。
* `Intel 机器人开发套件（SDK） <https://github.com/intel/robot_devkit>`__：一个开源项目，使开发者能够轻松、高效地创建、定制、优化机器人软件栈，并将其部署到基于机器人操作系统 2（ROS 2）框架的自主移动机器人（AMR）平台上。

参考资料
--------

ROS 组件位于：https://wiki.ros.org/IntelROSProject ，它展示了这些包之间的关系，同样适用于 ROS 2。
