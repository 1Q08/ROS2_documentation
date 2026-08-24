.. redirect-from::

包文档
======

ROS 包文档，也就是你通过 apt 或其他工具安装的特定软件包的文档，可以在多个地方找到。
以下是查找特定 ROS 软件包文档的简要清单。

* 大多数 ROS 2 软件包的包级文档都 `包含在此索引页中 <https://docs.ros.org/en/{DISTRO}/p/>`__。
* 所有 ROS 2 软件包的文档都随其信息一同托管在 `ROS Index <https://index.ros.org/>`_ 上。
  在 ROS Index 上搜索软件包，可以获得它们的相关信息，例如已发布的发行版、``README.md`` 文件、URL 以及其他重要元数据。

大型软件包
----------

像 MoveIt、Nav2 和 microROS 这样的大型软件包在 ros.org 上拥有自己的域名或子域名。
以下是一个简短的列表。

* `MoveIt <https://moveit.ai/>`__
* `Navigation2 <https://nav2.org/>`__
* `Control <https://control.ros.org/master/index.html>`__
* `microROS（嵌入式系统） <https://micro.ros.org/>`__

API 文档
--------

你可以使用以下链接，在 {DISTRO_TITLE} 发行版中找到 ROS 客户端库的 API 级文档：

* `rclcpp - C++ 客户端库 <https://docs.ros.org/en/{DISTRO}/p/rclcpp/generated/index.html>`_
* `rclcpp_lifecycle - C++ 生命周期库 <https://docs.ros.org/en/{DISTRO}/p/rclcpp_lifecycle/generated/index.html>`_
* `rclcpp_components - C++ 组件库 <https://docs.ros.org/en/{DISTRO}/p/rclcpp_components/generated/index.html>`_
* `rclcpp_action - C++ 动作库 <https://docs.ros.org/en/{DISTRO}/p/rclcpp_action/generated/index.html>`_

将你的软件包添加到 docs.ros.org
--------------------------------

所有已发布的 ROS 2 软件包都会自动添加到 docs.ros.org 和 `ROS Index <https://index.ros.org/>`_。
如果你想为自己的软件包启用或配置文档，请参见：:doc:`./How-To-Guides/Documenting-a-ROS-2-Package`。
