一旦你的拉取请求被提交，通常在一两天内，rosdistro 的一位维护者会审查并合并你的拉取请求。
如果你的包构建成功，在 24-48 小时内，你的包将出现在 **ros-testing** 仓库中，你可以在那里 :doc:`测试你的预发布二进制文件 <../../../Installation/Testing>`。

大约每两到四周，发行版的发布管理者会将 ros-testing 的内容手动同步到主 ROS 仓库中。
这时你的包才真正对 ROS 社区的其他成员可用。
要了解下一次同步（sync）何时到来，请订阅 `Open Robotics Discourse 上的打包与发布管理类别 <https://discourse.openrobotics.org/c/ros/release/16>`_。
