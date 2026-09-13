# 发布交付方案

## 决策

最终面向用户提供可直接编译的论文源码、示例论文PDF和Markdown使用手册：

- `uestc-thesis-example.pdf`：完整展示模板生成的学位论文效果；
- `GUIDE.md`：独立说明模板的安装、配置、写作和排错方法。

正式用户压缩包按论文语言分为`uestc-thesis-xovee-chinese.zip`与
`uestc-thesis-xovee-english.zip`，顶层文件夹分别为`uestc-thesis-xovee-chinese/`与
`uestc-thesis-xovee-english/`。每包30个源码和说明文件，正式包另含对应示例PDF，共31个文件。

按维护者2026年9月11日的决定，`THIRD_PARTY.md`暂不收入发布包，也暂不公开上传；
待维护者修订后在后续版本提供。现有许可边界仍保留在NOTICE及资源说明中。

使用手册的PDF计划已取消，不再从Markdown或LaTeX生成手册PDF，也不再维护手册专用
的LaTeX正文。示例论文PDF仍保留，用于展示模板的实际排版效果。

不单独提供“空白模板PDF”。空白PDF无法有效展示目录、图表、公式、参考文献、附录和
成果列表等关键版式；可直接修改的源码本身就是用户的空白模板。

## 各交付物的职责

### 论文源码

源码用于实际写作。每个语言包只有一个`main.tex`，集中保存论文选项、PDF属性和内容顺序；
`chapters/`只含共用双语摘要及所选语言的六个示例章节，英文包也使用不带`-english`的文件名。
`figures/`和`references.bib`保存图片与文献。开发仓库仍维护`main.tex`和`main-english.tex`
及两套章节源文件；class、BST、字体、外部PDF和校标只维护一份。源码中的注释只提供与当前位置直接相关的简短提示，不重复完整使用手册。

### 示例PDF

示例PDF用于回答“模板最终生成的论文是什么样子”。它应完整覆盖摘要、目录、正文、
图表、公式、参考文献、附录和成果列表等主要结构，并使用匿名、虚构或许可清晰的示例
内容。示例正文不承担完整教学任务，避免用户在开始写作前先删除大量说明文字。

### Markdown使用手册

开发仓库中的`GUIDE.md`为中文手册，`GUIDE-english.md`为对应英文翻译；两种用户包
各自将所选手册提供为`GUIDE.md`。手册用于回答“如何使用模板”，内容包括：

- 硕士、博士以及中文、英文选项；
- 编译环境、字体与首次编译流程；
- 封面、摘要、关键词、目录和章节配置；
- 图表、公式、定理、算法、参考文献、附录和成果列表；
- 模板自动保证的格式与用户自行负责的内容；
- 常见错误、排查方法和升级注意事项。

使用手册先以中文撰写，中文定稿后新增英文版。默认读者可能不是计算机、软件或工程相关
专业，也可能几乎不了解LaTeX；不得把编程、命令行或阅读源码的能力当作前提。

使用手册必须保持简洁，但不能省略重要步骤。每项说明应直接交代在哪里操作、修改什么、
完成后应该看到什么，并给出可以照着修改的明确示例。首次使用必需的概念在出现时用普通
语言解释，不纠结于实现细节，也不编写通用LaTeX教材或普通学术写作常识教程。

README负责最短开始路径，源码注释负责当前位置的提示，手册负责把实际任务讲清楚；
不为了避免重复而要求初学者在多个文件之间来回查找才能完成一个关键步骤。高级选择不
进入首次使用主流程。以后根据读者反复遇到的问题迭代内容，优先改进容易误解的说明。

手册可以直接在支持Markdown预览的界面中阅读，用户无需编译手册或了解Markdown语法。
项目README链接到`GUIDE.md`；用户压缩包提供对应语言的手册。暂不额外建立文档网站或
引入新的发布服务，后续是否需要其他阅读入口另行决定。

当前中文手册已覆盖常用写作流程，英文翻译已同步；两份手册均不再保留开头的草稿状态说明。本地编辑、编译与预览统一采用VS Code和
LaTeX Workshop，Windows安装TeX Live 2026，macOS安装MacTeX 2026。`.vscode/settings.json`
提供项目专用的latexmk/XeLaTeX编译流程与`output`预览路径，默认保存`.tex`后自动编译，
编译成功后更新右侧PDF预览；
`.vscode/extensions.json`推荐LaTeX Workshop。两份文件随用户发布包提供，不修改
用户的全局编辑器设置。Overleaf操作说明已纳入中英文指南；Linux已有官方安装说明链接。

Windows + TeX Live 2026、macOS + MacTeX 2026 和 Overleaf（XeLaTeX + TeX Live 2026）已完成示例与完整博士论文测试。英文README、章节说明和完整英文手册已同步。
这些编译验证不等同于从零安装及新手独立试用验证。

此前的`docs/user-guide-draft.md`、`guide.tex`、`docs/guide/`试排材料及
`output/pdf/uestc-thesis-guide-preview.pdf`只保留为历史记录，明确标注不再维护，不进入
用户发布包。取消PDF计划不删除已有试验资料，也不影响论文模板代码。

#### 高级用户章节（暂定）

在使用手册末尾保留一个非必读章节，暂定名为`You May Not Need to Know`。该章节面向需要
扩展或调试模板的高级用户，不进入普通用户的首次使用流程。内容仍应简洁，只解释会影响
模板兼容性、但普通用户通常无需处理的机制。

已记录的首个条目：

- 模板类已经使用`dvipsnames`和`table`选项加载`xcolor`，普通用户不应在正文中重复加载；
- 如确实需要增加其他`xcolor`选项，应在`\documentclass`之前使用
  `\PassOptionsToPackage{所需选项}{xcolor}`；
- 说明模板将`xcolor`置于`pdfpages`之前加载，是为了稳定传递选项并避免宏包加载顺序造成
  的选项冲突；这一机制不改变论文版面，也不会产生可感知的编译开销。

后续可将宏包扩展、字体覆盖、PDF元数据等真正需要高级用户了解的事项继续记录在本节，
但不为了充实章节而加入通用LaTeX知识。

### README

README作为GitHub入口，只保留最短可行的开始路径、下载入口以及示例论文PDF和
`GUIDE.md`的链接，不承载完整手册内容。

## 发布要求

- 示例论文PDF必须由同一Release对应的源码生成，`GUIDE.md`必须对应同一版本；
- 示例PDF必须完成逐页视觉检查；
- 使用手册必须与当前模板接口和默认值一致；
- 手册直接使用Markdown，用户不需要编译使用手册即可开始写作；
- Release中不得包含真实论文、个人信息、签字材料或许可不明确的资源；
- 是否在Git仓库中跟踪生成的示例PDF，可在建立自动发布流程时决定，但每个正式Release
  都必须提供示例论文PDF和Markdown手册，不要求手册PDF。

## 外部PDF分发门禁

首个Release采用方案B：维护者已确认学校明确同意本项目重新分发`cover.pdf`和
`declaration.pdf`。两个文件的个人化元数据已经清除，来源、许可结论和权利边界记录在
`THIRD_PARTY.md`，NOTICE明确其不受项目LPPL许可覆盖。授权沟通材料由维护者在公开仓库
之外保存；每次替换文件或生成Release时仍需重新执行结构、元数据和逐页检查。

## 当前本地发布草稿

2026年9月13日的本地草稿提供两个30文件源码ZIP，以及旁置的中英文示例PDF。ZIP由源码预检模式生成，再分别解压编译验证；尚未走完下述正式候选确认流程，也尚未发布。

## 打包门禁

发布工具供维护者使用，需要Python 3.10或更新版本及`pypdf`；生成正式候选包还需要TeX Live 2026。
发布文件在`tools/package_release.py`中逐个列明，加入章节、图片或备份不会自动将其收入发布包。
有意新增公开材料时，先审阅内容和许可，再更新名单；字体、默认PDF和校标图片还须核对锁定的哈希。

正式发布分为准备候选和确认生成两个步骤：

```text
python tools/package_release.py --language chinese
python tools/package_release.py --language english
```

这一步从名单内文件建立全新的临时目录，重新编译`main.tex`，不读取旧示例PDF或旧辅助文件。
构建同时核对实际输入来源，编译过程中源码变化会使准备失败。
每次按指定语言独立编译和检查。成功后在`dist/`生成以下维护者材料（以中文包为例）：

- `uestc-thesis-xovee-chinese-candidate.zip`：包含当前源码和刚编译示例的待审包；
- `uestc-thesis-xovee-chinese-candidate.example.pdf`：与待审包中示例逐字节一致，供逐页查看；
- `uestc-thesis-xovee-chinese-candidate.review.json`：完整文件清单及哈希、PDF属性和结构检查、被排除的额外文件、构建记录及人工审阅项。

审阅清单中的实际内容和图片，逐页查看PDF，并检查README、NOTICE及本次发布说明的非官方表述。
确认后，仅将审阅文件`review`下的`content_and_images`、`all_pdf_pages`、`non_official_wording`
三项改为`true`，保留自动生成的其他数据，再运行：

```text
python tools/package_release.py --reviewed dist/uestc-thesis-xovee-chinese-candidate.review.json
```

此时才生成默认正式包`dist/uestc-thesis-xovee-chinese.zip`及旁置的`.manifest.json`验收记录。
英文包同样审阅其`uestc-thesis-xovee-english-candidate.review.json`后单独确认；
确认命令从审阅记录读取语言。显式指定错误语言会被拒绝。记录同时绑定源文件映射和
重命名后的实际包内容，旧版混合包记录不能用于新包。最终包与已审待审包逐字节一致。源码、候选包、预览PDF或自动检查记录发生变化时，会拒绝沿用旧审阅；
必须重新准备候选并复核。审阅记录和检查材料不放进用户压缩包。

如本机找不到TeX工具，可在准备命令中指定`--tex-bin`，只影响本次构建，不修改系统环境。
不再接受外部`--example`文件，以免把其他版本的PDF误配给当前源码。

`GUIDE.md`和上述两份`.vscode`配置已列入用户文件白名单，不收入其他编辑器私有配置。
正式候选及最终确认均要求手册已完成审阅：
`GUIDE.md`中的唯一状态标记必须为`<!-- guide-status: ready -->`。当前未完成的手册使用
`<!-- guide-status: draft -->`，正式打包会明确拒绝；只有内容完成、经过审阅和首次使用
验证后，维护者才能改为`ready`。该标记只是流程检查，不能自动证明内容质量。

当前可分别用`python tools/package_release.py --source-only --language chinese`和
`python tools/package_release.py --source-only --language english`生成两份源码预检包，
默认输出分别为`dist/uestc-thesis-xovee-chinese-source-preview.zip`和
`dist/uestc-thesis-xovee-english-source-preview.zip`。省略语言参数时默认为中文。其中包含草稿`GUIDE.md`，
但不包含示例论文PDF，并旁置实际文件检查记录；该模式不属于正式Release，不能用其审阅文件生成正式包。打包不再接受
`--guide`参数或要求手册PDF。只收入经许可并锁定SHA-256的六个字体文件，不会收入其他
字体、`tests/`、`.github/`、`tools/`、`docs/`中的维护记录、编译缓存、手册PDF试排材料
或其他未列入白名单的内容。

自动检查会拒绝可识别的未公开联系方式、真实号码形式和本地路径，检查PDF元数据、页面尺寸、附件、
表单、批注及执行动作，并检查正式示例的标题、作者是否为占位信息。仅允许普通阅读链接和已核验的
字体版权标记；不会把版权元数据误删为隐私。自动扫描不能可靠识别人名、图片签名或未公开研究内容，
这些内容由与候选文件哈希绑定的人工审阅负责，具体边界见`distribution-privacy-audit.md`。
