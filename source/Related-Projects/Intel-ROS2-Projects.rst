.. redirect-from::

  Intel-ROS2-Projects

Intel ROS 2 项目
================

Intel® Robotics Open Source Project（Intel® ROS Project）致力于通过 Intel 技术与平台支持目标检测/定位/跟踪、人员检测、车辆检测、工业机器人臂抓取点分析等能力，涵盖 CPU、GPU、`Intel® Movidius™ NCS <https://www.intel.com/content/www/us/en/developer/tools/neural-compute-stick/overview.html>`__ 优化的深度学习后端、FPGA、`Intel® RealSense™ <https://www.intel.com/content/www/us/en/architecture-and-technology/realsense-overview.html>`__ 相机等。

关键项目
--------

我们正在逐步开发以下 ROS 2 项目，并通过 https://github.com/intel/ 或 ROS 2 GitHub 仓库发布源代码。

* `ROS2 OpenVINO <https://github.com/intel/ros2_openvino_toolkit>`__：用于 Intel® Visual Inference 与 Neural Network Optimization Toolkit 的 ROS 2 软件包，用于开发跨平台计算机视觉解决方案。
* `ROS2 RealSense Camera <https://github.com/IntelRealSense/realsense-ros>`__：Intel® RealSense™ D400 系列相机的 ROS 2 软件包。
* `ROS2 Movidius NCS <https://github.com/intel/ros2_intel_movidius_ncs>`__：使用 Intel® Movidius™ 神经计算棒（NCS）进行目标检测的 ROS 2 软件包。
* `ROS2 Object Messages <https://github.com/intel/ros2_object_msgs>`__：ROS 2 的对象消息定义。
* `ROS2 Object Analytics <https://github.com/intel/ros2_object_analytics>`__：用于目标检测、跟踪与 2D/3D 定位的 ROS 2 软件包。
* `ROS2 Message Filters <https://github.com/ros2/message_filters>`__：用于时间戳消息同步的 ROS 2 软件包。
* `ROS2 CV Bridge <https://github.com/ros-perception/vision_opencv/tree/ros2/cv_bridge>`__：用于与 OpenCV 对接的 ROS 2 软件包。
* `ROS2 Object Map <https://github.com/intel/ros2_object_map>`__：基于 ROS 2 对象分析信息，在 SLAM 的地图上标记对象标签的 ROS 2 软件包。
* `ROS2 Moving Object <https://github.com/intel/ros2_moving_object>`__：基于 ROS 2 对象分析信息，提供对象运动信息（如 x、y、z 轴上的对象速度）的 ROS 2 软件包。
* `ROS2 Grasp Library <https://github.com/intel/ros2_grasp_library>`__：用于抓取位置分析的 ROS 2 软件包，并兼容 `MoveIt <https://github.com/ros-planning/moveit2.git>`__ 的抓取接口。
* `ROS2 Navigation <https://github.com/ros-planning/navigation2>`__：机器人导航 ROS 2 软件包，已集成到 ROS 2 Crystal 版本。
* `Intel Robot DevKit (SDK) <https://github.com/intel/robot_devkit>`__：一个开源项目，帮助开发者基于 Robot Operating System 2（ROS 2）框架，轻松高效地创建、定制、优化并部署自主移动机器人（AMR）平台的软件栈。

参考
----

ROS 组件位于：https://wiki.ros.org/IntelROSProject，展示这些软件包之间的关系，该关系同样适用于 ROS 2。
