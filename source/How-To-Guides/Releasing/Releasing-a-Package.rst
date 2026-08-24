.. redirect-from::

    Releasing-a-ROS-2-package-with-bloom
    Guides/Releasing-a-ROS-2-package-with-bloom
    Tutorials/Releasing-a-ROS-2-package-with-bloom
    How-To-Guides/Releasing-a-ROS-2-package-with-bloom

发布包
======

.. toctree::
   :hidden:

   Index-Your-Packages
   First-Time-Release
   Subsequent-Releases
   Release-Team-Repository
   Release-Track

**发布一个包会让你的包在公共 ROS 2 buildfarm 上可用。**
这将：

* 使你的包可以在某个 ROS 发行版中通过包管理器（例如 Ubuntu 上的 ``apt``）安装在所有受支持的 Linux 平台上，如 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`_ 所述。
* 允许为你的包自动生成 API 文档。
* 使你的包成为 `ROS Index <https://index.ros.org>`_ 的一部分。
* （可选）允许你为仓库中的拉取请求运行自动 CI。

**按照以下指南之一来发布你的包：**

* :doc:`为你的包建立索引 <Index-Your-Packages>` - 如果这是该包的首次发布
* :doc:`首次发布 <First-Time-Release>` - 如果这是该包的首次发布，但它已经被索引
* :doc:`后续发布 <Subsequent-Releases>` - 如果你要发布一个已经发布过的包的新版本

成功按照说明操作后，你的包将在下一次发行版同步时发布到 ROS 生态系统中！
