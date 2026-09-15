MVSim
=====

这一系列教程将教你如何为 ROS 2 配置 `MVSim <https://mvsimulator.readthedocs.io/>`__ 仿真器。

MVSim 是一个轻量级、开源的多车仿真器，专注于移动机器人的 2D+3D 可视化。
它使用 Box2D 进行 2D 刚体物理仿真，并提供逼真的车辆动力学模型（差速驱动、阿克曼转向），
支持传感器仿真（2D/3D 激光雷达、相机、IMU、GPS）以及原生 ROS 2 集成。
MVSim 特别适合在低计算开销和快速迭代的前提下测试导航、SLAM 和多机器人协作场景。

.. contents:: 目录
   :depth: 2
   :local:

.. toctree::
   :maxdepth: 1

   Installation-Ubuntu
   Getting-Started-MVSim
   Defining-Worlds-MVSim
