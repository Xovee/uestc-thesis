# UESTC Thesis User Guide

This guide explains how to use UESTC Thesis and introduces some LaTeX basics. If anything is unclear, you can ask your preferred AI assistant.

For more LaTeX writing techniques, see the Chinese-language guide [The Not So Short Introduction to LaTeX 2ε](https://tug.org/docs/latex/lshort-chinese/lshort-zh-cn.pdf). Chapter 4 covers mathematical typesetting and common mathematical symbols.

## Getting Started

The short version: install TeX Live, install VS Code, install the LaTeX Workshop extension, download the UESTC Thesis template, and start writing.

### The Basic Workflow

Instead of writing in Word or WPS, you edit `.tex` files and compile them to produce a PDF.

Open `main.tex` in the language package you downloaded. This is the entry point for the entire thesis and brings all the chapters together.

### Installing LaTeX

- Windows: install TeX Live 2026; see the [official Windows instructions](https://tug.org/texlive/windows.html).
- macOS: download and install MacTeX 2026 from the [official MacTeX download page](https://tug.org/mactex/mactex-download.html).
- Linux: install TeX Live 2026; see the [official Linux/Unix installation instructions](https://tug.org/texlive/quickinstall.html).

### Installing VS Code and LaTeX Workshop

1. Download and install the version for your system from the [VS Code website](https://code.visualstudio.com/Download).
2. Open VS Code, click the **Extensions** icon on the left, search for `LaTeX Workshop`, and install the extension published by `James Yu`.
3. If VS Code was open while you installed LaTeX, close and reopen VS Code after installation.

### Editing Online (Optional)

[Overleaf](https://www.overleaf.com/) lets you edit your thesis and generate, preview, and download its PDF in a browser, without installing TeX Live or VS Code on your computer.

1. Log in to Overleaf, choose **New Project → Upload Project**, and upload the Chinese or English template ZIP you downloaded. No extraction is needed.
2. Open the project settings, set **Compiler** to `XeLaTeX` and **TeX Live version** to `2026`, and confirm that **Main document** is `main.tex`.
3. Click **Recompile** to check that the template example produces a PDF successfully.
4. Set your thesis information in `main.tex` and edit the chapter files in `chapters`. Click **Recompile** after making changes to see the result.
5. When finished, use the download button in the PDF preview area to save your thesis PDF.

Both Chinese and English examples have passed testing on the Free plan. Long theses or those with many figures and tables may exceed the free compile timeout. If this happens, compile locally or in a project created and owned by an Overleaf Premium subscriber.

### Downloading the Template

Choose `uestc-thesis-xovee-chinese.zip` for a thesis in Chinese or `uestc-thesis-xovee-english.zip` for a thesis in English.
Each package has a single `main.tex` entry point, with the sample chapters and default language already configured. Both packages retain the Chinese and English abstracts.

After extracting the package, the main files and folders are:

- `main.tex`: the thesis entry point;
- `chapters`: chapter content;
- `figures`: thesis figures;
- `references.bib`: bibliographic entries.

### Choosing XeLaTeX

Use `Recipe: latexmk (xelatex)`, rather than `pdfLaTeX` or another compiler.
The template's configuration already selects this recipe. When you open the template folder normally, you do not need to choose it manually.

### Generating the Thesis PDF

For your first build:

1. In VS Code, choose **File → Open Folder** and open the extracted template folder containing `main.tex`.
   The template's configuration is loaded automatically. If prompted to trust the folder, first check that the template comes from a source you trust.
2. Open `main.tex`, press `F1`, and select `LaTeX Workshop: Build LaTeX project` to compile it once.
3. When compilation finishes, press `F1` and select `LaTeX Workshop: View LaTeX PDF file` to open the PDF preview on the right.

The generated PDF is saved as `output/main.pdf` inside the template folder. You can send, print, or submit this file.

After that, edit the `.tex` files in `chapters` on the left and press `Ctrl/Command + S` to save. The PDF preview on the right updates after a successful build. Keep editing, saving, and checking the result; you do not need to start each build manually.

You may also find these shortcuts useful: select some text, press `Ctrl/Command + L`, and then `Ctrl/Command + B` to toggle bold formatting.
For more shortcuts and snippets, see the [LaTeX Workshop documentation](https://github.com/James-Yu/LaTeX-Workshop/wiki/Snippets#font-commands-and-snippets), or ask an AI assistant.

### The Thesis Cover

I recommend downloading the [university's cover template](https://gr.uestc.edu.cn/xiazai/114/3917), filling it in, exporting it as a `PDF`, and importing it into the project, instead of creating the cover in LaTeX.

## Examples

### Thesis Settings

- `main.tex` in your downloaded package is the thesis entry point.
- You generally do not need to edit `uestcthesis.cls`.
- `\documentclass[master,chinese]{uestcthesis}` selects a master's thesis in Chinese.
- `\documentclass[doctor,chinese]{uestcthesis}` selects a doctoral dissertation in Chinese.
- The English package defaults to `\documentclass[master,english]{uestcthesis}`. For a doctoral dissertation, change `master` to `doctor`.
- The language option changes the template's headings and formatting; it does not translate your written content.
- To add a package, place `\usepackage{...}` before `\begin{document}`, for example `\usepackage{multirow}`.
- To define your own command, place its definition before `\begin{document}`, for example `\newcommand{\mymethod}{Model Name}`.
- Set the PDF title and author information using `pdftitle={}` and `pdfauthor={}`.
- To hide a component, comment out its command. For example, use `% \uestclistoffigures` to omit the list of figures, or `% \input{chapters/symbols}` to omit the list of symbols. The usual shortcut for commenting is `Ctrl/Command + /`.
- To include fourth-level headings in the table of contents, add `tocdepth3`; for example, `\documentclass[master,chinese,tocdepth3]{uestcthesis}` for a master's thesis in Chinese.
- Page margins, spacing, font sizes, and other layout settings are already configured by the template.

### Abstracts

Edit `chapters/abstract.tex`.

### Table of Contents

The table of contents is generated automatically.

### List of Figures

Comment out `\uestclistoffigures` to omit the list of figures.

### List of Tables

Comment out `\uestclistoftables` to omit the list of tables.

### List of Symbols

Comment out `\input{chapters/symbols}` to omit the list of symbols.

### List of Acronyms

Comment out `\input{chapters/acronyms}` to omit the list of acronyms.

### Text Formatting

- Regular text: simply type it.
- Bold: `\textbf{bold text}`.
- Italics: `\textit{italic text}`.
- Bold italics: `\textbf{\textit{bold italic text}}`.
- Underlining: `\underline{underlined text}`.
- Superscripts: `m\textsuperscript{2}` produces m².
- Subscripts: `H\textsubscript{2}O` produces H₂O.
- Monospaced text: `\texttt{PyThon}`.
- Font size: `{\small smaller text}` and `{\large larger text}`. Keep the outer braces `{}`.
- Common font sizes in this template are `\small` (10.5 pt, Chinese size 五号), `\normalsize` (12 pt, 小四), `\large` (14 pt, 四号), and `\Large` (15 pt, 小三). Command names are case-sensitive.
- Text color: `\textcolor{red}{red text}`. You can replace `red` with `blue`, `green`, or another color name.
- Custom color: `\textcolor[RGB]{51,102,153}{text in a custom color}`. The three values specify red, green, and blue, each from 0 to 255.

### Special Characters

These characters need special commands when used in ordinary text:

- `%`: `\%`, for example `95\%`. A plain `%` starts a comment and hides the rest of that line.
- `&`: `\&`.
- `_`: `\_`.
- `#`: `\#`.
- `$`: `\$`.
- `{`: `\{`.
- `}`: `\}`.
- Backslash `\`: `\textbackslash{}`.
- For other symbols or problems, ask an AI assistant.

### Chapters and Headings

- First-level heading: `\chapter{Introduction}`.
- Second-level heading: `\section{Background}`.
- Third-level heading: `\subsection{Research Objectives}`.
- Fourth-level heading: `\subsubsection{First Objective}`.
- A fifth-level heading is not written as `\subsubsubsection{}`; adding another `sub` does not create a valid command.
- Body text: simply type it. To start a new paragraph, press Enter twice to leave a blank line.
- To add a chapter, create `chapter-2.tex` (or another filename) in `chapters`, then add `\input{chapters/chapter-2}` (or the corresponding filename) to `main.tex`.

### Figures

Place images in `figures`, or another folder if you specify the correct path when including them. I recommend vector images, such as `PDF` files, so that they stay sharp when enlarged.

#### A Single Figure

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\linewidth]{figures/uestc-logo.png}
    \caption{UESTC Visual Identity}
    \label{fig:guide-single}
    \fignote{Note: Add an optional figure note here.}
\end{figure}
```

- Replace `figures/uestc-logo.png` with the path to your image.
- `0.8\linewidth` means 80% of the current line width. Change this number to resize the image.
- `\label{}` assigns a reference label to the figure. Place it after `\caption{}` and use a unique label for each figure.
- Refer to the figure in your text with `As shown in \autoref{fig:guide-single}, ...`; you do not need to type the figure number yourself.
- `[htbp]` allows placement here (`h`), at the top (`t`) or bottom (`b`) of a page, or on a separate float page (`p`). It does not fix the figure at its position in the source. Sometimes moving the source code helps adjust placement. In general, I recommend `htbp` or `t`.

#### Side-by-Side Subfigures

This example uses the same image twice. Replace each path with the image you want:

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
    \caption[Side-by-side subfigures]{Side-by-side subfigures: (a) first image; (b) second image}
    \label{fig:guide-pair}
\end{figure}
```

- `0.55\linewidth` and `0.4\linewidth` give the left and right subfigures 55% and 40% of the current line width. `\hfill` puts the remaining space between them. Leave room for a gap when choosing the two widths.
- Inside a subfigure, `width=\linewidth` makes the image fill that subfigure's width.
- Keep each subfigure's `\caption{}` empty. The template automatically places `(a)` and `(b)` below the images in 10.5 pt type. Keep the following `\label{}` commands for cross-references.
- Put the descriptions after the main caption, for example `Side-by-side subfigures: (a) first image; (b) second image`. Update them when replacing or reordering the images.
- In the final `\caption[Short caption]{Full caption}`, the square brackets contain the text for the list of figures, and the braces contain the caption displayed below the figure.
- Reference the whole figure with `\autoref{fig:guide-pair}`, or the left subfigure with `\autoref{fig:guide-pair}(\subref{fig:guide-left})`.

### Tables

Here is an example of a three-line table:

```latex
\begin{table}[htbp]
    \centering
    \caption{Example Results for Different Methods}
    \label{tab:guide-results}
    \begin{tabular}{lcp{5cm}}
        \toprule
        Method & Accuracy (\%) & Description \\
        \midrule
        Baseline & 85.2 & Uses basic features only. \\
        Improved & 88.6 & Adds time and location features to compare the effects of different feature combinations. \\
        Proposed & \textbf{91.3} & Combines several types of features. \\
        \bottomrule
    \end{tabular}
    \tabnote{Note: These values are for illustration only (optional).}
\end{table}
```

- `\caption{}` sets the table caption and goes above the table. Put `\label{}` immediately after it, using a unique label for each table.
- `\begin{tabular}{lcp{5cm}}` defines three columns: `l` is left-aligned, `c` is centered, and `p{5cm}` is a 5 cm wide text column that wraps automatically. Use `r` for right alignment.
- `\toprule`, `\midrule`, and `\bottomrule` draw the top rule, the rule below the header, and the bottom rule. Use few horizontal rules, add more only when necessary, and avoid vertical rules.
- Long text wraps automatically in a `p{5cm}` column. Change `5cm` to adjust its width. Use `\newline` to insert a line break at a specific position within that cell. Columns of type `l`, `c`, and `r` do not wrap automatically.
- Refer to the table with `As shown in \autoref{tab:guide-results}, ...`; you do not need to type the table number yourself.
- `[htbp]` has the same meaning as for figures. A table may move to the top or bottom of a page or another suitable position.
- For a table with a specified total width and automatically allocated column widths, consider `tabularx`.
- For more advanced usage, ask an AI assistant.

### Mathematical Symbols and Equations

Inline mathematics: `$x_i=2$`.

A displayed equation:

```latex
\begin{equation}
\label{eq:example}
  x+y=z
\end{equation}
\noindent Here, $x$ and $y$ are the two addends, and $z$ is their sum.
```

`\noindent` makes the explanation start at the left margin.

A multiline equation:

```latex
\begin{equation}
\label{eq:multiline-example}
  \begin{aligned}
    x+y &= z \\
    2x+2y &= 2z
  \end{aligned}
\end{equation}
```

- `&` marks alignment points, and `\\` starts a new line. The example above shares a single equation number across both lines.
- Use `\eqref{eq:example}` to reference an equation; the number is automatically enclosed in parentheses.

#### Common Expressions

- Subscripts and superscripts: `x_i` and `x^2`. Enclose multiple characters in braces, as in `x_{i+1}` and `x^{n+1}`.
- Fractions: `\frac{a}{b}`.
- Square roots: `\sqrt{x}`.
- Greek letters: `\alpha`, `\theta`, and `\pi`.
- Summation: `\sum_{i=1}^{n} x_i`.
- A bar above a symbol: `\bar{x}`, for example for a sample mean.
- Text within mathematics: `\text{mean}`.

### Theorems and Proofs

```latex
\begin{theorem}
    \label{thm:guide-example}
    The sum of two even integers is even.
\end{theorem}

\begin{proof}
    For integers $m$ and $n$, $2m+2n=2(m+n)$ is even.
\end{proof}
```

- The template generates the theorem number and the black square at the end of the proof. Reference the theorem with `\autoref{thm:guide-example}`.
- Replace `theorem` with `definition`, `lemma`, or `corollary` for a definition, lemma, or corollary. These environments share a numbering sequence within each chapter.

### Footnotes

```latex
This is the main text\footnote{This is a footnote.}.
```

### Acknowledgements

Comment out `\input{chapters/acknowledgements}` to omit the acknowledgements.

### References

Store bibliographic entries in `references.bib` and cite them in your chapter files. The template generates citation numbers and the reference list automatically. Only cited entries appear in the reference list.

#### Adding References

Export a `BibTeX` entry from the publication's page or your reference manager, then copy it into `references.bib`. For example:

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

- `lecun2015deep` is the citation key used to cite this entry. Each key must be unique; keep only one entry for the same paper.
- Exported entries can contain errors. Check the authors, title, year, journal or conference name, and page numbers.
- Separate authors with `and`. Chinese authors can be entered as `author = {{张钹} and {朱军} and {苏航}}`.
- Protect capitalized abbreviations in titles with braces, such as `{IEEE}` and `{3D}`; otherwise, they may appear as `ieee` or `3d`.

#### Citing References in the Text

Use these commands in the `.tex` files in `chapters`:

```latex
Deep learning is widely used\cite{lecun2015deep}.
Cite several references together\cite{lecun2015deep,vaswani2017attention}.
Reference~\citep{lecun2015deep} introduces deep learning.
```

The result looks like this, assuming the two references are numbered 1 and 2 in order:

> Deep learning is widely used<sup>[1]</sup>. Cite several references together<sup>[1–2]</sup>. Reference [1] introduces deep learning.

- `\cite{}` produces a superscript citation. `\citep{}` produces a bracketed citation at the surrounding text size, suitable for sentences such as “Reference [1] introduces…”.
- Separate multiple citation keys with commas. The template sorts them and compresses consecutive numbers automatically; do not type `[1]` or `[2-4]` yourself.

#### Troubleshooting

- A citation appears as a question mark: check that its key matches the entry in `references.bib`, save the files, and complete another build. If the question mark remains, check for compilation errors.
- Bibliographic information is incorrect: edit the corresponding entry in `references.bib` and rebuild. Do not edit the generated PDF or `.bbl` file directly.


#### Examples by Reference Type

The examples below work with this template and follow the order of common reference types in Table 2-3 of the [university writing guidelines](https://gr.uestc.edu.cn/xiazai/114/3917). This English guide uses English-language publications; retain bibliographic information in its original language when citing other works.

##### Journal Articles

```bibtex
@article{guide-journal,
  author = {Yann LeCun and Yoshua Bengio and Geoffrey Hinton},
  title = {Deep learning},
  journal = {Nature},
  year = {2015},
  volume = {521},
  number = {7553},
  pages = {436--444}
}
```

> [1] LeCun Y, Bengio Y, Hinton G. Deep learning[J]. Nature, 2015, 521(7553): 436-444.

##### Conference Papers

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

##### Books

```bibtex
@book{guide-book,
  author = {Richard S. Sutton and Andrew G. Barto},
  title = {Reinforcement learning: An introduction},
  edition = {2},
  address = {Cambridge, MA},
  publisher = {MIT Press},
  year = {2018}
}
```

> [3] Sutton R S, Barto A G. Reinforcement learning: An introduction[M]. 2nd ed. Cambridge, MA: MIT Press, 2018.

##### Theses and Dissertations

```bibtex
@phdthesis{guide-thesis,
  author = {Ivan Edward Sutherland},
  title = {Sketchpad: A man-machine graphical communication system},
  address = {Cambridge, MA},
  school = {Massachusetts Institute of Technology},
  year = {1963}
}
```

> [4] Sutherland I E. Sketchpad: A man-machine graphical communication system[D]. Cambridge, MA: Massachusetts Institute of Technology, 1963.

##### Newspaper Articles

```bibtex
@newspaper{guide-newspaper,
  author = {Bruce Weber},
  title = {Swift and slashing, computer topples {Kasparov}},
  journal = {The New York Times},
  date = {1997-05-12},
  number = {A1}
}
```

> [5] Weber B. Swift and slashing, computer topples Kasparov[N]. The New York Times, 1997-05-12 (A1).

##### Reports

```bibtex
@techreport{guide-report,
  author = {Peter Mell and Timothy Grance},
  title = {The {NIST} definition of cloud computing},
  number = {NIST SP 800-145},
  address = {Gaithersburg, MD},
  institution = {National Institute of Standards and Technology},
  year = {2011}
}
```

> [6] Mell P, Grance T. The NIST definition of cloud computing: NIST SP 800-145[R]. Gaithersburg, MD: National Institute of Standards and Technology, 2011.

##### Granted Patents

```bibtex
@patent{guide-patent,
  author = {Lawrence Page},
  title = {Method for node ranking in a linked database},
  number = {US6285999B1},
  date = {2001-09-04}
}
```

> [7] Page L. Method for node ranking in a linked database: US6285999B1[P]. 2001-09-04.

##### Standards

```bibtex
@standard{guide-standard,
  author = {{International Organization for Standardization}},
  title = {Date and time---Representations for information interchange---Part 1: Basic rules},
  number = {ISO 8601-1:2019},
  address = {Geneva},
  publisher = {ISO},
  year = {2019}
}
```

> [8] International Organization for Standardization. Date and time—representations for information interchange—part 1: Basic rules: ISO 8601-1:2019[S]. Geneva: ISO, 2019.

##### Electronic Resources

Web pages:

```bibtex
@online{guide-webpage,
  author = {{CERN}},
  title = {{CERN} celebrates 20 years of a free, open web},
  date = {2013-04-30},
  urldate = {2026-09-11},
  url = {https://home.cern/cern-celebrates-20-years-of-a-free-open-web/}
}
```

> [9] CERN. CERN celebrates 20 years of a free, open web[EB/OL]. (2013-04-30) [2026-09-11]. https://home.cern/cern-celebrates-20-years-of-a-free-open-web/.

- For a web page, `date` is the publication or update date, and `urldate` is the date you accessed it. Use `YYYY-MM-DD` for both, such as `2026-03-12`. Enter the actual dates rather than copying those in the example.

Online books:

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

##### Preprints (arXiv and Similar Repositories)

When a formally published version exists and contains the material you cite, prefer the journal or conference paper. The example below uses the initial arXiv version (v1) of the Adam paper to illustrate a preprint entry:

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

- Set `date` to the release date of the version you cite and `urldate` to your actual access date. The `v1` at the end of the URL identifies version 1; use the version you actually cite.
- GB/T 7714—2015, the edition specified by the university guidelines, does not define a separate preprint type. This template uses `[EB/OL]` as a compatibility convention. The current GB/T 7714—2025 uses `[PP/OL]`; this example does not use that newer format.

### Lists

#### Ordered Lists

The university's examples use numbering such as `1.` and `（1）`, which provides a useful style reference, but do not explicitly assign these forms to particular list levels. The example below follows their indented first line and continuation lines returning to the left text margin. These are suggested template settings, not separately prescribed university list parameters.

```latex
\begin{enumerate}
    \item First item.
    \item Longer items wrap automatically, with continuation lines returning to the left text margin.
\end{enumerate}
```

For full-width parenthesized numbers, use `\begin{enumerate}[label=（\arabic*）,labelsep=0pt]`, without an extra gap after the closing parenthesis. Choose either form as appropriate and keep comparable lists consistent; these forms need not represent different nesting levels. For half-width parentheses in English prose, use `label=(\arabic*)`.

The template configures first-level lists to follow the body text: font, size, line spacing and justification are inherited, labels start at the first-line indentation, continuation lines return to the left text margin, and no extra paragraph spacing is added. Start each item with `\item`; numbering is automatic.

#### Unordered Lists

No uniform bullet-symbol requirement has been identified in the university guidelines. The following bullet style is an optional choice for parallel points with no inherent order, not a university-prescribed style. Prefer an ordered list when numbering or referring to individual items is useful.

```latex
\begin{itemize}
    \item First item.
    \item Second item.
\end{itemize}
```

These defaults apply to first-level lists; nested lists have not been standardized. Numbering options affect only the current list.

### Appendices

Comment out `\input{chapters/appendix}` to omit the appendices.

### Research Results During the Degree Program

Comment out `\input{chapters/achievements}` to omit the research results section.
