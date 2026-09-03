.. redirect-from::

    Developer-Guide
    Contributing/Developer-Guide

ROS 2 开发者指南
================

.. contents:: 目录
   :depth: 2
   :local:

本页定义我们在开发 ROS 2 时所采用的做法和策略。

.. _general-principles:

一般原则
--------

有些原则对所有的 ROS 2 开发都是通用的：


* **共同所有权**：
  每个参与 ROS 2 开发的人都应当对系统的所有部分怀有主人翁意识。
  一段代码的原始作者没有任何特殊的权限或义务来控制或维护那段代码。
  每个人都可以自由地在任何地方提出更改、处理任何类型的工单，以及审查任何 pull request。
* **愿意承担任何工作**：
  作为共同所有权的推论，每个人都应该愿意承担任何可用的任务，并为系统的任何方面做出贡献。
* **寻求帮助**：
  如果在某件事上遇到困难，请通过工单、评论或电子邮件（视情况而定）向其他开发者寻求帮助。

质量实践
--------

软件包可以根据它们所遵循的开发实践，依据 `REP 2004：软件包质量类别 <https://reps.openrobotics.org/rep-2004/>`_ 中的准则，归属于不同的质量级别。
这些类别通过它们在版本控制、测试、文档等方面的策略加以区分。

以下各节是我们遵循的具体开发规则，以确保核心软件包具有最高质量（"1 级"）。
我们建议所有 ROS 开发人员努力遵循以下策略，以确保整个 ROS 生态系统的质量。

有关更具体的代码建议，请参阅 :doc:`质量指南 <Quality-Guide>`。

生成式 AI 的使用
^^^^^^^^^^^^^^^^

在向 ROS 代码或文档做出任何形式的贡献时，你必须遵守有关生成式 AI 使用的 `OSRF 政策 <https://osralliance.org/wp-content/uploads/2025/05/OSRF-Policy-on-the-Use-of-Generative-Tools-Generative-AI-in-Contributions.pdf>`__。

这包括使用在现有人类创作内容上训练的模型，自动创建你贡献的任何部分的工具。
这不包括通过标准算法或经过适当许可的内容库生成内容的工具。

.. _semver:

版本控制
^^^^^^^^

我们将使用 `语义化版本控制准则 <http://semver.org/>`__ （``semver``）进行版本控制。

我们还将在 ``semver`` 完整含义之上遵循一些 ROS 特定规则：

* 在已发布的 ROS 发行版中，不应进行主版本号递增（即破坏性更改）。

  * 补丁（保持接口不变）和次版本（非破坏性）递增不会破坏兼容性，因此这类更改在发行版内*是*允许的。

  * ROS 主版本是发布破坏性更改的最佳时机。
    如果核心软件包需要多个破坏性更改，应将其合并到它们的集成分支（例如 rolling）中，以便在 CI 中快速发现问题，但要一起发布，以减少 ROS 用户的主版本数量。

  * 虽然主版本递增需要新的发行版，但新的发行版不一定需要主版本号提升（如果开发和发布可以在不破坏 API 的情况下完成）。

* 对于编译代码，ABI 被视为公共接口的一部分。
  任何需要重新编译依赖代码的更改都被视为主版本（破坏性）更改。

  * ABI 破坏性更改*可以*在发行版发布之前的次版本号提升中进行（被添加到 rolling 发行版中）。

* 我们在 Dashing 和 Eloquent 中为核心软件包强制执行 API 稳定性，即使它们的主版本组件是 ``0``，尽管 `SemVer 规范 <https://semver.org/#spec-item-4>`_ 对初始开发有相关规定。

  * 随后，软件包应努力达到成熟状态并增加到版本 ``1.0.0``，以符合 ``semver`` 规范。

注意事项
~~~~~~~~

这些规则是*尽力而为*的。
在不太可能的极端情况下，可能有必要在主版本/发行版内破坏 API。
计划外的破坏是递增主版本还是次版本，将根据具体情况进行评估。

例如，考虑这样一种情况：已发布的 X-turtle 对应主版本 ``1.0.0``，已发布的 Y-turtle 对应主版本 ``2.0.0``。

如果确定某个破坏 API 的修复在 X-turtle 中绝对必要，那么提升到 ``2.0.0`` 显然不是一个选项，因为 ``2.0.0`` 已经存在。

在这种情况下处理 X-turtle 版本的解决方案（两者都不理想）是：

1. 提升 X-turtle 的次版本：不理想，因为它违反了 SemVer 的原则，即破坏性更改必须提升主版本。

2. 将 X-turtle 的主版本提升到超过 Y-turtle（到 ``3.0.0``）：不理想，因为较旧发行版的版本会变得比较新发行版已有的版本更高，这将使版本特定的条件代码失效/破坏。

开发者必须决定使用哪种解决方案，或者更重要的是，他们愿意打破哪条原则。
我们无法建议选择哪一种，但在任何一种情况下，我们确实要求采取明确的措施，手动向用户传达这种中断及其解释（而不仅仅是版本递增）。

如果没有 Y-turtle，即使该修复在技术上只是补丁，X-turtle 也必须提升到 ``2.0.0``。
这种情况符合 SemVer，但违反了我们自己的规则，即不应在已发布的发行版中引入主版本递增。

这就是为什么我们认为版本控制规则是*尽力而为*的。
尽管上述示例不太可能发生，但准确定义我们的版本控制系统很重要。

公共 API 声明
~~~~~~~~~~~~~

根据 ``semver``，每个软件包必须清楚地声明公共 API。
我们将使用软件包质量声明的"公共 API 声明"部分来声明哪些符号属于公共 API。

对于大多数 C 和 C++ 软件包，声明是它安装的任何头文件。
然而，定义一组被视为私有的符号也是可以接受的。
避免在头文件中使用私有符号有助于 ABI 稳定性，但并非必需。

对于 Python 等其他语言，公共 API 必须明确定义，以便清楚地知道根据版本控制准则可以依赖哪些符号。
公共 API 也可以扩展到构建工件，如配置变量、CMake 配置文件等，以及可执行文件和命令行选项及输出。
公共 API 的任何元素都应在软件包的文档中清楚说明。
如果你使用的东西没有在软件包的文档中明确列为公共 API 的一部分，那么你就不能依赖它在次版本或补丁版本之间不变。

弃用策略
~~~~~~~~

在可能的情况下，我们还将使用主版本递增的 tick-tock 弃用和迁移策略。
新的弃用将在新的发行版中引入，并伴随编译器警告，表明该功能正在被弃用。
在下一个发行版中，该功能将被完全移除（没有警告）。

函数 ``foo`` 被弃用并由函数 ``bar`` 替换的示例：

=========  ========================================================
 版本       API
=========  ========================================================
X-turtle   void foo();
Y-turtle   [[deprecated("use bar()")]] void foo(); <br> void bar();
Z-turtle   void bar();
=========  ========================================================

在发行版发布之后，我们不得添加弃用。
不过，弃用不一定需要主版本号提升。
如果提升发生在发行版发布之前，弃用可以在次版本号提升中引入（类似于 ABI 破坏性更改）。

例如，如果 X-turtle 以 ``2.0.0`` 开始开发，则可以在 X-turtle 发布之前于 ``2.1.0`` 中添加弃用。

我们将尽可能尝试跨发行版保持兼容性。
然而，与 SemVer 相关的注意事项一样，tick-tock 甚至一般意义上的弃用，在某些情况下可能无法完全遵守。

变更控制流程
^^^^^^^^^^^^

* 所有更改都必须通过 pull request。

* 我们将在 ROSCore 仓库的 pull request 上强制执行 `开发者来源证书 (DCO) <https://developercertificate.org/>`_。

  * 它要求所有提交消息都包含 ``Signed-off-by`` 行，并带有与提交作者匹配的电子邮件地址。

  * 你可以向 ``git commit`` 调用传递 ``-s`` / ``--signoff``，或手动编写预期的消息（例如 ``Signed-off-by: Your Name Developer <your.name@example.com>``）。

  * 对于只处理空白删除、拼写更正和其他 `琐碎更改 <http://cr.openjdk.java.net/~jrose/draft/trivial-fixes.html>`_ 的 pull request，DCO *不* 是必需的。

* 始终为每个 pull request 在所有 `1 级平台 <https://reps.openrobotics.org/rep-2000/#support-tiers>`_ 上运行 CI 作业，并在 pull request 中包含作业链接。
  （如果你无法访问 Jenkins 作业，会有人为你触发这些作业。）

* 至少需要 1 名非 pull request 作者的开发者的批准，才能将其视为已批准。
  合并前必须获得批准。

  * 软件包可以选择增加此数字。

回移 PR 的准则
~~~~~~~~~~~~~~

在更改较旧版本的 ROS 时：

* 在打开将更改回移到较旧版本的 PR 之前，请确保这些功能或修复已在 rolling 分支中被接受并合并。
* 在回移到较旧版本时，还应考虑回移到任何其他 :doc:`仍然受支持的版本 <../../Releases>`，即使是非 LTS 版本。
* 如果你完整地回移单个 PR，请将回移 PR 的标题命名为 "[Distro] <原始 PR 的名称>"。
* 从你的回移 PR 的描述中链接到你所回移更改的所有 PR。
* 软件包维护者通常使用 `Mergifyio <https://mergify.com/>`_ 在需要时自动将 PR 回移到下游发行版，但在必要时，开发者仍可按上述方式执行手动回移操作。

文档
^^^^

所有软件包都应在它们的 README 中，或在从它们的 README 链接到的页面中，包含以下文档元素：

* 描述和目的
* 公共 API 的定义和描述
* 示例
* 如何构建和安装（应引用外部工具/工作流）
* 如何构建和运行测试
* 如何构建文档
* 如何开发（用于描述 ``python setup.py develop`` 之类的内容）
* 许可证和版权声明

每个源文件都必须有许可证和版权声明，并通过自动化 linter 检查。

每个软件包都必须有一个 LICENSE 文件，通常是 Apache 2.0 许可证，除非该软件包有现成的宽松许可证（例如 rviz 使用三条款 BSD）。

每个软件包都应尽可能假设读者是在没有 ROS 或其他相关项目先前知识的情况下偶然发现的，来描述它自身及其目的。

每个软件包都应定义并描述其公共 API，以便用户对语义化版本控制策略所涵盖的内容有合理的预期。
即使在 C 和 C++ 中（公共 API 可以通过 API 和 ABI 检查来强制执行），这也是描述代码布局和代码各部分功能的好机会。

应该很容易地拿到任何软件包，并从该软件包的文档中理解如何构建、运行、构建和运行测试以及构建文档。
显然，我们应避免对常见工作流重复说明，比如在工作空间中构建软件包，但基本工作流应当被描述或引用。

最后，它应包括面向开发者的任何文档。
这可能包括使用 ``python setup.py develop`` 之类的东西测试代码的工作流，或者可能意味着描述如何使用你的软件包提供的扩展点。

示例：

* `capabilities <https://docs.ros.org/hydro/api/capabilities/html/>`_

  * 这个例子给出了描述公共 API 的文档

* `catkin_tools <https://catkin-tools.readthedocs.org/en/latest/development/extending_the_catkin_command.html>`_

  * 这是描述软件包扩展点的示例

ROS 软件包的 API 文档
~~~~~~~~~~~~~~~~~~~~~

所有已发布 ROS 软件包的 API 文档都可以 `在这里找到 <https://docs.ros.org/en/{DISTRO}/p/>`__。
我们建议使用 `index.ros.org <https://index.ros.org/>`_ 搜索可用的 ROS 软件包，以查找它们的文档。

如果你是 ROS 软件包开发者，正在寻找有关记录软件包的指导，请参阅 :doc:`我们关于软件包级文档的"操作指南" <../../How-To-Guides/Documenting-a-ROS-2-Package>`。
所有已发布 ROS 2 软件包的文档都会自动托管在 `docs.ros.org <https://docs.ros.org/en/{DISTRO}/p/>`_ 上。

测试
^^^^

所有软件包都应有一定级别的 :ref:`系统、集成和/或单元测试。<TestingMain>`

**单元测试** 应始终在被测试的软件包中，并应使用 ``Mock`` 之类的工具，在构造的场景中尝试测试代码库的狭窄部分。
单元测试不应引入非测试工具的测试依赖，例如 gtest、nosetest、pytest、mock 等……

**集成测试** 可以测试代码各部分之间或代码各部分与系统之间的交互。
它们通常以我们期望用户使用软件接口的方式来测试这些接口。
与单元测试一样，集成测试应位于被测试的软件包中，除非绝对必要，否则不应引入非工具的测试依赖，即所有非工具依赖只有在极端审查下才应被允许，因此应尽可能避免。

**系统测试** 旨在测试软件包之间的端到端情况，应放在它们自己的软件包中，以避免软件包膨胀或耦合，并避免循环依赖。

一般来说，应尽量减少外部或跨软件包的测试依赖，以防止循环依赖和紧密耦合的测试软件包。

所有软件包都应有一些单元测试，可能还有集成测试，但应具有它们的程度取决于软件包的质量类别。
以下小节适用于"1 级"软件包：

代码覆盖率
~~~~~~~~~~

我们将提供行覆盖率，并达到 95% 以上的行覆盖率。
如果较低百分比的目标是合理的，则必须在显著位置记录。
我们可以提供分支覆盖率，或将代码排除在覆盖率之外（测试代码、调试代码等）。
我们要求在合并更改之前覆盖率增加或保持不变，但在有正当理由的情况下（例如删除先前被覆盖的代码可能导致百分比下降），做出降低代码覆盖率的更改可能是可以接受的。

性能
~~~~

我们强烈建议进行性能测试，但认识到对于某些软件包来说，性能测试没有意义。
如果有性能测试，我们将选择在每次更改时、或在每次发布前、或两者都进行检查。
我们还将要求为降低性能的合并更改或发布提供理由。

Linters 和静态分析
~~~~~~~~~~~~~~~~~~

我们将使用 :doc:`ROS 代码风格 <Code-Style-Language-Versions>`，并通过 `ament_lint_common <https://github.com/ament/ament_lint/tree/{REPOS_FILE_BRANCH}/ament_lint_common/doc/index.rst>`_ 中的 linter 来强制执行它。
属于 ``ament_lint_common`` 的所有 linter/静态分析都必须使用。

`ament_lint_auto <https://github.com/ament/ament_lint/blob/{REPOS_FILE_BRANCH}/ament_lint_auto/doc/index.rst>`_ 文档提供了有关运行 ``ament_lint_common`` 的信息。

一般实践
--------

有些实践对所有的 ROS 2 开发都是通用的。

这些实践不影响 `REP 2004 <https://reps.openrobotics.org/rep-2004/>`_ 中描述的软件包质量级别，但仍强烈建议用于开发过程。

问题 (Issues)
^^^^^^^^^^^^^

在提交 issue 时，请务必：

- 包含足够的信息，让另一个人能够理解该问题。
  在 ROS 2 中，以下各点对于缩小问题原因的范围是必需的。
  在每个类别中尽可能多地测试替代方案将特别有帮助。

  - **操作系统和版本。**
    理由：ROS 2 支持多个平台，有些 bug 特定于特定版本的操作系统/编译器。
  - **安装方法。**
    理由：有些问题只有在 ROS 2 从二进制归档或 deb 安装时才会显现。
    这可以帮助我们确定问题是否出在打包过程中。
  - **ROS 2 的具体版本。**
    理由：有些 bug 可能存在于特定的 ROS 2 版本中，后来被修复了。
    知道你的安装是否包含这些修复很重要。
  - **所使用的 DDS/RMW 实现** （参见 `此页面 <../../Concepts/Intermediate/About-Different-Middleware-Vendors>` 了解如何确定是哪一个）。
    理由：通信问题可能特定于所使用的底层 ROS 中间件。
  - **所使用的 ROS 2 客户端库。**
    理由：这有助于我们缩小问题可能所在的栈层范围。

- 包含重现该问题的步骤列表。
- 如果是 bug，考虑提供一个 `简短、自包含、正确（可编译）的示例 <http://sscce.org/>`__。
  如果其他人能够轻松重现问题，问题被解决的可能性会大得多。

- 提及已经尝试过的故障排除步骤，包括：

  - 升级到最新版本的代码，其中可能包含尚未发布的 bug 修复。
    参见 `此部分 <building-from-source>` 并按照说明获取 "rolling" 分支。
  - 尝试使用不同的 RMW 实现。
    参见 `此页面 <../../How-To-Guides/Working-with-multiple-RMW-implementations>` 了解如何操作。

分支
^^^^

.. note::
    这些只是准则。
    由软件包维护者选择与他们自己的工作流相匹配的分支名称。

好的做法是在软件包的源码仓库中为其目标的每个 ROS 发行版设置\ **单独的分支**。
这些分支通常以它们所针对的发行版命名。
例如，专门针对 Humble 发行版开发的 ``humble`` 分支。

发布也从这些分支进行，针对相应的发行版。
针对特定 ROS 发行版的开发可以在相应的分支上进行。
例如：针对 ``foxy`` 的开发提交提交到 ``foxy`` 分支，``foxy`` 的软件包发布从同一分支进行。

.. note::
    这要求软件包维护者酌情执行回移或前移，以使所有分支在功能上保持最新。
    维护者还必须在所有仍进行软件包发布的分支上执行一般维护（bug 修复等）。

    例如，如果某个功能被合并到 Rolling 特定的分支（例如 ``rolling`` 或 ``main``），并且该功能也适用于
    Humble 发行版（不破坏 API 等），那么将该功能回移到 Humble 特定的分支是好的做法。

    如果有新功能或 bug 修复可用，维护者可以为那些较旧的发行版进行发布。

**关于** ``main`` **和** ``rolling`` **呢？**

``main`` 通常针对 :doc:`Rolling <../../Releases/Release-Rolling-Ridley>` （因此是下一个尚未发布的 ROS 发行版），不过维护者也可以决定从 ``rolling`` 分支开发和发布。

库版本控制
^^^^^^^^^^

我们将对一个软件包中的所有库一起进行版本控制。
这意味着库从软件包继承它们的版本。
这样可以防止库和软件包版本出现分歧，并与一起发布共享同一仓库的软件包的策略共享相同的理由。
如果你需要库有不同的版本，那么考虑将它们拆分为不同的软件包。

开发流程
^^^^^^^^

* 默认分支（在大多数情况下是 rolling 分支）必须始终能够构建、通过所有测试并且在没有警告的情况下编译。
  如果在任何时候出现回归，首要任务是至少恢复到之前的状态。
* 始终在启用测试的情况下构建。
* 在更改后并在 pull request 中提出它们之前，始终在本地运行测试。
  除了使用自动化测试外，还要手动运行修改后的代码路径，以确保补丁按预期工作。
* 始终为每个 pull request 在所有平台上运行 CI 作业，并在 pull request 中包含作业链接。

有关推荐软件开发工作流的更多详细信息，请参阅 `软件开发生命周期`_ 部分。

对 RMW API 的更改
^^^^^^^^^^^^^^^^^

在更新 `RMW API <https://github.com/ros2/rmw>`__ 时，要求 1 级中间件库的 RMW 实现也一并更新。
例如，引入到 RMW API 中的新函数 ``rmw_foo()`` 必须在以下软件包中实现（截至 ROS Galactic）：

* `rmw_connextdds <https://github.com/ros2/rmw_connextdds>`__
* `rmw_cyclonedds <https://github.com/ros2/rmw_cyclonedds>`__
* `rmw_fastrtps <https://github.com/ros2/rmw_fastrtps>`__

如果可行，也应考虑对非 1 级中间件库的更新（例如取决于更改的大小）。
有关中间件库及其级别的列表，参见 `REP-2000 <https://reps.openrobotics.org/rep-2000/>`__。

跟踪任务
^^^^^^^^

为了帮助组织 ROS 2 的工作，核心 ROS 2 开发团队使用看板式的 `GitHub 项目看板 <https://github.com/orgs/ros2/projects>`_。

然而，并非所有 issue 和 pull request 都在项目看板上跟踪。
看板通常代表即将到来的发布或特定项目。
通过浏览 `ROS 2 仓库 <https://github.com/ros2>`_ 的各个 issue 页面，可以按仓库浏览工单。

任何给定 ROS 2 项目看板中列的名称和用途各不相同，但通常遵循相同的一般结构：

* **待办 (To do)**：
  与项目相关、准备好被分配的 issue
* **进行中 (In progress)**：
  目前正在进行中的活跃 pull request
* **审查中 (In review)**：
  工作已完成并准备好审查的 pull request，以及目前正在积极审查的 pull request
* **已完成 (Done)**：
  已合并/关闭的 pull request 和相关 issue（用于提供信息）

要请求进行更改的权限，只需在你感兴趣的工单上发表评论。
根据复杂程度，描述你计划如何处理它可能会有用。
我们将更新状态（如果你没有权限），你就可以开始处理 pull request 了。
如果你经常贡献，我们很可能会直接授予你自己管理标签等的权限。

软件包命名约定
^^^^^^^^^^^^^^

名称在 ROS 中扮演着重要角色，遵循命名约定可以简化学习和理解大型系统的过程。

ROS 软件包占据一个扁平的命名空间，因此命名应谨慎且一致。
`REP-144 <https://reps.openrobotics.org/rep-0144/>`__ 中有软件包命名的标准。

* 软件包名称应遵循常见的 C 变量命名约定：小写、以字母开头、使用下划线分隔符，例如 laser_viewer

* 软件包名称应足够具体，以识别软件包的作用。
  例如，运动规划器不叫 planner。
  如果它实现波前传播算法，它可以叫 wavefront_planner。
  在使名称具体和避免名称过于冗长之间显然存在张力。

  * 应避免使用 utils 之类的包罗万象的名称，因为它们没有界定软件包应包含什么或不包含什么。

* 要检查名称是否已被占用，请查阅 `<https://index.ros.org/packages/>`__。
  如果你希望你的仓库包含在该列表中，请参阅 `rosdistro 贡献指南 <https://github.com/ros/rosdistro/blob/master/CONTRIBUTING.md>`__。

* 我们的目标是开发一套规范的工具集，让机器人做有趣的事情。
  软件包名称应告诉你软件包的作用，而不是它来自哪里。
  作为一个社区，我们应该能够做到这一点。
  一个 Ubuntu 发行版提供了大约 33,000 个软件包，而没有在名称中插入来源或作者。

* 仅当软件包不打算被更广泛地使用时，才建议为软件包名称添加前缀（例如，特定于 PR2 机器人的软件包使用 ``pr2_`` 前缀）。
  在复刻现有软件包时，你可能会为软件包名称添加前缀，但同样，前缀希望能传达更改了什么，而不是谁更改的。

* 对于 ROS 软件包，在软件包名称前加 'ros' 是多余的。
  除非常核心的软件包，否则不建议这样做。

计量单位和坐标系约定
^^^^^^^^^^^^^^^^^^^^

ROS 中使用的标准单位和坐标约定已在 `REP-0103 <https://reps.openrobotics.org/rep-0103/>`__ 中正式化。
所有消息都应遵循这些准则，除非有非常充分的理由，并且该理由被非常清楚地记录以避免混淆。

ROS 中距离测量中"太近"或"太远"等特殊条件的表示已在 `REP-0117 <https://reps.openrobotics.org/rep-0117/>`__ 中正式化。

编程约定
^^^^^^^^

* 防御性编程：尽早确保假设成立。
  例如，检查每个返回码，并确保至少抛出一个异常，直到该情况被更优雅地处理。
* 所有错误消息都必须定向到 ``stderr``。
* 在尽可能窄的作用域中声明变量。
* 保持项目组（依赖、导入、包含等）按字母顺序排列。

C++ 特定
~~~~~~~~

* 避免使用直接流式传输（``<<``）到 ``stdout`` / ``stderr``，以防止多个线程之间交错。
* 避免对 ``std::shared_ptr`` 使用引用，因为这会破坏引用计数。
  如果原始实例超出作用域而引用仍在使用，它就会访问已释放的内存。

文件系统布局
^^^^^^^^^^^^

软件包和仓库的文件系统布局应遵循相同的约定，以便为浏览我们源码的用户提供一致的体验。

软件包布局
~~~~~~~~~~

* ``src``：包含所有 C 和 C++ 代码

  * 还包含未安装的 C/C++ 头文件

* ``include``：包含所有已安装的 C 和 C++ 头文件

  * ``<package name>``：对于所有已安装的 C 和 C++ 头文件，它们应按软件包名称进行文件夹命名空间化

* ``<package_name>``：包含所有 Python 代码
* ``test``：包含所有自动化测试和测试数据
* ``config``：包含配置文件，例如 YAML 参数文件和 RViz 配置文件
* ``doc``：包含所有文档
* ``launch``：包含所有启动文件
* ``msg``：包含所有 ROS 消息定义
* ``srv``：包含所有 ROS 服务定义
* ``action``：包含所有 ROS 动作定义
* ``package.xml``：按 `REP-0140 <https://reps.openrobotics.org/rep-0140/>`_ 定义（可能会为原型设计而更新）
* ``CMakeLists.txt``：仅使用 CMake 的 ROS 软件包
* ``setup.py``：仅使用 Python 代码的 ROS 软件包
* ``README``：可以在 GitHub 上渲染为项目的落地页

  * 这可以按方便的程度简短或详细，但至少应链接到项目文档
  * 考虑在此 README 中放置 CI 或代码覆盖率徽章
  * 它也可以是 ``.rst`` 或 GitHub 支持的任何其他格式

* ``CONTRIBUTING``：描述贡献准则

  * 这可能包括许可证影响，例如使用 Apache 2 许可证时。

* ``LICENSE``：此软件包许可证的副本
* ``CHANGELOG.rst``：符合 `REP-0132 <https://reps.openrobotics.org/rep-0132/>`_ 的变更日志

仓库布局
~~~~~~~~

每个软件包都应位于与软件包同名的子文件夹中。
如果仓库只包含一个软件包，它可以选择放在仓库的根目录中。

上游软件包
^^^^^^^^^^

Debian 和 Ubuntu 上游中的软件包
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

得益于 Jochen Sprickerhof 和 Leopold Palomo-Avellaneda 的不懈努力，一些 `ROS 2 软件包现在可以从 Debian 和 Ubuntu 主仓库中获得 <https://wiki.debian.org/DebianScience/Robotics/ROS2/Packages>`_。
`这里是 Jochen 在 ROSCon 2015 上对该过程的简短概述 <https://vimeo.com/142151399#t=29m15s>`_。
原始 ROS 软件包已被修改以遵循 Debian 准则，其中包括将软件包拆分为多个部分、在某些情况下更改名称、根据 FHS 准则安装到 /usr，以及在共享库上使用 soversions。

此外，一些引导依赖，如 ``vcstool`` 和 ``colcon`` 等命令行工具，以及 ``osrf-pycommon`` 和 ``ament`` 等一些库，也打包在上游中。

与 OSRF 提供的来自 http://packages.ros.org 的 ROS 软件包不同，上游仓库中的软件包不隶属于特定的 :doc:`ROS 发行版 <../../Releases>`。
相反，它们代表时间上的快照，将在 Debian unstable 中定期更新，然后在各个点锁定到下游 Debian 和 Ubuntu 发行版中。

不要混用流
~~~~~~~~~~

我们强烈建议不要在同一系统上混用来自上游 Debian/Ubuntu 和来自 http://packages.ros.org 的 ROS 软件包。
在某些情况下，这样的混合系统可以正常工作，但两组软件包之间可能会产生负面交互。
我们正在与 Jochen 和朋友们合作，通过文档和软件包冲突规范来尽量减少出现问题的机会，但我们预计一些风险仍然存在，包括一些相当微妙的问题。

因此，我们建议你选择要么从上游安装软件包，要么从 http://packages.ros.org 安装软件包，但不要两者都装。
你不仅不应该同时从两者安装软件包，而且如果你打算使用上游软件包，你甚至不应该在 apt 源中有 http://packages.ros.org 的条目（即在 ``/etc/apt/sources*`` 的任何文件中）。
两者都启用会导致两个源之间按名称重叠的软件包被混用，例如 ``python3-rospkg``。

已知差异
~~~~~~~~

与来自 packages.ros.org 的 ROS 软件包相比，人们应该注意上游 ROS 软件包中的一些差异：

* 软件包集合不完整。
* 软件包可能有不同的名称，并以不同的方式划分。

开发者工作流
------------

我们使用 `GitHub 项目看板 <https://github.com/orgs/ros2/projects>`_ 跟踪与即将到来的发布和大型项目相关的开放工单和活跃 PR。

通常的工作流是：

* 讨论设计（在相应仓库的 GitHub 工单中，如有需要，向 https://github.com/ros2/design 提交设计 PR）
* 在 fork 的功能分支上编写实现

  * 请查阅 `开发者指南 <Developer-Guide>` 获取准则和最佳实践

* 编写测试
* 启用并运行 linter
* 使用 ``colcon test`` 在本地运行测试（参见 :doc:`colcon 教程 <../../Tutorials/Beginner-Client-Libraries/Colcon-Tutorial>`）
* 一旦所有内容都在本地无警告构建并且所有测试都通过，在你的功能分支上运行 CI：

  * 转到 ci.ros2.org
  * 登录（右上角）
  * 点击 ``ci_launcher`` 作业
  * 点击 "Build with Parameters"（左列）
  * 在第一个框 "CI_BRANCH_TO_TEST" 中输入你的功能分支名称
  * 点击 ``build`` 按钮

  （如果你不是 ROS 2 提交者，你无权访问 CI 农场。
  在这种情况下，请 ping 你 PR 的审查者为你运行 CI）

* 如果你的用例需要运行代码覆盖率：

  * 转到 ci.ros2.org
  * 登录（右上角）
  * 点击 ``ci_linux_coverage`` 作业
  * 点击 "Build with Parameters"（左列）
  * 务必让 "CI_BUILD_ARGS" 和 "CI_TEST_ARGS" 保持默认值
  * 点击 ``build`` 按钮
  * 在文档末尾有关于如何 :ref:`解读报告结果 <read-coverage-report>` 和 :ref:`计算覆盖率 <calculate-coverage-rate>` 的说明

* 如果 CI 作业在没有警告、错误和测试失败的情况下构建完成，请将你的作业链接发布到你的 PR 或聚合你所有 PR 的高层级工单上（参见 `此处示例 <https://github.com/ros2/rcl/pull/106#issuecomment-271119200>`__）

  * 注意，这些徽章的 markdown 在 ``ci_launcher`` 作业的控制台输出中

* 当 PR 被批准时：

  * 提交 PR 的人使用 "Squash and Merge" 选项合并它，以便我们保持干净的历史

    * 如果提交值得保持分开：将所有吹毛求疵/linter/拼写错误的提交合并在一起，并合并剩余的集合

      * 注意：每个 PR 都应针对特定功能，因此 Squash and Merge 在 99% 的情况下都应该有意义

* 合并后删除分支

Gitconfig 优化
^^^^^^^^^^^^^^

为了能够推送到仓库，你需要在系统上设置 ssh 密钥。
然而，我们仓库的默认 URL 模式是使用 https，因为它是匿名可访问的。
在你的系统上，你可以使用 ``gitconfig`` 选项 ``insteadOf``，让 ``git`` 即使远程声明为 https 也自动使用你的 ssh 密钥。

将以下内容添加到你的 ``~/.gitconfig``

.. code-block::

    [url "ssh://git@github.com/"]
      insteadOf = https://github.com/

如果你在 GitLab 或 Bitbucket 上处理仓库，也可以做同样的事情。


架构开发实践
------------

本节描述在对 ROS 2 进行大型架构更改时应采用的理想生命周期。

软件开发生命周期
^^^^^^^^^^^^^^^^

本节逐步描述如何计划、设计和实现一个新功能：

1. 任务创建
2. 创建设计文档
3. 设计审查
4. 实现
5. 代码审查

任务创建
~~~~~~~~

需要对 ROS 2 关键部分进行更改的任务，应在发布周期的早期阶段进行设计审查。
如果设计审查发生在后期阶段，这些更改将成为未来发布的一部分。

* 应在相应的 `ros2 仓库 <https://github.com/ros2/>`_ 中创建一个 issue，清楚地描述正在进行的任务。

  * 它应有明确的成功标准，并突出预期的具体改进。
  * 如果该功能针对某个 ROS 发布，请确保在 ROS 发布工单中跟踪它（`示例 <https://github.com/ros2/ros2/issues/607>`__）。

编写设计文档
~~~~~~~~~~~~

设计文档绝不能包含机密信息。
你的更改是否需要设计文档取决于任务的大小。

1. 你正在进行小更改或修复 bug：

  * 设计文档不是必需的，但应在相应的仓库中打开一个 issue 来跟踪工作并避免重复劳动。

2. 你正在实现新功能，或希望为 OSRF 拥有的基础设施（如 Jenkins CI）做出贡献：

  * 需要设计文档，并应提交到 `ros2/design <https://github.com/ros2/design/>`__，以便在 https://design.ros2.org/ 上可访问。
  * 你应该 fork 仓库并提交详细说明设计的 pull request。

  在 pull request 或提交消息中提及相关的 ros2 issue（例如，``Design doc for task ros2/ros2#<issue id>``）。
  详细说明在 `ROS 2 Contribute <https://design.ros2.org/contribute.html>`__ 页面上。
  设计评论将直接在 pull request 上进行。

如果任务计划随特定版本的 ROS 一起发布，此信息应包含在 pull request 中。

设计文档审查
~~~~~~~~~~~~

一旦设计准备好进行审查，应打开一个 pull request，并指派适当的审查者。
建议将项目所有者——所有受影响软件包的维护者（按 ``package.xml`` 维护者字段定义，参见 `REP-140 <https://reps.openrobotics.org/rep-0140/#required-tags>`__）——作为审查者。

* 如果设计文档很复杂，或者审查者的日程有冲突，可以设置一个可选的设计审查会议。
  在这种情况下，

  **会议前**

  * 至少提前一周发送会议邀请
  * 建议会议时长为 1 小时
  * 会议邀请应列出审查期间要做的所有决定（需要软件包维护者批准的决定）
  * 会议必需出席者：设计 pull request 审查者
      会议可选出席者：所有 OSRF 工程师（如适用）

  **会议期间**

  * 任务所有者主持会议，介绍他们的想法并管理讨论，以确保按时达成一致

  **会议后**

  * 任务所有者应将会议记录发回给所有出席者
  * 如果对设计提出了小问题：

    * 任务所有者应根据反馈更新设计文档 pull request
    * 不需要额外的审查

  * 如果对设计提出了重大问题：

    * 可以接受删除没有明确一致意见的部分
    * 设计中存在争议的部分可以在将来作为单独的任务重新提交
    * 如果删除存在争议的部分不是一个选项，直接与软件包所有者合作以达成一致

* 一旦达成共识：

  * 确保 `ros2/design <https://github.com/ros2/design/>`__ pull request 已合并（如适用）
  * 更新并关闭与此设计任务相关的 GitHub issue

实现
~~~~

在开始之前，请查看 :doc:`Contributing-to-code/Making-a-PR` 了解 pull request 的最佳实践。

* 对于每个要修改的仓库：

  * 修改代码，完成后或定期进入下一步以备份你的工作。
  * 使用 ``git add -i`` `自我审查 <https://git-scm.com/book/en/v2/Git-Tools-Interactive-Staging>`__ 你的更改。
  * 使用 ``git commit -s`` 创建新的签名提交。

    * pull request 应包含最少的语义上有意义的提交（例如，大量 1 行提交是不可接受的）。
      在迭代反馈时创建新的 fixup 提交，或者如果你不想每次都创建新提交，可以选择使用 ``git commit --amend`` 修改现有提交。
    * 每个提交都必须有编写得当、有意义的提交消息。
      更多说明在 `这里 <https://chris.beams.io/posts/git-commit/>`__。
    * 移动文件必须在单独的提交中完成，否则 git 可能无法准确跟踪文件历史。
    * pull request 描述或提交消息中必须包含对相关 ros2 issue 的引用，以便在 pull request 合并时自动关闭它。
      更多详情参见此 `文档 <https://help.github.com/articles/closing-issues-using-keywords/>`__。
    * 推送新的提交。


构建农场介绍
------------

构建农场位于 `ci.ros2.org <https://ci.ros2.org/>`__。

每晚我们运行夜间作业，在各种平台上的各种场景中构建并运行所有测试。
此外，我们在合并前针对这些平台测试所有 pull request。

查看 :ref:`当前目标平台和架构集合 <binary-package-platforms>`，尽管它会随时间演进。

构建农场上有几类作业：

* 手动作业（由开发者手动触发）：

  * ci_linux：在 Ubuntu 上构建 + 测试代码
  * ci_linux-aarch64：在 ARM 64 位机器 (aarch64) 的 Ubuntu 上构建 + 测试代码
  * ci_linux_coverage：构建 + 测试 + 生成测试覆盖率
  * ci_linux-rhel：在 Red Hat Enterprise Linux 上构建 + 测试代码
  * ci_windows：在 Windows 上构建 + 测试代码
  * ci_launcher：触发上面列出的所有作业

* 夜间（每晚运行）：

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

  * Repeated：构建后运行每个测试最多 20 次或直到失败（又称 flakiness hunter）

    * nightly_linux_repeated
    * nightly_linux-aarch64_repeated
    * nightly_linux-rhel_repeated
    * nightly_win_rep

  * Coverage：

    * nightly_linux_coverage：构建 + 测试代码 + 分析 c/c++ 和 python 的覆盖率

      * 结果导出为 cobertura 报告


* packaging（每晚运行；结果打包到归档中）：

  * packaging_linux
  * packaging_linux-rhel
  * packaging_windows

另外两个构建农场通过提供源码和二进制软件包的构建、
持续集成、测试和分析来支持 ROS / ROS 2 生态系统。

有关详细信息、常见问题和故障排除，请参阅 :doc:`构建农场 <Build-Farms>`。

关于覆盖率运行的说明
^^^^^^^^^^^^^^^^^^^^

ROS 2 软件包的组织方式是，给定软件包的测试代码不仅包含在该软件包内，也可能存在于不同的软件包中。
换句话说：在测试阶段，软件包可以执行属于其他软件包的代码。

要达到 ROS 2 核心软件包中所有可用代码所达到的覆盖率，建议使用一组固定的提议仓库来运行构建。
该集合在 Jenkins 中覆盖率作业的默认参数中定义。


.. _read-coverage-report:

如何从构建农场报告中读取覆盖率
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

要查看给定软件包的覆盖率报告：

* 当 ``ci_linux_coverage`` 构建完成时，点击 ``Coverage Report``
* 向下滚动到 ``Coverage Breakdown by Package`` 表
* 在表中，查看第一列 "Name"

构建农场中的覆盖率报告包括 ROS 工作空间中使用的所有软件包。
覆盖率报告包括对应同一软件包的不同路径：

* 形如 ``src.*.<repository_name>.<package_name>.*`` 的名称条目
  这些对应软件包中针对其自身源码可用的单元测试运行
* 形如 ``build.<repository_name>.<package_name>.*`` 的名称条目
  这些对应软件包中针对构建或配置时生成的文件可用的单元测试运行
* 形如 ``install.<package_name>.*`` 的名称条目
  这些对应来自其他软件包测试运行的系统/集成测试

.. _calculate-coverage-rate:

如何从构建农场报告计算覆盖率
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

使用自动脚本获取组合的单元覆盖率：

 * 从 ci_linux_coverage Jenkins 构建中复制构建的 URL
 * 下载 `get_coverage_ros2_pkg <https://raw.githubusercontent.com/ros2/ci/master/tools/get_coverage_ros2_pkg.py>`__ 脚本
 * 执行脚本：``./get_coverage_ros2_pkg.py <jenkins_build_url> <ros2_package_name>`` （`README <https://github.com/ros2/ci/blob/master/tools/README.md>`__）
 * 从脚本输出中 "Combined unit testing" 的最后一行获取结果

替代方案：从覆盖率报告获取组合的单元覆盖率（需要手动计算）：

* 当 ci_linux_coverage 构建完成时，点击 ``Cobertura Coverage Report``
* 向下滚动到 ``Coverage Breakdown by Package`` 表
* 在表中，在第一列 "Name" 下查找（其中 <package_name> 是你测试中的软件包）：

  * 模式 ``src.*.<repository_name>.<package_name>.*`` 下的所有目录，获取 "Lines" 列中的两个绝对值。
  * 模式 ``build/.<repository_name>.*`` 下的所有目录，获取 "Lines" 列中的两个绝对值。

* 对于前面的选择：对于每个单元格，第一个值是已测试的行数，第二个是代码总行数。
  聚合所有行以获取已测试行数和被测代码总行数。
  相除以获取覆盖率。

.. _measure-coverage-locally:

如何使用 lcov 在本地测量覆盖率（Ubuntu）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

要在你自己的机器上测量覆盖率，安装 ``lcov``。

.. code-block:: console

     $ sudo apt install -y lcov

本节其余部分假设你在你的 colcon 工作空间中工作。
使用覆盖率标志以调试模式编译。
可以随意使用 colcon 标志来针对特定软件包。

.. code-block:: console

     $ colcon build --cmake-args -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS} --coverage" -DCMAKE_C_FLAGS="${CMAKE_C_FLAGS} --coverage"

``lcov`` 需要一个初始基线，你可以使用以下命令生成它。
根据需要更新输出文件位置。

.. code-block:: console

     $ lcov --no-external --capture --initial --directory . --output-file ~/ros2_base.info

为对你的覆盖率测量重要的软件包运行测试。
例如，如果测量 ``rclcpp``，也要用 ``test_rclcpp``

.. code-block:: console

     $ colcon test --packages-select rclcpp test_rclcpp

使用类似的命令捕获 lcov 结果，这次去掉 ``--initial`` 标志。

.. code-block:: console

     $ lcov --no-external --capture --directory . --output-file ~/ros2.info

组合跟踪 ``.info`` 文件：

.. code-block:: console

     $ lcov --add-tracefile ~/ros2_base.info --add-tracefile ~/ros2.info --output-file ~/ros2_coverage.info

生成 html 以便于可视化和标注已覆盖的行。

.. code-block:: console

    $ mkdir -p coverage
    $ genhtml ~/ros2_coverage.info --output-directory coverage
