.. redirect-from::

包文档
======

ROS 包文档，即通过 apt 或其他工具安装的特定包的文档，可以在多个地方找到。
下面简要列出了查找特定 ROS 包文档的位置。


* 大多数 ROS 2 包的包级文档都 `包含在此索引页面中 <https://docs.ros.org/en/{DISTRO}/p/>`__。
* 所有 ROS 2 包的文档都与其信息一同托管在 `ROS 索引 <https://index.ros.org/>`_ 上。
  在 ROS 索引中搜索包，将返回其信息，例如已发布的发行版、``README.md`` 文件、URL 以及其他重要元数据。

更大的包
--------

像 MoveIt、Nav2 和 microROS 这样较大的包，在 ros.org 上拥有自己的域或子域。
以下是一个简短列表。

* `MoveIt <https://moveit.ai/>`__
* `Navigation2 <https://nav2.org/>`__
* `Control <https://control.ros.org/master/index.html>`__
* `microROS（嵌入式系统） <https://micro.ros.org/>`__

API 文档
--------

您可以使用下面的链接找到 {DISTRO_TITLE} 发行版中 ROS 客户端库的 API 级文档：

* `rclcpp - C++ 客户端库 <https://docs.ros.org/en/{DISTRO}/p/rclcpp/generated/index.html>`_
* `rclcpp_lifecycle - C++ 生命周期库 <https://docs.ros.org/en/{DISTRO}/p/rclcpp_lifecycle/generated/index.html>`_
* `rclcpp_components - C++ 组件库 <https://docs.ros.org/en/{DISTRO}/p/rclcpp_components/generated/index.html>`_
* `rclcpp_action - C++ 动作库 <https://docs.ros.org/en/{DISTRO}/p/rclcpp_action/generated/index.html>`_

将您的包添加到 docs.ros.org
---------------------------

所有已发布的 ROS 2 包都会自动添加到 docs.ros.org 和 `ROS 索引 <https://index.ros.org/>`_。
如果您想启用或配置自己的包，请参阅：:doc:`./How-To-Guides/Documenting-a-ROS-2-Package`。
