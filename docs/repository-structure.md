# 仓库结构设计

目录围绕用户从下载到完成论文的任务组织。目标结构如下：

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/       # 问题与功能请求表单
│   └── pull_request_template.md
├── .vscode/                  # 用户使用的编译、预览配置与扩展推荐
├── chapters/                 # 用户撰写的论文各部分
├── docs/                     # 维护设计、规范依据与检查记录
├── figures/                  # 用户论文图片
├── fonts/                    # 经许可随项目提供的规定字体
├── tests/                    # 维护者使用的排版回归测试
├── .editorconfig
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE.md
├── cover.pdf                 # 默认学术学位硕士封面和中英文扉页
├── declaration.pdf           # 默认未签名声明与授权页
├── README.md                 # 最短可行的入门路径
├── README-english.md         # 英文包的开始说明，打包后为README.md
├── GUIDE.md                  # 中文Markdown使用手册
├── GUIDE-english.md          # 英文Markdown使用手册
├── latexmkrc                 # 统一编译入口
├── main.tex                  # 中文论文入口
├── main-english.tex          # 英文论文入口
├── references.bib            # 用户参考文献
├── uestcthesis.bst           # 按学校要求适配的BibTeX样式
└── uestcthesis.cls           # 模板实现
```

## 面向用户的文件

### `README.md`

只回答第一次使用最重要的问题：需要安装什么、修改哪些文件、如何编译、遇到问题
去哪里查。完整使用说明进入`GUIDE.md`，避免首页变成维护手册。

### `GUIDE.md`

面向可能不熟悉LaTeX的论文作者，用明确步骤和示例说明安装、写作与排错。该文件是手册
中文正文入口，英文版为GUIDE-english.md；均可直接预览，打包后各自提供为GUIDE.md。
不再制作手册PDF，示例论文的PDF展示职责保持不变。

### `.vscode/`

`settings.json`统一LaTeX Workshop的编译流程、输出位置和内置PDF预览，
`extensions.json`推荐所需扩展。只分发这两份通用项目配置，不分发维护者的个人路径、
快捷键或其他编辑器设置。命令行编译继续由`latexmkrc`提供，不依赖VS Code。

### `main.tex`与`main-english.tex`

开发仓库中分别作为中文论文和英文论文的入口；发布包中均为唯一的`main.tex`。
入口负责选择学位类型、填写PDF标题和作者、导入封面与
声明，并按生成顺序列出论文各部分。用户不需要某部分时，直接注释对应命令。学校正式
封面中的学号、学院和导师等信息仍在学校提供的Word文件中填写。

### `chapters/`

示例文件名直接体现论文结构，例如：

```text
chapters/
├── abstract.tex
├── symbols.tex
├── acronyms.tex
├── chapter-1.tex
├── acknowledgements.tex
├── appendix.tex
├── achievements.tex
└── *-english.tex             # 对应的英文示例文件
```

用户可以按自己的论文调整章节数量，但无需改变模板实现。

### `figures/`与`references.bib`

分别承担图片和文献管理。发行版提供少量许可清晰的示例内容，不使用作者真实论文素材。

### `fonts/`

提供经明确许可随本非盈利项目分发的宋体、黑体和Times New Roman文件。模板默认优先使用
这些文件，使不同操作系统获得一致字体；文件不完整时回退到系统同名字体。字体不受项目
LPPL许可覆盖，具体文件哈希和使用边界记录在`THIRD_PARTY.md`。

### `docs/`

保留面向维护者的设计、规范依据和检查记录，必要时供用户参考。安装、使用和排错
说明统一进入`GUIDE.md`，不再另建多份平行的手册正文：

- `release-deliverables.md`：记录源码、示例论文PDF和Markdown手册的发布分工；
- `standards-traceability.md`：记录学校规范、官方样式、模板实现和测试之间的对应关系；
- `distribution-privacy-audit.md`：记录第三方材料、学校标识、字体和个人信息的公开边界；
- `font-portability-audit.md`：记录规定字体的选择顺序、跨平台风险和验证要求；
- `design-principles.md`：解释稳定的产品与接口原则。

## 面向维护者的文件

### `tests/`

保存小而稳定的排版回归用例，覆盖页眉页脚、标题、目录、摘要、图表、参考文献和匿名
模式。测试文件不是教学示例，不出现在普通用户的Release压缩包中。

### `.github/`

负责协作和自动化。构建工作流应验证一次完整编译；发布工作流应自动生成面向用户的干净
压缩包，避免把测试、缓存和个人环境配置带入发行物。

自动化工作流尚未建立，当前使用本地测试和打包工具。THIRD_PARTY.md暂留维护者本地，首次公开提交和发布包均不包含；公开权利说明见NOTICE.md及资源目录说明。

## Release内容

正式打包工具的目标内容如下；当前本地草稿的示例PDF作为独立附件提供，详见release-deliverables.md。

```text
.vscode/settings.json
.vscode/extensions.json
README.md
GUIDE.md
LICENSE
NOTICE.md
cover.pdf
declaration.pdf
main.tex
uestcthesis.cls
uestcthesis.bst
latexmkrc
references.bib
chapters/
figures/
fonts/
uestc-thesis-example.pdf
```

中文、英文分别发布独立包，各自只有上面的一个`main.tex`与对应语言的六个章节，
另保留共用的双语摘要。英文包在打包时将英文入口和章节统一为普通文件名；英文README
也映射为包内的`README.md`。共享class、BST、字体和外部PDF不分叉维护。

发布包不包含`.github/`、`tests/`、`docs/`中的维护记录、编译缓存、未获许可的字体、真实
论文、已签字的声明页或维护者脚本。默认PDF和六个字体文件的来源及再分发许可边界记录
在`THIRD_PARTY.md`。
示例PDF用于展示完整论文版式，`GUIDE.md`用于说明模板使用方法；不单独提供空白模板PDF，
也不提供手册PDF。已放弃的LaTeX手册试排资料只作为历史记录保留，不进入Release。

## 分阶段落地

1. **确定用户路径**：完成目录、许可证、隐私和公开边界；
2. **最小可编译版本**：迁移类文件，建立匿名示例和清晰的主文档；
3. **可理解性**：编写入门、使用和排错文档；
4. **可靠性**：覆盖关键排版行为并建立自动构建；
5. **首个预览版**：打包一份普通用户可以直接使用的Release。
