从 ROS 1 迁移到 ROS 2
=====================

这些指南展示了如何将现有的 ROS 1 包转换为 ROS 2。
如果你是 ROS 1 与 ROS 2 之间移植的新手，建议按顺序阅读这些指南。

.. toctree::
   :maxdepth: 1

   Migrating-from-ROS1/Migrating-Packages
   Migrating-from-ROS1/Migrating-Package-XML
   Migrating-from-ROS1/Migrating-Interfaces
   Migrating-from-ROS1/Migrating-CPP-Package-Example
   Migrating-from-ROS1/Migrating-CPP-Packages
   Migrating-from-ROS1/Migrating-Python-Package-Example
   Migrating-from-ROS1/Migrating-Python-Packages
   Migrating-from-ROS1/Migrating-Launch-Files
   Migrating-from-ROS1/Migrating-Parameters
   Migrating-from-ROS1/Migrating-Scripts

自动转换工具
------------

还有一些自动转换工具，尽管它们并不全面：

* `Magical ROS 2 Conversion Tool <https://github.com/DLu/roscompile/tree/main/magical_ros2_conversion_tool>`_
* 将 ROS 1 XML 启动文件转换为 ROS 2 Python 启动文件的 Launch File 迁移器：https://github.com/aws-robotics/ros2-launch-file-migrator
* Amazon 已将其从 ROS 1 移植到 ROS 2 的工具发布在：https://github.com/awslabs/ros2-migration-tools/tree/master/porting\_tools
* `rospy2 <https://github.com/dheera/rospy2>`_ Python 项目，用于自动将 rospy 调用转换为 rclpy 调用
