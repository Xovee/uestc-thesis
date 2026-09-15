# 回归测试

## F06数学字体

`f06-math-fonts.tex` 及英文入口覆盖普通、粗体希腊字母、数学字母表、运算符、矩阵和中文混排。`assert_math_fonts.py` 检查编译日志及实际 PDF 字形，确认标准粗体大写希腊字母不缺失、数学字体保持 TeX 默认，并验证正文的 Times New Roman 字体没有改变。用例不包含私人论文内容，已接入快速与完整回归。

## R01短引用页界

`r01-reference-boundaries.tex`及英文入口检查普通图、表、公式、章节、子图引用、星号形式、
数学字号和间距、包含引用的标题与图题，以及正文引用跨到浮动页之后的情况。
`assert_reference_boundaries.py`读取实际PDF注释位置和所覆盖字符，禁止正文链接进入页眉、
页脚，检查图号点击范围、星号无链接语义，以及中间浮动页的文献链接。
两种语言用例已接入统一回归入口；辅助文件的锚点存在性不能替代PDF点击区域检查。
完整引用保护会限制英文长名称的断词；前后排版比较和已知警告已记录，维护者确认接受此取舍，
不能把功能检查通过等同于所有版面均无变化。

## 用户压缩包

Markdown手册的分发规则使用独立测试，不需要编译论文：

```text
python -m unittest discover -s tests -p test_package_release.py
```

测试确认源码预检包包含草稿`GUIDE.md`；正式候选要求手册已审阅，并从当前源文件重新构建示例。
正式包还要求完成与候选哈希绑定的内容、PDF逐页和非官方表述审阅；源码、候选或预览变化会拒绝沿用旧确认。
不再要求或收入手册PDF，也不接受外部旧示例PDF。
测试使用临时副本、虚构敏感信息及现有公开示例的只读检查，不发布Release，不修改真实手册的状态。
同时验证中文、英文独立包的名称、目录与30个源码和说明文件（正式包另含一个示例PDF），英文包入口和章节重命名后引用完整，
双语摘要均保留，语言及源文件映射变化不能复用审阅记录；
源码预检包保留`-source-preview.zip`后缀，避免与正式包混淆。
`.vscode`只收入通用的`settings.json`和`extensions.json`，不收入其他私有编辑器配置。

F07检查将实际面向用户的Markdown放入测试压缩包，逐一核对内联链接和引用式链接定义的
包内文件目标；网络外链及页内锚点单独排除，代码示例不作为导航链接。检查不验证网页
可访问性或锚点名称。维护者使用的docs、tests和tools目录继续排除在用户包之外。
真实源码预检包也应使用同一检查函数复核，不能仅根据仓库里的文件是否存在判断链接有效。

R02测试覆盖符合旧后缀规则的私人备份排除、源文件越界、受控二进制变化、构建中源码变化、
旧示例隔离、候选审阅失效和实际PDF的元数据、附件、批注、表单、执行动作等。PDF测试需要`pypdf`，
使用虚构联系方式和临时PDF；字体版权XMP使用现有默认PDF只读核验。正式流程的真实构建验收应在独立
测试副本中完成，模拟手册和审阅状态不得回写真实手册，也不代表已经批准实际Release。

## VS Code项目配置

以下检查同时验证打包和VS Code配置，不需要编译论文：

```text
python -m unittest discover -s tests -p "test_*.py"
```

配置检查覆盖latexmk/XeLaTeX编译流程、与`latexmkrc`一致的PDF输出位置、内置预览、
保存后自动编译与右侧预览默认值，以及配置不含个人绝对路径。这些静态检查不能替代VS Code界面实测。

## 排版回归

此目录保存维护者使用的排版回归测试，不作为用户教程，也不进入普通用户下载的Release。
测试应小而稳定，重点覆盖：

- 文档类选项、默认值和错误提示；
- 页眉、页脚、页码和单双面行为；
- 章、节、目录、图目录和表目录；
- 摘要、关键词、致谢、附录和成果列表；
- 图题、表题、脚注、公式和参考文献；
- 匿名送审及其他影响输出内容的模式。

当前测试覆盖硕士、博士与中英文论文的四种组合。英文完整示例直接使用用户入口main-english.tex，保证维护测试与用户入口一致。长图题、表题和附注用于检查换行、两端对齐、末行自然结束及垂直间距。

参考文献分页测试读取生成的PDF，要求第一页结束于第28条，第29条长文献完整出现在第二页；条目跨页或测试位置漂移时，断言失败。字段检查确认普通文献的DOI、URL和电子预印本标识隐藏，在线文献的访问地址保留。新增19条文献回归记录覆盖文献类型、作者缩写、版本、副标题、电子资源和特殊字符；同时检查引用排序与压缩、上标与正文引用的实际尺寸，以及参考文献的字号、编号对齐和局部分页设置。

附录编号测试覆盖中英文模式下的附录A和附录B，并自动检查节、子节、公式、图和表的编号。在项目根目录运行：

图表标题引用测试覆盖中英文模式，检查参考文献按照正文首次引用的顺序编号，不受前置
图表目录影响；同时检查三种目录的显示、辅助文件再生成和内部链接。该测试已接入完整回归。

统一回归入口会先检查默认外部PDF，然后编译所有排版用例和中英文完整示例，最后检查两份
示例PDF结构。未来本地检查和GitHub Actions都调用同一个入口，避免两套命令逐渐不一致：

```text
python tests/run_regression.py
```

日常修改可以先运行快速模式；它覆盖四种硕博、中英文组合、中英文完整示例和交叉引用：

```text
python tests/run_regression.py --quick
```

编号边界测试从第10章和第99页开始，检查两位章节编号、图表公式编号、三位目录页码和长页眉，不通过生成大量空白页面模拟真实论文长度。

标题分页测试检查长章标题在正文、页眉和目录中的换行，连续标题之间的间距，以及临近页底的标题是否与后续正文一起移动到下一页。页底标题位置不符合预期时，编译会直接报错。

注释表布局测试使用中英文短内容和长内容，检查主要符号表、缩略词表的自适应列宽和自动换行。

PDF结构断言检查中英文示例的A4页面、外部封面与声明页标签、前置部分和正文页码标签、
必需书签及其目标、内部链接和文档元数据。它只属于维护者测试，不影响模板编译，也不
进入普通用户下载的Release。安装维护者测试依赖后运行：

```text
python -m pip install -r tests/requirements.txt
# 以下路径对应统一回归入口的默认输出；使用--build-dir时同步替换目录。
python tests/assert_pdf_structure.py build/regression/uestc-thesis-template-preview.pdf
python tests/assert_pdf_structure.py build/regression/full-example-english.pdf --language english
```

外部PDF断言独立检查默认`cover.pdf`和`declaration.pdf`的文件哈希、页数、A4尺寸、
元数据、附件、表单、JavaScript和批注。它会在官方材料被意外替换时失败；有意更新文件
后，必须先完成人工逐页复核，再更新断言中的哈希。在项目根目录运行：

```text
python tests/assert_external_pdfs.py
```

```text
latexmk -xelatex -outdir=build/tests -jobname=master-chinese tests/smoke.tex
latexmk -xelatex -outdir=build/tests -jobname=doctor-chinese tests/smoke-doctor.tex
latexmk -xelatex -outdir=build/tests -jobname=master-english tests/smoke-english.tex
latexmk -xelatex -outdir=build/tests -jobname=doctor-english tests/smoke-doctor-english.tex
latexmk -xelatex -outdir=build/tests -jobname=full-example-english tests/full-example-english.tex
latexmk -xelatex -outdir=build/tests -jobname=bibliography-pagination tests/bibliography-pagination.tex
latexmk -xelatex -outdir=build/tests -jobname=appendix-numbering tests/appendix-numbering.tex
latexmk -xelatex -outdir=build/tests -jobname=appendix-numbering-english tests/appendix-numbering-english.tex
latexmk -xelatex -outdir=build/tests -jobname=numbering-boundaries tests/numbering-boundaries.tex
latexmk -xelatex -outdir=build/tests -jobname=numbering-boundaries-english tests/numbering-boundaries-english.tex
latexmk -xelatex -outdir=build/tests -jobname=heading-pagination tests/heading-pagination.tex
latexmk -xelatex -outdir=build/tests -jobname=heading-pagination-english tests/heading-pagination-english.tex
latexmk -xelatex -outdir=build/tests -jobname=notation-lists tests/notation-lists.tex
latexmk -xelatex -outdir=build/tests -jobname=notation-lists-english tests/notation-lists-english.tex
```

## TeX Live版本与尺寸回归

开发和验收环境为TeX Live 2026，不再持续回归旧版本。安装`requirements.txt`后，可指定
发行版的bin目录运行同一入口（Windows示例）：

```text
python tests/run_regression.py --tex-bin C:/texlive/2026/bin/windows --build-dir build/regression-tl2026
```

省略`--tex-bin`时使用当前PATH；指定时仅影响本次进程。不同版本必须使用不同输出
目录。编译文档数量以当前回归入口的用例列表和运行摘要为准；历史数量仅作为对应版本的验证记录。`--quick`也包含版式尺寸测试、F01最小例、中英文F02字号、F03表内行距与F04子图测试。
输出目录中的`environment.json`记录工具路径、版本及主示例加载的宏包版本，
`layout-contract.layout.json`记录实际PDF尺寸与断言结果。

`layout-contract.tex`和`assert_layout_contract.py`检查A4纸张、正文12pt、20pt固定
行距、首行24pt缩进、左右30mm边距、混排自动间距、标题字号与连续标题间距、
公式居中和编号靠右。公式四种上下间距另在TeX运行时断言为6pt。
这些检查不要求跨版本的完整示例页数或逐像素输出相同。

## 目录页码占位（F01）

`f01-original.tex`保留真实英文节标题与三位页码导致末字被白底遮盖的最小例。
`f01-boundaries.tex`及英文入口覆盖四级目录、图目录、表目录、1至4位阿拉伯页码，
以及比数字页码更宽的罗马页码。页码宽度在目录正常读取时测量，写入aux供下一遍使用；
latexmk会自动完成收敛，不额外读取目录文件，也不重复执行目录里的引用命令。
最宽页码仅用于标题换行的安全右边距；每行页码盒采用当前页码实测宽度加2pt，
使点线延伸到各行实际页码附近，避免宽罗马页码撑大短页码前的空白。

`assert_toc_page_columns.py`直接检查PDF文字基线、标题与页码间距、白色矩形遮盖、
页码右对齐及链接目标存在性。另检查点线可见边缘到页码的距离，考虑2pt留白和点线周期，
要求在1.8至6.5bp之间。基线分组兼容中西文字体不同的字形上沿；固定条目数量
可以防止未识别的条目被静默漏检。只检查“字符串仍存在”无法识别原来的视觉遮盖。

例如：

```text
python tests/assert_toc_page_columns.py build/regression/f01-original.pdf --pages 1 --entries 2
python tests/assert_toc_page_columns.py build/regression/f01-boundaries.pdf --pages 2 3 4 --entries 12
```

## 附录正文字号（F02）

`f02-appendix-fonts.tex`及三个语言/学位入口检查附录A/B、四级标题、定理与证明、
脚注、图表、陈列公式以及后续成果页。样例前后都有普通正文作为对照。

`assert_appendix_fonts.py`在实际PDF中检查36处文字或公式字号，并核对公式编号。
另读取TeX记录，确认附录普通段落为10.5pt、固定20pt行距、21pt首行缩进（两个字符），
成果页默认文字恢复12pt、20pt行距、24pt缩进。标题、脚注、图表题保留独立字号。
成果列表示例可继续在局部分组中使用五号，不依赖附录字号遗留状态。

学校规范§2.5要求陈列公式及其编号使用小四号；附录正文变小时，标准的equation、
align、alignat、flalign、gather、multline（含星号形式）、displaymath及`\[...\]`
均保持12pt，环境结束后恢复附录正文的10.5pt。行内数学随普通文字字号。

```text
python tests/assert_appendix_fonts.py build/regression/f02-appendix-fonts.pdf
python tests/assert_appendix_fonts.py build/regression/f02-appendix-fonts-english.pdf --english
```


## 表内文字行距（F03）

`f03-table-spacing.tex`及英文模式入口使用同一份中西文混排压力样例，检查标准
tabular、tabularx、tabular*，p/X/m/b列、粗体、嵌套表格、自然换行及较高的数学内容。
这是维护者测试，不是用于提交的英文论文样例。

`assert_table_spacing.py`读取实际PDF，核对37项间距和70处文字字号：默认表内多行文字为13.6pt；
普通短行保持17pt，局部arraystretch=1.3时为26pt。显式normalsize列继续使用12pt/20pt。
检查单行m列与l列的对齐，表外正文、表附注及局部1.5倍行距的恢复，避免表格设置泄漏。
自然换行和高分式另须结合PDF视觉检查，不能只靠编译成功或普通基线断言判断无碰撞。

学校§2.4.2规定五号、单倍行距，并建议行高约0.6cm；13.6pt是结合官方Word宋体样例
作出的实现取值，不是学校规定的固定磅数。原有arraystretch=.85及行高基准分别保留。
测试不要求全文页码不变：长表格收紧后，其位置、附近正文及引用页码可能正常重排。

```text
python tests/assert_table_spacing.py build/regression/f03-table-spacing.pdf
python tests/assert_table_spacing.py build/regression/f03-table-spacing-english.pdf
```


## 子图字号与分图题位置（F04）

`prepare_subfigure_example.py`直接从GUIDE.md的“并排子图”小节提取LaTeX示例，写入
本次构建目录。`f04-subfigures.tex`及英文入口实际编译这一示例，避免测试另写一份
正确代码而漏掉手册错误。英文模式也原样使用中文手册块；整份文档仅是维护者压力样例。

另有普通单图和正文对照、三个子图的长说明、页底浮动与图目录。试修前后对照可定义
FFourLegacyCaptions复现长说明放在各子图下方的旧写法；正常回归不启用该分支。

`assert_subfigures.py`在实际PDF中核对16处字号、5个子图序号的位置、13个标签及链接。
分图序号为10.5pt并居中位于对应图下；分图题在主图题之后；长图题和对应子图同页。
同时确认整图/子图引用的可见编号、目标页，以及图目录只包含3个简短总图题。

统一入口会自动提取手册示例，并在完整和快速模式中运行两个用例。单独检查可使用：

```text
python tests/prepare_subfigure_example.py GUIDE.md build/tests/f04-guide-example.tex
latexmk -xelatex -outdir=build/tests tests/f04-subfigures.tex
python tests/assert_subfigures.py build/tests/f04-subfigures.pdf
```

对子图只设置`font={small}`，覆盖subcaption默认的`font+=smaller`；保留原有间距、
计数器与超链接机制。子图自身保留空caption和label，在总图题中按顺序说明各子图；
总caption的可选短标题用于图目录。字号设置可自动生效，旧论文中已有的分图题文字
仍需作者按新示例移动；模板不会从用户内容中自动抽取或重排说明文字。


## F05 英文数字版次

`f05-editions.tex`与`f05-editions-english.tex`使用同一组42条维护者书目，
检查论文语言选项不会改变文献自身的版次语言规则。覆盖英文1、2、3、4、10至14、
20至24、100至103、110至114、121至123及211至213，另含中文版次、空字段、
Revised、Revised edition、文字版次、自动语言识别和incollection容器版次。

`assert_editions.py`分别读取BBL和最终PDF，逐条检查版次字段及其标点，
并核对42条书目的编号和顺序。预期结果为明确列出的字符串，不使用待测转换函数计算。
数字初版和空字段应省略；英文末两位为11、12、13时使用th，其余后缀保持原有规则。
混合语言书目仅用于维护测试，不是英文论文提交范例。

```text
latexmk -xelatex -outdir=build/tests tests/f05-editions.tex
python tests/assert_editions.py build/tests/f05-editions.pdf
latexmk -xelatex -outdir=build/tests tests/f05-editions-english.tex
python tests/assert_editions.py build/tests/f05-editions-english.pdf
```

两个用例均已接入快速和完整回归。修复前的同样输入在每个论文语言模式下有11条
英文版次错误，BBL与PDF双重检查共报22项偏差；修复后42条全部通过。
