Lyrical Luth 发行时间表
=======================

关于 Lyrical Luth 的开发进展，请参阅 `此项目看板 <https://github.com/orgs/ros2/projects/70>`__。
关于 Lyrical Luth 遵循的整体流程，请参阅 :doc:`流程说明页面 <../Release-Process>`。

**尽快** - 将 ROS Rolling 迁移到 ROS Lyrical 的目标平台
    * RHEL 10 + Ubuntu 26.04：一旦核心软件包在两个平台上都能成功构建，就进行迁移。
    * Windows 11：一旦构建通过（green build）就进行迁移

**2026 年 4 月 13 日（周一）** - Alpha + RMW 冻结（*已延期；原定 4 月 6 日*）
    * ROS Base 软件包的初步测试
    * RMW 供应商软件包的 API 与特性冻结。

**2026 年 4 月 20 日（周一）** - 冻结（*已延期；原定 4 月 13 日*）
    * Rolling Ridley 中 ROS Base 软件包的 API 与特性冻结。
    * 在此之后只应发布缺陷修复版本。
    * 可以发布新软件包。

**2026 年 4 月 21 日（周二）** - 分支创建（*已延期；原定 4 月 20 日*）
    * 从 Rolling Ridley 创建分支
    * ``rosdistro`` 重新开放，以接收针对 ROS Base 软件包的 Rolling PR。
    * Lyrical 的开发从 ``ros-rolling-*`` 软件包转向 ``ros-lyrical-*`` 软件包。

**2026 年 4 月 27 日（周一）** - beta
    * ROS 桌面版软件包的更新版本可用。
    * 征集公开测试。

**2026 年 4 月 30 日（周四）** - 启动教程派对（Tutorial Party）
    * 开放教程以供社区测试。

**2026 年 5 月 11 日（周一）** - release candidate
    * 构建到 ROS 桌面版为止的 release candidate 软件包

**2026 年 5 月 18 日（周一）** - 发行版冻结
    * 冻结所有 ROS 桌面版软件包上的所有 Lyrical 分支
    * 不会合并任何 Lyrical 分支的 pull request，也不会合并 ``rosdistro`` 仓库中针对 ``lyrical/distribution.yaml`` 的 pull request。

**2026 年 5 月 22 日（周五）** - 正式发布
    * 发行公告。
    * ROS 桌面版软件包的源码冻结解除，``rosdistro`` 重新开放以接收 Lyrical 的 pull request。

**2031 年 5 月** - 生命周期终止
    * ROS Lyrical 将停止接收更新，包括安全更新
