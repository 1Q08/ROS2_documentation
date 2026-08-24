.. redirect-from::

    Tutorials/Security/The-Keystore

.. _The-Keystore:

理解安全密钥库
==============

**目标：** 探索位于 ROS 2 安全密钥库中的文件。

**教程级别：** 高级

**耗时：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:


背景
----

在继续之前，请确保你已完成 :doc:`Introducing-ros2-security` 教程。

``sros2`` 包可用于创建启用 ROS 2 安全性所需的密钥、证书和策略。
但是，安全配置极其灵活。
对 ROS 2 安全密钥库的基本理解，将有助于与现有 PKI（公钥基础设施）集成，并按照组织策略管理敏感密钥材料。


安全制品位置
------------

在前面的教程中启用了通信安全，现在让我们看看启用安全性时创建了哪些文件。
正是这些文件使加密成为可能。

``sros2`` 工具（``ros2 security ...``）将文件分为公钥、私钥和 enclave 密钥材料。

ROS 使用环境变量 ``ROS_SECURITY_KEYSTORE`` 定义的目录作为密钥库。
对于本教程，我们使用目录 ``~/sros2_demo/demo_keystore``。


公钥材料
^^^^^^^^

你会在 ``~/sros2_demo/demo_keystore/public`` 的 public 目录中找到三份加密证书；不过，身份和权限证书实际上只是指向证书颁发机构（CA）证书的链接。

在公钥基础设施中，`证书颁发机构 <https://en.wikipedia.org/wiki/Certificate_authority>`_ 充当信任锚：它验证参与者的身份和权限。
对于 ROS，这意味着所有参与 ROS 图的节点（可能扩展到整个机器人舰队中的每个机器人）。
通过将证书颁发机构的证书（``ca.cert.pem``）放到机器人上的正确位置，所有 ROS 节点都能与使用同一证书颁发机构的其他节点建立相互信任。

虽然我们在教程中是即时创建证书颁发机构，但在生产系统中，这应按照预先定义的安全计划来完成。
通常，生产系统的证书颁发机构应离线创建，并在初始设置时放置到机器人上。
它可以是每台机器人独有的，也可以在打算互相信任的整个机器人舰队中共享。

DDS（以及延伸至 ROS）支持身份信任链和权限信任链的分离，因此每个功能都有自己的证书颁发机构。
在大多数情况下，ROS 系统安全计划不要求分离这些职责，因此安全工具会生成一个同时用于身份和权限的单一证书颁发机构。

使用 ``openssl`` 查看此 x509 证书并以文本形式显示：

.. code-block:: console

  $ cd ~/sros2_demo/demo_keystore/public
  $ openssl x509 -in ca.cert.pem -text -noout

输出应该类似于以下内容::

  Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            02:8e:9a:24:ea:10:55:cb:e6:ea:e8:7a:c0:5f:58:6d:37:42:78:aa
        Signature Algorithm: ecdsa-with-SHA256
        Issuer: CN = sros2CA
        Validity
            Not Before: Jun  1 16:57:37 2021 GMT
            Not After : May 31 16:57:37 2031 GMT
        Subject: CN = sros2CA
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key: (256 bit)
                pub:
                    04:71:e9:37:d7:32:ba:b8:a0:97:66:da:9f:e3:c4:
                    08:4f:7a:13:59:24:c6:cf:6a:f7:95:c5:cd:82:c0:
                    7f:7f:e3:90:dd:7b:0f:77:d1:ee:0e:af:68:7c:76:
                    a9:ca:60:d7:1e:2c:01:d7:bc:7e:e3:86:2a:9f:38:
                    dc:ed:39:c5:32
                ASN1 OID: prime256v1
                NIST CURVE: P-256
        X509v3 extensions:
            X509v3 Basic Constraints: critical
                CA:TRUE, pathlen:1
    Signature Algorithm: ecdsa-with-SHA256
         30:45:02:21:00:d4:fc:d8:45:ff:a4:51:49:98:4c:f0:c4:3f:
         e0:e7:33:19:8e:31:3c:d0:43:e7:e9:8f:36:f0:90:18:ed:d7:
         7d:02:20:30:84:f7:04:33:87:bb:4f:d3:8b:95:61:48:df:83:
         4b:e5:92:b3:e6:ee:3c:d5:cf:30:43:09:04:71:bd:dd:7c

关于此 CA 证书需要注意的几点：
 - 证书主题名 ``sros2CA`` 是 ``sros2`` 工具提供的默认名称。
 - 此证书自创建之时起有效期为十年。
 - 与所有证书一样，它包含一个用于公钥-私钥加密的公钥。
 - 作为根证书颁发机构，这是一个 `自签名证书 <https://en.wikipedia.org/wiki/Self-signed_certificate>`_；也就是说，它使用自己的私钥进行签名。

由于这是一份公开证书，可以按需自由复制，以便在整个 ROS 系统中建立信任。


私钥材料
^^^^^^^^

私钥材料可以在密钥库目录 ``~/sros2_demo/demo_keystore/private`` 中找到。
与 ``public`` 目录类似，它包含一个证书颁发机构密钥 ``ca.key.pem`` 以及指向它的符号链接，分别用作身份 CA 私钥和权限 CA 私钥。

.. warning::

  保护好此私钥，并为其创建一个安全的备份！

这是与作为 ROS 系统中所有安全性锚点的公开证书颁发机构相关联的私钥。
你将使用它来修改 ROS 图的加密策略并添加新的 ROS 参与者。
根据机器人安全需求，该密钥可以通过访问权限加以保护，并锁定给另一个账户，或者可以将其完全移出机器人，放到另一个系统或设备上。
如果该文件丢失，你将无法更改访问权限，也无法向系统添加新参与者。
同样地，任何能访问该文件的用户或进程都有能力修改系统策略和参与者。

此文件仅在配置机器人时需要，机器人运行并不需要它。
它可以安全地离线存储在另一个系统或可移动介质中。

``sros2`` 工具使用 `椭圆曲线加密 <https://en.wikipedia.org/wiki/Elliptic-curve_cryptography>`_ 而不是 RSA，以提高安全性并减小密钥大小。
使用以下命令查看此椭圆曲线私钥的详细信息：


.. code-block:: console

  $ cd ~/sros2_demo/demo_keystore/private
  $ openssl ec -in ca.key.pem -text -noout
  read EC key
  Private-Key: (256 bit)
  priv:
      93:da:76:b9:e3:91:ab:e9:42:76:f2:38:f1:9d:94:
      90:5e:b5:96:7b:7f:71:ee:13:1b:d4:a0:f9:48:fb:
      ae:77
  pub:
      04:71:e9:37:d7:32:ba:b8:a0:97:66:da:9f:e3:c4:
      08:4f:7a:13:59:24:c6:cf:6a:f7:95:c5:cd:82:c0:
      7f:7f:e3:90:dd:7b:0f:77:d1:ee:0e:af:68:7c:76:
      a9:ca:60:d7:1e:2c:01:d7:bc:7e:e3:86:2a:9f:38:
      dc:ed:39:c5:32
  ASN1 OID: prime256v1
  NIST CURVE: P-256

除了私钥本身之外，请注意公钥也被列出，并且它与证书颁发机构 ``ca.cert.pem`` 中列出的公钥一致。


域治理策略
^^^^^^^^^^

在密钥库内的 enclave 目录 ``~/sros2_demo/demo_keystore/enclaves`` 中找到域治理策略。
``enclave`` 目录包含 XML 治理策略文档 ``governance.xml``，以及一份由权限 CA 签名的文档副本 ``governance.p7s``。

``governance.p7s`` 文件包含域范围内的设置，例如如何处理未认证的参与者、是否加密发现过程，以及主题访问的默认规则。

使用以下命令验证治理文件的 `S/MIME 签名 <https://en.wikipedia.org/wiki/S/MIME>`_：

.. code-block:: console

  $ openssl smime -verify -in governance.p7s -CAfile ../public/permissions_ca.cert.pem

此命令会打印出 XML 文档，最后一行将是 ``Verification successful``，表示该文档已由权限 CA 正确签名。


安全 enclave
^^^^^^^^^^^^

安全进程（通常是 ROS 节点）在安全 enclave 中运行。
在最简单的情况下，所有进程可以合并到同一个 enclave 中，这样所有进程都将使用相同的安全策略。
但是，要对不同进程应用不同策略，进程可以在启动时使用不同的安全 enclave。
有关安全 enclave 的更多详细信息，请参阅 `设计文档 <https://design.ros2.org/articles/ros2_security_enclaves.html>`_。
运行节点时，通过 ROS 参数 ``--enclave`` 指定安全 enclave。

**每个安全 enclave 需要六个文件** 才能启用安全性。
每个文件 **必须** 按如下定义的名称命名，并遵循 `DDS Security 标准 <https://www.omg.org/spec/DDS-SECURITY/1.1/About-DDS-SECURITY/>`_ 的规定。
为了避免同一文件有多个副本，``sros2`` 工具为每个 enclave 创建指向单一治理策略、身份 CA 和上述权限 CA 的链接。

查看 ``listener`` enclave 中的以下六个文件。
其中三个是该 enclave 特有的，而另外三个是这个 ROS 系统通用的：

 - ``key.pem``，用于在此 enclave 内加密和解密的私钥
 - ``cert.pem``，此 enclave 的公开证书；此证书已由身份 CA 签名
 - ``permissions.p7s``，此 enclave 的权限；此文件已由权限 CA 签名
 - ``governance.p7s``，指向此域签名安全策略文件的链接
 - ``identity_ca.cert.pem``，指向此域身份 CA 的链接
 - ``permissions_ca.cert.pem``，指向此域权限 CA 的链接

私有加密密钥 ``key.pem`` 应根据你的安全计划加以保护。
此密钥用于加密、解密和验证此特定 enclave 内的通信。
如果密钥丢失或被盗，应吊销该密钥，并为此 enclave 创建新身份。

文件 ``permissions.xml`` 也已在此目录中创建，可用于重新生成已签名的权限文件。
但是，启用安全性并不需要此文件，因为 DDS 使用的是该文件的签名版本。


做个测验！
----------

看看你能否回答这些关于 ROS 安全密钥库的问题。
从一个新的终端会话开始，并使用前一教程中创建的密钥库启用安全性：

.. code-block:: console

  $ export ROS_SECURITY_KEYSTORE=~/sros2_demo/demo_keystore
  $ export ROS_SECURITY_ENABLE=true
  $ export ROS_SECURITY_STRATEGY=Enforce

  $ cd ~/sros2_demo/demo_keystore/enclaves/talker_listener/listener

在开始之前，为 ``permissions.p7s`` 创建一份备份副本。

.. tabs::

  .. group-tab:: 问题 1

    在文本编辑器中打开 ``permissions.p7s``。
    对 XML 内容做一个可忽略的更改（例如添加一个空格或一个空行），然后保存文件。
    启动 listener 节点：

    .. code-block:: console

      $ ros2 run demo_nodes_cpp listener --ros-args --enclave /talker_listener/listener

    你预期会发生什么？

    你能启动 talker 节点吗？

    .. code-block:: console

      $ ros2 run demo_nodes_cpp talker --ros-args --enclave /talker_listener/talker

    启动 listener 和启动 talker 有什么区别？

  .. group-tab:: 答案 1

    listener 无法启动并抛出错误。
    当 ``permissions.p7s`` 文件被修改时（无论多么轻微），该文件的签名就会失效。
    当权限文件无效时，启用了安全性并强制执行的节点将无法启动。

    talker 会按预期启动。
    它使用的是另一个 enclave 中的 ``permissions.p7s`` 文件，该文件仍然有效。

.. tabs::

  .. group-tab:: 问题 2

    什么命令可以让你检查已修改的 ``permissions.p7s`` 文件的签名是否有效？

  .. group-tab:: 答案 2

    使用 ``openssl smime`` 命令检查 ``permissions.p7s`` 是否已由权限 CA 正确签名：

    .. code-block:: console

      $ openssl smime -verify -in permissions.p7s -CAfile permissions_ca.cert.pem

在继续下一个教程之前，请恢复你原始的、已正确签名的 ``permissions.p7s`` 文件。
