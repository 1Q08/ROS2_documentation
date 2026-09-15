.. redirect-from::

   Concepts/About-Domain-ID

ROS_DOMAIN_ID
=============

.. contents:: 目录
   :local:

概述
----

正如其他地方解释的那样，ROS 2 用于通信的默认中间件是 DDS。
在 DDS 中，让不同逻辑网络共享同一物理网络的主要机制称为域 ID（Domain ID）。
处于同一域中的 ROS 2 节点可以自由地发现彼此并发送消息，而不同域中的 ROS 2 节点则不能。
所有 ROS 2 节点默认使用域 ID 0。
为避免同一网络上运行 ROS 2 的不同计算机组之间发生干扰，每组应设定不同的域 ID。

选择域 ID（简版）
-----------------

下文解释了 ROS 2 中应使用的域 ID 范围推导方式。
如果想跳过背景知识而直接选一个安全数字，只需简单地选取 0 到 101（含）之间的域 ID 即可。


选择域 ID（长版）
-----------------

域 ID 用于 DDS 计算发现与通信所使用的 UDP 端口。
参见 `这篇文章 <https://community.rti.com/content/forum-topic/statically-configure-firewall-let-omg-dds-traffic-through>`__，了解端口计算方式的详细说明。
回顾基础网络知识，UDP 端口是 `无符号 16 位整数 <https://en.wikipedia.org/wiki/User_Datagram_Protocol#Ports>`__。
因此，可分配的最大端口号为 65535。
利用上文中公式做一些数学运算，就可知可分配的最大域 ID 为 232，最小域 ID 为 0。

平台相关约束
^^^^^^^^^^^^

为了获得最大兼容性，选择域 ID 时还应遵循一些额外的平台相关约束。
特别是，最好避免将域 ID 分配到操作系统的 `临时端口范围 <https://en.wikipedia.org/wiki/Ephemeral_port>`__ 中。
这样可以避免 ROS 2 节点使用的端口与计算机上其他网络服务产生冲突。

以下是关于临时端口的各平台说明。

.. tabs::

   .. group-tab:: Linux

     默认情况下，Linux 内核将 32768-60999 端口用于临时端口。
     这意味着在不与临时端口冲突的前提下，可以安全使用域 ID 0-101 和 215-232。
     Linux 中临时端口范围可通过设置 ``/proc/sys/net/ipv4/ip_local_port_range`` 中的自定义值来配置。
     如果使用了自定义临时端口范围，上述数字可能需要相应调整。

   .. group-tab:: macOS

     默认情况下，macOS 的临时端口范围是 49152-65535。
     这意味着域 ID 0-166 可以安全使用，而不会与临时端口冲突。
     macOS 中临时端口范围可通过设置自定义 sysctl 值 ``net.inet.ip.portrange.first`` 和 ``net.inet.ip.portrange.last`` 来配置。
     如果使用了自定义临时端口范围，上述数字可能需要相应调整。

   .. group-tab:: Windows

     默认情况下，Windows 的临时端口范围是 49152-65535。
     这意味着域 ID 0-166 可以安全使用，而不会与临时端口冲突。
     Windows 中临时端口范围可通过 `使用 netsh <https://docs.microsoft.com/en-us/troubleshoot/windows-server/networking/default-dynamic-port-range-tcpip-chang>`__ 配置。
     如果使用了自定义临时端口范围，上述数字可能需要相应调整。

参与者约束
^^^^^^^^^^

对于计算机上每个运行中的 ROS 2 进程，会创建一个 DDS “参与者”。
由于每个 DDS 参与者都占用计算机上的两个端口，因此在一台计算机上运行超过 120 个 ROS 2 进程后，可能会溢出到其他域 ID 或临时端口。

为说明原因，考虑域 ID 1 与 2。

- 域 ID 1 使用 7650 和 7651 端口进行组播。
- 域 ID 2 使用 7900 和 7901 端口进行组播。
- 在域 ID 1 中创建第 1 个进程（第 0 个参与者）时，7660 和 7661 端口会用于单播。
- 在域 ID 1 中创建第 120 个进程（第 119 个参与者）时，7898 和 7899 端口会用于单播。
- 在域 ID 1 中创建第 121 个进程（第 120 个参与者）时，7900 和 7901 端口会用于单播，且与域 ID 2 重叠。

如果已知计算机在一段时间内只会位于单个域 ID 中，而且域 ID 足够小，那么上述限制可放宽，允许创建更多 ROS 2 进程。

当选择接近平台特定域 ID 范围上限的域 ID 时，还应额外考虑另一条约束。

例如，假设一台 Linux 计算机的域 ID 为 101：

- 计算机上的第 0 个 ROS 2 进程会连接到 32650、32651、32660 和 32661 端口。
- 第 1 个 ROS 2 进程会连接到 32650、32651、32662 和 32663 端口。
- 第 53 个 ROS 2 进程会连接到 32650、32651、32766 和 32767 端口。
- 第 54 个 ROS 2 进程会连接到 32650、32651、32768 和 32769 端口，进入临时端口范围。

因此，在 Linux 上使用域 ID 101 时，应创建的最大进程数为 54。
同理，在 Linux 上使用域 ID 232 时，最大允许创建的进程数为 63，因为最大端口号是 65535。

macOS 与 Windows 的情况类似，但数字不同。
在 macOS 和 Windows 中，当选择域 ID 166（范围上限）时，若不碰到临时端口范围，最多可在一台计算机上创建 120 个 ROS 2 进程。

域 ID 到 UDP 端口计算器
^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

    <table>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>域 ID:</label></td>
        <td><input type="number" min="0" max="232" size="3" class="display" value="0" id="domainID" onChange="calculate(this.value)"/></td>
      </tr>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>参与者 ID:</label></td>
        <td><input type="number" min="0" size="3" class="display" value="0" id="participantID" onChange="calculate(this.value)"/></td>
      </tr>
    </table>
    <hr/>
    <table>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>发现组播端口:</label></td>
        <td><input type="text" size="5" class="discoveryMulticastPort" disabled/></td>
      </tr>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>用户组播端口:</label></td>
        <td><input type="text" size="5" class="userMulticastPort" disabled/></td>
      </tr>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>发现单播端口:</label></td>
        <td><input type="text" size="5" class="discoveryUnicastPort" disabled/></td>
      </tr>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>用户单播端口:</label></td>
        <td><input type="text" size="5" class="userUnicastPort" disabled/></td>
      </tr>
    </table>
    <br/>
    <br/>

    <script type="text/javascript">
      window.addEventListener('load', (event) => {
         calculate(event);
      });
      const discoveryMcastPort = document.querySelector('.discoveryMulticastPort');
      const userMcastPort = document.querySelector('.userMulticastPort');
      const discoveryUnicastPort = document.querySelector('.discoveryUnicastPort');
      const userUnicastPort = document.querySelector('.userUnicastPort');

      const domainID = document.getElementById('domainID');
      const participantID = document.getElementById('participantID');

      // calculate function
      function calculate(event) {
        const d0 = 0;
        const d2 = 1;
        const d1 = 10;
        const d3 = 11;
        const PB = 7400;
        const DG = 250;
        const PG = 2;

        discoveryMcastPort.value = PB + (DG * domainID.value) + d0;
        userMcastPort.value = PB + (DG * domainID.value) + d2;
        discoveryUnicastPort.value = PB + (DG * domainID.value) + d1 + (PG * participantID.value);
        userUnicastPort.value = PB + (DG * domainID.value) + d3 + (PG * participantID.value);
      }
    </script>
