Lyrical Luth 发布时间线
=======================

有关 Lyrical Luth 的开发进度，请参见 `此项目看板 <https://github.com/orgs/ros2/projects/70>`__。
有关 Lyrical Luth 遵循的整体流程，请参见 :doc:`流程描述页面 <../Release-Process>`。

**尽快** - 将 ROS Rolling 迁移到 ROS Lyrical 的目标平台
    * RHEL 10 + Ubuntu 26.04：一旦核心软件包在两个平台上都能成功构建，就立即迁移。
    * Windows 11：一旦我们有了绿色构建，就立即迁移。

**2026 年 4 月 13 日（周一）** - Alpha + RMW 冻结（*延迟；原定 4 月 6 日*）
    * ROS Base 软件包的初步测试
    * RMW 提供方软件包的 API 和功能冻结。

**2026 年 4 月 20 日（周一）** - 冻结（*延迟；原定 4 月 13 日*）
    * Rolling Ridley 中 ROS Base 软件包的 API 和功能冻结。
    * 在此之后只应发布缺陷修复版本。
    * 可以发布新软件包。

**2026 年 4 月 21 日（周一）** - 分支（*延迟；原定 4 月 20 日*）
    * 从 Rolling Ridley 分支
    * ``rosdistro`` 重新开放 ROS Base 软件包的 Rolling 拉取请求。
    * Lyrical 的开发从 ``ros-rolling-*`` 软件包切换到 ``ros-lyrical-*`` 软件包。

**2026 年 4 月 27 日（周一）** - Beta
    * 提供 ROS Desktop 软件包的更新版本。
    * 呼吁进行通用测试。

**2026 年 4 月 30 日（周四）** - 启动教程聚会
    * 开放教程供社区测试。

**2026 年 5 月 11 日（周一）** - 候选版本
    * 构建直到 ROS Desktop 的候选版本软件包

**2026 年 5 月 18 日（周一）** - 发行版冻结
    * 冻结所有 ROS desktop 软件包上的所有 Lyrical 分支
    * 针对任何 Lyrical 分支或 ``rosdistro`` 仓库中 ``lyrical/distribution.yaml`` 的拉取请求都不会被合并。

**2026 年 5 月 22 日（周五）** - 正式发布
    * 发布公告。
    * ROS desktop 软件包的源代码冻结解除，``rosdistro`` 重新开放 Lyrical 的拉取请求。

**2031 年 5 月** - 停止维护
    * ROS Lyrical 将停止接收更新，包括安全更新
