---
name: sustainable-project-structure
description: 为新项目搭建或为现有项目重构可持续维护的文件夹架构，兼容网页／软件开发项目、企划／调查／分析项目及两者混合项目。用于限制根目录增长、明确文件归属、设置临时区与归档区、建立旧路径迁移索引、为开发页面维护 READMECHS／SPEC／CHANGELOG、沉淀可复用资产和项目级 Skill，并在移动文件后验证引用与可再现性。
---

# 可持续项目目录

先识别项目类型和真实工作流，再决定目录；不要把某个项目的编号或文档模板机械复制到所有项目。

## 工作流程

1. 读取当前目录及适用的 `AGENTS.md`、`CLAUDE.md`、README、部署脚本和现有 Skill 说明。
2. 盘点两层目录、根级散落文件、缓存、临时生成物、部署入口、运行引用和可能被旧会话引用的路径。
3. 将项目判定为以下一种：
   - `development`：网页、软件、API、自动化工具等持续开发项目。
   - `research`：企划、调查、分析、会议、资料与交付物为主的项目。
   - `hybrid`：企划／分析项目中包含独立开发子项目，或开发项目中包含较大的研究工作流。
4. 只为长期稳定的责任边界创建根目录。先提出编号、名称、所有权和迁移表，再执行已有文件移动。
5. 建立根目录治理说明、临时生命周期、归档策略、迁移索引和项目 Skill 权威路径。
6. 更新所有受影响的源码引用、测试、部署白名单、说明文件和 Skill 相对路径。
7. 运行结构检查和项目原有测试；确认旧路径可由迁移索引直接找到当前最终路径。

## 按项目类型选择规则

- 开发项目：完整读取 [development-projects.md](references/development-projects.md)。让每个页面或可独立维护模块拥有一个所有者目录。只有这类开发单元强制维护 `docs/READMECHS.md`、`docs/SPEC.md`、`docs/CHANGELOG.md`。
- 企划／调查／分析项目：完整读取 [research-projects.md](references/research-projects.md)。按工作流、事实来源、会议、交付物和复用资产划分；固定分区和多文件主题维护 README，不默认创建 SPEC 或 CHANGELOG。
- 混合项目：同时读取上述两份参考。根项目使用主工作流的结构，独立开发子目录内部使用开发项目规则，避免把源码、研究原始资料和交付物混在同一层。
- 整理已有项目或移动路径：额外完整读取 [migration-and-governance.md](references/migration-and-governance.md)。

## 新项目快速搭建

先预览，再应用。脚本默认不写入任何内容，也不会覆盖已有文件：

```bash
python3 scripts/scaffold_project.py init \
  --root /path/to/project \
  --name ExampleProject \
  --profile development \
  --unit 01_Account \
  --unit 10_Service \
  --agent codex

python3 scripts/scaffold_project.py init \
  --root /path/to/project \
  --name ExampleProject \
  --profile development \
  --unit 01_Account \
  --unit 10_Service \
  --agent codex \
  --apply
```

企划／分析项目把 `--profile` 改为 `research`。项目已存在内容时，先人工盘点，再明确添加 `--allow-existing`；该参数只允许补齐缺失文件，仍不会覆盖文件。

项目级 Skill 默认位置：

- 开发模板：`92_ProjectSkills/`，适合严格编号的可见根目录。
- 企划／分析模板：`.agents/skills/`，适合 repo-scoped Skill 的标准隐藏路径。
- 已有项目另有明确约定时，使用 `--skill-dir` 保持现有唯一权威路径，不制造第二份权威副本。

## 审计

```bash
python3 scripts/scaffold_project.py audit \
  --root /path/to/project \
  --profile development \
  --unit 01_Account \
  --unit 10_Service
```

审计结果不能替代项目测试。至少补做：

- 搜索旧路径和新路径的硬编码引用。
- 验证部署清单中每个本地源文件存在。
- 检查每个项目 Skill 的 `SKILL.md`、`agents/`、`references/`、`scripts/`、`assets/` 相对路径。
- 删除可再生缓存和无参考价值的 AI 中间产物。
- 保留有价值的过程资料，但放入页面历史、主题目录、复用资产或归档区。

## 关键约束

- 未经用户批准，不为现有项目新增根目录类别，不批量移动高风险文件。
- 根目录治理文件必须列出白名单和新增目录的审批方式。
- 迁移索引只记录移动、重命名和被替代的旧路径；新建文件不登记，日常任务不预读。
- 迁移表中的目标必须是当前最终路径，不能要求旧会话连续跳转多次。
- 临时目录必须有任务级生命周期；最终交付物和 Skill 权威源不得只留在临时区。
- 可复用资产先经过实际任务验证；触发条件、工作流和安全边界稳定后再形成 Skill。
- Skill 不依赖临时目录、个人敏感文件、实时凭据或仅存在于另一台机器的路径。
- 目录整理不应擅自改变线上 URL、API 路由、部署目标、权限语义或数据位置。
