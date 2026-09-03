添加你的项目
============

使用下面的表单为你的组织或项目生成 YAML 条目。
生成后，你可以复制 YAML 片段，并向 ``rolling`` 分支上的
`adopters.yaml <https://github.com/ros2/ros2_documentation/blob/rolling/source/The-ROS2-Project/Adopters/adopters.yaml>`__
文件提交拉取请求。

策略
----

这个列表是\ **自行申报、自行证明**\ 的。
除非收到投诉，否则条目会在很少审查的情况下被接受。
由于贡献通过 Pull Request 提交，它们很容易审计，必要时可以稍后清理。

如何贡献
--------

1. 填写下面的表单。
2. 点击\ **生成 YAML**\ 生成片段。
3. 点击\ **在 GitHub 上打开 PR**，在 GitHub 的网页编辑器中打开文件（YAML 会自动复制到你的剪贴板）。
4. 将生成的 YAML 粘贴到文件中 ``adopters:`` 列表的末尾。
5. 提交更改并打开拉取请求。

.. note::

   对 ROS 2 文档仓库的所有拉取请求都需要
   `Developer Certificate of Origin (DCO) <https://developercertificate.org/>`__ 签署。
   如果你使用 GitHub 网页编辑器，
   `DCO bot <https://github.com/apps/dco>`__ 会在你的 PR 上评论，
   如果缺少签署，会给出添加签署的说明。
   要通过命令行签署，请使用 ``git commit --signoff``。

.. raw:: html

   <div class="adopters-form-container">
   <form id="adopters-yaml-form">

     <div class="form-group">
       <label for="field-organization">组织 *</label>
       <span class="form-hint">公司或机构名称</span>
       <input type="text" id="field-organization" placeholder="e.g., Acme Robotics Inc.">
     </div>

     <div class="form-group">
       <label for="field-organization-url">组织 URL</label>
       <span class="form-hint">可选</span>
       <input type="url" id="field-organization-url" placeholder="https://www.example.com">
     </div>

     <div class="form-group">
       <label for="field-project">项目 *</label>
       <span class="form-hint">使用 ROS 的具体项目</span>
       <input type="text" id="field-project" placeholder="e.g., Autonomous Forklift">
     </div>

     <div class="form-group">
       <label for="field-project-url">项目 URL</label>
       <span class="form-hint">可选</span>
       <input type="url" id="field-project-url" placeholder="https://www.example.com/project">
     </div>

     <div class="form-group">
       <label>领域 * <span class="form-hint">（选择一个或多个）</span></label>
       <div class="domain-checkboxes">
         <label><input type="checkbox" name="domain" value="Agriculture"> 农业</label>
         <label><input type="checkbox" name="domain" value="Aerial/Drone"> 航空/无人机</label>
         <label><input type="checkbox" name="domain" value="Automotive"> 汽车</label>
         <label><input type="checkbox" name="domain" value="Components"> 组件</label>
         <label><input type="checkbox" name="domain" value="Construction"> 建筑</label>
         <label><input type="checkbox" name="domain" value="Consumer Robot"> 消费机器人</label>
         <label><input type="checkbox" name="domain" value="Defense/Government"> 国防/政府</label>
         <label><input type="checkbox" name="domain" value="Education"> 教育</label>
         <label><input type="checkbox" name="domain" value="Energy"> 能源</label>
         <label><input type="checkbox" name="domain" value="Healthcare/Medical"> 医疗保健/医疗</label>
         <label><input type="checkbox" name="domain" value="Humanoid"> 人形机器人</label>
         <label><input type="checkbox" name="domain" value="Logistics/Warehouse"> 物流/仓储</label>
         <label><input type="checkbox" name="domain" value="Manufacturing"> 制造</label>
         <label><input type="checkbox" name="domain" value="Marine"> 海洋</label>
         <label><input type="checkbox" name="domain" value="Research"> 研究</label>
         <label><input type="checkbox" name="domain" value="Space"> 太空</label>
         <label><input type="checkbox" name="domain" value="Service Robot"> 服务机器人</label>
       </div>
     </div>

     <div class="form-group">
       <label for="field-date-added">添加日期 *</label>
       <span class="form-hint">自动生成 (YYYY-MM-DD)</span>
       <input type="text" id="field-date-added" readonly style="width: 120px; background: #e9ecef;">
     </div>

     <div class="form-group">
       <label for="field-country">国家 *</label>
       <span class="form-hint">选择一个或多个国家</span>
       <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
         <select id="field-country" style="width: 280px;">
           <option value="">-- 选择国家 --</option>
         </select>
         <button type="button" id="adopters-add-country-btn" class="btn btn-secondary" style="margin-top: 0;">添加</button>
       </div>
       <div id="adopters-selected-countries" class="adopters-country-tags"></div>
     </div>

     <div class="form-group">
       <label for="field-description">描述 *</label>
       <span class="form-hint">简要说明你如何使用 ROS</span>
       <textarea id="field-description" placeholder="e.g., Autonomous navigation for warehouse logistics using ROS 2 and Nav2."></textarea>
     </div>

     <div id="adopters-form-errors" style="display: none;"></div>

     <button type="button" id="adopters-generate-btn" class="btn btn-primary">生成 YAML</button>
     <button type="button" id="adopters-copy-btn" class="btn btn-secondary" style="display: none;">复制到剪贴板</button>
     <button type="button" id="adopters-open-pr-btn" class="btn btn-success" style="display: none;">在 GitHub 上打开 PR</button>

     <pre id="adopters-yaml-output" style="display: none;"></pre>

   </form>
   </div>
