# UESTC Thesis

电子科技大学研究生学位论文 LaTeX 模板，支持硕士、博士及中英文论文。

**中文** · [English](README-english.md)

[下载模板](#下载模板) · [查看效果](docs/previews/chinese.pdf) · [使用指南](GUIDE.md)

![模板预览：封面、正文与参考文献](docs/previews/chinese.png)

## 优势

- **易**：使用简单，入门快捷。
- **准**：遵循学校规范，贴合官方模板。
- **快**：编译高效，经过真实长篇论文验证。
- **新**：持续维护，跟进规范与用户反馈。


## 下载模板

首个 Release 正在准备中，发布后可在[下载页面](https://github.com/Xovee/uestc-thesis/releases)按论文语言选择：

| 中文论文 | English thesis |
| --- | --- |
| `uestc-thesis-xovee-chinese.zip` | `uestc-thesis-xovee-english.zip` |
| [示例 PDF](docs/previews/chinese.pdf) · [中文指南](GUIDE.md) | [Sample PDF](docs/previews/english.pdf) · [English guide](GUIDE-english.md) |

每个包只有一个 `main.tex` 入口，正文示例和语言已配好，同时保留中英文摘要。

## 快速开始

准备 **TeX Live 2026、VS Code 和 LaTeX Workshop 扩展**；安装方法见[使用指南](GUIDE.md)。

1. **打开模板**：解压下载包，用 VS Code 打开整个模板文件夹。
2. **填写与写作**：在 `main.tex` 中选择硕士或博士，在 `chapters/` 中修改论文内容；图片放入 `figures/`，文献写入 `references.bib`。封面按学校 Word 模板填写并导出，替换 `cover.pdf`。
3. **生成 PDF**：打开 `main.tex`，按 `F1` 执行 `LaTeX Workshop: Build LaTeX project`，再执行 `LaTeX Workshop: View LaTeX PDF file`。之后保存修改即可自动编译，输出为 `output/main.pdf`。

已验证 Windows + TeX Live 2026、macOS + MacTeX 2026，以及 Overleaf（XeLaTeX + TeX Live 2026）。免费版本的Overleaf可能不支持编译内容很多的学位论文（编译时间有限制）。

本项目为非官方模板；提交前请按[学校最新要求](https://gr.uestc.edu.cn/xiazai/114/3917)检查论文。

## 反馈与贡献

遇到问题或有改进建议，欢迎提交 [Issue](https://github.com/Xovee/uestc-thesis/issues) 或 Pull Request。报告编译问题时，最好附上系统、TeX Live 版本、错误信息和可复现的小例子。当然，有问题的时候可以先问一下大模型。

## 许可

Copyright © 2025–2026 [Xovee Xu](https://www.xoveexu.com/)。

模板代码采用 [LPPL 1.3c](LICENSE)，第三方材料的权利说明见 [NOTICE.md](NOTICE.md)。

## 致谢

感谢[台文鑫](https://wxtai.github.io/)和 [Abdisalam](https://scholar.google.com/citations?user=1eUyqGQAAAAJ&hl=en&oi=ao) 提供博士学位论文用于本模板的测试。

## Contact

[Xovee Xu](https://www.xoveexu.com/)

- `xovee.xu at gmail.com`
- `xovee at uestc.edu.cn`
