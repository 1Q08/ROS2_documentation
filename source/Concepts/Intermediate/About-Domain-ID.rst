.. redirect-from::

   Concepts/About-Domain-ID

ROS_DOMAIN_ID
=============

.. contents:: 目录
   :local:

概述
----

正如其他地方所解释的，ROS 2 用于通信的默认中间件是 DDS。
在 DDS 中，让不同的逻辑网络共享同一物理网络的主要机制被称为域 ID（Domain ID）。
同一域上的 ROS 2 节点可以自由地相互发现并发送消息，而不同域上的 ROS 2 节点则不能。
默认情况下，所有 ROS 2 节点都使用域 ID 0。
为了避免在同一网络上运行 ROS 2 的不同计算机组之间产生干扰，应为每个组设置不同的域 ID。

选择域 ID（简短版）
-------------------

下面的文字解释了 ROS 2 中应使用的域 ID 范围的推导过程。
若要跳过这些背景知识并直接选择一个安全的数字，只需选择一个介于 0 和 101 之间（含端点）的域 ID。


选择域 ID（详细版）
-------------------

DDS 使用域 ID 来计算用于发现和通信的 UDP 端口。
有关端口如何计算的详细信息，请参阅 `这篇文章 <https://community.rti.com/content/forum-topic/statically-configure-firewall-let-omg-dds-traffic-through>`__。
回顾我们的基础网络知识，UDP 端口是一个 `无符号 16 位整数 <https://en.wikipedia.org/wiki/User_Datagram_Protocol#Ports>`__。
因此，可以分配的最高端口号是 65535。
用上面文章中的公式做一些计算，这意味着可以分配的最高域 ID 是 232，而可以分配的最低域 ID 是 0。

平台特定约束
^^^^^^^^^^^^

为了最大程度的兼容性，在选择域 ID 时应遵循一些额外的平台特定约束。
特别是，最好避免在操作系统的 `临时端口范围 <https://en.wikipedia.org/wiki/Ephemeral_port>`__ 内分配域 ID。
这可以避免 ROS 2 节点使用的端口与计算机上其他网络服务之间的潜在冲突。

以下是一些关于临时端口的平台特定说明。

.. tabs::

   .. group-tab:: Linux

     默认情况下，Linux 内核使用端口 32768-60999 作为临时端口。
     这意味着可以安全地使用域 ID 0-101 和 215-232，而不会与临时端口冲突。
     Linux 中的临时端口范围是可配置的，通过在 ``/proc/sys/net/ipv4/ip_local_port_range`` 中设置自定义值来实现。
     如果使用了自定义临时端口范围，则可能需要相应地调整上述数字。

   .. group-tab:: macOS

     默认情况下，macOS 上的临时端口范围是 49152-65535。
     这意味着可以安全地使用域 ID 0-166，而不会与临时端口冲突。
     macOS 中的临时端口范围是可配置的，通过为 ``net.inet.ip.portrange.first`` 和 ``net.inet.ip.portrange.last`` 设置自定义 sysctl 值来实现。
     如果使用了自定义临时端口范围，则可能需要相应地调整上述数字。

   .. group-tab:: Windows

     默认情况下，Windows 上的临时端口范围是 49152-65535。
     这意味着可以安全地使用域 ID 0-166，而不会与临时端口冲突。
     Windows 中的临时端口范围是可配置的，通过 `使用 netsh <https://docs.microsoft.com/en-us/troubleshoot/windows-server/networking/default-dynamic-port-range-tcpip-chang>`__ 来实现。
     如果使用了自定义临时端口范围，则可能需要相应地调整上述数字。

参与者约束
^^^^^^^^^^

对于在计算机上运行的每个 ROS 2 进程，都会创建一个 DDS“参与者”。
由于每个 DDS 参与者在计算机上占用两个端口，因此在一台计算机上运行超过 120 个 ROS 2 进程可能会溢出到其他域 ID 或临时端口中。

要了解原因，请考虑域 ID 1 和 2。

- 域 ID 1 使用端口 7650 和 7651 进行组播。
- 域 ID 2 使用端口 7900 和 7901 进行组播。
- 在域 ID 1 中创建第 1 个进程（第零个参与者）时，端口 7660 和 7661 用于单播。
- 在域 ID 1 中创建第 120 个进程（第 119 个参与者）时，端口 7898 和 7899 用于单播。
- 在域 ID 1 中创建第 121 个进程（第 120 个参与者）时，端口 7900 和 7901 用于单播，并与域 ID 2 重叠。

如果已知计算机在任何时候都只使用单个域 ID，并且该域 ID 足够低，那么可以安全地创建比这更多的 ROS 2 进程。

在选择接近平台特定域 ID 范围顶部的域 ID 时，还应考虑一个额外的约束。

例如，假设一台 Linux 计算机的域 ID 为 101：

- 计算机上的第零个 ROS 2 进程将连接到端口 32650、32651、32660 和 32661。
- 计算机上的第一个 ROS 2 进程将连接到端口 32650、32651、32662 和 32663。
- 计算机上的第 53 个 ROS 2 进程将连接到端口 32650、32651、32766 和 32767。
- 计算机上的第 54 个 ROS 2 进程将连接到端口 32650、32651、32768 和 32769，进入临时端口范围。

因此，在 Linux 上使用域 ID 101 时，应创建的最大进程数是 54。
类似地，在 Linux 上使用域 ID 232 时，应创建的最大进程数是 63，因为最高端口号是 65535。

macOS 和 Windows 上的情况类似，但数字不同。
在 macOS 和 Windows 上，当选择域 ID 166（范围顶部）时，在进入临时端口范围之前，计算机上可以创建的最大 ROS 2 进程数是 120。

域 ID 到 UDP 端口计算器
^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

    <table>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>Domain ID:</label></td>
        <td><input type="number" min="0" max="232" size="3" class="display" value="0" id="domainID" onChange="calculate(this.value)"/></td>
      </tr>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>Participant ID:</label></td>
        <td><input type="number" min="0" size="3" class="display" value="0" id="participantID" onChange="calculate(this.value)"/></td>
      </tr>
    </table>
    <hr/>
    <table>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>Discovery Multicast Port:</label></td>
        <td><input type="text" size="5" class="discoveryMulticastPort" disabled/></td>
      </tr>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>User Multicast Port:</label></td>
        <td><input type="text" size="5" class="userMulticastPort" disabled/></td>
      </tr>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>Discovery Unicast Port:</label></td>
        <td><input type="text" size="5" class="discoveryUnicastPort" disabled/></td>
      </tr>
      <tr>
        <td style="text-align: right; vertical-align: middle;"><label>User Unicast Port:</label></td>
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
