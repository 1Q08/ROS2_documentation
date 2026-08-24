.. redirect-from::

    Deploying-ROS2-on-IBM-Cloud
    Tutorials/Deploying-ROS-2-on-IBM-Cloud

在 IBM Cloud Kubernetes 上部署 [社区贡献]
=========================================


.. contents:: 目录
   :depth: 3
   :local:

关于
----

本文介绍如何使用 Docker 文件在 IBM Cloud 上运行 ROS 2。
首先简要概述 docker 镜像及其在本地的运行方式，然后探讨 IBM Cloud 以及用户如何在其上部署容器。
之后，简要介绍用户如何在 IBM Cloud 上使用来自 github 的自己的 ROS 2 自定义软件包。
提供如何创建集群并在 IBM Cloud 上利用 Kubernetes 的演示，最后将 Docker 镜像部署到集群上。
原文发表于 `此处 <https://github.com/mm-nasr/ros2_ibmcloud>`__ 和 `此处 <https://medium.com/@mahmoud-nasr/running-ros2-on-ibm-cloud-1b1284cbd487>`__。

IBM Cloud 上的 ROS 2
--------------------

在本教程中，我们展示如何轻松地将 ROS 2 与你自己的自定义软件包集成并在
IBM Cloud 上运行。

ROS 2 是新一代 ROS，对多机器人编队提供了更多控制。
随着云计算的进步，云机器人在当今时代变得越来越重要。
在本教程中，我们将简要介绍如何在 IBM Cloud 上运行 ROS 2。
到教程结束时，你将能够在 ROS 2 中创建自己的软件包，
并使用 docker 文件将它们部署到云上。

以下说明假设你使用的是 Linux，并且已在
Ubuntu 18.04（Bionic Beaver）上测试过。

第 1 步：设置你的系统
---------------------

在深入介绍具体过程之前，我们先确保所有必需的软件都已正确安装。
我们将为你指向适当的资源来设置你的系统，只强调与我们的用例相关的细节。

a) Docker 文件？
^^^^^^^^^^^^^^^^

Docker 文件是一种可以独立于你的系统运行的容器形式，
这样你就可以设置可能数百个不同的项目，而不会相互影响。
你甚至可以在同一台机器上设置不同版本的 Linux，而无需虚拟机。
Docker 文件的优势在于节省空间，并且仅在运行时使用你的系统资源。
此外，docker 通用且可移植。
它们包含独立运行所需的所有先决条件，
这意味着你可以轻松地为特定的系统或服务使用 docker 文件，而无需任何繁琐的步骤！

兴奋了吗？
让我们先按照下面的 `链接 <https://docs.docker.com/get-docker/>`__ 将 docker 安装到你的系统。
从教程中，你应该已经做了一些健全性检查，以确保 docker 已正确设置。
不过为了以防万一，让我们再次运行以下命令，它使用 hello-world docker 镜像：

.. code-block:: console

   $ sudo docker run hello-world
   Hello from Docker!
   This message shows that your installation appears to be working correctly.

   To generate this message, Docker took the following steps:
    1. The Docker client contacted the Docker daemon.
    2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
       (amd64)
    3. The Docker daemon created a new container from that image which runs the
       executable that produces the output you are currently reading.
    4. The Docker daemon streamed that output to the Docker client, which sent it
       to your terminal.

   To try something more ambitious, you can run an Ubuntu container with:
    $ docker run -it ubuntu bash

   Share images, automate workflows, and more with a free Docker ID:
    https://hub.docker.com/

   For more examples and ideas, visit:
    https://docs.docker.com/get-started/

b) ROS 2 镜像
^^^^^^^^^^^^^

ROS 于 2019 年 1 月为多个 ROS 发行版
`宣布 <https://discourse.openrobotics.org/t/announcing-official-docker-images-for-ros2/7381/2>`__ 了镜像容器。
有关 ROS 2 docker 镜像使用的更详细说明可在
`此处 <https://hub.docker.com/_/ros/>`__ 找到。

让我们跳过这些，直接进入正题；创建一个本地 ROS 2 docker。
我们将创建自己的 Dockerfile（而不是使用现成镜像），因为我们在 IBM Cloud 上部署时需要这种方法。
首先，我们创建一个新目录来存放我们的 Dockerfile 以及稍后需要的任何其他文件，并导航到它。
使用你喜欢的 $EDITOR，打开一个名为 *Dockerfile* 的新文件（确保文件名正确）：

.. code-block:: console

   $ mkdir ~/ros2_docker

   $ cd ~/ros2_docker

   $ $EDITOR Dockerfile

在 *Dockerfile* 中插入以下内容并保存（也可在
`此处 <https://github.com/mm-nasr/ros2_ibmcloud/blob/main/dockers/ros2_basic/Dockerfile>`__ 找到）：

.. code-block:: bash

   FROM ros:foxy

   # install ros package
   RUN apt-get update && apt-get install -y \
         ros-${ROS_DISTRO}-demo-nodes-cpp \
         ros-${ROS_DISTRO}-demo-nodes-py && \
       rm -rf /var/lib/apt/lists/* && mkdir /ros2_home

   WORKDIR /ros2_home

   # launch ros package
   CMD ["ros2", "launch", "demo_nodes_cpp", "talker_listener_launch.py"]

-  **FROM**：从 ros:foxy Docker 镜像创建一层
-  **RUN**：通过在其中安装 vim 并创建一个名为 /ros2_home 的目录来构建你的容器
-  **WORKDIR**：告知容器其工作目录应在哪里

当然，你可以自由更改 ROS 发行版（此处使用 *foxy*）或更改目录名。
上面的 docker 文件设置了 ROS-foxy，并安装了 C++ 和 Python 的演示节点。
然后启动一个运行 talker 和 listener 节点的文件。
我们稍后就会看到它的实际运行，但它们的行为与 `ROS wiki <https://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28c%2B%2B%29>`__ 中发布的发布者-订阅者示例非常相似。

现在，我们准备好构建 docker 镜像以便在其中运行 ROS 2 了（是的，就这么简单！）。

**注意**：如果你因权限不足或 *permission denied* 而出现错误，请尝试使用 *sudo* 权限运行该命令：

.. code-block:: console

   $ docker build .

   ~ You will see a bunch of lines that execute the docker file instructions followed by:

   Successfully built 0dc6ce7cb487

*0dc6ce7cb487* 对你来说很可能不同，因此请记住它并复制到某个地方以备参考。
你可以随时返回并使用以下命令检查系统上的 docker 镜像：

.. code-block:: console

   $ sudo docker ps -as

现在，使用以下命令运行 docker 文件：

.. code-block:: console

   $ docker run -it 0dc6ce7cb487
   [INFO] [launch]: All log files can be found below /root/.ros/log/2020-10-28-02-41-45-177546-0b5d9ed123be-1
   [INFO] [launch]: Default logging verbosity is set to INFO
   [INFO] [talker-1]: process started with pid [28]
   [INFO] [listener-2]: process started with pid [30]
   [talker-1] [INFO] [1603852907.249886590] [talker]: Publishing: 'Hello World: 1'
   [listener-2] [INFO] [1603852907.250964490] [listener]: I heard: [Hello World: 1]
   [talker-1] [INFO] [1603852908.249786312] [talker]: Publishing: 'Hello World: 2'
   [listener-2] [INFO] [1603852908.250453386] [listener]: I heard: [Hello World: 2]
   [talker-1] [INFO] [1603852909.249882257] [talker]: Publishing: 'Hello World: 3'
   [listener-2] [INFO] [1603852909.250536089] [listener]: I heard: [Hello World: 3]
   [talker-1] [INFO] [1603852910.249845718] [talker]: Publishing: 'Hello World: 4'
   [listener-2] [INFO] [1603852910.250509355] [listener]: I heard: [Hello World: 4]
   [talker-1] [INFO] [1603852911.249506058] [talker]: Publishing: 'Hello World: 5'
   [listener-2] [INFO] [1603852911.250152324] [listener]: I heard: [Hello World: 5]
   [talker-1] [INFO] [1603852912.249556670] [talker]: Publishing: 'Hello World: 6'
   [listener-2] [INFO] [1603852912.250212678] [listener]: I heard: [Hello World: 6]

如果它正常工作，你应该会看到与上面类似的内容。
可以看到，有两个 ROS 节点（一个发布者和一个订阅者）正在运行，它们的输出通过 ROS INFO 提供给我们。

第 2 步：在 IBM Cloud 上运行镜像
--------------------------------

以下步骤假设你已拥有 IBM cloud 账户并已安装 ibmcloud CLI。
如果没有，请先查看这个
`链接 <https://cloud.ibm.com/docs/cli/reference/ibmcloud/download_cli.html>`__ 来完成安装。

我们还需要通过运行以下命令确保 IBM Cloud Container Registry 的 CLI 插件已安装

.. code-block:: console

   $ ibmcloud plugin install container-registry

之后，通过终端登录到你的 ibmcloud 账户：

.. code-block:: console

   $ ibmcloud login --sso

从这里开始，让我们创建一个容器注册表命名空间。
确保使用一个独特且能描述其用途的名称。
这里我使用 *ros2nasr*。

.. code-block:: console

   $ ibmcloud cr namespace-add ros2nasr

IBM cloud 有很多快捷方式，可以帮助我们立即将容器部署到云上。
下面的命令构建容器，并将其标记为名称 **ros2foxy** 和版本 **1**。
确保使用你创建的正确注册表名称，并且你可以随意更改容器名称。
末尾的 ``.`` 表示 *Dockerfile* 在当前目录中（这很重要），如果不是，
请将其更改为指向包含 Dockerfile 的目录。

.. code-block:: console

   $ ibmcloud cr build --tag registry.bluemix.net/ros2nasr/ros2foxy:1 .

现在你可以通过运行以下命令确认容器已被推送到你创建的注册表

.. code-block:: console

   $ ibmcloud cr image-list
   Listing images...

   REPOSITORY               TAG   DIGEST         NAMESPACE   CREATED         SIZE     SECURITY STATUS
   us.icr.io/ros2nasr/ros2foxy   1     031be29301e6   ros2nasr    36 seconds ago   120 MB   No Issues

   OK

接下来，登录到你的注册表以运行 docker 镜像是很重要的。
同样，如果你遇到 *permission denied* 错误，请使用 sudo 权限执行该命令。
之后，按如下所示运行你的 docker 文件。

.. code-block:: console

   $ ibmcloud cr login
   Logging in to 'registry.ng.bluemix.net'...
   Logged in to 'registry.ng.bluemix.net'.
   Logging in to 'us.icr.io'...
   Logged in to 'us.icr.io'.

   OK

   $ docker run -v -it registry.ng.bluemix.net/ros2nasr/ros2foxy:1

其中 *ros2nasr* 是你创建的注册表名称，
*ros2foxy:1* 是 docker 容器的标签和版本，如前所述。

现在你应该看到你的 docker 文件正在运行，并提供与你
在本机本地运行它时看到的类似输出。

第 3 步：使用自定义 ROS 2 软件包
--------------------------------

现在我们的完整流程已经跑通了，从创建 Dockerfile，一直到部署它并在 IBM Cloud 上看到它运行。
但是，如果我们想使用我们（或其他人）创建的一组自定义软件包呢？

这一切都与你如何设置 Dockerfile 有关。
让我们使用 ROS 2 在 `此处 <https://hub.docker.com/_/ros/>`__ 提供的示例。
创建一个新目录和新 Dockerfile（或覆盖现有文件），并在其中添加以下内容（或下载
`此处 <https://github.com/mm-nasr/ros2_ibmcloud/blob/main/dockers/git_pkgs_docker/Dockerfile>`__ 的文件）

.. code-block:: bash

   ARG FROM_IMAGE=ros:foxy
   ARG OVERLAY_WS=/opt/ros/overlay_ws

   # multi-stage for caching
   FROM $FROM_IMAGE AS cacher

   # clone overlay source
   ARG OVERLAY_WS
   WORKDIR $OVERLAY_WS/src
   RUN echo "\
   repositories: \n\
     ros2/demos: \n\
       type: git \n\
       url: https://github.com/ros2/demos.git \n\
       version: ${ROS_DISTRO} \n\
   " > ../overlay.repos
   RUN vcs import ./ < ../overlay.repos

   # copy manifests for caching
   WORKDIR /opt
   RUN mkdir -p /tmp/opt && \
       find ./ -name "package.xml" | \
         xargs cp --parents -t /tmp/opt && \
       find ./ -name "COLCON_IGNORE" | \
         xargs cp --parents -t /tmp/opt || true

   # multi-stage for building
   FROM $FROM_IMAGE AS builder

   # install overlay dependencies
   ARG OVERLAY_WS
   WORKDIR $OVERLAY_WS
   COPY --from=cacher /tmp/$OVERLAY_WS/src ./src
   RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
       apt-get update && rosdep install -y \
         --from-paths \
           src/ros2/demos/demo_nodes_cpp \
           src/ros2/demos/demo_nodes_py \
         --ignore-src \
       && rm -rf /var/lib/apt/lists/*

   # build overlay source
   COPY --from=cacher $OVERLAY_WS/src ./src
   ARG OVERLAY_MIXINS="release"
   RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
       colcon build \
         --packages-select \
           demo_nodes_cpp \
           demo_nodes_py \
         --mixin $OVERLAY_MIXINS

   # source entrypoint setup
   ENV OVERLAY_WS $OVERLAY_WS
   RUN sed --in-place --expression \
         '$isource "$OVERLAY_WS/install/setup.bash"' \
         /ros_entrypoint.sh

   # run launch file
   CMD ["ros2", "launch", "demo_nodes_cpp", "talker_listener_launch.py"]

浏览上面显示的代码，我们可以看到如何通过 4 个步骤从 github 添加自定义软件包：

1. 创建一个包含从 Github 克隆的自定义软件包的覆盖层：

.. code-block:: bash

   ARG OVERLAY_WS
   WORKDIR $OVERLAY_WS/src
   RUN echo "\
   repositories: \n\
     ros2/demos: \n\
       type: git \n\
       url: https://github.com/ros2/demos.git \n\
       version: ${ROS_DISTRO} \n\
   " > ../overlay.repos
   RUN vcs import ./ < ../overlay.repos

2. 使用 rosdep 安装软件包依赖

.. code-block:: bash

   # install overlay dependencies
   ARG OVERLAY_WS
   WORKDIR $OVERLAY_WS
   COPY --from=cacher /tmp/$OVERLAY_WS/src ./src
   RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
       apt-get update && rosdep install -y \
         --from-paths \
           src/ros2/demos/demo_nodes_cpp \
           src/ros2/demos/demo_nodes_py \
         --ignore-src \
       && rm -rf /var/lib/apt/lists/*

3. 构建 *你需要的* 软件包

.. code-block:: bash

   # build overlay source
   COPY --from=cacher $OVERLAY_WS/src ./src
   ARG OVERLAY_MIXINS="release"
   RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
       colcon build \
         --packages-select \
           demo_nodes_cpp \
           demo_nodes_py \
         --mixin $OVERLAY_MIXINS

4. 运行 launch 文件

.. code-block:: bash

   # run launch file
   CMD ["ros2", "launch", "demo_nodes_cpp", "talker_listener_launch.py"]

同样，我们可以更改使用的软件包，安装它们的依赖，然后运行它们。

**回到 IBM Cloud**

使用这个 Dockerfile，我们可以按照之前相同的步骤将其部署到 IBM Cloud 上。
由于我们已经创建了注册表并且已登录 IBM Cloud，因此可以直接构建新的 Dockerfile。
注意我是如何保持标签相同但更改了版本的，这样我就可以更新之前创建的 docker 镜像。
（如果你愿意，可以随意创建一个全新的）

.. code-block:: console

   $ ibmcloud cr build --tag registry.bluemix.net/ros2nasr/ros2foxy:2 .

然后，确保你已登录到注册表并运行新的 docker 镜像：

.. code-block:: console

   $ ibmcloud cr login
   Logging in to 'registry.ng.bluemix.net'...
   Logged in to 'registry.ng.bluemix.net'.
   Logging in to 'us.icr.io'...
   Logged in to 'us.icr.io'.

   OK

   $ docker run -v -it registry.ng.bluemix.net/ros2nasr/ros2foxy:2

你应该再次看到相同的输出。
不过，这次我们是通过来自 github 的自定义软件包完成的，这使我们能够在 IBM Cloud 上使用我们为 ROS 2 个人创建的软件包。

额外内容：删除 Docker 镜像
^^^^^^^^^^^^^^^^^^^^^^^^^^

当你发现需要从 IBM Cloud 删除特定的 docker 镜像时，应该这样做！

1. 列出你拥有的所有镜像，找到所有共享
   *IMAGE* 名称对应于
   *registry.ng.bluemix.net/ros2nasr/ros2foxy:2*（在我的例子中）的镜像。
   然后使用它们的 *NAMES* 删除它们

.. code-block:: console

   $ docker rm your_docker_NAMES

2. 使用其 *IMAGE* 名称从 IBM Cloud 删除 docker 镜像

.. code-block:: console

   $ docker rmi registry.ng.bluemix.net/ros2nasr/ros2foxy:2

第 4 步：Kubernetes
-------------------

a) 创建集群
^^^^^^^^^^^

使用控制台创建集群。
说明见 `此处 <https://cloud.ibm.com/docs/containers?topic=containers-clusters#clusters_ui>`__。
使用的设置详见下文。
这些仅是建议，如果你需要可以更改。
但是，请确保你理解所选选项的含义：

1. 计划：*Standard*

2. 编排服务：*Kubernetes v1.18.10*

3. 基础设施：*Classic*

4. 位置：

-  资源组：*Default*

-  地域：*North America* （你可以自由更改）

-  可用性：*Single zone*
   （你可以自由更改，但请确保通过查阅 IBM Cloud 文档了解所选选项的影响。）

-  工作区域：*Toronto 01* （选择物理上离你最近的位置）

5. 工作节点池：

-  虚拟 - 共享，Ubuntu 18

-  内存：16 GB

-  每个区域的工作节点数：*1*

6. 主服务端点：*私有和公共端点*

7. 资源详情（完全灵活）：

-  集群名称：*mycluster-tor01-rosibm*

-  标签：*version:1*

创建集群后，你将重定向到一个页面，该页面详细介绍了如何设置 CLI 工具并访问你的集群。
请按照这些说明操作（或查看 `此处 <https://github.com/mm-nasr/ros2_ibmcloud/blob/main/Kubernetes-Cluster-Set-up.md>`__ 的说明）
并等待进度条显示你创建的工作节点已准备就绪，在集群名称旁边显示 *Normal*。
你也可以从 Kubernetes 内的 IBM Cloud 控制台进入此屏幕。

b) 部署你的 Docker 镜像 *终于到了！*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. 使用你喜欢的 $EDITOR 创建一个名为
   *ros2-deployment.yaml* 的部署配置 yaml 文件，并在其中插入以下内容：

.. code-block:: bash

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: <deployment>
   spec:
     replicas: <number_of_replicas>
     selector:
       matchLabels:
         app: <app_name>
     template:
       metadata:
         labels:
           app: <app_name>
       spec:
         containers:
         - name: <app_name>
           image: <region>.icr.io/<namespace>/<image>:<tag>

你应该按照
`此处 <https://cloud.ibm.com/docs/containers?topic=containers-images#namespace>`__ 所述替换 *"<" ">"* 之间显示的标签。
在我的例子中，文件看起来像这样：

.. code-block:: bash

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: ros2-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: ros2-ibmcloud
     template:
       metadata:
         labels:
           app: ros2-ibmcloud
       spec:
         containers:
         - name: ros2-ibmcloud
           image: us.icr.io/ros2nasr/ros2foxy:2

使用以下命令部署该文件

.. code-block:: console

   $ kubectl apply -f ros2-deployment.yaml
   deployment.apps/ros2-deployment created

现在你的 docker 镜像已完全部署到你的集群上！

第 5 步：为你的 Docker 镜像使用 CLI
-----------------------------------

1. 通过 IBM Cloud 控制台 Kubernetes 导航到你的集群。

2. 点击页面右上角的 *Kubernetes dashboard*。

现在你应该能够看到集群所有不同参数的完整列表，以及其 CPU 和内存使用情况。

3. 导航到 *Pods* 并点击你的部署。

4. 在右上角，点击 *Exec into pod*

现在你就在你的 docker 镜像内部了！
你可以 source 你的工作空间（如果需要）并运行 ROS 2！
例如：

.. code-block:: console

   root@ros2-deployment-xxxxxxxx:/opt/ros/overlay_ws# . install/setup.sh
   root@ros2-deployment-xxxxxxxx:/opt/ros/overlay_ws# ros2 launch demo_nodes_cpp talker_listener_launch.py

最终说明
--------

至此，你已经能够使用 github 上的 ROS 2 软件包创建自己的 docker 镜像。
只需做少量更改，也可以使用本地 ROS 2 软件包。
这可以是另一篇文章的主题。
不过，鼓励你查看以下 `Dockerfile <https://github.com/mm-nasr/ros2_ibmcloud/tree/main/dockers/local_pkgs_docker>`__，它使用了 demos 仓库的本地副本。
同样，你也可以使用自己的本地软件包。
