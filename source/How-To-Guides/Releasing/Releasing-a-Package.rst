.. redirect-from::

    Releasing-a-ROS-2-package-with-bloom
    Guides/Releasing-a-ROS-2-package-with-bloom
    Tutorials/Releasing-a-ROS-2-package-with-bloom
    How-To-Guides/Releasing-a-ROS-2-package-with-bloom

发布软件包
==========

.. toctree::
   :hidden:

   Index-Your-Packages
   First-Time-Release
   Subsequent-Releases
   Release-Team-Repository
   Release-Track

**发布软件包会让你自己的软件包出现在公共 ROS 2 构建农场（buildfarm）中。**
这样做将会：

* 让你的软件包可以在某个 ROS 发行版中所有受支持的 Linux 平台上，通过软件包管理器（例如 Ubuntu 上的 ``apt``）安装，具体规则见 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`_。
* 让你的软件包可以自动生成 API 文档。
* 让你的软件包被收录进 `ROS Index <https://index.ros.org>`_。
* （可选）让你可以为仓库中的拉取请求启用自动 CI。

**请按照下列指南之一来发布你的软件包：**

* :doc:`索引你的软件包 <Index-Your-Packages>` —— 如果这是该软件包的首次发布
* :doc:`首次发布 <First-Time-Release>` —— 如果这是该软件包的首次发布，但它已被索引
* :doc:`后续发布 <Subsequent-Releases>` —— 如果你要发布的是已发布软件包的新版本

成功按照说明操作之后，你的软件包将在下一次发行版同步时发布到 ROS 生态系统中！
