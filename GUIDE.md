<!-- guide-status: ready -->

# UESTC Thesis 使用手册

本手册介绍UESTC Thesis的使用方法，包括一些LaTeX的基础知识。有什么不清楚不明白的，可以先问问你所使用的大模型。

更多LaTeX写作方法可参阅中文指南[《一份（不太）简短的LaTeX 2ε介绍》](https://tug.org/docs/latex/lshort-chinese/lshort-zh-cn.pdf)，其中第四章介绍公式排版和常用数学符号。

## 入门

超短版本：安装TeX Live，安装VS Code，安装LaTeX Workshop插件，下载UESTC Thesis模板，开始写论文。

### 写作的基本过程

我们不再使用Word或者WPS来撰写论文，而是通过编辑`.tex`文件来修改内容，然后进行编译，生成PDF文件。

打开所下载语言包中的`main.tex`文件，这是整篇论文的总入口，负责把各个章节组合起来。

### 安装LaTeX软件

- Windows：安装TeX Live 2026，参见[官方Windows说明页](https://tug.org/texlive/windows.html)
- macOS：从[MacTeX官方下载页](https://tug.org/mactex/mactex-download.html)下载并安装MacTeX 2026
- Linux：安装TeX Live 2026，参见[官方Linux/Unix安装说明](https://tug.org/texlive/quickinstall.html)

### 安装VS Code和LaTeX Workshop

1. 从[VS Code官网](https://code.visualstudio.com/Download)下载适合自己系统的版本并安装。
2. 打开VS Code，点击左侧“扩展”（Extensions）图标，搜索`LaTeX Workshop`，
   安装发布者为`James Yu`的扩展。
3. 如果安装LaTeX软件时VS Code已经打开，安装完成后退出并重新打开VS Code。

### 如果你喜欢在线编辑（可选）

使用[Overleaf](https://www.overleaf.com/)可以在浏览器中编辑学位论文，以及生成、预览和下载PDF，无需在电脑上安装TeX Live或VS Code。

1. 登录Overleaf，点击 **New Project → Upload Project**，上传所下载的中文或英文模板ZIP，无需解压。
2. 打开项目设置，将 **Compiler** 设为 `XeLaTeX`，将 **TeX Live version** 设为 `2026`，确认 **Main document** 为 `main.tex`。
3. 点击 **Recompile**，先确认模板示例能够正常生成PDF。
4. 在 `main.tex` 中设置论文信息，在 `chapters` 中编辑正文；修改后点击 **Recompile** 查看效果。
5. 完成后，点击PDF预览区域的下载按钮，保存论文PDF。

中英文示例已在免费计划下测试通过。长篇或图表较多的论文可能超过免费计划的编译时限；遇到超时，可以选择本地编译，或者在Overleaf会员账号所创建的项目中完成编译。

### 下载模板

按论文语言下载中文包`uestc-thesis-xovee-chinese.zip`或英文包`uestc-thesis-xovee-english.zip`。
每个包都只有一个`main.tex`入口，正文和默认语言已配好；两种语言的摘要都保留。

解压后，文件夹里的重要文件包括：

- `main.tex`：学位论文总入口；
- `chapters`：各章内容；
- `figures`：论文图片；
- `references.bib`：参考文献。

### 编译方法选择XeLaTeX

不要用`pdfLaTeX`或者其他的，使用`Recipe: latexmk (xelatex)`。
模板附带的配置已选好这个编译方法，正常打开模板文件夹后不需要再手动选择。

### 生成学位论文

第一次使用时：

1. 在VS Code中选择“文件”→“打开文件夹”，打开解压后包含`main.tex`的模板文件夹。
   模板自带的配置会自动读取；如提示是否信任，请先确认模板来源可信。
2. 打开`main.tex`，按`F1`选择`LaTeX Workshop: Build LaTeX project`，先编译一次。
3. 编译完成后，按`F1`选择`LaTeX Workshop: View LaTeX PDF file`，在右侧打开PDF预览。

生成的PDF文件位于模板文件夹中的`output/main.pdf`，可用于发送、打印或提交。

之后在左侧编辑`chapters`中的`.tex`文件，按`ctrl/command + S`保存，编译成功后右侧PDF会自动更新。继续修改、保存、看效果即可，不需要每次手动点击编译。

还有一些你可能会喜欢的快捷键，例如选中文字后，先按`Ctrl/Command + L`，再按`Ctrl/Command + B`，即可切换加粗。
更多快捷键和代码片段可参见[LaTeX Workshop官方帮助：快捷键与代码片段](https://github.com/James-Yu/LaTeX-Workshop/wiki/Snippets#font-commands-and-snippets)，或者问问大模型。

### 学位论文的封面

不建议使用LaTeX，直接下载[学校提供的封面模板](https://gr.uestc.edu.cn/xiazai/114/3917)，填写完成后，导出为`PDF`文件，导入到项目中即可。

## 示例

### 论文设置

- 所下载包中的`main.tex`是学位论文入口
- 一般情况不要修改`uestcthesis.cls`
- `\documentclass[master,chinese]{uestcthesis}`：中文硕士学位论文
- `\documentclass[doctor,chinese]{uestcthesis}`：中文博士学位论文
- 英文包默认使用`\documentclass[master,english]{uestcthesis}`；博士论文把`master`改为`doctor`
- 语言选项只改变模板标题和格式，不会翻译已写好的正文
- 如果你想引入额外的packages，在`\begin{document}`命令之前使用`\usepackage{...}`命令引入，例如`\usepackage{multirow}`
- 如果你想自定义命令，在`\begin{document}`命令之前去定义，例如`\newcommand{\mymethod}{模型名}`
- PDF文件的标题和作者信息：通过`pdftitle={}`和`pdfauthor={}`来修改
- 如果你不想显示某些内容，注释掉相应的代码，例如如果不想显示*图目录*，可以注释代码：`% \uestclistoffigures`（快捷键一般为`ctrl/command + /`）；如果不想显示*主要符号表*，可以注释代码：`% \input{chapters/symbols}`
- 如果想让目录显示四级标题（以中文硕士学位论文为例）：`\documentclass[master,chinese,tocdepth3]{uestcthesis}`
- 无需手动修改模板的页边距、间距、字号等内容，模板已经设置好了

### 摘要

编辑`chapters/abstract.tex`

### 目录

目录自动生成，无需操心。

### 图目录

注释掉`\uestclistoffigures`即可不显示图目录。

### 表目录

注释掉`\uestclistoftables`即可不显示表目录。

### 主要符号表

注释掉`\input{chapters/symbols}`即可不显示主要符号表。

### 缩略词表

注释掉`\input{chapters/acronyms}`即可不显示缩略词表。

### 文字样式

- 常规文本：直接打字即可
- 粗体：`\textbf{粗体文字}`
- 斜体：`\textit{斜体文字}`
- 粗斜体：`\textbf{\textit{粗斜体文字}}`
- 下划线：`\underline{带下划线的文字}`
- 上标：`m\textsuperscript{2}`，显示为m²
- 下标：`H\textsubscript{2}O`，显示为H₂O
- 等宽字体：`\texttt{PyThon}`
- 字号：`{\small 小一点的文字}`、`{\large 大一点的文字}`，外层的`{}`不要丢
- 本模板的常用字号：`\small`是五号，`\normalsize`是小四，`\large`是四号，`\Large`是小三，注意大小写
- 文字颜色：`\textcolor{red}{红色文字}`，也可以把`red`换成`blue`、`green`等
- 自定义颜色：`\textcolor[RGB]{51,102,153}{自定义颜色的文字}`，三个数字依次表示红、绿、蓝，各取0到255

### 特殊字符

正文中的这些英文半角符号需要特殊写法：

- `%`：`\%`，例如`95\%`；直接写`%`会把它后面同一行的内容当成注释
- `&`：`\&`
- `_`：`\_`
- `#`：`\#`
- `$`：`\$`
- `{`：`\{`
- `}`：`\}`
- 反斜线`\`：`\textbackslash{}`
- 其他符号或者出了什么问题，就问大模型吧

### 章节与标题

- 一级标题：`\chapter{绪论}`
- 二级标题：`\section{引言}`
- 三级标题：`\subsection{研究内容}`
- 四级标题：`\subsubsection{研究内容一}`
- 注意，五级标题并不是`\subsubsubsection{}`，四并不是亖
- 正文：直接打字就行，新起一个段落，直接回车两次，插入一个空行
- 创建新的章节：在`chapters`目录下新建`chapter-2.tex`或者其他文件名，然后在`main.tex`里写上`\input{chapters/chapter-2}`或者对应的文件名

### 图片

图片放在`figures`文件夹（或者其他文件夹，引入图片的时候要指定正确的路径）。我建议你使用矢量格式的图片，例如`PDF`文件，这样图片放大后不会变模糊。

#### 单张图片

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\linewidth]{figures/uestc-logo.png}
    \caption{电子科技大学校标组合}
    \label{fig:guide-single}
    \fignote{注：这里写图的附注（可选）。}
\end{figure}
```

- 把`figures/uestc-logo.png`换成自己的图片路径
- `0.8\linewidth`表示当前行宽的80%，改这个数字可以调整图片大小
- `\label{}`是图片的引用标签，放在`\caption{}`后面，每张图的标签不能重复
- 正文中写`如\autoref{fig:guide-single} 所示，……`即可引用这张图，不用手写图号
- `[htbp]`允许图片排在当前位置（`here`）、页顶（`top`）、页底（`bottom`）或单独的浮动页，不保证图片固定在代码所在的位置；有的时候你需要调整代码的位置，从而调整图片的位置。不过一般情况下，我建议你使用`htbp`或者`t`。

#### 并排子图

下面先用同一张示例图演示，使用时换成各自的图片：

```latex
\begin{figure}[htbp]
    \centering
    \begin{subfigure}[b]{0.55\linewidth}
        \centering
        \includegraphics[width=\linewidth]{figures/uestc-logo.png}
        \caption{}
        \label{fig:guide-left}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.4\linewidth}
        \centering
        \includegraphics[width=\linewidth]{figures/uestc-logo.png}
        \caption{}
        \label{fig:guide-right}
    \end{subfigure}
    \caption[并排子图示例]{并排子图示例：(a)第一张图；(b)第二张图}
    \label{fig:guide-pair}
\end{figure}
```

- `0.55\linewidth`和`0.4\linewidth`分别表示左右子图占当前行宽的55%和40%，`\hfill`把剩余空间留在两图之间；两张子图的总宽度要留出间隔
- 子图里的`width=\linewidth`表示填满各自的子图宽度
- 每张子图里的`\caption{}`保留为空，让模板在对应图片下方自动生成五号字的`(a)`、`(b)`；其后的`\label{}`用于引用，不要删除
- 分图题写在最后的总图题之后，例如`并排子图示例：(a)第一张图；(b)第二张图`；更换图片或调整顺序时，同步修改对应说明
- 最后一个`\caption[简短总图题]{完整图题}`中，方括号的文字用于图目录，花括号的文字显示在图片下方
- 引用整张图：`\autoref{fig:guide-pair}`；引用左边的子图：`\autoref{fig:guide-pair}(\subref{fig:guide-left})`

### 表格

下面是一个三线表的例子。

```latex
\begin{table}[htbp]
    \centering
    \caption{不同方法的结果示例}
    \label{tab:guide-results}
    \begin{tabular}{lcp{5cm}}
        \toprule
        方法 & 准确率（\%） & 说明 \\
        \midrule
        基准方法 & 85.2 & 仅使用基础特征。 \\
        改进方法 & 88.6 & 在基础特征之外，加入时间和位置信息等额外特征，用于比较不同特征组合的效果。 \\
        本文方法 & \textbf{91.3} & 综合使用多种特征。 \\
        \bottomrule
    \end{tabular}
    \tabnote{注：表中数据仅用于演示（可选）。}
\end{table}
```

- `\caption{}`是表题，放在表格上方；`\label{}`紧跟在它后面，每张表的标签不能重复
- `\begin{tabular}{lcp{5cm}}`表示表格共有三列：`l`表示左对齐，`c`表示居中，`p{5cm}`表示这一列的文字区域宽度为5厘米，并自动换行；右对齐可以用`r`
- `\toprule`、`\midrule`、`\bottomrule`分别是表格顶部、表头下方和底部的三条横线；三线表的原则：少加横线，除非极为必要，不加竖线
- 较长的文字放在`p{5cm}`列里会自动换行，可以修改`5cm`来调整列宽；如果想在这个单元格里的指定位置换行，可以写`\newline`。`l`、`c`、`r`列不会自动换行
- 正文中写`如\autoref{tab:guide-results} 所示，……`即可引用这张表，不用手写表号
- `[htbp]`的含义与图片相同，表格可能排到页顶、页底或其他合适的位置
- 如果需要指定整张表的宽度，并自动分配部分列的宽度，可以进一步使用`tabularx`
- 更高阶的用法，建议咨询大模型。

### 数学符号和公式

行内公式：`$x_i=2$`

行间公式：

```latex
\begin{equation}
\label{eq:example}
  x+y=z
\end{equation}
\noindent 式中，$x$和$y$为两个加数；$z$为两者之和。
```

`\noindent`使“式中”顶格书写。

多行公式：

```latex
\begin{equation}
\label{eq:multiline-example}
  \begin{aligned}
    x+y &= z \\
    2x+2y &= 2z
  \end{aligned}
\end{equation}
```

- `&`用于对齐，`\\`用于换行，上面的多行公式共用一个编号
- 用`\eqref{eq:example}`引用公式，自动显示带括号的编号

#### 常见写法

- 上下标：`x_i`、`x^2`；上下标有多个字符时用花括号括起来，例如`x_{i+1}`、`x^{n+1}`
- 分式：`\frac{a}{b}`
- 根号：`\sqrt{x}`
- 希腊字母：`\alpha`、`\theta`、`\pi`
- 求和：`\sum_{i=1}^{n} x_i`
- 上方横线：`\bar{x}`，例如表示样本均值
- 公式中的文字：`\text{平均值}`

### 定理与证明

```latex
\begin{theorem}
    \label{thm:guide-example}
    两个偶数之和仍为偶数。
\end{theorem}

\begin{proof}
    设两个偶数为$2m$和$2n$，则其和为$2(m+n)$，因此仍为偶数。
\end{proof}
```

- 定理编号和证明结尾的黑色方块由模板自动生成；正文中用`\autoref{thm:guide-example}`引用定理
- 将`theorem`换成`definition`、`lemma`或`corollary`，分别表示定义、引理或推论；这些环境与定理共用一套章内编号

### 脚注
```latex
这里是正文\footnote{这是脚注。}。
```


### 致谢

注释掉`\input{chapters/acknowledgements}`即可不显示致谢。

### 参考文献

文献信息放在`references.bib`里，正文中用引用命令指定文献，编号和参考文献列表由模板自动生成。只有在正文中引用的文献，才会出现在文末参考文献列表中。

#### 添加文献

从论文的出版页面或文献管理软件导出`BibTeX`格式的条目，复制到`references.bib`中。例如：

```bibtex
@article{lecun2015deep,
  author = {Yann LeCun and Yoshua Bengio and Geoffrey Hinton},
  title = {Deep learning},
  journal = {Nature},
  year = {2015},
  volume = {521},
  number = {7553},
  pages = {436--444}
}
```

- `lecun2015deep`是这条文献的引用标签，正文中用它来引用；每条文献的标签不能重复，同一篇文献保留一条记录即可
- 导出的条目也可能有误，重点核对作者、题名、年份、期刊或会议名称及页码
- 多个作者之间用`and`分隔；中文作者可以写成`author = {{张钹} and {朱军} and {苏航}}`
- 标题中需要保留大写的缩写，用花括号保护，如`{IEEE}`、`{3D}`，否则可能显示`ieee`或`3d`

#### 正文引用

在章节的`.tex`文件中使用：

```latex
深度学习已得到广泛应用\cite{lecun2015deep}。
同时引用多篇文献\cite{lecun2015deep,vaswani2017attention}。
文献\citep{lecun2015deep}介绍了深度学习。
```

上述代码的效果（假设这两篇文献依次编号为1和2）：

> 深度学习已得到广泛应用<sup>[1]</sup>。同时引用多篇文献<sup>[1–2]</sup>。文献[1]介绍了深度学习。

- `\cite{}`显示上标引用；`\citep{}`显示与正文同样大小的方括号引用，适合“文献[1]介绍了……”这样的句子
- 多篇文献的标签用英文逗号分隔，模板会自动排序并合并连续编号，不用手写`[1]`、`[2-4]`

#### 可能出现的问题

- 引用显示为问号：检查引用标签是否与`references.bib`中的一致、文件是否已保存，再完成一次编译；仍有问号时，查看编译是否报错
- 文献信息有误：修改`references.bib`中的对应条目，再编译；不要直接修改生成的PDF或`.bbl`文件

#### 不同类型的文献示例

下面的写法适用于本模板，按[学校撰写规范](https://gr.uestc.edu.cn/xiazai/114/3917)表2-3的顺序列出常见类型。

##### 期刊论文

```bibtex
@article{guide-journal,
  author = {{王浩刚} and {聂在平}},
  title = {三维矢量散射积分方程中奇异性分析},
  journal = {电子学报},
  year = {1999},
  volume = {27},
  number = {12},
  pages = {68--71}
}
```

> [1] 王浩刚, 聂在平. 三维矢量散射积分方程中奇异性分析[J]. 电子学报, 1999, 27(12): 68-71.

##### 会议论文

```bibtex
@inproceedings{guide-conference,
  author = {Bergamasco, Filippo and Albarelli, Andrea and Cosmo, Luca and Torsello, Andrea and Rodola, Emanuele and Cremers, Daniel},
  title = {Adopting an unconstrained ray model in light-field cameras for {3D} shape reconstruction},
  booktitle = {{IEEE} Conference on Computer Vision and Pattern Recognition},
  location = {Boston, USA},
  year = {2015},
  pages = {3003--3012}
}
```

> [2] Bergamasco F, Albarelli A, Cosmo L, et al. Adopting an unconstrained ray model in light-field cameras for 3D shape reconstruction[C]. IEEE Conference on Computer Vision and Pattern Recognition, Boston, USA, 2015: 3003-3012.

##### 专著

```bibtex
@book{guide-book,
  author = {{罗杰斯}},
  title = {西方文明史：问题与源头},
  translator = {{潘惠霞} and {魏婧} and {杨艳} and others},
  edition = {2},
  address = {大连},
  publisher = {东北财经大学出版社},
  year = {2011},
  pages = {15--16}
}
```

> [3] 罗杰斯. 西方文明史：问题与源头[M]. 潘惠霞, 魏婧, 杨艳, 等译. 2 版. 大连: 东北财经大学出版社, 2011: 15-16.

##### 学位论文

```bibtex
@phdthesis{guide-thesis,
  author = {{陈念永}},
  title = {毫米波细胞生物效应及抗肿瘤研究},
  address = {成都},
  school = {电子科技大学},
  year = {2001},
  pages = {50--60}
}
```

> [4] 陈念永. 毫米波细胞生物效应及抗肿瘤研究[D]. 成都: 电子科技大学, 2001: 50-60.

##### 报纸文章

```bibtex
@newspaper{guide-newspaper,
  author = {{顾春}},
  title = {牢牢把握稳中求进的总基调},
  journal = {人民日报},
  date = {2012-03-31},
  number = {3}
}
```

> [5] 顾春. 牢牢把握稳中求进的总基调[N]. 人民日报, 2012-03-31 (3).

##### 报告

```bibtex
@techreport{guide-report,
  author = {{冯西桥}},
  title = {核反应堆压力容器的{LBB}分析},
  address = {北京},
  institution = {清华大学核能技术设计研究院},
  year = {1997}
}
```

> [6] 冯西桥. 核反应堆压力容器的 LBB 分析[R]. 北京: 清华大学核能技术设计研究院, 1997.

##### 授权专利

```bibtex
@patent{guide-patent,
  author = {{肖珍新}},
  title = {一种新型排渣阀调节降温装置},
  number = {ZL201120085830.0},
  date = {2012-04-25}
}
```

> [7] 肖珍新. 一种新型排渣阀调节降温装置: ZL201120085830.0[P]. 2012-04-25.

##### 标准

```bibtex
@standard{guide-standard,
  author = {{全国信息与文献标准化技术委员会}},
  title = {学位论文编写规则},
  number = {GB/T 7713.1-2006},
  address = {北京},
  publisher = {中国标准出版社},
  year = {2007},
  pages = {17--20}
}
```

> [8] 全国信息与文献标准化技术委员会. 学位论文编写规则: GB/T 7713.1-2006[S]. 北京: 中国标准出版社, 2007: 17-20.

##### 电子文献

网页：

```bibtex
@online{guide-webpage,
  author = {{电子科技大学研究生院}},
  title = {电子科技大学研究生学位论文撰写规范（2022年1月修订）},
  date = {2025-09-03},
  urldate = {2026-03-12},
  url = {https://gr.uestc.edu.cn/xiazai/114/3917}
}
```

> [9] 电子科技大学研究生院. 电子科技大学研究生学位论文撰写规范（2022年1月修订）[EB/OL]. (2025-09-03) [2026-03-12]. https://gr.uestc.edu.cn/xiazai/114/3917.

- 网页的`date`填写发布日期或更新日期，`urldate`填写实际访问日期，格式均为`年-月-日`（如`2026-03-12`）；请按实际情况填写，不要照抄示例日期

在线图书：

```bibtex
@book{guide-online-book,
  author = {William Deverell and David Igler},
  title = {A companion to {California} history},
  address = {New York},
  publisher = {John Wiley \& Sons},
  year = {2013},
  pages = {21--22},
  date = {2013-11-15},
  urldate = {2014-06-24},
  url = {https://onlinelibrary.wiley.com/doi/10.1002/9781444305036.ch2},
  medium = {OL}
}
```

> [10] Deverell W, Igler D. A companion to California history[M/OL]. New York: John Wiley & Sons, 2013: 21-22 (2013-11-15) [2014-06-24]. https://onlinelibrary.wiley.com/doi/10.1002/9781444305036.ch2.

##### 预印本（arXiv等）

已有正式发表版本且引用内容一致时，优先引用正式的期刊或会议论文。下面以Adam论文的arXiv初稿（v1）演示预印本写法：

```bibtex
@online{guide-preprint,
  author = {Diederik Kingma and Jimmy Ba},
  title = {{Adam}: A method for stochastic optimization},
  date = {2014-12-22},
  urldate = {2026-09-11},
  url = {https://arxiv.org/abs/1412.6980v1}
}
```

> [11] Kingma D, Ba J. Adam: A method for stochastic optimization[EB/OL]. (2014-12-22) [2026-09-11]. https://arxiv.org/abs/1412.6980v1.

- `date`填写所引版本的发布日期，`urldate`填写实际访问日期；链接末尾的`v1`表示第1版，应改为实际引用的版本
- 学校采用的GB/T 7714—2015未单列预印本；这里的`[EB/OL]`是本模板的兼容写法。现行GB/T 7714—2025使用`[PP/OL]`，本例未采用该新版格式

### 列表

#### 有序列表

学校规范的示例使用了 `1.` 和 `（1）` 等编号，可作为列表样式的参考，但没有明确规定它们必须对应哪一级列表。下面的写法参照其首行缩进、续行回到正文左边界的排法；这是模板提供的参考写法，不是学校单独规定的列表参数。

```latex
\begin{enumerate}
    \item 第一项内容。
    \item 较长的条目会自动换行，续行回到正文左边界。
\end{enumerate}
```

如需使用全角括号编号，将开头改为 `\begin{enumerate}[label=（\arabic*）,labelsep=0pt]`，右括号后不加额外间隔。这两种形式可以按内容选用，同类列表保持一致，不必把它们固定为上下级。

模板已为一级列表设置正文式排版：字体、字号、行距和两端对齐沿用正文，编号从首行缩进位置开始，续行回到正文左边界，不增加额外段落间距。每项用 `\item`，不必手动输入数字。

#### 无序列表

目前未在学校规范中找到统一的无序列表符号要求。下例使用圆点，适合没有先后顺序的并列内容；它是可选写法，不是学校指定样式。需要编号或在正文中指代某一项时，优先使用有序列表。

```latex
\begin{itemize}
    \item 第一项内容。
    \item 第二项内容。
\end{itemize}
```

以上默认样式适用于一级列表；嵌套列表未作统一调整。编号选项只影响当前列表。

### 附录

注释掉`\input{chapters/appendix}`即可不显示附录。

### 攻读学位期间取得的成果

注释掉`\input{chapters/achievements}`即可不显示攻读学位期间取得的成果。
