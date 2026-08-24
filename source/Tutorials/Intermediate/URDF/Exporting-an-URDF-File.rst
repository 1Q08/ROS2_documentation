生成 URDF 文件
==============

**目标：** 学习如何导出一个 URDF 文件

**教程级别：** 中级

**时间：** 5 分钟

.. contents:: 目录
   :depth: 2
   :local:

大多数机器人学家以团队形式工作，而这些团队通常包括一位开发机器人 CAD 模型的机械工程师。
与其手工编写 URDF，不如从许多不同的 CAD 和建模程序中导出一个 URDF 模型。
这些导出工具通常由熟悉他们所使用的特定 CAD 程序的人开发。
下面你会找到一个面向各种 CAD 和 3D 建模软件系统的可用 URDF 导出器列表。
*ROS 核心维护者并不维护这些包。
因此，我们对它们的性能或易用性不作任何声明。*
不过，我们认为提供一份可用 URDF 导出器的列表会很有帮助。

**CAD 导出器**

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

**其他 URDF 导出和转换工具**

 * `Gazebo SDFormat to URDF Parser <https://github.com/ros/sdformat_urdf/tree/jazzy>`_
 * `SDF to URDF Converter in Python <https://github.com/andreasBihlmaier/pysdf>`_
 * `URDF to Webots Simulator Format <https://github.com/cyberbotics/urdf2webots>`_
 * `Blender Robotics Tools <https://github.com/robotology/blender-robotics-utils/>`_ 仓库包含了许多有用的工具，包括一个用于从 Blender 导出 `URDF 文件 <https://github.com/robotology/blender-robotics-utils/tree/master?tab=readme-ov-file#urdftoblender>`_ 的工具。
 * `CoppeliaSim URDF Exporter <https://manual.coppeliarobotics.com/en/importExport.htm#urdf>`_
 * `Isaac Sim URDF Exporter <https://docs.omniverse.nvidia.com/isaacsim/latest/advanced_tutorials/tutorial_advanced_export_urdf.html>`_

**查看 URDF 和 SDF 文件**
 * `常见 URDF 启动文件示例 <https://github.com/ros/urdf_launch>`_
 * URDF 文件的 Web 查看器：`GitHub Repo <https://github.com/gkjohnson/urdf-loaders/>`_ 和 `Live Website <https://gkjohnson.github.io/urdf-loaders/javascript/example/bundle/index.html>`_
 * `在 RViz 中查看 SDF 模型 <https://github.com/Yadunund/view_sdf_rviz>`_
 * `Jupyterlab URDF Viewer <https://github.com/IsabelParedes/jupyterlab-urdf>`_

如果你有一个喜欢的 URDF 工具，请考虑将它添加到上面的列表中！
