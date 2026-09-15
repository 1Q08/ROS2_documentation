.. redirect-from::

    Eclipse-Oxygen-with-ROS-2-and-rviz2
    Tutorials/Eclipse-Oxygen-with-ROS-2-and-rviz2

使用 Eclipse Oxygen 与 ``rviz2`` [社区贡献]
===========================================

.. contents:: 目录
   :depth: 1
   :local:

设置
----

本教程假设 Eclipse Oxygen、git 和 `Egit <http://www.eclipse.org/egit/download/>`_ 已经安装。

在整个教程中，我们将 eclipse 工作区命名为与 ros2 软件包相同的名称，但这不是必需的。

提示：我们使用嵌套项目，并为每个 ROS-2 软件包使用一个 Eclipse 工作区。

.. image:: images/eclipse-oxygen-01.png


创建一个 C++ 项目。

.. image:: images/eclipse-oxygen-02.png



.. image:: images/eclipse-oxygen-03.png


选择 ROS 2 软件包名称作为项目名称。
选择一个 Makefile 项目和 Other Toolchain。

.. image:: images/eclipse-oxygen-04.png


点击“完成”

.. image:: images/eclipse-oxygen-05.png


我们的项目应显示在“项目资源管理器”中。

.. image:: images/eclipse-oxygen-06.png


在我们的项目内部创建一个名为“src”的文件夹。

.. image:: images/eclipse-oxygen-07.png


导入一个 git 仓库。

.. image:: images/eclipse-oxygen-08.png


输入仓库 URL。

.. image:: images/eclipse-oxygen-09.png


重要：使用我们之前创建的项目的源文件夹作为目标文件夹。

提示：如果你在选择目标文件夹路径时遇到问题，Eclipse 对话框需要在名称字段中填写一个名称。

.. image:: images/eclipse-oxygen-10.png


使用新项目向导进行导入。

.. image:: images/eclipse-oxygen-11.png


创建一个 General->Project。

.. image:: images/eclipse-oxygen-12.png


使用 git 仓库名称作为项目名称。
重要：使用我们克隆 git 仓库的文件夹作为“位置”。

.. image:: images/eclipse-oxygen-13.png


git 项目和新项目应在项目资源管理器视图中可见。
同一文件被列出多次，但只有一个项目与 Egit 关联。

.. image:: images/eclipse-oxygen-14.png


再次重复此过程。
导入 git 仓库 pluginlib。

.. image:: images/eclipse-oxygen-15.png


重要：使用源文件夹内的一个文件夹作为“目标->目录”。

.. image:: images/eclipse-oxygen-16.png


重要：使用我们克隆 git 仓库的文件夹作为新项目的位置。

.. image:: images/eclipse-oxygen-17.png


对 tinyxml2_vendor git 仓库运行同样的过程。

.. image:: images/eclipse-oxygen-18.png


重要：再次使用源文件夹内的一个文件夹。

.. image:: images/eclipse-oxygen-19.png


重要：使用我们克隆的文件夹位置作为新项目文件夹。

.. image:: images/eclipse-oxygen-20.png


现在所有四个项目都应在项目资源管理器视图中可见。

.. image:: images/eclipse-oxygen-21.png


点击项目资源管理器视图右上角，可以将项目展示改为分层视图。
现在它看起来像是硬盘上的 ROS-2 项目。
但此视图会丢失与 Egit 的关联，因此请使用扁平项目展示。
Egit 关联在你想查看例如哪个作者编写了哪行代码等情况时很有用。

.. image:: images/eclipse-oxygen-22.png


转到“C/C++ 构建”部分，并将“ament”填入“构建命令”。

.. image:: images/eclipse-oxygen-23.png


转到“行为”选项卡，取消勾选“clean”，并在构建文本框中填入“build”。

.. image:: images/eclipse-oxygen-24.png


在“构建项目”能够工作之前，我们需要关闭 Eclipse。
打开一个 shell 并 source ROS-2 的 setup.bash 文件，然后 cd 到 eclipse 项目的目录（这里是 /home/ubu/rviz2_ws/rviz2_ws），并从此目录内启动 Eclipse。

.. image:: images/eclipse-oxygen-25.png


现在代码补全、egit 注解、eclipse C/C++ 工具等都应当正常工作。

.. image:: images/eclipse-oxygen-26.png


Eclipse 索引器
--------------

打开 rviz2 的 main.cpp 可能会显示大量“未解析的包含”警告。
要修复此问题，转到 Project->Properties->C++ General->Path and Symbols。
点击“References”选项卡并选择“ros2_ws”。


.. image:: images/eclipse-oxygen-27.png


转到 C/C++-General->Path-and-Symbols，点击“源位置”选项卡并点击“链接文件夹”。
选择 qt5 包含路径的位置。


.. image:: images/eclipse-oxygen-28.png


应显示下一张图片。
最好向源位置添加排除项，这样某些目录（如“Build”和“Install”）就不会被索引。


.. image:: images/eclipse-oxygen-29.png


转到 C++General->Preprocessor includes，选择“CDT GCC 内置编译器设置 [Shared]”，并在“获取编译器规范的命令”文本框中输入以下内容：

.. code-block:: bash

   -std=c++14


.. image:: images/eclipse-oxygen-30.png


转到“C/C++-General->Indexer”并选择图中所示内容。
例如“将未使用的头文件索引为 c 文件”以解析例如 QApplication，因为 QApplication 头文件的内容仅为 “#include "qapplication.h"”。


.. image:: images/eclipse-oxygen-31.png


运行索引器之后（这会在稍后发生，因此你也会在稍后看到），你可以看到它添加了什么


.. image:: images/eclipse-oxygen-32.png


之后右键点击 rviz2 项目并选择“Indexer->Rebuild”，这将开始重建索引（右下角有一个显示进度的图标）。
一旦索引完成重建，它应能解析所有包含路径。


.. image:: images/eclipse-oxygen-33.png


使用 eclipse 调试
-----------------

转到“C/C++-Build”并在构建命令中添加：

.. code-block:: bash

   -DCMAKE_BUILD_TYPE=Debug


.. image:: images/eclipse-oxygen-34.png


然后在 eclipse 中转到“Run->Debug Configurations”，添加以下内容并点击“Debug”。


.. image:: images/eclipse-oxygen-35.png
