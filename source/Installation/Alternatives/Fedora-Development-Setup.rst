.. redirect-from::

  Installation/Fedora-Development-Setup

Fedora（源码）
==============

如何搭建开发环境？
------------------

在 Fedora 上构建 ROS 2 需要以下系统依赖项。
可以使用 ``dnf`` 如下安装它们：

.. code-block:: bash

   sudo dnf install \
     cmake \
     cppcheck \
     eigen3-devel \
     gcc-c++ \
     liblsan \
     libXaw-devel \
     libyaml-devel \
     make \
     opencv-devel \
     patch \
     python3-colcon-common-extensions \
     python3-coverage \
     python3-devel \
     python3-empy \
     python3-nose \
     python3-pip \
     python3-pydocstyle \
     python3-pyparsing \
     python3-pytest \
     python3-pytest-cov \
     python3-pytest-mock \
     python3-pytest-runner \
     python3-rosdep \
     python3-setuptools \
     python3-vcstool \
     poco-devel \
     poco-foundation \
     python3-flake8 \
     python3-flake8-import-order \
     redhat-rpm-config \
     uncrustify \
     wget


完成后，你可以按照剩余的 :ref:`说明 <rhel-dev-get-ros2-code>` 来获取并构建 ROS 2。

