.. redirect-from::

   Concepts/About-Cross-Compilation

交叉编译
========

.. contents:: 目录
   :local:

概述
----

Open Robotics 为多个平台提供预构建的 ROS 2 包，但仍有许多开发者出于不同原因依赖 `交叉编译 <https://en.wikipedia.org/wiki/Cross_compiler>`__，例如：
 - 开发机器与目标系统不匹配。
 - 针对特定的核心架构调整构建（例如，在为 Raspberry Pi3 构建时设置 -mcpu=cortex-a53 -mfpu=neon-fp-armv8）。
 - 目标文件系统与 Open Robotics 发布的预构建镜像所支持的文件系统不同。

它是如何工作的？
----------------

交叉编译简单的软件（例如，不依赖外部库）相对简单，只需要使用交叉编译工具链来代替原生工具链。

有许多因素会使这个过程变得更加复杂：
 - 被构建的软件必须支持目标架构。
   特定于架构的代码必须根据目标架构在构建过程中被适当地隔离和启用。
   例如汇编代码。
 - 所有依赖（例如库）都必须以预构建或交叉编译包的形式存在，然后才能交叉编译使用它们的软件。
 - 当使用构建工具（例如 colcon）构建软件栈（而不是独立软件）时，构建工具应提供一种机制，使开发者能够在栈中每段软件所使用的底层构建系统上启用交叉编译。

替代方案
--------

交叉编译的一个替代方案是使用 ``docker buildx`` `构建多平台 Docker 镜像 <https://github.com/docker/buildx#building-multi-platform-images>`__。
