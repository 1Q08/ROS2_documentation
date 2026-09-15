添加你的项目
============

使用下面的表单为你的组织或项目生成 YAML 条目。
生成后，你可以复制 YAML 片段，并向 ``rolling`` 分支上的
`adopters.yaml <https://github.com/ros2/ros2_documentation/blob/rolling/source/The-ROS2-Project/Adopters/adopters.yaml>`__
文件提交拉取请求。

政策
----

该列表是 **自我报告且自我证明** 的。
除非收到投诉，否则条目会以最小的审查力度被接受。
由于贡献是通过拉取请求提交的，它们易于审计，如有必要日后也可以清理。

如何贡献
--------

1. 填写下面的表单。
2. 单击 **Generate YAML** 生成片段。
3. 单击 **Open PR on GitHub** 在 GitHub 的网页编辑器中打开该文件（YAML 会自动复制到你的剪贴板）。
4. 将生成的 YAML 粘贴到文件中 ``adopters:`` 列表的末尾。
5. 提交更改并打开拉取请求。

.. note::

   所有对 ROS 2 文档仓库的拉取请求都需要
   `开发者原创声明（DCO） <https://developercertificate.org/>`__ 签署。
   如果你使用 GitHub 网页编辑器，
   `DCO 机器人 <https://github.com/apps/dco>`__ 会在你的 PR 上评论，
   提示你在缺少签署时如何补充。
   要通过命令行签署，请使用 ``git commit --signoff``。

.. raw:: html

   <div class="adopters-form-container">
   <form id="adopters-yaml-form">

     <div class="form-group">
       <label for="field-organization">Organization *</label>
       <span class="form-hint">Company or institution name</span>
       <input type="text" id="field-organization" placeholder="e.g., Acme Robotics Inc.">
     </div>

     <div class="form-group">
       <label for="field-organization-url">Organization URL</label>
       <span class="form-hint">Optional</span>
       <input type="url" id="field-organization-url" placeholder="https://www.example.com">
     </div>

     <div class="form-group">
       <label for="field-project">Project *</label>
       <span class="form-hint">The specific project using ROS</span>
       <input type="text" id="field-project" placeholder="e.g., Autonomous Forklift">
     </div>

     <div class="form-group">
       <label for="field-project-url">Project URL</label>
       <span class="form-hint">Optional</span>
       <input type="url" id="field-project-url" placeholder="https://www.example.com/project">
     </div>

     <div class="form-group">
       <label>Domain * <span class="form-hint">(select one or more)</span></label>
       <div class="domain-checkboxes">
         <label><input type="checkbox" name="domain" value="Agriculture"> Agriculture</label>
         <label><input type="checkbox" name="domain" value="Aerial/Drone"> Aerial/Drone</label>
         <label><input type="checkbox" name="domain" value="Automotive"> Automotive</label>
         <label><input type="checkbox" name="domain" value="Components"> Components</label>
         <label><input type="checkbox" name="domain" value="Construction"> Construction</label>
         <label><input type="checkbox" name="domain" value="Consumer Robot"> Consumer Robot</label>
         <label><input type="checkbox" name="domain" value="Defense/Government"> Defense/Government</label>
         <label><input type="checkbox" name="domain" value="Education"> Education</label>
         <label><input type="checkbox" name="domain" value="Energy"> Energy</label>
         <label><input type="checkbox" name="domain" value="Healthcare/Medical"> Healthcare/Medical</label>
         <label><input type="checkbox" name="domain" value="Humanoid"> Humanoid</label>
         <label><input type="checkbox" name="domain" value="Logistics/Warehouse"> Logistics/Warehouse</label>
         <label><input type="checkbox" name="domain" value="Manufacturing"> Manufacturing</label>
         <label><input type="checkbox" name="domain" value="Marine"> Marine</label>
         <label><input type="checkbox" name="domain" value="Research"> Research</label>
         <label><input type="checkbox" name="domain" value="Space"> Space</label>
         <label><input type="checkbox" name="domain" value="Service Robot"> Service Robot</label>
       </div>
     </div>

     <div class="form-group">
       <label for="field-date-added">Date Added *</label>
       <span class="form-hint">Auto-generated (YYYY-MM-DD)</span>
       <input type="text" id="field-date-added" readonly style="width: 120px; background: #e9ecef;">
     </div>

     <div class="form-group">
       <label for="field-country">Country *</label>
       <span class="form-hint">Select one or more countries</span>
       <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
         <select id="field-country" style="width: 280px;">
           <option value="">-- Select a country --</option>
         </select>
         <button type="button" id="adopters-add-country-btn" class="btn btn-secondary" style="margin-top: 0;">Add</button>
       </div>
       <div id="adopters-selected-countries" class="adopters-country-tags"></div>
     </div>

     <div class="form-group">
       <label for="field-description">Description *</label>
       <span class="form-hint">Brief explanation of how you use ROS</span>
       <textarea id="field-description" placeholder="e.g., Autonomous navigation for warehouse logistics using ROS 2 and Nav2."></textarea>
     </div>

     <div id="adopters-form-errors" style="display: none;"></div>

     <button type="button" id="adopters-generate-btn" class="btn btn-primary">Generate YAML</button>
     <button type="button" id="adopters-copy-btn" class="btn btn-secondary" style="display: none;">Copy to Clipboard</button>
     <button type="button" id="adopters-open-pr-btn" class="btn btn-success" style="display: none;">Open PR on GitHub</button>

     <pre id="adopters-yaml-output" style="display: none;"></pre>

   </form>
   </div>
