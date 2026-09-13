<h1 align="center">UESTC Thesis</h1>

<p align="center">LaTeX thesis template for the University of Electronic Science and Technology of China</p>
<p align="center">Master’s theses · Doctoral dissertations &nbsp; / &nbsp; Chinese · English</p>

<p align="center"><code>1.0.0</code> &nbsp; <code>TeX Live 2026</code> &nbsp; <code>XeLaTeX</code></p>

[中文](README.md) · **English**

[Download](#download) · [Write on Overleaf](#write-on-overleaf) · [Preview PDF](docs/previews/english.pdf) · [User guide](GUIDE-english.md)

| Easy | Accurate | Fast | Maintained |
| :---: | :---: | :---: | :---: |
| Simple to use and quick to get started. | Follows UESTC requirements and closely matches the official template. | Efficient compilation, validated on multiple real theses and dissertations. | Ongoing updates informed by school requirements and user feedback. |

![Template preview: cover, main text and references](docs/previews/english.png)

## Download

**1.0.0 is being refined and has not been released yet.** Once published, choose the ZIP for your thesis language on the [download page](https://github.com/Xovee/uestc-thesis/releases).

| English thesis | 中文论文 |
| :---: | :---: |
| `uestc-thesis-xovee-english.zip` | `uestc-thesis-xovee-chinese.zip` |
| [Sample PDF](docs/previews/english.pdf) · [User guide](GUIDE-english.md) | [查看示例 PDF](docs/previews/chinese.pdf) · [阅读指南](GUIDE.md) |

Each package has one `main.tex` entry file with the language and example chapters configured. Both include Chinese and English abstracts.

## Write on Overleaf

Edit and compile in [Overleaf](https://www.overleaf.com/) without installing software:

1. Choose **New Project → Upload Project** and upload the Chinese or English template ZIP. No extraction is needed.
2. In project settings, select **XeLaTeX**, **TeX Live 2026**, and `main.tex` as the main document.
3. Click **Recompile** and check the example before editing your thesis.

See the [user guide](GUIDE-english.md) for full instructions. One-click import links for both languages will be enabled when public release attachments are available. Long theses may exceed the compile timeout on the free plan.

## Write locally

Install **TeX Live 2026 (MacTeX 2026 on macOS), VS Code and the LaTeX Workshop extension**; see the [user guide](GUIDE-english.md) for setup instructions.

1. **Open the template**: extract the package and open the entire folder in VS Code.
2. **Make it yours**: select `master` or `doctor` in `main.tex` and edit your thesis in `chapters/`. Put images in `figures/` and references in `references.bib`. Complete the school's Word cover template, export it to PDF and replace `cover.pdf`.
3. **Build the PDF**: open `main.tex`, press `F1`, and run `LaTeX Workshop: Build LaTeX project`, then `LaTeX Workshop: View LaTeX PDF file`. Subsequent edits build automatically when saved. The output is `output/main.pdf`.

Verified on **Windows · macOS · Overleaf**, using TeX Live / MacTeX 2026 and XeLaTeX.

> This is an unofficial template. Check your final thesis against the [current UESTC requirements](https://gr.uestc.edu.cn/xiazai/114/3917).

## Feedback and contributions

Questions and improvements are welcome through [Issues](https://github.com/Xovee/uestc-thesis/issues) and pull requests. For build problems, please include your operating system, TeX Live version, error messages and a small reproducible example where possible. You can also ask an AI assistant for initial troubleshooting help.

## License

Copyright © 2025–2026 [Xovee Xu](https://www.xoveexu.com/).

Template code is licensed under [LPPL 1.3c](LICENSE); see [NOTICE.md](NOTICE.md) for third-party rights.

## Acknowledgements

Thanks to [Wenxin Tai](https://wxtai.github.io/) and [Abdisalam](https://scholar.google.com/citations?user=1eUyqGQAAAAJ&hl=en&oi=ao) for providing their doctoral dissertations for testing this template.

## Contact

[Xovee Xu](https://www.xoveexu.com/)

- `xovee.xu at gmail.com`
- `xovee at uestc.edu.cn`
