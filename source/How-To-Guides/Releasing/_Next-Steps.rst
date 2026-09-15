你的拉取请求提交之后，通常在一天或两天之内，rosdistro 的某位维护者就会审核并合并你的拉取请求。
如果你的软件包构建成功，那么在 24–48 小时内，你的软件包将会出现在 **ros-testing** 仓库中，你可以在这里 :doc:`测试你的预发布二进制包 <../../../Installation/Testing>`。

大约每两到四周，发行版的发布经理会手动将 ros-testing 的内容同步到 ROS 主仓库中。
这时你的软件包才真正对 ROS 社区的其他成员可用。
要获取下一次同步（sync）时间的更新信息，请订阅 `Open Robotics Discourse 上的打包与发布管理类别 <https://discourse.openrobotics.org/c/ros/release/16>`_。
