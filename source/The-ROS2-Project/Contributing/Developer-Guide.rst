.. redirect-from::

    Developer-Guide
    Contributing/Developer-Guide

ROS 2 开发者指南
================

.. contents:: 目录
   :depth: 2
   :local:

本页面定义了我们在开发 ROS 2 时所采用的实践与政策。

.. _general-principles:

一般原则
--------

有些原则适用于所有 ROS 2 开发工作：


* **共同所有权：**
  ROS 2 的每一位参与者都应当对整个系统的所有部分都抱有主人翁意识。
  某段代码的原始作者并不拥有任何特殊权限或义务去控制或维护那段代码。
  任何人都可以自由地对任何地方提出修改建议、处理任何类型的工单，以及评审任何拉取请求。
* **乐于承担任何工作：**
  作为共同所有权的一个推论，每个人都应当愿意承担任何可用的任务，并为系统的任何方面做出贡献。
* **主动寻求帮助：**
  如果您在某件事上遇到困难，请向您的开发者同伴寻求帮助，可以通过工单、评论或电子邮件等适当方式进行。

质量实践
--------

根据 `REP 2004：包质量类别 <https://reps.openrobotics.org/rep-2004/>`_ 中的指导原则，软件包可以依据其所遵循的开发实践归属于不同的质量等级。
这些类别因其在版本管理、测试、文档等方面的政策而有所区别。

以下各节是我们为确保核心软件包达到最高质量（“Level 1”）而遵循的具体开发规则。
我们建议所有 ROS 开发者都努力遵循以下政策，以确保整个 ROS 生态系统的质量。

有关更具体的代码建议，请参阅 :doc:`质量指南 <Quality-Guide>` 。

使用生成式 AI
^^^^^^^^^^^^^

在向 ROS 代码或文档做出任何形式的贡献时，您必须遵守 `OSRF 政策 <https://osralliance.org/wp-content/uploads/2025/05/OSRF-Policy-on-the-Use-of-Generative-Tools-Generative-AI-in-Contributions.pdf>`__ 中关于使用生成式 AI 的规定。

这包括那些使用基于现有的人为创作内容训练出来的模型自动生成您贡献内容中任何部分的工具。
它不包括通过标准算法生成内容，或使用适当授权的内容库生成内容的工具。

.. _semver:

版本管理
^^^^^^^^

我们将使用 `语义化版本控制指南 <http://semver.org/>`__ （``semver``）进行版本管理。

我们还将在 ``semver`` 完整含义的基础上遵循一些 ROS 特有的规则：

* 不应在已发布的 ROS 发行版中引入主版本号递增（即破坏性变更）。

  * 补丁版本（保持接口不变）和次版本（非破坏性）递增不会破坏兼容性，因此这类变更 *是* 允许在发行版内进行的。

  * ROS 主版本发布是发布破坏性变更的最佳时机。
    如果某个核心软件包需要多项破坏性变更，它们应当被合并到其集成分支（例如 rolling）中，以便在 CI 中快速发现问题，但应一起发布，以减少 ROS 用户所经历的 ROS 主版本发布次数。

  * 尽管主版本号递增需要新的发行版，但新的发行版并不一定需要主版本号递增（如果开发和发布能够在不破坏 API 的情况下进行的话）。

* 对于编译型代码，ABI 被视为公共接口的一部分。
  任何需要重新编译依赖代码的变更都被视为主版本（破坏性）变更。

  * ABI 破坏性变更 *可以* 在发行版发布 *之前* 的次版本号递增中进行（即进入 rolling 发行版）。

* 即使 Dashing 和 Eloquent 的主版本号组成部分是 ``0``，我们仍然对这两个发行版中的核心软件包强制要求 API 稳定性，尽管 `SemVer 的规范 <https://semver.org/#spec-item-4>`_ 对初始开发阶段另有说明。

  * 因此，软件包应当努力达到成熟状态并提升到 ``1.0.0`` 版本，以符合 ``semver`` 的规范。

注意事项
~~~~~~~~

这些规则是 *尽力而为* 的。
在不太可能的极端情况下，可能有必要在一个主版本/发行版内破坏 API。
未计划内的破坏究竟应递增主版本号还是次版本号，将根据具体情况逐一评估。

例如，考虑这样一种情形：已发布的 X-turtle 对应主版本 ``1.0.0``，而已发布的 Y-turtle 对应主版本 ``2.0.0``。

如果发现在 X-turtle 中必须进行一项破坏 API 的修复，那么显然不能选择递增到 ``2.0.0``，因为 ``2.0.0`` 已经存在。

在这种情况下，处理 X-turtle 版本号的方案有两种，而且都不理想：

1. 递增 X-turtle 的次版本号：不理想，因为它违反了 SemVer 中破坏性变更必须递增主版本号的原则。

2. 将 X-turtle 的主版本号提升到超过 Y-turtle（即 ``3.0.0``）：不理想，因为较旧发行版的版本号会高于较新发行版已经可用的版本号，从而使针对特定版本的条件代码失效或被破坏。

开发者必须自行决定采用哪种方案，或者更重要的是，决定愿意打破哪条原则。
我们无法推荐其中任何一种，但无论采用哪种方案，我们都要求采取明确的措施，手动向用户传达这一破坏性变化及其原因解释（而不仅仅是递增版本号）。

如果没有 Y-turtle，即使该修复在技术上只是一个补丁，X-turtle 也必须递增到 ``2.0.0``。
这种情况符合 SemVer，但违背了我们自己的规则，即不应在已发布的发行版中引入主版本号递增。

这就是为什么我们认为版本管理规则是 *尽力而为* 的。
尽管上面的例子不太可能出现，但准确地定义我们的版本管理系统仍然很重要。

公共 API 声明
~~~~~~~~~~~~~

根据 ``semver``，每个软件包都必须清楚地声明一个公共 API。
我们将使用软件包质量声明中的“公共 API 声明”小节来声明哪些符号属于公共 API 的一部分。

对于大多数 C 和 C++ 软件包而言，声明就是它所安装的任何头文件。
不过，定义一组被视为私有的符号也是可以接受的。
在头文件中避免出现私有符号有助于 ABI 稳定性，但并非强制要求。

对于 Python 等其他语言，必须显式定义公共 API，这样才能清楚地知道哪些符号可以依据版本管理指南被依赖。
公共 API 还可以扩展到构建产物，例如配置变量、CMake 配置文件等，以及可执行程序和命令行选项及输出。
公共 API 的任何元素都应当在软件包的文档中清楚地说明。
如果您正在使用的某个东西没有在软件包文档中被明确列为公共 API 的一部分，那么您就不能依赖它在次版本或补丁版本之间保持不变。

弃用策略
~~~~~~~~

在可能的情况下，我们还将对主版本号递增采用“tick-tock”式的弃用和迁移策略。
新的弃用将在新的发行版中引入，并伴随编译器警告，说明该功能正在被弃用。
在下一个发行版中，该功能将被彻底移除（不再有警告）。

函数 ``foo`` 被弃用并由函数 ``bar`` 替换的示例：

=========  ========================================================
 Version    API
=========  ========================================================
X-turtle   void foo();
Y-turtle   [[deprecated("use bar()")]] void foo(); <br> void bar();
Z-turtle   void bar();
=========  ========================================================

我们不得在发行版发布之后新增弃用。
不过，弃用并不一定需要主版本号递增。
如果次版本号递增发生在发行版发布之前（类似于 ABI 破坏性变更），那么弃用可以在该次版本号递增中引入。

例如，如果 X-turtle 以 ``2.0.0`` 开始开发，那么可以在 X-turtle 发布之前的 ``2.1.0`` 中加入弃用。

我们将尽可能尝试保持各发行版之间的兼容性。
然而，就像与 SemVer 相关的注意事项一样，tick-tock 甚至一般意义上的弃用在某些情况下可能无法完全遵循。

变更控制流程
^^^^^^^^^^^^

* 所有变更都必须经过拉取请求。

* 在 ROSCore 仓库中，我们将在拉取请求上强制执行 `开发者原创认证（DCO） <https://developercertificate.org/>`_ 。

  * 它要求所有提交信息都包含 ``Signed-off-by`` 行，且其电子邮件地址与提交作者一致。

  * 您可以在调用 ``git commit`` 时传入 ``-s`` / ``--signoff`` ，或者手动写入预期的信息（例如 ``Signed-off-by: Your Name Developer <your.name@example.com>``）。

  * 对于仅涉及删除空白、修正拼写错误以及其他 `琐碎变更 <http://cr.openjdk.java.net/~jrose/draft/trivial-fixes.html>`_ 的拉取请求， *不* 要求 DCO。

* 对于每个拉取请求，都要为所有 `第一级平台 <https://reps.openrobotics.org/rep-2000/#support-tiers>`_ 运行 CI 任务，并在拉取请求中附上任务的链接。
  （如果您无权访问 Jenkins 任务，会有人为您触发这些任务。）

* 需要至少 1 位未撰写该拉取请求的开发者同伴批准，才能认为该拉取请求已获批准。
  在合并之前必须获得批准。

  * 软件包可以选择提高这一数字。

向后移植 PR 的指南
~~~~~~~~~~~~~~~~~~

在修改旧版本 ROS 时：

* 在针对旧版本创建向后移植的 PR 之前，请确保相关功能或修复已被接受并合并到 rolling 分支中。
* 向后移植到旧版本时，也请考虑向后移植到任何其他 :doc:`仍受支持的版本 <../../Releases>` ，即使是非 LTS 版本。
* 如果您要完整地向后移植单个 PR，请将向后移植的 PR 标题命名为“[Distro] <name of original PR>”。
* 在向后移植 PR 的描述中链接所有您正在向后移植其变更的 PR。
* 软件包维护者通常会使用 `Mergifyio <https://mergify.com/>`_ 在需要时自动将 PR 向后移植到下游发行版，不过开发者在必要时仍可按上述方式执行手动向后移植操作。

文档
^^^^

所有软件包都应在其 README 中提供以下文档要素，或从 README 链接到这些内容：

* 描述和用途
* 公共 API 的定义和描述
* 示例
* 如何构建和安装（应引用外部工具/工作流）
* 如何构建和运行测试
* 如何构建文档
* 如何开发（对于描述诸如 ``python setup.py develop`` 之类的操作很有用）
* 许可证和版权声明

每个源文件都必须带有许可证和版权声明，并通过自动化的 linter 进行检查。

每个软件包都必须有一个 LICENSE 文件，通常是 Apache 2.0 许可证，除非该软件包已有现成的宽松许可证（例如 rviz 使用三条款 BSD 许可证）。

每个软件包都应尽可能在读者事先不了解 ROS 或其他相关项目的前提下，来描述自身及其用途。

每个软件包都应定义并描述其公共 API，以便用户对语义化版本管理政策所覆盖的范围有合理的预期。
即使在 C 和 C++ 中，公共 API 可以通过 API 和 ABI 检查来强制执行，描述代码的布局以及各部分代码的功能仍然是一个很好的机会。

应当能够轻松地拿到任意一个软件包，并从该软件包的文档中理解如何构建、运行、构建并运行测试，以及构建文档。
显然，对于诸如在工作空间中构建软件包这类常见工作流，我们应避免重复，但基本的工作流应当被描述或引用。

最后，它还应当包含面向开发者的任何文档。
这可能包括使用 ``python setup.py develop`` 之类的方式测试代码的工作流，也可能意味着描述如何利用您的软件包所提供的扩展点。

示例：

* `capabilities <https://docs.ros.org/hydro/api/capabilities/html/>`_

  * 这个示例展示了描述公共 API 的文档

* `catkin_tools <https://catkin-tools.readthedocs.org/en/latest/development/extending_the_catkin_command.html>`_

  * 这是一个描述软件包扩展点的示例

ROS 软件包的 API 文档
~~~~~~~~~~~~~~~~~~~~~

所有已发布的 ROS 软件包的 API 文档都可以 `在这里找到 <https://docs.ros.org/en/{DISTRO}/p/>`__ 。
我们建议使用 `index.ros.org <https://index.ros.org/>`_ 搜索可用的 ROS 软件包以找到它们的文档。

如果您是 ROS 软件包开发者，正在寻找有关为软件包编写文档的指导，请参阅 :doc:`我们关于软件包级文档的“操作指南” <../../How-To-Guides/Documenting-a-ROS-2-Package>` 。
所有已发布的 ROS 2 软件包的文档都会自动托管在 `docs.ros.org <https://docs.ros.org/en/{DISTRO}/p/>`_ 上。

测试
^^^^

所有软件包都应具有某种程度的 :ref:`系统、集成和/或单元测试。<TestingMain>`

**单元测试** 应当始终位于被测试的软件包中，并且应当利用 ``Mock`` 之类的工具，在构造好的场景中尝试测试代码库中较窄的部分。
单元测试不应引入非测试工具的测试依赖项，例如 gtest、nosetest、pytest、mock 等……

**集成测试** 可以测试代码各部分之间，或代码各部分与系统之间的交互。
它们通常以我们期望用户使用软件接口的方式来测试这些接口。
与单元测试一样，集成测试应位于被测试的软件包中，并且除非绝对必要，否则不应引入非工具的测试依赖项。也就是说，所有非工具的依赖项都只应在极为严格的审查下才被允许，因此应尽可能避免。

**系统测试** 旨在测试软件包之间的端到端场景，应当放在它们各自的软件包中，以避免软件包膨胀或耦合，同时避免循环依赖。

一般而言，应尽量减少外部或跨软件包的测试依赖项，以防止循环依赖和测试软件包之间的紧耦合。

所有软件包都应有一些单元测试，可能还有集成测试，但它们应达到的程度取决于该软件包的质量类别。
以下小节适用于“Level 1”软件包：

代码覆盖率
~~~~~~~~~~

我们将提供行覆盖率，并达到 95% 以上的行覆盖率。
如果较低的目标百分比是合理的，则必须显著地记录在文档中。
我们可以提供分支覆盖率，或将代码从覆盖率统计中排除（测试代码、调试代码等）。
我们要求在合并变更之前覆盖率提升或保持不变，不过在给出适当理由的情况下，允许做出降低代码覆盖率的变更（例如删除之前被覆盖的代码可能导致百分比下降）。

性能
~~~~

我们强烈建议进行性能测试，但也认识到它们对某些软件包并不适用。
如果有性能测试，我们将选择检查每次变更、每次发布之前，或两者兼而有之。
我们还将要求对降低性能的变更或发布给出合理的理由。

Linter 与静态分析
~~~~~~~~~~~~~~~~~

我们将使用 :doc:`ROS 代码风格 <Code-Style-Language-Versions>` ，并通过 `ament_lint_common <https://github.com/ament/ament_lint/tree/{REPOS_FILE_BRANCH}/ament_lint_common/doc/index.rst>`_ 中的 linter 来强制执行。
所有属于 ``ament_lint_common`` 的 linter/静态分析工具都必须被使用。

`ament_lint_auto <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_lint_auto/doc/index.rst>`_ 文档提供了有关运行 ``ament_lint_common`` 的信息。

一般实践
--------

有些实践适用于所有 ROS 2 开发工作。

这些实践不会影响 `REP 2004 <https://reps.openrobotics.org/rep-2004/>`_ 中所述的软件包质量等级，但仍然强烈推荐在开发过程中采用。

Issue
^^^^^

提交 issue 时请确保：

- 包含足够的信息，以便他人理解该问题。
  在 ROS 2 中，需要以下要点来缩小问题的成因范围。
  在每一类信息上都尽可能多地尝试各种替代方案进行测试会特别有帮助。

  - **操作系统及其版本。**
    理由：ROS 2 支持多个平台，某些 bug 是特定操作系统/编译器版本所特有的。
  - **安装方式。**
    理由：有些问题只有在 ROS 2 通过二进制归档或 deb 包安装时才会出现。
    这有助于我们判断问题是否出在打包过程中。
  - **具体的 ROS 2 版本。**
    理由：某些 bug 可能存在于特定的 ROS 2 发行版中并在之后被修复。
    了解您的安装是否包含这些修复非常重要。
  - **正在使用的 DDS/RMW 实现** （关于如何确定使用的是哪一个，请参阅 `本页面 <../../Concepts/Intermediate/About-Different-Middleware-Vendors>` ）。
    理由：通信问题可能特定于所使用的底层 ROS 中间件。
  - **正在使用的 ROS 2 客户端库。**
    理由：这有助于我们缩小问题可能出在技术栈中哪一层。

- 包含一份重现该问题的步骤列表。
- 如果是 bug，请考虑提供一个 `简短、自包含、正确（可编译）的示例 <http://sscce.org/>`__ 。
  如果其他人能够轻松重现，问题就更有可能得到解决。

- 说明已经尝试过的故障排查步骤，包括：

  - 升级到最新版本的代码，其中可能包含尚未发布的 bug 修复。
    请参阅 `本小节 <building-from-source>` 并按照说明获取“rolling”分支。
  - 尝试使用不同的 RMW 实现。
    关于如何进行，请参阅 `本页面 <../../How-To-Guides/Working-with-multiple-RMW-implementations>` 。

分支
^^^^

.. note::
    这些只是指导原则。
    由软件包维护者自行选择与其自身工作流相匹配的分支名称。

一个良好的实践是，在软件包的源仓库中，为它针对的每个 ROS 发行版都建立 **独立的分支** 。
这些分支通常以它们所针对的发行版命名。
例如，一个专门针对 Humble 发行版进行开发的 ``humble`` 分支。

发布也从这些分支进行，针对相应的发行版。
针对特定 ROS 发行版的开发可以在相应的分支上进行。
例如：针对 ``foxy`` 的开发提交被提交到 ``foxy`` 分支，而 ``foxy`` 的软件包发布也从同一个分支进行。

.. note::
    这要求软件包维护者视情况执行向后移植或向前移植，以使所有分支都具备最新的功能。
    维护者还必须对所有仍在从其中进行软件包发布的分支执行日常维护（bug 修复等）。

    例如，如果某个功能被合并到 Rolling 专属分支（如 ``rolling`` 或 ``main``），并且该功能也适用于 Humble 发行版（不破坏 API 等），那么良好的实践是将其向后移植到 Humble 专属分支。

    如果有新的功能或 bug 修复可用，维护者可以为那些较旧的发行版进行发布。

**那么** ``main`` **和** ``rolling`` **呢？**

``main`` 通常针对 :doc:`Rolling <../../Releases/Release-Rolling-Ridley>` （因此也针对下一个尚未发布的 ROS 发行版），不过维护者也可以决定改从 ``rolling`` 分支进行开发和发布。

库的版本管理
^^^^^^^^^^^^

我们将对软件包内的所有库统一进行版本管理。
这意味着库的版本继承自软件包。
这样可以防止库和软件包的版本发生偏离，并且与将共享同一仓库的软件包一起发布的政策基于相同的理由。
如果您需要让库具有不同的版本，那么请考虑将它们拆分为不同的软件包。

开发流程
^^^^^^^^

* 默认分支（大多数情况下是 rolling 分支）必须始终能够构建、通过所有测试并且编译无警告。
  如果任何时候出现了回归，首要任务就是至少恢复到之前的状态。
* 始终在启用测试的情况下进行构建。
* 在做出变更之后、在拉取请求中提出变更之前，始终在本地运行测试。
  除了使用自动化测试之外，还要手动运行被修改的代码路径，以确保补丁按预期工作。
* 始终为每个拉取请求在所有平台上运行 CI 任务，并在拉取请求中包含任务的链接。

有关推荐的软件开发工作流的更多细节，请参阅 `软件开发生命周期`_ 一节。

对 RMW API 的变更
^^^^^^^^^^^^^^^^^

在更新 `RMW API <https://github.com/ros2/rmw>`__ 时，要求第一级中间件库的 RMW 实现也一并更新。
例如，向 RMW API 中引入的新函数 ``rmw_foo()`` 必须在以下软件包中实现（截至 ROS Galactic）：

* `rmw_connextdds <https://github.com/ros2/rmw_connextdds>`__
* `rmw_cyclonedds <https://github.com/ros2/rmw_cyclonedds>`__
* `rmw_fastrtps <https://github.com/ros2/rmw_fastrtps>`__

在可行的情况下（例如取决于变更的规模），也应考虑为非第一级中间件库进行更新。
中间件库的列表及其层级请参阅 `REP-2000 <https://reps.openrobotics.org/rep-2000/>`__ 。

任务跟踪
^^^^^^^^

为帮助组织 ROS 2 的工作，ROS 2 核心开发团队使用看板式的 `GitHub 项目板 <https://github.com/orgs/ros2/projects>`_ 。

不过，并非所有 issue 和拉取请求都在项目板上跟踪。
一块项目板通常代表一个即将到来的发布或某个具体项目。
通过浏览 `ROS 2 仓库 <https://github.com/ros2>`_ 各自的 issue 页面，可以按仓库逐个浏览工单。

各个 ROS 2 项目板中列的名称和用途不尽相同，但通常遵循相同的总体结构：

* **To do**：
  与项目相关、可以被分派的 issue
* **In progress**：
  正在进行工作的活跃拉取请求
* **In review**：
  工作已完成并可供评审的拉取请求，以及当前正在积极评审的拉取请求
* **Done**：
  已合并/关闭的拉取请求及相关 issue（仅供参考）

要请求修改权限，只需在您感兴趣的工单上发表评论即可。
根据复杂程度，描述您计划如何解决它可能会有帮助。
我们将更新状态（如果您没有权限的话），之后您就可以开始为拉取请求进行工作了。如果您经常贡献，我们很可能会直接授予您自行管理标签等的权限。

软件包命名规范
^^^^^^^^^^^^^^

名称在 ROS 中扮演着重要角色，遵循命名规范可以简化学习和理解大型系统的过程。

ROS 软件包占用一个扁平命名空间，因此命名应当谨慎且一致。
`REP-144 <https://reps.openrobotics.org/rep-0144/>`__ 中给出了软件包命名的标准

* 软件包名称应遵循常见的 C 变量命名规范：小写、以字母开头、使用下划线分隔，例如 laser_viewer

* 软件包名称应足够具体，以便说明该软件包的功能。
  例如，运动规划器不叫 planner。
  如果它实现了波前传播算法，那么它可能叫 wavefront_planner。
  显然，在让名称足够具体与避免名称过于冗长之间存在张力。

  * 应避免使用诸如 utils 这样的笼统名称，因为它们没有界定哪些内容属于该软件包、哪些内容应在软件包之外。

* 要检查某个名称是否已被占用，请查阅 `<https://index.ros.org/packages/>`__ 。
  如果您希望自己的仓库被纳入该列表，请参阅 `rosdistro 贡献指南 <https://github.com/ros/rosdistro/blob/master/CONTRIBUTING.md>`__ 。

* 我们的目标是为让机器人做有趣的事情而开发一套规范的工具。
  软件包名称应告诉您该软件包做什么，而不是它来自哪里。
  作为一个社区，我们应当能够做到这一点。
  一个 Ubuntu 发行版提供了大约 33,000 个软件包，而名称中并未包含来源或作者信息。

* 只有当软件包不打算被更广泛地使用时，才建议为软件包名称添加前缀（例如，PR2 机器人专用的软件包使用 ``pr2_`` 前缀）。
  在 fork 现有软件包时，您也可以为软件包名称添加前缀，但同样地，该前缀最好能够说明发生了什么变化，而不是谁更改了它。

* 为 ROS 软件包名称添加 'ros' 前缀是多余的。
  除非是非常核心的软件包，否则不建议这样做。

度量单位与坐标系规范
^^^^^^^^^^^^^^^^^^^^

ROS 中使用的标准单位和坐标规范已在 `REP-0103 <https://reps.openrobotics.org/rep-0103/>`__ 中正式确定。
除非有非常充分的理由，并且有非常清晰的文档说明以避免混淆，否则所有消息都应遵循这些准则。

ROS 中距离测量值里诸如“太近”或“太远”这类特殊情况的表示方法，已在 `REP-0117 <https://reps.openrobotics.org/rep-0117/>`__ 中正式确定。

编程规范
^^^^^^^^

* 防御性编程：确保假设尽早得到验证。
  例如，检查每一个返回码，并确保至少抛出异常，直到该情况得到更优雅的处理。
* 所有错误消息都必须输出到 ``stderr`` 。
* 在尽可能最小的作用域中声明变量。
* 使成组的条目（依赖项、导入、包含等）按字母顺序排列。

C++ 专属
~~~~~~~~

* 避免使用直接流式输出（``<<``）到 ``stdout`` / ``stderr`` ，以防止多个线程之间发生交错。
* 避免对 ``std::shared_ptr`` 使用引用，因为这会破坏引用计数。
  如果原始实例离开作用域而引用仍在使用，就会访问已释放的内存。

文件系统布局
^^^^^^^^^^^^

软件包和仓库的文件系统布局应遵循相同的规范，以便为浏览我们源代码的用户提供一致的体验。

软件包布局
~~~~~~~~~~

* ``src``：包含所有 C 和 C++ 代码

  * 也包含未安装的 C/C++ 头文件

* ``include``：包含所有已安装的 C 和 C++ 头文件

  * ``<package name>``：对于所有已安装的 C 和 C++ 头文件，应以软件包名作为文件夹命名空间

* ``<package_name>``：包含所有 Python 代码
* ``test``：包含所有自动化测试和测试数据
* ``config``：包含配置文件，例如 YAML 参数文件和 RViz 配置文件
* ``doc``：包含所有文档
* ``launch``：包含所有 launch 文件
* ``msg``：包含所有 ROS 消息定义
* ``srv``：包含所有 ROS 服务定义
* ``action``：包含所有 ROS 动作定义
* ``package.xml``：如 `REP-0140 <https://reps.openrobotics.org/rep-0140/>`_ 中所定义（在原型开发阶段可以有所调整）
* ``CMakeLists.txt``：仅使用 CMake 的 ROS 软件包需要
* ``setup.py``：仅使用 Python 代码的 ROS 软件包需要
* ``README``：可以在 GitHub 上作为项目的落地页进行渲染

  * 它可以像您希望的那么简短或详细，但至少应链接到项目文档
  * 考虑在此 README 中加入 CI 或代码覆盖率徽章
  * 它也可以是 ``.rst`` 或 GitHub 支持的任何其他格式

* ``CONTRIBUTING``：描述贡献指南

  * 这可能包含许可证方面的说明，例如在使用 Apache 2 许可证时。

* ``LICENSE``：该软件包的一份或多份许可证副本
* ``CHANGELOG.rst``：符合 `REP-0132 <https://reps.openrobotics.org/rep-0132/>`_ 的变更日志

仓库布局
~~~~~~~~

每个软件包都应位于一个与软件包同名的子文件夹中。
如果一个仓库只包含一个软件包，则可以选择将其放在仓库的根目录下。

上游软件包
^^^^^^^^^^

Debian 和 Ubuntu 上游中的软件包
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

得益于 Jochen Sprickerhof 和 Leopold Palomo-Avellaneda 的勤勉努力，部分 `ROS 2 软件包现已可从 Debian 和 Ubuntu 主仓库中获得 <https://wiki.debian.org/DebianScience/Robotics/ROS2/Packages>`_ 。
`这里是 Jochen 在 ROSCon 2015 上对该流程的简要介绍 <https://vimeo.com/142151399#t=29m15s>`_ 。
原始 ROS 软件包已被修改以遵循 Debian 准则，其中包括将软件包拆分为多个部分、在某些情况下更改名称、按照 FHS 准则安装到 /usr，以及对共享库使用 soversions。

此外，一些引导依赖项，例如 ``vcstool`` 和 ``colcon`` 等命令行工具，以及 ``osrf-pycommon`` 和 ``ament`` 等一些库，也已在上游打包。

与 http://packages.ros.org 提供的 OSRF ROS 软件包不同，上游仓库中的软件包并不绑定到特定的 :doc:`ROS 发行版 <../../Releases>` 。
相反，它们代表某一时刻的快照，会在 Debian unstable 中定期更新，然后在各个时间点被锁定到下游的 Debian 和 Ubuntu 发行版中。

不要混用这些来源
~~~~~~~~~~~~~~~~

我们强烈建议不要在同一系统上混用来自上游 Debian/Ubuntu 的 ROS 软件包和来自 http://packages.ros.org 的 ROS 软件包。
在某些情况下，这种混合系统可以正常工作，但这两组软件包之间可能会产生负面的相互影响。
我们正在与 Jochen 及其伙伴合作，通过文档和软件包冲突声明来尽量减少出现问题的可能性，但我们预计仍会存在一些风险，包括一些相当微妙的问题。

因此，我们建议您选择要么从上游安装软件包，要么从 http://packages.ros.org 安装，但不要两者同时使用。
您不仅不应同时从两者安装软件包，而且如果您打算使用上游软件包，那么您的 apt 源中甚至不应存在 http://packages.ros.org 的相关条目（即 ``/etc/apt/sources*`` 下的任何文件中都不应有）。
同时启用两者可能导致两个源之间名称重叠的软件包发生混用，例如 ``python3-rospkg`` 。

已知差异
~~~~~~~~

与来自 packages.ros.org 的 ROS 软件包相比，上游 ROS 软件包存在一些人们应当注意的差异：

* 软件包集合并不完整。
* 软件包可能有不同的名称，并且被以不同的方式划分。

开发者工作流
------------

我们使用 `GitHub 项目板 <https://github.com/orgs/ros2/projects>`_ 来跟踪与即将到来的发布和较大项目相关的未关闭工单和活跃 PR。

通常的工作流是：

* 讨论设计（在相应仓库上提 GitHub 工单，如有需要再向 https://github.com/ros2/design 提交设计 PR）
* 在 fork 的功能分支上编写实现

  * 请查阅 `开发者指南 <Developer-Guide>` 以了解准则和最佳实践

* 编写测试
* 启用并运行 linter
* 使用 ``colcon test`` 在本地运行测试（见 :doc:`colcon 教程 <../../Tutorials/Beginner-Client-Libraries/Colcon-Tutorial>` ）
* 一旦所有内容都能在本地无警告地构建、且所有测试都通过，就在您的功能分支上运行 CI：

  * 前往 ci.ros2.org
  * 登录（右上角）
  * 点击 ``ci_launcher`` 任务
  * 点击 “Build with Parameters”（左列）
  * 在第一个框 “CI_BRANCH_TO_TEST” 中输入您的功能分支名称
  * 点击 ``build`` 按钮

  （如果您不是 ROS 2 提交者，则没有访问 CI 农场的权限。
  在这种情况下，请通知您 PR 的评审者代您运行 CI）

* 如果您的用例需要运行代码覆盖率：

  * 前往 ci.ros2.org
  * 登录（右上角）
  * 点击 ``ci_linux_coverage`` 任务
  * 点击 “Build with Parameters”（左列）
  * 务必让 “CI_BUILD_ARGS” 和 “CI_TEST_ARGS” 保持默认值
  * 点击 ``build`` 按钮
  * 在文档末尾有关于如何 :ref:`解读报告结果 <read-coverage-report>` 和 :ref:`计算覆盖率 <calculate-coverage-rate>` 的说明

* 如果 CI 任务在无警告、无错误、无测试失败的情况下完成构建，请将您的任务链接发布在您的 PR 上，或者发布在汇总您所有 PR 的高层级工单上（参见 `此处 <https://github.com/ros2/rcl/pull/106#issuecomment-271119200>`__ 的示例）

  * 请注意，这些徽章的 markdown 代码位于 ``ci_launcher`` 任务的控制台输出中

* 当 PR 被批准后：

  * 提交 PR 的人使用 “Squash and Merge” 选项将其合并，以便我们保持整洁的历史记录

    * 如果这些提交值得分开保留：将所有吹毛求疵/linter/拼写错误的提交压缩在一起，并合并剩余的部分

      * 注意：每个 PR 都应针对一个特定功能，因此 99% 的情况下 Squash and Merge 是合理的

* 合并后删除该分支

Gitconfig 优化
^^^^^^^^^^^^^^

为了能够推送到仓库，您需要在系统上配置好 ssh 密钥。
然而，我们仓库的默认 url 方案是使用 https，因为它可以被匿名访问。
在您的系统上，您可以使用 ``gitconfig`` 的 ``insteadOf`` 选项，让 ``git`` 即使远程地址声明为 https 也自动使用您的 ssh 密钥。

将以下内容添加到您的 ``~/.gitconfig``

.. code-block::

    [url "ssh://git@github.com/"]
      insteadOf = https://github.com/

如果您在 GitLab 或 Bitbucket 上的仓库中工作，也可以做同样的事情。


架构开发实践
------------

本节描述在对 ROS 2 进行重大架构变更时应采用的理想生命周期。

软件开发生命周期
^^^^^^^^^^^^^^^^

本节逐步描述如何规划、设计和实现一个新功能：

1. 任务创建
2. 编写设计文档
3. 设计评审
4. 实现
5. 代码评审

任务创建
~~~~~~~~

需要对 ROS 2 的关键部分进行变更的任务，应在发布周期的早期阶段进行设计评审。
如果设计评审发生在后期阶段，那么这些变更将成为未来某个发布的一部分。

* 应在相应的 `ros2 仓库 <https://github.com/ros2/>`__ 中创建一个 issue，清楚地描述正在进行的工作。

  * 它应有明确的成功标准，并突出说明期望从中获得的具体改进。
  * 如果该功能针对某个 ROS 发布，请确保在 ROS 发布工单中对其进行跟踪（`示例 <https://github.com/ros2/ros2/issues/607>`__）。

编写设计文档
~~~~~~~~~~~~

设计文档绝不能包含机密信息。
您的变更是否需要设计文档，取决于任务的规模大小。

1. 您正在做一个小改动或修复一个 bug：

  * 不需要设计文档，但应在相应的仓库中创建一个 issue 来跟踪工作并避免重复劳动。

2. 您正在实现一个新功能，或者希望为 OSRF 拥有的基础设施（例如 Jenkins CI）做贡献：

  * 需要设计文档，且应贡献到 `ros2/design <https://github.com/ros2/design/>`__ ，以便在 https://design.ros2.org/ 上公开访问。
  * 您应 fork 该仓库并提交一个详细说明该设计的拉取请求。

  在拉取请求或提交信息中提及相关的 ros2 issue（例如 ``Design doc for task ros2/ros2#<issue id>`` ）。
  详细说明见 `ROS 2 Contribute <https://design.ros2.org/contribute.html>`__ 页面。
  设计评论将直接写在拉取请求上。

如果该任务计划随某个特定版本的 ROS 发布，则此信息应包含在拉取请求中。

设计文档评审
~~~~~~~~~~~~

一旦设计可供评审，就应打开一个拉取请求并指派合适的评审者。
建议将项目负责人——所有受影响软件包的维护者（由 ``package.xml`` 的 maintainer 字段定义，见 `REP-140 <https://reps.openrobotics.org/rep-0140/#required-tags>`__ ）——作为评审者纳入其中。

* 如果设计文档很复杂，或者评审者的日程有冲突，可以组织一次可选的设计评审会议。
  在这种情况下，

  **会议前**

  * 至少提前一周发送会议邀请
  * 建议会议时长为一小时
  * 会议邀请应列出评审期间需要做出的所有决定（需要软件包维护者批准的决定）
  * 会议必需出席者：设计拉取请求的评审者
      会议可选出席者：所有 OSRF 工程师（如果适用）

  **会议中**

  * 任务负责人主持会议，展示自己的想法并管理讨论，以确保按时达成一致

  **会议后**

  * 任务负责人应向所有与会者回传会议记录
  * 如果针对该设计提出了小问题：

    * 任务负责人应根据反馈更新设计文档的拉取请求
    * 不需要额外的评审

  * 如果针对该设计提出了重大问题：

    * 可以删除没有明确一致意见的章节
    * 设计中存在争议的部分可以在将来作为单独的任务重新提交
    * 如果无法删除有争议的部分，请直接与软件包所有者合作以达成一致

* 一旦达成共识：

  * 如果适用，请确保 `ros2/design <https://github.com/ros2/design/>`__ 的拉取请求已被合并
  * 更新并关闭与此设计任务关联的 GitHub issue

实现
~~~~

在开始之前，请查看 :doc:`Contributing-to-code/Making-a-PR` 以了解拉取请求的最佳实践。

* 对于每个要修改的仓库：

  * 修改代码，完成后或定期进入下一步以备份您的工作。
  * 使用 ``git add -i`` 对您的变更进行 `自查 <https://git-scm.com/book/en/v2/Git-Tools-Interactive-Staging>`__ 。
  * 使用 ``git commit -s`` 创建一个新的签名提交。

    * 一个拉取请求应包含数量最少且在语义上有意义的提交（例如，大量单行提交是不可接受的）。
      在根据反馈迭代时创建新的 fixup 提交，或者如果您不想每次都创建新提交，可以使用 ``git commit --amend`` 修改现有提交。
    * 每个提交都必须有写得恰当、有意义的提交信息。
      更多说明见 `此处 <https://chris.beams.io/posts/git-commit/>`__ 。
    * 移动文件必须在单独的提交中完成，否则 git 可能无法准确跟踪文件历史。
    * 拉取请求描述或提交信息中必须包含对相关 ros2 issue 的引用，这样当拉取请求被合并时该 issue 会自动关闭。
      更多细节请参阅此 `文档 <https://help.github.com/articles/closing-issues-using-keywords/>`__ 。
    * 推送新的提交。


构建农场简介
------------

构建农场位于 `ci.ros2.org <https://ci.ros2.org/>`__ 。

每晚我们都会运行夜间任务，在各种平台上以各种场景构建并运行所有测试。
此外，在合并之前，我们会针对这些平台测试所有拉取请求。

请查看 :ref:`当前的目标平台和架构集合 <binary-package-platforms>` ，不过它会随时间演进。

构建农场上有几类任务：

* 手动任务（由开发者手动触发）：

  * ci_linux：在 Ubuntu 上构建 + 测试代码
  * ci_linux-aarch64：在 ARM 64 位机器（aarch64）上的 Ubuntu 中构建 + 测试代码
  * ci_linux_coverage：构建 + 测试 + 生成测试覆盖率
  * ci_linux-rhel：在 Red Hat Enterprise Linux 上构建 + 测试代码
  * ci_windows：在 Windows 上构建 + 测试代码
  * ci_launcher：触发上述所有任务

* 夜间任务（每晚运行）：

  * Debug：使用 CMAKE_BUILD_TYPE=Debug 构建 + 测试代码

    * nightly_linux_debug
    * nightly_linux-aarch64_debug
    * nightly_linux-rhel_debug
    * nightly_win_deb

  * Release：使用 CMAKE_BUILD_TYPE=Release 构建 + 测试代码

    * nightly_linux_release
    * nightly_linux-aarch64_release
    * nightly_linux-rhel_release
    * nightly_win_rel

  * Repeated：构建后将每个测试最多运行 20 次或直至失败（又称“不稳定猎手”）

    * nightly_linux_repeated
    * nightly_linux-aarch64_repeated
    * nightly_linux-rhel_repeated
    * nightly_win_rep

  * Coverage：

    * nightly_linux_coverage：构建 + 测试代码 + 分析 c/c++ 和 python 的覆盖率

      * 结果导出为 cobertura 报告


* packaging（每晚运行；结果被打包成归档文件）：

  * packaging_linux
  * packaging_linux-rhel
  * packaging_windows

另有构建农场通过提供源码包和二进制包的构建、持续集成、测试和分析，为 ROS / ROS 2 生态系统提供支持。

有关详细信息、常见问题和故障排查，请参阅 :doc:`构建农场 <Build-Farms>` 。

关于覆盖率运行的说明
^^^^^^^^^^^^^^^^^^^^

ROS 2 软件包的编排方式使得某个软件包的测试代码不仅包含在该软件包内，也可能存在于另一个软件包中。
换句话说：软件包在测试阶段可以运行属于其他软件包的代码。

要达到 ROS 2 核心软件包中所有代码所达到的覆盖率，建议使用一组固定的拟用仓库来运行构建。
该集合在 Jenkins 中覆盖率任务的默认参数中定义。


.. _read-coverage-report:

如何从构建农场报告中读取覆盖率
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

要查看某个软件包的覆盖率报告：

* 当 ``ci_linux_coverage`` 构建完成后，点击 ``Coverage Report``
* 向下滚动到 ``Coverage Breakdown by Package`` 表格
* 在该表格中，查看第一列名为 “Name” 的列

构建农场中的覆盖率报告包含 ROS 工作空间中用到的所有软件包。
覆盖率报告包含与同一软件包对应的不同路径：

* 形式为： ``src.*.<repository_name>.<package_name>.*`` 的 Name 条目
  这些对应软件包针对其自身源代码运行的单元测试
* 形式为： ``build.<repository_name>.<package_name>.*`` 的 Name 条目
  这些对应软件包针对其构建或配置时生成的文件运行的单元测试
* 形式为： ``install.<package_name>.*`` 的 Name 条目
  这些对应来自其他软件包测试运行的系统/集成测试

.. _calculate-coverage-rate:

如何从构建农场报告计算覆盖率
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

使用自动脚本获取合并后的单元覆盖率：

 * 从 ci_linux_coverage 的 Jenkins 构建中复制该构建的 URL
 * 下载 `get_coverage_ros2_pkg <https://raw.githubusercontent.com/ros2/ci/master/tools/get_coverage_ros2_pkg.py>`__ 脚本
 * 执行该脚本： ``./get_coverage_ros2_pkg.py <jenkins_build_url> <ros2_package_name>`` （ `README <https://github.com/ros2/ci/blob/master/tools/README.md>`__ ）
 * 从脚本输出中最后一行 “Combined unit testing” 获取结果

替代方法：从覆盖率报告获取合并后的单元覆盖率（需要手动计算）：

* 当 ci_linux_coverage 构建完成后，点击 ``Cobertura Coverage Report``
* 向下滚动到 ``Coverage Breakdown by Package`` 表格
* 在该表格中，在第一列 “Name” 下查找（其中 <package_name> 是您正在测试的软件包）：

  * 所有位于 ``src.*.<repository_name>.<package_name>.*`` 模式下的目录，获取 “Lines” 列中的两个绝对值。
  * 所有位于 ``build/.<repository_name>.*`` 模式下的目录，获取 “Lines” 列中的两个绝对值。

* 根据前面的选择：对于每个单元格，第一个值是已测试的行数，第二个是代码总行数。
  汇总所有行，得到已测试的行数总和以及被测代码总行数。
  相除即可得到覆盖率。

.. _measure-coverage-locally:

如何在本地使用 lcov 测量覆盖率（Ubuntu）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

要在您自己的机器上测量覆盖率，请安装 ``lcov`` 。

.. code-block:: console

     $ sudo apt install -y lcov

本节的其余部分假设您在 colcon 工作空间中工作。
使用覆盖率标志进行 debug 编译。
可以随意使用 colcon 标志来针对特定软件包。

.. code-block:: console

     $ colcon build --cmake-args -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS} --coverage" -DCMAKE_C_FLAGS="${CMAKE_C_FLAGS} --coverage"

``lcov`` 需要一个初始基线，您可以使用以下命令生成它。
请根据您的需要更新输出文件位置。

.. code-block:: console

     $ lcov --no-external --capture --initial --directory . --output-file ~/ros2_base.info

对与您的覆盖率测量相关的软件包运行测试。
例如，如果测量 ``rclcpp`` ，同时也测量 ``test_rclcpp``

.. code-block:: console

     $ colcon test --packages-select rclcpp test_rclcpp

使用类似的命令捕获 lcov 结果，这次去掉 ``--initial`` 标志。

.. code-block:: console

     $ lcov --no-external --capture --directory . --output-file ~/ros2.info

合并 trace 文件 ``.info`` ：

.. code-block:: console

     $ lcov --add-tracefile ~/ros2_base.info --add-tracefile ~/ros2.info --output-file ~/ros2_coverage.info

生成 html，以便于可视化和标注已覆盖的行。

.. code-block:: console

    $ mkdir -p coverage
    $ genhtml ~/ros2_coverage.info --output-directory coverage
