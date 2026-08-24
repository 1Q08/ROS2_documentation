部署指南
========

**目标：** 理解将安全制品部署到生产系统时的最佳实践。

**教程级别：** 高级

**耗时：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:


背景
----

典型的部署场景通常涉及将容器化应用或软件包分发到远程系统中。
在部署启用安全性的应用时，应特别小心，需要用户对打包文件的敏感性加以考量。

遵循 `DDS Security 标准 <https://www.omg.org/spec/DDS-SECURITY/1.1/About-DDS-SECURITY/>`_，
``sros2`` 包提供了一组工具，用于在 ROS 2 环境下以高度模块化和灵活的方式管理安全性。

如何组织不同证书、密钥和目录的基本核心指南，仍然是避免危及系统安全的关键因素。
这包括防护意识，以及选择部署到远程生产系统上所需最小文件集以避免安全暴露的标准。

前置条件
--------

* 安装了带有 compose 插件的 docker。
  请参阅 `Docker 安装 <https://docs.docker.com/engine/install/>`_ 和 `Compose 插件 <https://docs.docker.com/compose/install>`_ 中详述的安装步骤。
* （推荐）对 `ROS 2 安全设计 <https://design.ros2.org/articles/ros2_dds_security.html>`_ 有基本了解。
* （推荐）完成前面的安全教程。
  特别是：

    * :doc:`Introducing-ros2-security`
    * :doc:`The-Keystore`
    * :doc:`Access-Controls`

通用指南
--------

ROS 2 利用 DDS Security 扩展来确保同一 enclave 内消息交换的安全性。
enclave 内不同的已签名文件和证书，是由一个受信任的 `证书颁发机构（CA） <https://en.wikipedia.org/wiki/Certificate_authority>`_ 实体的私钥和证书生成的。
事实上，每个 enclave 可以为身份和权限分别选择两个不同的 CA。
这些 CA 制品存储在 `密钥库（Keystore） <https://design.ros2.org/articles/ros2_security_enclaves.html>`_ 的 ``private/`` 和 ``public/`` 子目录中，其文件夹结构如下：

.. code-block:: text

  keystore
  ├── enclaves
  │   └── ...
  │       └── ...
  ├── private
  │   └── ...
  └── public
      └── ...

在生产系统典型部署中，创建和使用某个证书颁发机构的一个良好实践是：

#. 在仅供内部使用的组织系统内创建它。
#. 生成/修改所需的 enclave 时，牢记：

    * 并非所有生成的 enclave 都应部署到所有目标设备。
    * 一个合理的做法是每个应用一个 enclave，从而实现关注点分离。

#. 在设置期间，将 ``public/`` 与对应的 ``enclaves/`` 一起分发到不同的远程生产设备中。
#. 将 ``private/`` 密钥和/或证书请求保留并保护在组织内。

需要注意的是，如果 ``private/`` 文件丢失，将无法再更改访问权限、添加或修改安全配置文件。

此外，还可以考虑进一步的实践：

* 为 ``enclaves/`` 目录内容授予只读权限。
* 如果为生成 enclave 的私钥提供了符合 PKCS#11 的 URI，则可以使用 `硬件安全模块（HSM） <https://en.wikipedia.org/wiki/Hardware_security_module>`_ 来存储它们。

下表总结了前面的陈述，将密钥库目录与推荐位置对应起来：

+-------------+------+----------+------------+
| 目录 / 位置 | 组织 | 目标设备 | 材料敏感度 |
+=============+======+==========+============+
| public      | ✓    | ✓        | 低         |
+-------------+------+----------+------------+
| private     | ✓    | ✕        | 高         |
+-------------+------+----------+------------+
| enclaves    | ✓    | ✓        | 中         |
+-------------+------+----------+------------+



构建一个部署场景
----------------

为了说明一个简单的部署场景，将基于 ``ros:<DISTRO>`` 提供的镜像构建一个新的 docker 镜像。
从这个镜像开始，将创建三个容器，目标是：

* 在本地主机的共享卷中初始化密钥库。
* 模拟两个已部署的远程设备，它们以安全的方式相互交互。

在本示例中，本地主机充当组织系统。
让我们从创建工作区文件夹开始：

.. code-block:: console

  $ mkdir ~/security_gd_tutorial
  $ cd ~/security_gd_tutorial

生成 Docker 镜像
^^^^^^^^^^^^^^^^

为了构建新的 docker 镜像，需要一个 Dockerfile。
要下载本教程提供的 Dockerfile，请运行：

.. code-block:: console

  $ wget https://raw.githubusercontent.com/ros2/ros2_documentation/{DISTRO}/source/Tutorials/Advanced/Security/resources/deployment_gd/Dockerfile

现在，使用以下命令构建 docker 镜像：

.. code-block:: console

  $ docker build -t ros2_security/deployment_tutorial --build-arg ROS_DISTRO={DISTRO} .

理解 compose 文件
^^^^^^^^^^^^^^^^^

compose 配置文件使用一个镜像来创建作为服务的容器。
在本教程中，配置中定义了三个服务：

* *keystore-creator*：与前面的教程类似，它在内部初始化一个新的密钥库目录树。
  这将创建 *enclaves/*、*public/* 和 *private/*，这些在 `ROS 2 Security enclaves <https://design.ros2.org/articles/ros2_security_enclaves.html>`_ 中有更详细的说明。
  ``keystore`` 目录被配置为跨容器共享的卷。

* *listener* 和 *talker*：在本教程中充当远程设备角色。
  所需的 ``Security`` 环境变量以及来自共享卷的必要密钥库文件都会被加载。

compose 配置 yaml 文件可以通过以下方式下载：

.. code-block:: console

  $ wget https://raw.githubusercontent.com/ros2/ros2_documentation/{DISTRO}/source/Tutorials/Advanced/Security/resources/deployment_gd/compose.deployment.yaml

运行示例
--------

在同一工作目录 ``~/security_gd_tutorial`` 中，运行以下命令启动示例：

.. code-block:: console

  $ docker compose -f compose.deployment.yaml up

这应该会产生以下输出：

- *tutorial-listener-1*: ``Found security directory: /keystore/enclaves/talker_listener/listener``
- *tutorial-talker-1*: ``Found security directory: /keystore/enclaves/talker_listener/talker``
- *tutorial-listener-1*: ``Publishing: 'Hello World: <number>'``
- *tutorial-talker-1*: ``I heard: [Hello World: <number>]``

检查容器
^^^^^^^^

在容器运行以模拟本教程中两个远程设备的同时，打开两个不同的终端，分别连接到每个容器。
在第一个终端中运行：

.. code-block:: console

  $ docker exec -it tutorial-listener-1 bash
  $ cd keystore
  $ tree

在第二个终端中运行：

.. code-block:: console

  $ docker exec -it tutorial-talker-1 bash
  $ cd keystore
  $ tree

应该会得到与下面所示类似的输出：

.. code-block:: bash

  # Terminal 1
  keystore
   ├── enclaves
   │   ├── governance.p7s
   │   ├── governance.xml
   │   └── talker_listener
   │       └── listener
   │           ├── cert.pem
   │           ├── governance.p7s
   │           ├── identity_ca.cert.pem
   │           ├── key.pem
   │           ├── permissions_ca.cert.pem
   │           ├── permissions.p7s
   │           └── permissions.xml
   └── public
       ├── ca.cert.pem
       ├── identity_ca.cert.pem
       └── permissions_ca.cert.pem

  # Terminal 2
  keystore
   ├── enclaves
   │   ├── governance.p7s
   │   ├── governance.xml
   │   └── talker_listener
   │       └── talker
   │           ├── cert.pem
   │           ├── governance.p7s
   │           ├── identity_ca.cert.pem
   │           ├── key.pem
   │           ├── permissions_ca.cert.pem
   │           ├── permissions.p7s
   │           └── permissions.xml
   └── public
       ├── ca.cert.pem
       ├── identity_ca.cert.pem
       └── permissions_ca.cert.pem

请注意：

* *private/* 文件夹不会被移动，而是留在本地主机（组织）中。
* 每个已部署的设备都包含其应用所需的最小 enclave。

.. note::

  为了简单起见，在此 enclave 内，身份和权限使用同一个 CA。
