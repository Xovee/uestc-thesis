<h1 align="center">UESTC Thesis</h1>

<p align="center">电子科技大学研究生学位论文 LaTeX 模板</p>

<p align="center">
  <a href="#下载模板"><img src="https://img.shields.io/badge/%E4%B8%8B%E8%BD%BD%E6%A8%A1%E6%9D%BF-2563EB?style=for-the-badge&amp;logo=github&amp;logoColor=white" alt="下载模板" height="34"></a>
  <a href="https://github.com/Xovee/uestc-thesis/blob/main/GUIDE.md"><img src="https://img.shields.io/badge/%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97-455A64?style=for-the-badge&amp;logo=readthedocs&amp;logoColor=white" alt="使用指南" height="34"></a>
  <a href="https://github.com/Xovee/uestc-thesis/blob/main/docs/previews/chinese.pdf"><img src="https://img.shields.io/badge/%E9%A2%84%E8%A7%88%20PDF-455A64?style=for-the-badge" alt="预览 PDF" height="34"></a>
  <a href="#overleaf-在线写作"><img src="https://img.shields.io/badge/Overleaf-47A141?style=for-the-badge&amp;logo=overleaf&amp;logoColor=white" alt="Overleaf" height="34"></a>
</p>

<p align="center"><strong>中文</strong> · <a href="https://github.com/Xovee/uestc-thesis/blob/main/README-english.md">English</a></p>

![模板预览：封面、正文与参考文献](docs/previews/chinese.png)

- **易**：使用简单，入门快捷。
- **准**：遵循学校规范，贴合官方模板。
- **快**：编译高效，在多篇真实学位论文上经过验证。
- **新**：持续维护，跟进规范与用户反馈。

## 下载模板

**1.0.0 正在完善，尚未正式发布。** 发布后在[下载页面](https://github.com/Xovee/uestc-thesis/releases)选择对应语言的 ZIP。

| 中文论文 | English thesis |
| :---: | :---: |
| `uestc-thesis-xovee-chinese.zip` | `uestc-thesis-xovee-english.zip` |
| [查看示例 PDF](docs/previews/chinese.pdf) · [阅读指南](GUIDE.md) | [Sample PDF](docs/previews/english.pdf) · [User guide](GUIDE-english.md) |

每个包只有一个 `main.tex` 入口，正文示例和语言已配好，同时保留中英文摘要。

## 本地写作

安装 **TeX Live 2026（macOS 使用 MacTeX 2026）、VS Code 和 LaTeX Workshop 扩展**，具体方法见[使用指南](GUIDE.md)。

1. **打开模板**：解压下载包，用 VS Code 打开整个模板文件夹。
2. **填写与写作**：在 `main.tex` 中选择硕士或博士，在 `chapters/` 中修改论文内容；图片放入 `figures/`，文献写入 `references.bib`。封面按学校 Word 模板填写并导出，替换 `cover.pdf`。
3. **生成 PDF**：打开 `main.tex`，按 `F1` 执行 `LaTeX Workshop: Build LaTeX project`，再执行 `LaTeX Workshop: View LaTeX PDF file`。之后保存修改即可自动编译，输出为 `output/main.pdf`。

已验证：**Windows · macOS · Overleaf**，均使用 TeX Live / MacTeX 2026 和 XeLaTeX。

> 提交前请按[学校最新要求](https://gr.uestc.edu.cn/xiazai/114/3917)检查论文。

## Overleaf 在线写作

无需安装软件，在 [Overleaf](https://www.overleaf.com/) 中编辑和编译论文：

1. 选择 **New Project → Upload Project**，上传中文或英文模板 ZIP，无需解压。
2. 在项目设置中选择 **XeLaTeX**、**TeX Live 2026**，主文件为 `main.tex`。
3. 点击 **Recompile**，确认示例生成后开始修改论文。

完整操作见[使用指南](GUIDE.md)。中英文一键导入入口将在公开的发布附件可用后启用。长篇论文可能超过免费计划的编译时限。

## 反馈与贡献

遇到问题或有改进建议，欢迎提交 [Issue](https://github.com/Xovee/uestc-thesis/issues) 或 Pull Request。报告编译问题时，最好附上系统、TeX Live 版本、错误信息和可复现的小例子。当然，有问题的时候可以先问一下大模型。

## 许可

Copyright © 2025–2026 [Xovee Xu](https://www.xoveexu.com/)。

模板代码采用 [LPPL 1.3c](LICENSE)，第三方材料的权利说明见 [NOTICE.md](NOTICE.md)。

## 致谢

感谢[台文鑫](https://wxtai.github.io/)和 [Abdisalam](https://scholar.google.com/citations?user=1eUyqGQAAAAJ&hl=en&oi=ao) 提供博士学位论文用于本模板的测试。

## 联系方式

[Xovee Xu](https://www.xoveexu.com/)

- `xovee.xu at gmail.com`
- `xovee at uestc.edu.cn`
