<div align="center">

# 可持续项目目录

**让开发、研究和混合项目在持续迭代、AI 协作与人员交接中保持清晰、可维护、可再现。**

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=flat-square)](skills/sustainable-project-structure/SKILL.md)
![Version](https://img.shields.io/badge/version-1.1.0-2563eb?style=flat-square)
![Language](https://img.shields.io/badge/README-中文为主-dc2626?style=flat-square)
![Public Safe](https://img.shields.io/badge/public--safe-no%20secrets-16a34a?style=flat-square)

**中文** · [English](README.en.md)

</div>

---

## 这是什么

`sustainable-project-structure` 是一个面向 Codex 的项目结构治理 Skill。它不会机械地套用固定模板，而是先识别项目的真实工作流，再帮助你：

- 限制根目录无序增长；
- 明确页面、服务、研究资料和交付物的归属；
- 管理临时文件、归档内容与旧路径迁移；
- 为持续开发单元建立可维护的文档体系；
- 保证项目级 Skill、脚本与参考资料能够在新会话和新电脑上再现。

它既适合新项目搭建，也适合已经积累了大量历史文件、AI 中间产物和旧路径引用的现有项目。

## 为什么需要它

项目真正变乱，通常不是因为缺少文件夹，而是因为每次任务都创建了一个新的入口：

| 常见问题 | 这个 Skill 的处理方式 |
| --- | --- |
| 根目录不断出现 `tmp`、`output`、截图和下载副本 | 建立任务级临时区和明确的清理周期 |
| 页面源码、API、测试与部署文件分散 | 让每个开发单元拥有清晰的所有者目录 |
| 文件移动后旧会话找不到资料 | 用旧路径到最终路径的直接迁移索引保持可追溯性 |
| 研究资料、会议记录和交付物混在一起 | 按事实来源、工作流和交付关系组织内容 |
| 项目级 Skill 只存在于临时 ZIP 或另一台电脑 | 固定唯一权威位置并检查完整相对依赖 |
| 所有项目都被迫维护同一套文档 | 根据开发、研究或混合项目选择不同治理强度 |

## 三种项目模型

| 模型 | 适用场景 | 组织重点 |
| --- | --- | --- |
| `development` | 网站、SaaS、API、自动化工具 | 页面／服务所有权、源码、测试、部署与规格 |
| `research` | 企划、调查、会议、数据分析与正式交付物 | 来源、过程、决策、可编辑原稿与交付关系 |
| `hybrid` | 研究项目内含 Dashboard，或开发项目含大型研究流程 | 根项目遵循主工作流，独立开发子项目采用开发规则 |

## 核心能力

- **根目录治理**：建立白名单、编号含义和新增目录的审批边界。
- **所有权归一**：把专属源码、API、测试、工具和文档放进同一维护单元。
- **分层文档**：为持续开发单元维护 `READMECHS.md`、`SPEC.md`、`CHANGELOG.md`。
- **临时生命周期**：让下载、转换、截图和 AI 中间产物在任务完成时自然退出项目。
- **安全迁移**：移动文件前建立映射，移动后更新引用、部署清单与测试。
- **Skill 可再现性**：避免把唯一权威副本、凭据或本机路径留在临时环境中。

## 推荐结构示例

### 开发项目

```text
ExampleProject/
├── 01_Account/
│   ├── public/
│   ├── private/
│   ├── tests/
│   └── docs/
│       ├── READMECHS.md
│       ├── SPEC.md
│       └── CHANGELOG.md
├── 10_Service/
├── 80_SharedRuntime/
├── 90_ProjectDocs/
├── 91_ProjectTools/
├── 92_ProjectSkills/
├── 98_Archive/
├── 99_Temporary/
├── AGENTS.md
├── PROJECT_STRUCTURE.md
└── MOVED_PATHS.md
```

### 研究与企划项目

```text
ResearchProject/
├── 01_Research/
├── 02_Meetings/
├── 03_Sources/
├── 04_Deliverables/
├── 80_Reference/
├── 90_ReusableAssets/
├── .agents/skills/
├── 98_Archive/
├── 99_Temporary/
├── AGENTS.md
├── PROJECT_STRUCTURE.md
└── MOVED_PATHS.md
```

这些名称是起点，不是强制标准。已有项目应保留成熟且可理解的业务分类。

## 安装

### 使用 Agent Skills CLI

```bash
npx skills add tsetsugekka/sustainable-project-structure \
  --skill sustainable-project-structure
```

请保留 `--skill sustainable-project-structure`，避免在多 Skill 仓库场景下安装非目标内容。

### 手动安装

```bash
git clone https://github.com/tsetsugekka/sustainable-project-structure.git
mkdir -p ~/.codex/skills
cp -R sustainable-project-structure/skills/sustainable-project-structure \
  ~/.codex/skills/
```

## 使用示例

```text
使用 $sustainable-project-structure 为这个新网站设计目录。
每个页面要独立维护，非页面内容统一放到高位编号区域。
```

```text
整理这个已有项目的根目录，但先给出迁移表，
不要破坏旧会话、部署清单和未提交修改。
```

```text
这是一个企划和数据分析项目，不是网站。
请按事实来源、会议、交付物和复用资产来设计目录。
```

## 安全的脚手架与审计

脚本默认只预览，不写入任何文件：

```bash
python3 skills/sustainable-project-structure/scripts/scaffold_project.py init \
  --root /path/to/project \
  --name ExampleProject \
  --profile development \
  --unit 01_Account \
  --unit 10_Service \
  --agent codex
```

确认预览后再添加 `--apply`。即使使用 `--allow-existing`，脚本也只补齐缺失项，不覆盖已有文件。

审计现有结构：

```bash
python3 skills/sustainable-project-structure/scripts/scaffold_project.py audit \
  --root /path/to/project \
  --profile development \
  --unit 01_Account \
  --unit 10_Service
```

## 仓库结构

```text
skills/sustainable-project-structure/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── development-projects.md
│   ├── migration-and-governance.md
│   └── research-projects.md
└── scripts/scaffold_project.py
```

## 安全边界

- 不在未获授权时批量移动或删除现有文件。
- 不覆盖用户已有文件，不把归档区当作无限期垃圾桶。
- 不把真实凭据、个人资料、私有日志或绝对本机路径写入 Skill。
- 不因本地目录调整擅自改变线上 URL、API、权限或数据位置。
- 结构审计不能替代项目原有测试、构建和部署验证。

## 说明

目录模板不是目的，稳定的责任边界才是目的。请根据项目规模、团队习惯、合规要求和现有部署方式调整最终结构，并在执行高影响迁移前检查版本控制状态和备份策略。
