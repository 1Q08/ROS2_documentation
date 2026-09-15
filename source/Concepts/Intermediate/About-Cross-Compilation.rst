.. redirect-from::

   Concepts/About-Cross-Compilation

交叉编译
========

.. contents:: 目录
   :local:

概述
----

Open Robotics 为多种平台提供了预构建的 ROS 2 包，但仍有许多开发者出于各种原因依赖 `交叉编译 <https://en.wikipedia.org/wiki/Cross_compiler>`__，例如：
 - 开发机器与目标系统不一致。
 - 针对特定核心架构调优构建（例如在构建 Raspberry Pi3 时设置 -mcpu=cortex-a53 -mfpu=neon-fp-armv8）。
 - 目标文件系统不是 Open Robotics 发布的预构建镜像所支持的那些。

它是如何工作的？
----------------

交叉编译简单软件（例如不依赖外部库的软件）相对简单，只需用交叉编译器工具链替代本机工具链即可。

有许多因素会让该过程变得更复杂：
 - 所构建的软件必须支持目标架构。
   架构相关的代码必须被正确隔离，并在构建时根据目标架构启用。
   例如汇编代码。
 - 在使用它们的目标软件被交叉编译之前，所有依赖项（例如库）都必须已存在，无论是预构建包还是交叉编译包。
 - 在使用构建工具（例如 colcon）构建软件栈（而非独立软件）时，期望构建工具提供一种机制，让开发者能够在软件栈中各个软件所使用的底层构建系统上启用交叉编译。

替代方案
--------

交叉编译的一种替代方案是使用 ``docker buildx`` `构建多平台 Docker 镜像 <https://github.com/docker/buildx#building-multi-platform-images>`__。
