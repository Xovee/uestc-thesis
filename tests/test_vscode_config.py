"""Static checks for the user-facing VS Code setup; no editor or TeX run required."""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class VSCodeConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.settings = json.loads((ROOT / ".vscode/settings.json").read_text(encoding="utf-8"))

    def test_default_recipe_uses_latexmk_with_xelatex(self) -> None:
        recipes = self.settings["latex-workshop.latex.recipes"]
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0]["name"], "latexmk (xelatex)")
        self.assertEqual(
            self.settings["latex-workshop.latex.recipe.default"], recipes[0]["name"]
        )
        tools = self.settings["latex-workshop.latex.tools"]
        self.assertEqual(len(tools), 1)
        self.assertEqual(recipes[0]["tools"], [tools[0]["name"]])
        self.assertEqual(tools[0]["command"], "latexmk")
        self.assertIn("-xelatex", tools[0]["args"])
        self.assertNotIn("-pdf", tools[0]["args"])
        self.assertIn("%DOC%", tools[0]["args"])
        self.assertEqual(tools[0]["cwd"], "%DIR%")
        # Existing TeX-program comments must not bypass latexmk with a single XeLaTeX pass.
        self.assertFalse(self.settings["latex-workshop.latex.build.enableMagicComments"])

    def test_pdf_location_matches_latexmkrc(self) -> None:
        rc = (ROOT / "latexmkrc").read_text(encoding="utf-8")
        output = re.search(r"\$out_dir\s*=\s*'([^']+)'", rc)
        self.assertIsNotNone(output)
        assert output is not None
        self.assertEqual(
            self.settings["latex-workshop.latex.outDir"], "%DIR%/" + output.group(1)
        )
        args = self.settings["latex-workshop.latex.tools"][0]["args"]
        self.assertIn("-outdir=%OUTDIR%", args)
        self.assertIn("-synctex=1", rc)

    def test_build_on_save_and_right_side_pdf_viewer(self) -> None:
        self.assertEqual(self.settings["latex-workshop.latex.autoBuild.run"], "onSave")
        self.assertEqual(self.settings["latex-workshop.view.pdf.viewer"], "tab")
        self.assertEqual(self.settings["latex-workshop.view.pdf.tab.editorGroup"], "right")

    def test_only_latex_workshop_extension_is_recommended(self) -> None:
        extensions = json.loads(
            (ROOT / ".vscode/extensions.json").read_text(encoding="utf-8")
        )
        self.assertEqual(extensions, {"recommendations": ["james-yu.latex-workshop"]})

    def test_settings_have_no_machine_specific_paths(self) -> None:
        serialized = json.dumps(self.settings)
        self.assertNotRegex(serialized, r"[A-Za-z]:[\\/]|/Users/|/home/|/texlive/")


if __name__ == "__main__":
    unittest.main()
