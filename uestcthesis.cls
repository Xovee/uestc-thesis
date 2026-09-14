%%
%% uestcthesis.cls
%% Copyright (C) 2025--2026 Xovee Xu
%%
%% This work may be distributed and/or modified under the
%% conditions of the LaTeX Project Public License, either version 1.3c
%% of this license or (at your option) any later version.
%% The latest version of this license is available at
%% https://www.latex-project.org/lppl.txt
%%
%% This work has the LPPL maintenance status `maintained'.
%% The Current Maintainer of this work is Xovee Xu.
%%
%% The work consists of the files described in NOTICE.md.
%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{uestcthesis}[2026/09/14 v1.0.2 UESTC Thesis Class by Xovee Xu]


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 设定

% 加载基础文档类
\LoadClass[12pt,twoside]{report} % 加载report文档类

\RequirePackage[
    a4paper,
    left=3cm,           % for 页边距
    right=3cm,          % for 页边距
    top=3cm,            % for 页边距
    bottom=3.18cm,      % for 页边距
    headheight=1.5cm,   % 控制页眉位置
    headsep=13.8pt,     % 控制页眉位置
    % showframe         % 显示页面框架
]{geometry}


% 引入packages
% 正文字体不接管传统数学字母表，避免粗体希腊字母的编码错配。
\PassOptionsToPackage{no-math}{fontspec}
\RequirePackage[
    PunctStyle=quanjiao,                % 全角中文标点符号
    CJKmath=true,                       % 在公式中使用中文
    % 自动混排间距为模板实现约定（非学校规定数值）；保留源码中的普通词间空格。
    CJKecglue={\hskip .25em plus .1em minus .1em},
    xCJKecglue=false,
    CJKspace=false,
    CJKglue={\hskip 0pt plus 0.05\baselineskip minus 0.05\baselineskip} % 调整文字间间距
]{xeCJK}                                % 中文支持
% \usepackage{fontspec}                   % 字体支持
\RequirePackage[
    dvipsnames,
    table
]{xcolor}                               % 颜色和表格着色支持
\RequirePackage{pdfpages}               % 在文档中插入pdf
\RequirePackage{fancyhdr}               % 页眉页脚支持
\RequirePackage[aftersep]{titlesec}     % 标题格式
\RequirePackage{setspace}               % 行间距
\RequirePackage{zhnumber}               % 中文数字
\RequirePackage{anyfontsize}            %
\RequirePackage[
    hidelinks,
    hyperfootnotes=false,
]{hyperref}    % 超链接与PDF书签支持
\RequirePackage[]{tocloft}              % 目录支持
\RequirePackage{graphicx}               % 图片支持
\RequirePackage{booktabs}               % 三线表横线支持
\RequirePackage{tabularx}               % 自适应列宽的表格支持
\RequirePackage{subcaption}             % 子图、子表及其标题支持
\RequirePackage{caption}                % 图表标题格式
\RequirePackage{enumitem}               % 有序、无序及描述列表格式
% 一级列表沿用正文的字体与行距，首行缩进，续行回到正文左边界。
\setlist[enumerate,1]{label=\arabic*.,wide=2em,topsep=0pt,partopsep=0pt,itemsep=0pt,parsep=0pt}
\setlist[itemize,1]{label=\textbullet,wide=2em,topsep=0pt,partopsep=0pt,itemsep=0pt,parsep=0pt}

\RequirePackage[
    perpage,
    bottom,
    flushmargin,
    hang,
]{footmisc}                             % 脚注支持
\RequirePackage{scrextend}              % 脚注支持
\RequirePackage{tikz}                   % 脚注支持
\RequirePackage{scalerel}               % 脚注支持
\RequirePackage[sort&compress]{gbt7714} % BibTeX与顺序编码引用
\RequirePackage{notoccite}              % 避免前置目录中的引用影响文献编号
\citestyle{gbt7714-numerical}
\setcitestyle{citesep={,\space}}

\RequirePackage{amsmath,amssymb}        % 数学支持
\RequirePackage{amsthm}                 % 定理和证明环境
\RequirePackage{aliascnt}               % 定理类环境共享编号并保留各自引用名称
\RequirePackage[chapter]{algorithm}     % 算法浮动环境（按章编号）
\RequirePackage{algpseudocode}          % 算法伪代码



% 定义学位类型、论文语言和目录标题显示参数
\newif\ifuestc@doctor
\newif\ifuestc@master
\newif\ifuestc@chinese
\newif\ifuestc@english
\DeclareOption{doctor}{\uestc@doctortrue}
\DeclareOption{master}{\uestc@mastertrue}
\DeclareOption{chinese}{\uestc@chinesetrue}
\DeclareOption{english}{\uestc@englishtrue}
\DeclareOption{tocdepth3}{\setcounter{tocdepth}{3}}
\ProcessOptions\relax
\ifuestc@doctor
    \ifuestc@master
        \ClassError{uestcthesis}
            {不能同时选择doctor和master}
            {请只保留一个学位类型选项。}%
    \fi
\fi
\ifuestc@chinese
    \ifuestc@english
        \ClassError{uestcthesis}
            {不能同时选择chinese和english}
            {请只保留一个论文语言选项。}%
    \fi
\fi
% 未指定学位类型时默认硕士。
\ifuestc@doctor
    \newcommand{\uestc@degree@zh}{博士}
    \newcommand{\uestc@degree@en}{Doctoral Dissertation}
    \newcommand{\uestc@achievements@en}{%
        Research Results Obtained During the Study for Doctoral Degree}
\else
    \newcommand{\uestc@degree@zh}{硕士}
    \newcommand{\uestc@degree@en}{Master Thesis}
    \newcommand{\uestc@achievements@en}{%
        Research Results Obtained During the Study for Master's Degree}
\fi
% 未指定论文语言时默认中文。
\ifuestc@english
    \newcommand{\uestc@mainheader}{%
        \uestc@degree@en{} of University of Electronic Science and Technology of China}
    \newcommand{\uestc@contents@title}{Contents}
    \newcommand{\uestc@contents@header}{Contents}
    \newcommand{\uestc@contents@bookmark}{Contents}
    \newcommand{\uestc@figures@title}{Figures}
    \newcommand{\uestc@figures@header}{Figures}
    \newcommand{\uestc@tables@title}{Tables}
    \newcommand{\uestc@tables@header}{Tables}
    \newcommand{\uestc@symbols@title}{Symbols}
    \newcommand{\uestc@symbols@header}{Symbols}
    \newcommand{\uestc@acronyms@title}{Acronyms}
    \newcommand{\uestc@acronyms@header}{Acronyms}
    \newcommand{\uestc@acknowledgements@title}{Acknowledgements}
    \newcommand{\uestc@acknowledgements@header}{Acknowledgements}
    \newcommand{\uestc@references@title}{References}
    \newcommand{\uestc@achievements@title}{\uestc@achievements@en}
    \newcommand{\uestc@figure@name}{Figure}
    \newcommand{\uestc@figure@listprefix}{Figure\space}
    \newcommand{\uestc@table@name}{Table}
    \newcommand{\uestc@table@listprefix}{Table\space}
    \newcommand{\uestc@theorem@name}{Theorem}
    \newcommand{\uestc@lemma@name}{Lemma}
    \newcommand{\uestc@proposition@name}{Proposition}
    \newcommand{\uestc@corollary@name}{Corollary}
    \newcommand{\uestc@definition@name}{Definition}
    \newcommand{\uestc@assumption@name}{Assumption}
    \newcommand{\uestc@remark@name}{Remark}
    \newcommand{\uestc@proof@name}{Proof}
    \newcommand{\uestc@headingfont}{\rmfamily\bfseries}
\else
    \newcommand{\uestc@mainheader}{电子科技大学\uestc@degree@zh{}学位论文}
    \newcommand{\uestc@contents@title}{目\hspace{1em}录}
    \newcommand{\uestc@contents@header}{目\hspace{.5em}录}
    \newcommand{\uestc@contents@bookmark}{目录}
    \newcommand{\uestc@figures@title}{\hspace{.25em}图目录}
    \newcommand{\uestc@figures@header}{图目录}
    \newcommand{\uestc@tables@title}{\hspace{.25em}表目录}
    \newcommand{\uestc@tables@header}{表目录}
    \newcommand{\uestc@symbols@title}{主要符号表}
    \newcommand{\uestc@symbols@header}{主要符号表}
    \newcommand{\uestc@acronyms@title}{缩略词表}
    \newcommand{\uestc@acronyms@header}{缩略词表}
    \newcommand{\uestc@acknowledgements@title}{致\hspace{1em}谢}
    \newcommand{\uestc@acknowledgements@header}{致\hspace{.5em}谢}
    \newcommand{\uestc@references@title}{参考文献}
    \newcommand{\uestc@achievements@title}{%
        攻读\uestc@degree@zh{}学位期间取得的成果}
    \newcommand{\uestc@figure@name}{图}
    \newcommand{\uestc@figure@listprefix}{图}
    \newcommand{\uestc@table@name}{表}
    \newcommand{\uestc@table@listprefix}{表}
    \newcommand{\uestc@theorem@name}{定理}
    \newcommand{\uestc@lemma@name}{引理}
    \newcommand{\uestc@proposition@name}{命题}
    \newcommand{\uestc@corollary@name}{推论}
    \newcommand{\uestc@definition@name}{定义}
    \newcommand{\uestc@assumption@name}{假设}
    \newcommand{\uestc@remark@name}{注}
    \newcommand{\uestc@proof@name}{证明}
    \newcommand{\uestc@headingfont}{\sffamily}
\fi


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 设定字体

% 六个本地字体文件齐全时优先使用fonts目录，否则使用系统字体。
\newif\ifuestc@localfonts
\uestc@localfontstrue
\newcommand*\uestc@checklocalfont[1]{%
    \IfFileExists{fonts/#1}{}{\uestc@localfontsfalse}%
}
\uestc@checklocalfont{simsun.ttc}
\uestc@checklocalfont{simhei.ttf}
\uestc@checklocalfont{times.ttf}
\uestc@checklocalfont{timesbd.ttf}
\uestc@checklocalfont{timesi.ttf}
\uestc@checklocalfont{timesbi.ttf}

\ifuestc@localfonts
    \ClassInfo{uestcthesis}{Using local thesis fonts from fonts/}

    % 中文字体：宋体、黑体
    \setCJKmainfont{simsun.ttc}[
        Path=fonts/,
        AutoFakeBold=2,
        AutoFakeSlant=0.25
    ]
    \setCJKsansfont{simhei.ttf}[
        Path=fonts/,
        AutoFakeBold=3,
        AutoFakeSlant=0.25
    ]
    \setCJKmonofont{simsun.ttc}[Path=fonts/]

    % 英文字体：Times New Roman
    \setmainfont{times.ttf}[
        Path=fonts/,
        BoldFont=timesbd.ttf,
        ItalicFont=timesi.ttf,
        BoldItalicFont=timesbi.ttf
    ]
    \setsansfont{times.ttf}[
        Path=fonts/,
        BoldFont=timesbd.ttf,
        ItalicFont=timesi.ttf,
        BoldItalicFont=timesbi.ttf
    ]
    % 英文等宽字体：Inconsolata（随TeX发行版提供）
    \setmonofont{Inconsolatazi4}[
        Scale=MatchLowercase,
        Extension=.otf,
        UprightFont=*-Regular,
        ItalicFont=*-Regular,
        BoldFont=*-Bold,
        BoldItalicFont=*-Bold,
        RawFeature={+ss01,+ss02}
    ]
\else
    \ClassInfo{uestcthesis}{Local thesis fonts are incomplete; using system fonts}

    % 中文字体：宋体、黑体
    \setCJKmainfont{SimSun}[
        AutoFakeBold=2,
        AutoFakeSlant=0.25
    ]
    \setCJKsansfont{SimHei}[
        AutoFakeBold=3,
        AutoFakeSlant=0.25
    ]
    \setCJKmonofont{SimSun}

    % 英文字体：Times New Roman
    \setmainfont{Times New Roman}
    \setsansfont{Times New Roman}
    % 英文等宽字体：Inconsolata（随TeX发行版提供）
    \setmonofont{Inconsolatazi4}[
        Scale=MatchLowercase,
        Extension=.otf,
        UprightFont=*-Regular,
        ItalicFont=*-Regular,
        BoldFont=*-Bold,
        BoldItalicFont=*-Bold,
        RawFeature={+ss01,+ss02}
    ]
\fi
% \setmathfont{Times New Roman}

% 字号
\renewcommand\footnotesize{\@setfontsize\footnotesize{9pt}{20pt}}   % 小五
\renewcommand\small{\@setfontsize\small{10.5pt}{20pt}}              % 五号
\renewcommand\normalsize{\@setfontsize\normalsize{12pt}{20pt}}      % 小四
\renewcommand\large{\@setfontsize\large{14pt}{20pt}}                % 四号
\renewcommand\Large{\@setfontsize\Large{15pt}{20pt}}                % 小三
\renewcommand\LARGE{\@setfontsize\LARGE{16pt}{20pt}}                % 三号
\renewcommand\huge{\@setfontsize\huge{18pt}{20pt}}                  % 小二
\renewcommand\Huge{\@setfontsize\Huge{22pt}{20pt}}                  % 二号


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 设定文档标题格式

\ifuestc@english
    \renewcommand{\thechapter}{Chapter \arabic{chapter}}
\else
    \renewcommand{\thechapter}{第\zhnumber{\arabic{chapter}}章}  % 章序号：第[中文数字]章
\fi
\renewcommand\thesection{\arabic{chapter}.\arabic{section}}  % 节号：章序号.节号
\renewcommand\thesubsection{\arabic{chapter}.\arabic{section}.\arabic{subsection}}  % 子节号：章序号.节号.子节号

% 章标题格式
\titleformat{\chapter}
    {\vspace{-18.7pt}\uestc@headingfont\Large\filcenter} % report默认在chapter前增加了vspace
    {\hspace{-4pt}\thechapter}{.5em}{}
\titlespacing{\chapter}{0pt}{24pt}{18pt}[0pt]
% 节标题格式
\titleformat{\section}
    {\uestc@headingfont\large}
    {\bfseries\rmfamily\thesection~}{0pt}{}
\titlespacing{\section}{0pt}{18pt plus 2pt minus 2pt}{6pt plus 1pt minus 1pt}
% 子节标题格式
\titleformat{\subsection}
    {\uestc@headingfont\large}
    {\bfseries\rmfamily\thesubsection\space}{0pt}{}
\titlespacing{\subsection}{0pt}{12pt plus 2pt minus 2pt}{6pt plus 1pt minus 1pt}
% 子子节标题格式
\setcounter{secnumdepth}{3} % 显示到四级标题
\titleformat{\subsubsection}
    {\uestc@headingfont\normalsize}
    {\bfseries\rmfamily\thesubsubsection\space}{0pt}{}
\titlespacing{\subsubsection}{0pt}{12pt plus 2pt minus 2pt}{6pt plus 1pt minus 1pt}

% 文档行结构设置
\setlength{\parskip}{0pt}
\baselineskip=20pt
\marginparsep=0pt
\ifuestc@english
    \XeTeXlinebreaklocale "en"
\else
    \XeTeXlinebreaklocale "zh"
\fi
\XeTeXlinebreakskip = 0pt plus 1pt
\raggedbottom % 页面底部段落设置
\setlength{\topskip}{15pt} % 页面内第一行文字上边距
% \flushbottom
\setlength{\emergencystretch}{3em}
\widowpenalty=150
\clubpenalty=0

% 文字断行设置
\hyphenpenalty=1000
\tolerance=1000

% 缩进两个字符
\setlength{\parindent}{2em}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 设定文档页眉页脚格式

% 默认设置 -> redefine plain style
\fancyhf{}
\renewcommand{\chaptermark}[1]{\markboth{\thechapter\hspace{.5em}#1}{}}
\fancyhead[CO]{\small\leftmark\vspace{-1.8pt}}
\fancyhead[CE]{\small\uestc@mainheader\vspace{-1.8pt}}
\fancyfoot[C]{\footnotesize \thepage}
\renewcommand{\headrulewidth}{0.75pt}
\setlength{\footskip}{1.11cm}
\setlength{\floatsep}{18pt plus 2pt minus 2pt} % 浮动体间距

\fancypagestyle{plain}[fancy]{}
% 中文摘要页眉页脚
\fancypagestyle{zhabshf}[fancy]{
    \fancyhead[CO]{\small 摘\hspace{.5em}要\vspace{-1.8pt}}
    \fancyhead[CE]{\small 摘\hspace{.5em}要\vspace{-1.8pt}}
    \fancyfoot[C]{\footnotesize \thepage}
}
% 英文摘要页眉页脚
\fancypagestyle{enabshf}[fancy]{
    \fancyhead[CO]{\small ABSTRACT\vspace{-1.8pt}}
    \fancyhead[CE]{\small ABSTRACT\vspace{-1.8pt}}
    \fancyfoot[C]{\footnotesize \thepage}
}
% 目录页眉页脚
\fancypagestyle{tochr}[fancy]{
    \fancyhf{}
    \fancyhead[CO]{\small\uestc@contents@header\vspace{-1.8pt}}
    \fancyhead[CE]{\small\uestc@contents@header\vspace{-1.8pt}}
    \fancyfoot[C]{\footnotesize \thepage}
}
% 图目录页眉页脚
\fancypagestyle{lofhr}[fancy]{
    \fancyhead[CO]{\small\uestc@figures@header\vspace{-1.8pt}}
    \fancyhead[CE]{\small\uestc@figures@header\vspace{-1.8pt}}
    \fancyfoot[C]{\footnotesize \thepage}
}
% 表目录页眉页脚
\fancypagestyle{lothr}[fancy]{
    \fancyhead[CO]{\small\uestc@tables@header\vspace{-1.8pt}}
    \fancyhead[CE]{\small\uestc@tables@header\vspace{-1.8pt}}
    \fancyfoot[C]{\footnotesize \thepage}
}
% 主要符号表页眉页脚
\fancypagestyle{symbolshf}[fancy]{
    \fancyhead[CO]{\small\uestc@symbols@header\vspace{-1.8pt}}
    \fancyhead[CE]{\small\uestc@symbols@header\vspace{-1.8pt}}
    \fancyfoot[C]{\footnotesize \thepage}
}
% 缩略词表页眉页脚
\fancypagestyle{acronymshf}[fancy]{
    \fancyhead[CO]{\small\uestc@acronyms@header\vspace{-1.8pt}}
    \fancyhead[CE]{\small\uestc@acronyms@header\vspace{-1.8pt}}
    \fancyfoot[C]{\footnotesize \thepage}
}
% 正文页眉页脚
\fancypagestyle{mainhf}[fancy]{
    \fancyhead[CO]{\small\leftmark\vspace{-1.8pt}}
    \fancyhead[CE]{\small\uestc@mainheader\vspace{-1.8pt}}
    \fancyfoot[C]{\footnotesize \thepage}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 定义新的特殊页面：摘要、ABSTRACT

% 中文摘要页面
\newcommand{\zhabstract}{%
    \clearpage
    \pdfbookmark[0]{摘要}{uestc.abstract.zh}%
    \chapter*{\sffamily\mdseries 摘\hspace{1em}要}
    \pagestyle{zhabshf}
}
% 英文摘要页面
\newcommand{\enabstract}{%
    \clearpage
    \pdfbookmark[0]{ABSTRACT}{uestc.abstract.en}%
    \chapter*{\rmfamily\bfseries ABSTRACT}
    \pagestyle{enabshf}
}
% 中文摘要中的关键词
\newcommand{\keywords}[1]{%
    \par
    \vspace{12pt}%
    \begingroup
    \hangindent=4em%
    \noindent\textbf{\makebox[4em]{关键词：}}#1%
    \par
    \endgroup
}
% 英文摘要中的关键词
\newcommand{\enkeywords}[1]{%
    \par
    \vspace{12pt}%
    \begingroup
    \hangindent=5em%
    \noindent\textbf{\makebox[5em]{Keywords: }}#1%
    \par
    \endgroup
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 外部PDF页面：使用独立的内部页标签，避免与正文页码重复。

\newcommand{\uestcincludeexternalpdf}[3]{%
    \begingroup
    \setcounter{page}{1}%
    \renewcommand{\thepage}{#1\arabic{page}}%
    \includepdf[pages=#2]{#3}%
    \endgroup
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 前置部分样式

\newcommand{\uestcfrontmatter}{%
    \clearpage
    \pagenumbering{Roman}
    \setcounter{page}{1}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 目录页面、图目录页面、表目录页面

% 目录标题格式
\renewcommand{\cftbeforetoctitleskip}{5.3pt}
\renewcommand{\cftaftertoctitleskip}{18pt}
\renewcommand{\cfttoctitlefont}{\hfill\Large\uestc@headingfont}
\renewcommand{\cftaftertoctitle}{\hfill}

% 图目录标题格式
\renewcommand{\cftbeforeloftitleskip}{5.3pt}
\renewcommand{\cftafterloftitleskip}{18pt}
\renewcommand{\cftloftitlefont}{\hfill\Large\uestc@headingfont}
\renewcommand{\cftafterloftitle}{\hfill}

% 目录标题格式
\renewcommand{\cftbeforelottitleskip}{5.3pt}
\renewcommand{\cftafterlottitleskip}{18pt}
\renewcommand{\cftlottitlefont}{\hfill\Large\uestc@headingfont}
\renewcommand{\cftafterlottitle}{\hfill}

\setlength{\cftbeforechapskip}{0pt} % 目录章entry上间距

\renewcommand{\cftdot}{\raisebox{1pt}{\ensuremath{\cdot}}} % 略微提升leader的位置，使其与文字垂直居中对齐
\renewcommand{\cftdotsep}{.5} % leader密度
\renewcommand{\cftchapfont}{\uestc@headingfont} % 章标题字体

% 目录标题缩进
\ifuestc@english
    \cftsetindents{chapter}{0em}{3.5em}
\else
    \cftsetindents{chapter}{0em}{3.5em}
\fi
\cftsetindents{section}{1.7em}{1.8em}
\cftsetindents{subsection}{3.6em}{2.5em}
\cftsetindents{subsubsection}{6.1em}{3.2em}

% 定义ToC, LoF, LoT中的entries格式，主要为了支持数字超过1位时的对齐问题
\renewcommand{\numberline}[1]{%
  \@cftbsnum #1\@cftasnum\hspace{.5em}\@cftasnumb%
}

\renewcommand{\cftchapleader}{\cftdotfill{\cftsecdotsep}} % 增加章级别的leader
\renewcommand{\cftchappagefont}{\normalfont} % 章页码字体变为正常字体，默认为粗体
\setlength\cftparskip{0pt} % 目录entries间距

% 各目录测量页码，将最宽值写入aux供下一遍设置标题换行的安全右边距。
% 每行页码盒仅采用该页码的实际宽度，避免短页码前留下整列空白。
% 不额外读取toc/lof/lot，避免目录内引用或其他命令被重复执行。
\newdimen\uestc@listpnummax
\newdimen\uestc@listpnumwidth
\newcommand{\uestclistpnumwidth}[2]{%
    \expandafter\gdef\csname uestc@listpnum@#1\endcsname{#2}%
}
\newcommand{\uestc@beginlistpnums}[1]{%
    \begingroup
    \def\uestc@activelist{#1}%
    \global\uestc@listpnummax=0pt\relax
    \@ifundefined{uestc@listpnum@#1}{%
        \settowidth{\uestc@listpnumwidth}{\normalfont 0}%
    }{%
        \uestc@listpnumwidth=\csname uestc@listpnum@#1\endcsname\relax
    }%
    \edef\@pnumwidth{\the\uestc@listpnumwidth}%
    \edef\@tocrmarg{\the\dimexpr\uestc@listpnumwidth+2pt\relax}%
}
\newcommand{\uestc@endlistpnums}[1]{%
    \ifdim\uestc@listpnummax>0pt\relax
        \if@filesw
            \immediate\write\@auxout{%
                \string\uestclistpnumwidth{#1}{\the\uestc@listpnummax}}%
        \fi
        \ifdim\uestc@listpnummax=\uestc@listpnumwidth\else
            \ClassWarningNoLine{uestcthesis}{%
                Page-number width for #1 changed. Rerun LaTeX}%
        \fi
    \fi
    \endgroup
}
\newcommand{\uestc@measurelistpnum}[2]{%
    \ifdefined\uestc@activelist
        % fillnum在tocloft的单条目录分组内调用，设置只作用于当前条目。
        \setbox\@tempboxa=\hbox{\csname cft#1pagefont\endcsname #2}%
        \edef\@pnumwidth{\the\dimexpr\wd\@tempboxa+2pt\relax}%
        \ifdim\wd\@tempboxa>\uestc@listpnummax
            \global\uestc@listpnummax=\wd\@tempboxa
        \fi
    \fi
}
% notoccite会接管@starttoc，故挂接最终读取命令而不依赖tocloft的旧入口。
\newcommand{\uestc@withstandardlist}[2]{%
    \ifboolexpr{test {\ifstrequal{#1}{toc}} or
        test {\ifstrequal{#1}{lof}} or test {\ifstrequal{#1}{lot}}}{#2{#1}}{}%
}
\AddToHookWithArguments{cmd/@starttoc/before}{%
    \uestc@withstandardlist{#1}{\uestc@beginlistpnums}}
\AddToHookWithArguments{cmd/@starttoc/after}{%
    \uestc@withstandardlist{#1}{\uestc@endlistpnums}}

% 保留tocloft原生页码盒、链接/结构钩子和当前点线样式。
\newcommand{\uestc@configurelistpnum}[1]{%
    \csletcs{uestc@native@#1fillnum}{cft#1fillnum}%
    \csletcs{uestc@native@#1leader}{cft#1leader}%
    \csdef{cft#1leader}{\hspace{2pt}\csuse{uestc@native@#1leader}}%
    \csdef{cft#1fillnum}##1{%
        \uestc@measurelistpnum{#1}{##1}%
        \ifstrequal{#1}{chap}{%
            \ifuestc@english
                % 自然英文词间距，同时保留页码区并抵消末行右缩进。
                \rightskip=\@tocrmarg plus 2em\relax
                \parfillskip=-\@tocrmarg\relax
            \fi
        }{}%
        \csuse{uestc@native@#1fillnum}{##1}%
    }%
}
\uestc@configurelistpnum{chap}
\uestc@configurelistpnum{sec}
\uestc@configurelistpnum{subsec}
\uestc@configurelistpnum{subsubsec}
\uestc@configurelistpnum{fig}
\uestc@configurelistpnum{tab}

% 目录命令
\renewcommand{\contentsname}{\uestc@contents@title} % 目录标题
\newcommand{\uestctableofcontents}{
    \clearpage
    \pagestyle{tochr}
    \pdfbookmark[0]{\uestc@contents@bookmark}{uestc.contents}%
    \tableofcontents
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 图目录、表目录
\renewcommand{\listfigurename}{\uestc@figures@title}
\newcommand{\uestclistoffigures}{
    \clearpage
    \pagestyle{lofhr}
    \pdfbookmark[0]{\uestc@figures@header}{uestc.listoffigures}%
    \listoffigures
}

\renewcommand{\listtablename}{\uestc@tables@title}
\newcommand{\uestclistoftables}{
    \clearpage
    \pagestyle{lothr}
    \pdfbookmark[0]{\uestc@tables@header}{uestc.listoftables}%
    \listoftables
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 主要符号表页面
\newcommand{\uestcsymbols}{%
    \clearpage
    \pdfbookmark[0]{\uestc@symbols@header}{uestc.symbols}%
    \chapter*{\uestc@symbols@title}
    \pagestyle{symbolshf}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 缩略词表页面
\newcommand{\uestcacronyms}{%
    \clearpage
    \pdfbookmark[0]{\uestc@acronyms@header}{uestc.acronyms}%
    \chapter*{\uestc@acronyms@title}
    \pagestyle{acronymshf}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 正文章节样式

\newcommand{\uestcmainmatter}{%
    \clearpage
    \pagenumbering{arabic}
    \setcounter{page}{1}
    \pagestyle{mainhf}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 图格式
\setlength{\textfloatsep}{12pt plus 2pt minus 2pt} % 浮动元素间距
\setlength{\intextsep}{12pt plus 2pt minus 2pt} % 浮动元素与文字间距
\DeclareCaptionLabelSeparator{halfzhspace}{\hspace{.5em}}
\DeclareCaptionListFormat{lofcaptionfmt}{\uestc@figure@listprefix#1#2}  % #1 and #2
\captionsetup[figure]{
    font={small},
    aboveskip=6pt plus 1pt minus 1pt,
    belowskip=0pt,
    format={plain},
    indention=0em,
    labelsep={halfzhspace},
    justification={justified},
    margin={4em},
    position=auto,
    name=\uestc@figure@name,
    listformat=lofcaptionfmt,
}
\renewcommand{\thefigure}{\arabic{chapter}-\arabic{figure}}

% \AtEndEnvironment{figure}{\addvspace{-6pt}}

\cftsetindents{figure}{0em}{3.1em}

\subcaptionsetup[figure]{
    font={small}, % 分图序号使用五号，覆盖宏包默认的smaller
    skip=0pt,
    belowskip=0pt
}

% \begin{table}\ContinuedFloat will result two tables with the same number


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 图附注
\newcommand{\fignote}[1]{%
    \vspace{12pt}%
    \par\small\noindent
    \leftskip=0pt\rightskip=0pt\parfillskip=0pt plus 1fil
    #1\par%
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 表格式
% 表内文字使用独立的单倍行距；13.6pt是结合宋体Word样例的实现取值。
% 保留原有行支撑盒，使单行表格高度与用户的arraystretch设置保持稳定。
\newsavebox{\uestc@tablestrut}
\newcommand{\uestc@tablefont}{%
    \linespread{1}\small
    \setbox\uestc@tablestrut\copy\strutbox
    \fontsize{10.5pt}{13.6pt}\selectfont
    \setbox\strutbox\copy\uestc@tablestrut
}
\AtBeginEnvironment{tabular}{\uestc@tablefont}
\AtBeginEnvironment{tabularx}{\uestc@tablefont}
\AtBeginEnvironment{tabular*}{\uestc@tablefont}
\DeclareCaptionListFormat{lotcaptionfmt}{\uestc@table@listprefix#1#2}
\renewcommand{\arraystretch}{.85} % 设置为模板建议的约0.6厘米：20*0.85=17pt~=0.6cm
\captionsetup[table]{
    font={small},
    aboveskip=6pt,
    belowskip=0pt,
    format={plain},
    indention=0em,
    labelsep={halfzhspace},
    justification={justified},
    margin={4em},
    position=auto,
    name=\uestc@table@name,
    listformat=lotcaptionfmt,
}
\renewcommand{\thetable}{\arabic{chapter}-\arabic{table}}

\cftsetindents{table}{0em}{3.1em} % 表目录缩进

% \AtEndEnvironment{table}{\addvspace{-6pt}}

\setlength{\heavyrulewidth}{1.5pt}
\setlength{\lightrulewidth}{.75pt}
\setlength{\cmidrulewidth}{.75pt}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 算法
\renewcommand{\thealgorithm}{\arabic{chapter}-\arabic{algorithm}}
\providecommand*{\algorithmautorefname}{}
\ifuestc@english
    \renewcommand*{\algorithmautorefname}{Algorithm}
\else
    \floatname{algorithm}{算法}
    \renewcommand*{\algorithmautorefname}{算法}
\fi


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 表附注
\newcommand{\tabnote}[1]{%
    \vspace{12pt}%
    \par\small\noindent
    \leftskip=0pt\rightskip=0pt\parfillskip=0pt plus 1fil
    #1\par
    \vspace{6pt}%
}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 脚注
\renewcommand{\footnoterule}{\noindent\rule{5.1cm}{.6pt}\vspace{6pt}} %% 6

\renewcommand{\@makefntext}[1]{
    \noindent\hangindent=1.5em
    \setstretch{.58}%
    \raisebox{-1pt}{\scalebox{1.3}{\circled{\thefootnotemark}}}\hspace{.5em}{#1}
}

\newcommand{\fnrad}{.175}
\newcommand\circled[2][\fnrad]{\kern.5pt\scalerel*{\tikz{\useasboundingbox (-#1,-#1) rectangle (#1,#1);\node{#2};\draw[line width=.3pt] circle[radius=#1];}}{X}\kern.5pt}
\deffootnotemark{\textsuperscript{\smash{\circled{\thefootnotemark}}}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 致谢页面
\newcommand{\uestcacknowledgements}{
    \chapter*{\uestc@acknowledgements@title%
        \markboth{\uestc@acknowledgements@header}{}}
    \addcontentsline{toc}{chapter}{\uestc@acknowledgements@title}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 参考文献页面
% 在列表计算宽度前设置五号字和编号间距；沿用natbib的悬挂缩进。
\renewcommand{\bibfont}{\small\setlength{\labelsep}{.5em}}
\setlength{\bibsep}{0pt}
\renewcommand{\bibsection}{%
    \chapter*{\uestc@references@title\markboth{\uestc@references@title}{}}%
    \addcontentsline{toc}{chapter}{\uestc@references@title}%
}
\let\uestc@thebibliography\thebibliography
\let\uestc@endthebibliography\endthebibliography
\renewenvironment{thebibliography}[1]{%
    \uestc@thebibliography{#1}%
    % 仅禁止同一条文献段落内的分页；环境结束后恢复正文参数。
    \interlinepenalty=10000\relax
    \let\url\nolinkurl
}{\uestc@endthebibliography}

% 文件名省略.bib；多个文献库用逗号分隔。
\newcommand{\uestcprintbibliography}[1][references]{%
    \bibliographystyle{uestcthesis}%
    \bibliography{#1}%
}

% 保留原模板上标前后的去空白、断行控制和零宽节点。
% gbt7714默认额外加入的1pt间距不属于学校示例要求。
\newcommand*\uestc@cite@unspace{%
    \ifhmode
        \ifdim\lastskip>\z@
            \unskip\expandafter\uestc@cite@unspace
        \else
            \ifnum\lastpenalty>\z@
                \unpenalty\expandafter\uestc@cite@unspace
            \fi
        \fi
    \fi
}
\renewcommand\NAT@citesuper[3]{%
    \ifNAT@swa
        \if*#2*\else#2\NAT@spacechar\fi
        \uestc@cite@unspace
        \nobreak\hskip\z@skip
        \textsuperscript{\NAT@@open#1\NAT@@close\if*#3*\else#3\fi}%
        \kern\z@
    \else
        #1%
    \fi
    \endgroup
}

% cite为上标；citep为句子成分中的非上标方括号引用。
% 在natbib原有局部分组内切换，保留星号、前注和页码参数的解析。
\DeclareRobustCommand\citep{%
    \begingroup
    \NAT@superfalse\NAT@set@cites
    \NAT@swatrue\let\NAT@ctype\z@\NAT@partrue
    \@ifstar{\NAT@fulltrue\NAT@citetp}{\NAT@fullfalse\NAT@citetp}%
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 引用样式
\ifuestc@english
    % 章和附录编号已经包含Chapter或Appendix，不再重复添加名称。
    \def\chapterautorefname~#1\null{#1}
    \def\appendixautorefname~#1\null{#1}
    \def\sectionautorefname{Section}
    \def\subsectionautorefname{Subsection}
    \def\subsubsectionautorefname{Subsubsection}
    \renewcommand{\figureautorefname}{Figure}
    \renewcommand{\tableautorefname}{Table}
    \renewcommand{\equationautorefname}{Equation}
\else
    % 章和附录编号已经包含中文名称；节号在引用时补为“第X节”。
    \def\chapterautorefname~#1\null{#1}
    \def\appendixautorefname~#1\null{#1}
    \def\sectionautorefname~#1\null{第#1节}
    \def\subsectionautorefname~#1\null{第#1节}
    \def\subsubsectionautorefname~#1\null{第#1节}
    \renewcommand{\figureautorefname}{图}
    \renewcommand{\tableautorefname}{表}
    \renewcommand{\equationautorefname}{式}
    \def\equationautorefname~#1\null{式~(#1)\null}
\fi
\renewcommand{\theequation}{\arabic{chapter}-\arabic{equation}}

% 短引用的文字和链接边界必须一起排版，避免XeLaTeX页界链接覆盖页眉/页脚。
% 星号形式没有链接；数学引用组成单个数学原子，以保留数学字号和间距。
\newcommand*{\uestc@referencebox}[2]{%
    \ifmmode
        \mathord{#1{#2}}%
    \else
        \mbox{#1{#2}}%
    \fi
}
% nameref在begindocument中重设ref/pageref，因此在该阶段结束后保存最终定义。
\AddToHook{begindocument/end}{%
    \NewCommandCopy{\uestc@originalref}{\ref}%
    \RenewDocumentCommand{\ref}{s m}{%
        \IfBooleanTF{#1}
            {\uestc@originalref*{#2}}%
            {\uestc@referencebox\uestc@originalref{#2}}%
    }%
    \NewCommandCopy{\uestc@originalautoref}{\autoref}%
    \RenewDocumentCommand{\autoref}{s m}{%
        \IfBooleanTF{#1}
            {\uestc@originalautoref*{#2}}%
            {\uestc@referencebox\uestc@originalautoref{#2}}%
    }%
    \NewCommandCopy{\uestc@originalpageref}{\pageref}%
    \RenewDocumentCommand{\pageref}{s m}{%
        \IfBooleanTF{#1}
            {\uestc@originalpageref*{#2}}%
            {\uestc@referencebox\uestc@originalpageref{#2}}%
    }%
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 定理和证明环境
% 学校规范要求“定理 X.X”“引理 X.X”和“证明”等字使用黑体，
% 证明结尾使用黑色方块。所有定理类环境按章共用一套编号。
\newtheoremstyle{uestctheorem}%
    {6pt}% 段前距
    {6pt}% 段后距
    {\normalfont}% 正文
    {0pt}% 缩进
    {\uestc@headingfont\upshape}% 标题
    {}% 标题后的标点
    {.5em}% 标题后的间距
    {}% 标题格式
\theoremstyle{uestctheorem}
\newtheorem{theorem}{\uestc@theorem@name}[chapter]
\renewcommand{\thetheorem}{\arabic{chapter}.\arabic{theorem}}
\newaliascnt{lemma}{theorem}
\newtheorem{lemma}[lemma]{\uestc@lemma@name}
\aliascntresetthe{lemma}
\newaliascnt{proposition}{theorem}
\newtheorem{proposition}[proposition]{\uestc@proposition@name}
\aliascntresetthe{proposition}
\newaliascnt{corollary}{theorem}
\newtheorem{corollary}[corollary]{\uestc@corollary@name}
\aliascntresetthe{corollary}
\newaliascnt{definition}{theorem}
\newtheorem{definition}[definition]{\uestc@definition@name}
\aliascntresetthe{definition}
\newaliascnt{assumption}{theorem}
\newtheorem{assumption}[assumption]{\uestc@assumption@name}
\aliascntresetthe{assumption}
\newaliascnt{remark}{theorem}
\newtheorem{remark}[remark]{\uestc@remark@name}
\aliascntresetthe{remark}
\def\theoremautorefname{\uestc@theorem@name}
\def\lemmaautorefname{\uestc@lemma@name}
\def\propositionautorefname{\uestc@proposition@name}
\def\corollaryautorefname{\uestc@corollary@name}
\def\definitionautorefname{\uestc@definition@name}
\def\assumptionautorefname{\uestc@assumption@name}
\def\remarkautorefname{\uestc@remark@name}
\renewcommand{\qedsymbol}{\ensuremath{\blacksquare}}
\renewenvironment{proof}[1][\uestc@proof@name]{%
    \par
    \pushQED{\qed}%
    \normalfont
    \topsep 6pt plus 2pt minus 2pt\relax
    \trivlist
    \item[\hskip\labelsep\uestc@headingfont\upshape #1]\ignorespaces
}{%
    \popQED
    \endtrivlist
    \@endpefalse
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 公式
\setlength{\abovedisplayskip}{6pt} % 公式上间距
\setlength{\belowdisplayskip}{6pt} % 公式下间距
\setlength{\abovedisplayshortskip}{6pt} % 前一行较短时的公式上间距
\setlength{\belowdisplayshortskip}{6pt} % 前一行较短时的公式下间距


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 附录页面
\newif\ifuestc@appendixbody
% 附录普通文字用五号；陈列公式和编号仍按规范使用小四号。
% 环境分组会在公式结束后自动恢复附录正文字号，行内数学随正文。
\newcommand{\uestc@appendixdisplayfont}[1]{%
    \AtBeginEnvironment{#1}{\ifuestc@appendixbody\normalsize\fi}%
}
\forcsvlist{\uestc@appendixdisplayfont}{equation,equation*,align,align*,alignat,alignat*,flalign,flalign*,gather,gather*,multline,multline*,displaymath}

\newcommand{\uestcappendix}{
    \par
    \appendix
    \uestc@appendixbodytrue
    \small
    \setlength{\parindent}{2em}
    \ifuestc@english
        \renewcommand{\thechapter}{Appendix \Alph{chapter}}
    \else
        \renewcommand{\thechapter}{附录\Alph{chapter}}
    \fi
    \renewcommand{\thesection}{\Alph{chapter}.\arabic{section}}
    \renewcommand{\thesubsection}{%
        \Alph{chapter}.\arabic{section}.\arabic{subsection}}
    \renewcommand{\thefigure}{\Alph{chapter}-\arabic{figure}}
    \renewcommand{\thetable}{\Alph{chapter}-\arabic{table}}
    \renewcommand{\theequation}{\Alph{chapter}-\arabic{equation}}
    \renewcommand{\thealgorithm}{\Alph{chapter}-\arabic{algorithm}}
    \renewcommand{\thetheorem}{\Alph{chapter}.\arabic{theorem}}
    \aliascntresetthe{lemma}
    \aliascntresetthe{proposition}
    \aliascntresetthe{corollary}
    \aliascntresetthe{definition}
    \aliascntresetthe{assumption}
    \aliascntresetthe{remark}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 攻读学位期间取得的成果页面
\newcommand{\uestcachievements}{
    \par
    \ifuestc@appendixbody
        \uestc@appendixbodyfalse
        \normalsize
        \setlength{\parindent}{2em}
    \fi
    \chapter*{\uestc@achievements@title%
        \markboth{\uestc@achievements@title}{}}
    \addcontentsline{toc}{chapter}{\uestc@achievements@title}
}



\endinput
