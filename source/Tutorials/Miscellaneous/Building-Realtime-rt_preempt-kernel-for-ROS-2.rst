.. redirect-from::

    Building-Realtime-rt_preempt-kernel-for-ROS-2
    Tutorials/Building-Realtime-rt_preempt-kernel-for-ROS-2

构建实时 Linux 内核 [社区贡献]
==============================

本教程基于在 Intel x86_64 上全新安装的 Ubuntu 20.04.1。
当前内核为 5.4.0-54-generic，但我们将安装最新的稳定版 RT_PREEMPT。
构建内核至少需要 30GB 的可用磁盘空间。

请查看 `此 wiki <https://wiki.linuxfoundation.org/realtime/start>`_ 以获取最新的稳定版本，撰写本文时最新稳定版本为“Latest Stable Version 5.4-rt”。
点击 `该链接 <http://cdn.kernel.org/pub/linux/kernel/projects/rt/5.4/>`_ 即可获得确切的版本号。
目前为 ``patch-5.4.78-rt44.patch.gz``。

.. image:: images/realtime-kernel-patch-version.png

我们在主目录中创建一个目录：

.. code-block:: console

   $ mkdir ~/kernel

然后进入该目录：

.. code-block:: console

   $ cd ~/kernel

我们可以用浏览器打开 `此页面 <https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/>`_ ，查看其中是否有该版本。
你可以从该网站下载它，并手动将其从 /Downloads 移动到 /kernel 文件夹，也可以右键单击链接选择“复制链接地址”，然后使用 wget 下载。
例如：

.. code-block:: console

   $ wget https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.4.78.tar.gz

使用以下命令解压：

.. code-block:: console

   $ tar -xzf linux-5.4.78.tar.gz

从 `kernel.org <http://cdn.kernel.org/pub/linux/kernel/projects/rt/5.4/>`_ 下载与我们刚刚下载的内核版本匹配的 rt_preempt 补丁

.. code-block:: console

   $ wget http://cdn.kernel.org/pub/linux/kernel/projects/rt/5.4/older/patch-5.4.78-rt44.patch.gz

使用以下命令解压：

.. code-block:: console

   $ gunzip patch-5.4.78-rt44.patch.gz

然后进入 linux 目录：

.. code-block:: console

   $ cd linux-5.4.78/

并使用实时补丁为内核打补丁

.. code-block:: console

   $ patch -p1 < ../patch-5.4.78-rt44.patch

我们只想使用 Ubuntu 安装自带的配置，因此用以下命令获取 Ubuntu 配置：

.. code-block:: console

   $ cp /boot/config-5.4.0-54-generic .config

打开 Software & Updates。
在 Ubuntu Software 菜单中勾选“Source code”复选框。

构建内核需要一些工具，安装它们：

.. code-block:: console

   $ sudo apt-get build-dep linux
   $ sudo apt-get install libncurses-dev flex bison openssl libssl-dev dkms libelf-dev libudev-dev libpci-dev libiberty-dev autoconf fakeroot

要启用所有 Ubuntu 配置，只需使用

.. code-block:: console

   $ yes '' | make oldconfig

接下来我们需要在内核中启用 rt_preempt。
执行

.. code-block:: console

   $ make menuconfig

并设置以下选项

.. code-block:: bash

  # Enable CONFIG_PREEMPT_RT
   -> General Setup
    -> Preemption Model (Fully Preemptible Kernel (Real-Time))
     (X) Fully Preemptible Kernel (Real-Time)

  # Enable CONFIG_HIGH_RES_TIMERS
   -> General setup
    -> Timers subsystem
     [*] High Resolution Timer Support

  # Enable CONFIG_NO_HZ_FULL
   -> General setup
    -> Timers subsystem
     -> Timer tick handling (Full dynticks system (tickless))
      (X) Full dynticks system (tickless)

  # Set CONFIG_HZ_1000 (note: this is no longer in the General Setup menu, go back twice)
   -> Processor type and features
    -> Timer frequency (1000 HZ)
     (X) 1000 HZ

  # Set CPU_FREQ_DEFAULT_GOV_PERFORMANCE [=y]
   ->  Power management and ACPI options
    -> CPU Frequency scaling
     -> CPU Frequency scaling (CPU_FREQ [=y])
      -> Default CPUFreq governor (<choice> [=y])
       (X) performance

保存并退出 menuconfig。
现在我们开始构建内核，这将花费相当长的时间。
（在现代 CPU 上需要 10-30 分钟）

.. code-block:: console

   $ make -j `nproc` deb-pkg

构建完成后，检查 deb 软件包

.. code-block:: console

   $ ls ../*deb
   ../linux-headers-5.4.78-rt41_5.4.78-rt44-1_amd64.deb  ../linux-image-5.4.78-rt44-dbg_5.4.78-rt44-1_amd64.deb
   ../linux-image-5.4.78-rt41_5.4.78-rt44-1_amd64.deb    ../linux-libc-dev_5.4.78-rt44-1_amd64.deb

然后安装所有内核 deb 软件包

.. code-block:: console

   $ sudo dpkg -i ../*.deb

现在实时内核应该已经安装完成。
重启系统：

.. code-block:: console

   $ sudo reboot

并检查新的内核版本：

.. code-block:: console

   $ uname -a
   Linux ros2host 5.4.78-rt44 #1 SMP PREEMPT_RT Fri Nov 6 10:37:59 CET 2020 x86_64 xx
