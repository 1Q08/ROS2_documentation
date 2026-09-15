生成 URDF 文件
==============

**目标：** 学习如何导出 URDF 文件

**教程级别：** 中级

**时长：** 5 分钟

.. contents:: 目录
   :depth: 2
   :local:

大多数机器人工程师都以团队形式工作，而这些团队中通常包含一位负责开发机器人 CAD 模型的机械工程师。
与其手工编写 URDF，不如从许多不同的 CAD 和建模程序中导出 URDF 模型。
这些导出工具通常由熟悉其所用特定 CAD 程序的人员开发。
下面你会找到适用于各种 CAD 和 3D 建模软件系统的可用 URDF 导出工具列表。
*ROS 核心维护者并不维护这些软件包。
因此，我们不对其性能或易用性作任何声明。*
不过，我们认为整理一份可用的 URDF 导出工具列表会很有帮助。

**CAD 导出工具**

 * `Blender URDF Exporter <https://github.com/dfki-ric/phobos>`_
 * `CREO Parametric URDF Exporter <https://github.com/icub-tech-iit/creo2urdf>`_
 * `FreeCAD ROS Workbench <https://github.com/galou/freecad.cross>`_
 * `RobotCAD (FreeCAD OVERCROSS) <https://github.com/drfenixion/freecad.overcross>`_
 * `Freecad to Gazebo Exporter <https://github.com/Dave-Elec/freecad_to_gazebo>`_
 * `Fusion 360 URDF Exporter <https://github.com/dheena2k2/fusion2urdf-ros2>`_
 * `fusion2URDF (Fusion 360, ros2_control, closed loops) <https://github.com/Adriaeik/fusion2URDF>`_
 * `FusionSDF: Fusion 360 to SDF exporter <https://github.com/andreasBihlmaier/FusionSDF>`_
 * `OnShape URDF Exporter <https://github.com/Rhoban/onshape-to-robot>`_
 * `SolidWorks URDF Exporter <https://github.com/ros/solidworks_urdf_exporter>`_
 * `ExportURDF Library (Fusion360, OnShape, Solidworks) <https://github.com/daviddorf2023/ExportURDF>`_

**其他 URDF 导出与转换工具**

 * `Gazebo SDFormat to URDF Parser <https://github.com/ros/sdformat_urdf>`_
 * `SDF to URDF Converter in Python <https://github.com/andreasBihlmaier/pysdf>`_
 * `URDF to Webots Simulator Format <https://github.com/cyberbotics/urdf2webots>`_
 * The `Blender Robotics Tools <https://github.com/robotology/blender-robotics-utils/>`_ 仓库包含许多实用工具，其中包括从 Blender 导出 `URDF 文件 <https://github.com/robotology/blender-robotics-utils/tree/master?tab=readme-ov-file#urdftoblender>`_ 的工具
 * `CoppeliaSim URDF Exporter <https://manual.coppeliarobotics.com/en/importExport.htm#urdf>`_
 * `Isaac Sim URDF Exporter <https://docs.omniverse.nvidia.com/isaacsim/latest/advanced_tutorials/tutorial_advanced_export_urdf.html>`_

**查看 URDF 和 SDF 文件**
 * `Examples of Common URDF Launch Files <https://github.com/ros/urdf_launch>`_
 * Web 查看器（用于 URDF 文件）：`GitHub 仓库 <https://github.com/gkjohnson/urdf-loaders/>`_ 和 `在线网站 <https://gkjohnson.github.io/urdf-loaders/javascript/example/bundle/index.html>`_
 * `View SDF Models in RViz <https://github.com/Yadunund/view_sdf_rviz>`_
 * `Jupyterlab URDF Viewer <https://github.com/IsabelParedes/jupyterlab-urdf>`_

如果你有喜欢的 URDF 工具，欢迎将其添加到上面的列表中！
