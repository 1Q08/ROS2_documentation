使用 VSCode 和 Docker 设置 ROS 2 [社区贡献]
===========================================


.. contents:: Contents
    :depth: 2
    :local:


安装 VS Code 和 Docker
----------------------


使用 Visual Studio Code 和 Docker 容器将使你能够运行你最喜欢的 ROS 2 发行版，而无需更改你的操作系统或使用虚拟机。
通过本教程，你可以设置一个 Docker 容器，用于你未来的 ROS 2 项目。


安装 Docker
^^^^^^^^^^^


要安装 Docker 并设置正确的用户权限，请使用以下命令。

.. code-block:: console

    $ sudo apt install docker.io git python3-pip
    $ pip3 install vcstool
    $ echo export PATH=$HOME/.local/bin:$PATH >> ~/.bashrc
    $ source ~/.bashrc
    $ sudo groupadd docker
    $ sudo usermod -aG docker $USER
    $ newgrp docker

现在你可以通过运行以下命令来检查安装是否成功：

.. code-block:: console

    $ docker run hello-world

如果你无法直接运行 hello-world，可能需要先启动 Docker 守护进程：

.. code-block:: console

    $ sudo systemctl start docker

安装 VS Code
^^^^^^^^^^^^

要安装 VS Code，请使用以下命令：

.. code-block:: console

    $ sudo apt update
    $ sudo apt install software-properties-common apt-transport-https wget -y
    $ wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
    $ sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
    $ sudo apt install code


你可以在终端中输入 ``code`` 来运行 VS Code。


安装 Remote Development 扩展
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在 VS Code 的扩展（CTRL+SHIFT+X）中搜索 "Remote Development" 扩展并安装它。


在 Docker 和 VS Code 中配置工作空间
-----------------------------------

添加你的 ROS 2 工作空间
^^^^^^^^^^^^^^^^^^^^^^^

添加一个工作空间，以便在其中构建并在容器中打开它，例如：

.. code-block:: console

    $ cd ~/
    $ mkdir ws
    $ cd ws
    $ mkdir src

现在在你的工作空间根目录中创建一个 ``.devcontainer`` 文件夹，并向该 ``.devcontainer`` 文件夹中添加 ``devcontainer.json`` 和 ``Dockerfile``。
工作空间结构应如下所示：

::

    ws
    ├── .devcontainer
    │   ├── devcontainer.json
    │   └── Dockerfile
    ├── src
        ├── package1
        └── package2


使用 ``File->Open Folder...`` 或 ``Ctrl+K Ctrl+O``，在 VS Code 中打开工作空间的 ``ws`` 文件夹。

为你的环境编辑 ``devcontainer.json``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

为了让 Dev Container 正常工作，我们必须使用正确的用户来构建它。
因此，将以下内容添加到 ``.devcontainer/devcontainer.json``：

.. code-block:: json

    {
        "name": "ROS 2 Development Container",
        "privileged": true,
        "remoteUser": "YOUR_USERNAME",
        "build": {
            "dockerfile": "Dockerfile",
            "args": {
                "USERNAME": "YOUR_USERNAME"
            }
        },
        "workspaceFolder": "/home/ws",
        "workspaceMount": "source=${localWorkspaceFolder},target=/home/ws,type=bind",
        "customizations": {
            "vscode": {
                "extensions":[
                    "ms-vscode.cpptools",
                    "ms-vscode.cpptools-themes",
                    "twxs.cmake",
                    "donjayamanne.python-extension-pack",
                    "eamodio.gitlens",
                    "ms-iot.vscode-ros"
                ]
            }
        },
        "containerEnv": {
            "DISPLAY": "unix:0",
            "ROS_AUTOMATIC_DISCOVERY_RANGE": "LOCALHOST",
            "ROS_DOMAIN_ID": "42"
        },
        "runArgs": [
            "--net=host",
            "--pid=host",
            "--ipc=host",
            "-e", "DISPLAY=${env:DISPLAY}"
        ],
        "mounts": [
           "source=/tmp/.X11-unix,target=/tmp/.X11-unix,type=bind,consistency=cached",
           "source=/dev/dri,target=/dev/dri,type=bind,consistency=cached"
        ],
        "postCreateCommand": "sudo rosdep update && sudo rosdep install --from-paths src --ignore-src -y && sudo chown -R $(whoami) /home/ws/"
    }



使用 ``Ctrl+F`` 打开搜索和替换菜单。
搜索 ``YOUR_USERNAME`` 并将其替换为你的 ``Linux username``。
如果你不知道你的用户名，可以在终端中运行 ``echo $USERNAME`` 来查找。


编辑 ``Dockerfile``
^^^^^^^^^^^^^^^^^^^

打开 Dockerfile 并添加以下内容：


.. code-block:: bash

    FROM ros:ROS_DISTRO
    ARG USERNAME=USERNAME
    ARG USER_UID=1000
    ARG USER_GID=$USER_UID

    # Delete user if it exists in container (e.g Ubuntu Noble: ubuntu)
    RUN if id -u $USER_UID ; then userdel `id -un $USER_UID` ; fi

    # Create the user
    RUN groupadd --gid $USER_GID $USERNAME \
        && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
        #
        # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
        && apt-get update \
        && apt-get install -y sudo \
        && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
        && chmod 0440 /etc/sudoers.d/$USERNAME
    RUN apt-get update && apt-get upgrade -y
    RUN apt-get install -y python3-pip
    ENV SHELL /bin/bash

    # ********************************************************
    # * Anything else you want to do like clean up goes here *
    # ********************************************************

    # [Optional] Set the default user. Omit if you want to keep the default as root.
    USER $USERNAME
    CMD ["/bin/bash"]

将上面的 ``ROS_DISTRO`` 替换为你希望用作基础镜像的 ROS 2 发行版，例如 ``rolling``。


打开并构建开发容器
------------------

使用 ``View->Command Palette...`` 或 ``Ctrl+Shift+P`` 打开命令面板。
搜索命令 ``Dev Containers: Reopen in Container`` 并执行它。
这将为你构建开发 Docker 容器。
这会需要一些时间——放松一下或去喝杯咖啡。


测试容器
^^^^^^^^

要测试一切是否正常工作，使用 ``View->Terminal`` 或 ``Ctrl+Shift+``` 和 VS Code 中的 ``New Terminal`` 在容器中打开一个终端。
在终端内执行以下操作：

.. code-block:: console

    $ sudo apt install ros-$ROS_DISTRO-rviz2 -y
    $ source /opt/ros/$ROS_DISTRO/setup.bash
    $ rviz2

.. Note:: 显示 RVIZ 时可能会出现问题。
          请确保使用 ``xhost +local:<USERNAME>`` 允许用户访问 X 窗口系统。
          如果仍然没有窗口弹出，请检查 ``echo $DISPLAY`` 的值——如果输出是 1，你可以使用 ``echo "export DISPLAY=unix:1" >> /etc/bash.bashrc`` 修复此问题，然后再次测试。
          你也可以在 devcontainer.json 中更改 DISPLAY 值并重新构建它。
