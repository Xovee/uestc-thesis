# UESTC Thesis

A LaTeX template for master's theses and doctoral dissertations at the University of Electronic Science and Technology of China, supporting Chinese and English.

[中文](README.md) · **English**

[Download](#download) · [Preview](docs/previews/english.pdf) · [User guide](GUIDE-english.md)

![Template preview: cover, main text and references](docs/previews/english.png)

## Why use it

- **Easy**: simple to use and quick to get started.
- **Accurate**: follows UESTC requirements and closely matches the official template.
- **Fast**: efficient compilation, validated on multiple real theses and dissertations.
- **Maintained**: ongoing updates informed by school requirements and user feedback.

## Download

The first release is being prepared. Once published, choose your thesis language on the [download page](https://github.com/Xovee/uestc-thesis/releases):

| English thesis | 中文论文 |
| --- | --- |
| `uestc-thesis-xovee-english.zip` | `uestc-thesis-xovee-chinese.zip` |
| [Sample PDF](docs/previews/english.pdf) · [English guide](GUIDE-english.md) | [示例 PDF](docs/previews/chinese.pdf) · [中文指南](GUIDE.md) |

Each package has one `main.tex` entry file with the language and example chapters configured. Both include Chinese and English abstracts.

## Quick start

Install **TeX Live 2026, VS Code and the LaTeX Workshop extension**; see the [user guide](GUIDE-english.md) for setup instructions.

1. **Open the template**: extract the package and open the entire folder in VS Code.
2. **Make it yours**: select `master` or `doctor` in `main.tex` and edit your thesis in `chapters/`. Put images in `figures/` and references in `references.bib`. Complete the school's Word cover template, export it to PDF and replace `cover.pdf`.
3. **Build the PDF**: open `main.tex`, press `F1`, and run `LaTeX Workshop: Build LaTeX project`, then `LaTeX Workshop: View LaTeX PDF file`. Subsequent edits build automatically when saved. The output is `output/main.pdf`.

Verified on Windows with TeX Live 2026, macOS with MacTeX 2026, and Overleaf with XeLaTeX and TeX Live 2026. Long theses may exceed the compile timeout on the free Overleaf plan.

This is an unofficial template. Check your final thesis against the [current UESTC requirements](https://gr.uestc.edu.cn/xiazai/114/3917).

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
