# 维护说明

用户安装和写作见[中文指南](../GUIDE.md)及[英文指南](../GUIDE-english.md)。本文只记录模板维护、验证和打包方法；学校要求与实现依据见[规范追溯](standards-traceability.md)。

## 源码与资源

仓库维护中文、英文两个入口及对应章节，共用类文件、BibTeX样式、字体和外部PDF。用户包按语言分别生成，各自只有一个`main.tex`和一份`GUIDE.md`，均保留双语摘要。

编译链为XeLaTeX、BibTeX和latexmk。`uestcthesis.bst`基于gbt7714适配，不同时维护Biber后端。切换后端时只清理编译辅助文件；不要删除正文或文献库。特殊姓名使用BibTeX支持的TeX写法，专名用花括号保护大小写。文献一般不跨页，但超过整页高度的单条文献仍需作者处理。

六个字体文件全部存在时，模板从`fonts/`加载宋体、黑体及Times New Roman四种字形；缺少任一文件时整体回退到系统同名字体。系统字体也缺失时由fontspec报错，不静默替换字体。

模板代码许可见[LICENSE](../LICENSE)，第三方资源边界见[NOTICE](../NOTICE.md)、[字体说明](../fonts/README.md)和[图片说明](../figures/README.md)。授权沟通材料由维护者在仓库外保存。`THIRD_PARTY.md`暂不公开，也不收入首次发布包。

新增分发文件须更新打包工具中的明确名单；更换字体、默认PDF或校标时，还须重新核验许可、文件身份和版面结果，再更新锁定的哈希。真实论文、签名、个人配置和编译缓存不进入仓库或用户包。

## 环境与排版约定

开发与验收采用TeX Live 2026，不持续维护旧版本兼容性。已在Windows + TeX Live 2026、macOS + MacTeX 2026及Overleaf（XeLaTeX + TeX Live 2026）完成示例与真实博士论文编译测试。独立Linux本地环境及GitHub Actions尚未验证；仓库目前没有自动构建工作流。

学校规范优先于实现约定。跨版本的断行或分页差异需结合具体版面判断，不以页数完全一致作为验收标准。中西文自动间距采用`CJKecglue={\hskip .25em plus .1em minus .1em}`、`xCJKecglue=false`和`CJKspace=false`；这些是模板实现选择，不是学校规定的数值。改变字体、字号、行距或其他排版行为时，检查修改前后的实际PDF。

## 测试

从仓库根目录运行，需要Python 3.10或更新版本、TeX Live 2026以及可用的Poppler命令：

```text
python -m pip install -r tests/requirements.txt
python -m unittest discover -s tests -p "test_*.py"
python tests/run_regression.py --quick
```

排版或构建变更发布前运行完整回归：

```text
python tests/run_regression.py
```

测试入口支持`--tex-bin`指定发行版目录、`--build-dir`指定输出目录，不修改系统设置。默认在`build/regression/`保存PDF及`environment.json`等环境记录。各测试的用途和单独执行方法见[测试说明](../tests/README.md)。带问题编号的测试仍用于防止已修复问题再次出现，不是可随意删除的试验文件。

2026年9月13日的Windows验证通过52项打包与配置测试，完整回归编译36份文档；中英文示例分别为18页和19页。这是一次验证记录，后续内容变化不要求维持相同页数。自动检查不能替代示例PDF的逐页视觉检查。

## 打包与发布

用户源码包各含30个源码和说明文件；正式打包工具另加入同次构建的示例PDF，共31个文件。`tests/`、`tools/`、维护文档和协作配置保留在开发仓库，不收入用户包。README预览位于`docs/previews/`，应随示例更新。

仅检查源码包时运行：

```text
python tools/package_release.py --source-only --language chinese
python tools/package_release.py --source-only --language english
```

输出到`dist/`，文件名以`-source-preview.zip`结尾，旁置检查记录；不含示例PDF，也不能凭该记录确认正式发布。正式发布使用经过确认的候选包，并旁置中英文示例PDF。

正式候选要求中文指南已完成内容审阅和首次使用验证，且`GUIDE.md`中唯一状态标记为`<!-- guide-status: ready -->`。1.0.0的中英文指南已完成审阅并设置此标记。后续内容改动仍须复核，不得只为绕过检查而设置状态。英文指南须同步审阅。

```text
python tools/package_release.py --language chinese
python tools/package_release.py --language english
```

工具在干净目录中从当前源码编译，生成每种语言的`-candidate.zip`、`-candidate.example.pdf`及`-candidate.review.json`。不使用外部旧示例PDF。检查内容、图片、全部PDF页面，以及README、NOTICE和发布说明的非官方表述后，仅将审阅记录中`review`下的`content_and_images`、`all_pdf_pages`、`non_official_wording`三项设为`true`，保留其他数据。

```text
python tools/package_release.py --reviewed dist/uestc-thesis-xovee-chinese-candidate.review.json
python tools/package_release.py --reviewed dist/uestc-thesis-xovee-english-candidate.review.json
```

确认后生成正式ZIP及旁置的`.manifest.json`。源码、候选、预览或检查数据变化后，旧审阅失效，须重新准备和复核。打包工具检查文件名单、哈希、可识别的隐私线索及PDF结构和交互对象；人名、签名图像和未公开研究内容仍须人工判断。审阅记录和本地历史档案不收入用户包。

发布说明应列出版本变化及验证环境；源码、指南和示例PDF必须对应同一版本。这里只描述准备流程，执行打包不等于已经创建GitHub Release。
