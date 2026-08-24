.. redirect-from::

    Tutorials/Security/Access-Controls

.. _Access-Controls:

设置访问控制
============

**目标：** 限制节点可以使用的主题。

**教程级别：** 高级

**耗时：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:


背景
----

在继续之前，请确保你已完成 :doc:`Introducing-ros2-security` 教程。

权限非常灵活，可用于控制 ROS 图中的许多行为。

对于本教程，我们演示一个仅允许在默认的 ``chatter`` 主题上发布消息的策略。
例如，这可以防止在启动 listener 时重映射主题，或防止将同一安全 enclave 用于其他目的。

为了强制执行此策略，我们需要在启动节点之前更新 ``permissions.xml`` 文件并重新签名。
这可以通过手工修改权限文件，或使用 XML 模板来完成。


修改 ``permissions.xml``
^^^^^^^^^^^^^^^^^^^^^^^^

首先为你的权限文件创建备份，然后打开 ``permissions.xml`` 进行编辑：

.. code-block:: console

  $ cd ~/sros2_demo/demo_keystore/enclaves/talker_listener/talker
  $ mv permissions.p7s permissions.p7s~
  $ mv permissions.xml permissions.xml~
  $ vi permissions.xml

我们将修改 ``<publish>`` 和 ``<subscribe>`` 的 ``<allow_rule>``。
此 XML 文件中的主题使用 DDS 命名格式，而不是 ROS 名称。
有关 ROS 与 DDS 之间主题名映射的详细信息，请参阅 `主题和服务名设计文档 <https://design.ros2.org/articles/topic_and_service_names.html#mapping-of-ros-2-topic-and-service-names-to-dds-concepts>`_。

将以下 XML 内容粘贴到 ``permissions.xml`` 中，保存文件并退出文本编辑器。
这展示了 ``chatter`` 和 ``rosout`` ROS 主题分别重命名为 DDS 的 ``rt/chatter`` 和 ``rt/rosout`` 主题：

.. code-block:: xml
  :emphasize-lines: 15,16,17,18,23,24

  <dds xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.omg.org/spec/DDS-SECURITY/20170901/omg_shared_ca_permissions.xsd">
    <permissions>
      <grant name="/talker_listener/talker">
        <subject_name>CN=/talker_listener/talker</subject_name>
        <validity>
          <not_before>2021-06-01T16:57:53</not_before>
          <not_after>2031-05-31T16:57:53</not_after>
        </validity>
        <allow_rule>
          <domains>
            <id>0</id>
          </domains>
          <publish>
            <topics>
              <topic>rt/chatter</topic>
              <topic>rt/rosout</topic>
              <topic>rt/parameter_events</topic>
              <topic>*/talker/*</topic>
            </topics>
          </publish>
          <subscribe>
            <topics>
              <topic>rt/parameter_events</topic>
              <topic>*/talker/*</topic>
            </topics>
          </subscribe>
        </allow_rule>
        <allow_rule>
          <domains>
            <id>0</id>
          </domains>
          <publish>
            <topics>
              <topic>ros_discovery_info</topic>
            </topics>
          </publish>
          <subscribe>
            <topics>
              <topic>ros_discovery_info</topic>
            </topics>
          </subscribe>
        </allow_rule>
        <default>DENY</default>
      </grant>
    </permissions>
  </dds>

此策略允许 talker 在 ``chatter`` 和 ``rosout`` 主题上发布。
它还包括 talker 节点管理参数所需的发布和订阅权限（这是所有节点的要求）。
发现权限与原始模板保持一致。


签名策略文件
^^^^^^^^^^^^

下一条命令根据更新后的 XML 文件 ``permissions.xml`` 创建新的 S/MIME 签名策略文件 ``permissions.p7s``。
该文件必须使用权限 CA 证书签名，**这需要访问权限 CA 私钥**。
如果私钥已受到保护，则可能需要额外的步骤，根据你的安全计划来解锁并使用它。

.. code-block:: console

  $ openssl smime -sign -text -in permissions.xml -out permissions.p7s \
    --signer permissions_ca.cert.pem \
    -inkey ~/sros2_demo/demo_keystore/private/permissions_ca.key.pem


启动节点
^^^^^^^^

在更新后的权限就位后，我们可以使用与前面教程相同的命令成功启动节点：

.. code-block:: console

  $ ros2 run demo_nodes_cpp talker --ros-args --enclave /talker_listener/talker

然而，尝试重映射 ``chatter`` 主题会阻止节点启动（注意，这要求将 ``ROS_SECURITY_STRATEGY`` 设置为 ``Enforce``）。

.. code-block:: console

  $ ros2 run demo_nodes_cpp talker --ros-args --enclave /talker_listener/talker \
    --remap chatter:=not_chatter


使用模板
^^^^^^^^

安全策略很快就会变得令人困惑，因此 ``sros2`` 工具增加了从模板创建策略的能力。
使用 ``sros2`` 仓库中提供的 `示例策略文件 <https://github.com/ros2/sros2/blob/{REPOS_FILE_BRANCH}/sros2/test/policies/sample.policy.xml#L1>`_ 即可完成。
让我们为 ``talker`` 和 ``listener`` 分别创建一个仅使用 ``chatter`` 主题的策略。

首先，下载包含示例策略文件的 ``sros2`` 仓库：

.. code-block:: console

  $ git clone https://github.com/ros2/sros2.git /tmp/sros2

然后使用 ``create_permission`` 动词并指向示例策略来生成 XML 权限文件：

.. code-block:: console

  $ ros2 security create_permission demo_keystore \
    /talker_listener/talker \
    /tmp/sros2/sros2/test/policies/sample.policy.xml
  $ ros2 security create_permission demo_keystore \
    /talker_listener/listener \
    /tmp/sros2/sros2/test/policies/sample.policy.xml

这些权限文件允许节点仅发布或订阅 ``chatter`` 主题，并启用参数所需的通信。

在一个终端中，如前面的安全教程那样启用安全性，运行 ``talker`` 演示程序：

.. code-block:: console

  $ ros2 run demo_nodes_cpp talker --ros-args -e /talker_listener/talker

在另一个终端中，对 ``listener`` 程序执行相同操作：

.. code-block:: console

  $ ros2 run demo_nodes_py listener --ros-args -e /talker_listener/listener

此时，你的 ``talker`` 和 ``listener`` 节点将使用显式的访问控制列表进行安全通信。
但是，以下让 ``listener`` 节点订阅 ``chatter`` 以外主题的尝试将会失败：

.. code-block:: console

  $ ros2 run demo_nodes_py listener --ros-args --enclave /talker_listener/listener \
    --remap chatter:=not_chatter
