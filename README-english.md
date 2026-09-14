<h1 align="center">UESTC Thesis</h1>

<p align="center">LaTeX thesis template for the University of Electronic Science and Technology of China</p>

<p align="center">
  <a href="#download"><img src="https://img.shields.io/badge/Download-2563EB?style=for-the-badge&amp;logo=github&amp;logoColor=white" alt="Download" height="34"></a>
  <a href="https://github.com/Xovee/uestc-thesis/blob/main/GUIDE-english.md"><img src="https://img.shields.io/badge/Guide-455A64?style=for-the-badge&amp;logo=readthedocs&amp;logoColor=white" alt="User guide" height="34"></a>
  <a href="https://github.com/Xovee/uestc-thesis/blob/main/docs/previews/english.pdf"><img src="https://img.shields.io/badge/PDF-455A64?style=for-the-badge" alt="Preview PDF" height="34"></a>
  <a href="#write-on-overleaf"><img src="https://img.shields.io/badge/Overleaf-47A141?style=for-the-badge&amp;logo=overleaf&amp;logoColor=white" alt="Overleaf" height="34"></a>
</p>

<p align="center"><a href="https://github.com/Xovee/uestc-thesis/blob/main/README.md">中文</a> · <strong>English</strong></p>

[![Template preview: cover, main text and references](docs/previews/english.png)](docs/previews/english.pdf)

Faithfully reproduces the university’s Word template: easy to use, quick to compile, and continuously updated.

## Download

**Current version: 1.0.2.** Download the template for your thesis language, or read the [release notes](https://github.com/Xovee/uestc-thesis/releases/tag/v1.0.2).

| English Thesis | 中文学位论文 |
| :---: | :---: |
| [Download English ZIP](https://github.com/Xovee/uestc-thesis/releases/download/v1.0.2/uestc-thesis-xovee-english.zip) | [中文模板 ZIP](https://github.com/Xovee/uestc-thesis/releases/download/v1.0.2/uestc-thesis-xovee-chinese.zip) |
| [Open in Overleaf](https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fgithub.com%2FXovee%2Fuestc-thesis%2Freleases%2Fdownload%2Fv1.0.2%2Fuestc-thesis-xovee-english.zip) | [Open in Overleaf](https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fgithub.com%2FXovee%2Fuestc-thesis%2Freleases%2Fdownload%2Fv1.0.2%2Fuestc-thesis-xovee-chinese.zip) |
| [Sample PDF](docs/previews/english.pdf) · [User guide](GUIDE-english.md) | [查看示例 PDF](docs/previews/chinese.pdf) · [阅读指南](GUIDE.md) |

Each package has one `main.tex` entry file with the language and example chapters configured. Both include Chinese and English abstracts.

## Write locally

1. **Install the tools**: TeX Live 2026 (MacTeX 2026 on macOS), VS Code and the LaTeX Workshop extension.
2. **Open the template**: extract your language package and open the entire folder containing `main.tex` in VS Code.
3. **Build and preview**: compile `main.tex` with LaTeX Workshop to generate `output/main.pdf`. Check that the example builds before editing; subsequent edits build automatically when saved.

See the [user guide](GUIDE-english.md) for installation, first-build instructions and cover setup.

Verified on **Windows · macOS · Overleaf**, using TeX Live / MacTeX 2026 and XeLaTeX.

> Check your final thesis against the [current UESTC requirements](https://gr.uestc.edu.cn/xiazai/114/3917).

## Write on Overleaf

Edit and compile in [Overleaf](https://www.overleaf.com/) without installing software:

1. Use **Open in Overleaf** in the download table above, or choose **New Project → Upload Project** and upload the ZIP without extracting it.
2. In project settings, select **XeLaTeX**, **TeX Live 2026**, and `main.tex` as the main document.
3. Click **Recompile** and check the example before editing your thesis.

See the [user guide](GUIDE-english.md) for full instructions. Long theses may exceed the compile timeout on the free plan.

## Make it your thesis

| What to change | Where to edit |
| :--- | :--- |
| Degree | In `main.tex`, keep `master` for a master’s thesis or change it to `doctor` for a doctoral dissertation. |
| Abstracts and chapters | Edit the `.tex` files in `chapters/`; manage chapter order in `main.tex`. |
| Figures and references | Place images in `figures/` and add bibliography entries to `references.bib`. |
| Cover and title pages | Fill in the university’s Word template, export the cover and Chinese/English title pages together as `cover.pdf`, and replace the sample file. |

For formatting examples and detailed steps, see the [user guide](GUIDE-english.md). You normally do not need to edit `uestcthesis.cls`.

## Feedback and contributions

Questions and improvements are welcome through [Issues](https://github.com/Xovee/uestc-thesis/issues) and pull requests. For build problems, please include your operating system, TeX Live version, error messages and a small reproducible example where possible. You can also ask an AI assistant for initial troubleshooting help.

Contact [Xovee Xu](https://www.xoveexu.com/): `xovee.xu at gmail.com` or `xovee at uestc.edu.cn`.

## Acknowledgements and license

Thanks to [Wenxin Tai](https://wxtai.github.io/) and [Abdisalam](https://scholar.google.com/citations?user=1eUyqGQAAAAJ&hl=en&oi=ao) for providing their doctoral dissertations for testing this template.

Template code is licensed under [LPPL 1.3c](LICENSE); see [NOTICE.md](NOTICE.md) for third-party rights.

Copyright © 2025–2026 [Xovee Xu](https://www.xoveexu.com/).
