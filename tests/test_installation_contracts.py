import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLATION = ROOT / "02_setup" / "2.2_installation.md"


class InstallationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = INSTALLATION.read_text(encoding="utf-8")

    def test_posix_diagnostics_cover_runtime_prefix_path_and_doctor(self):
        required = (
            "node --version",
            "npm prefix -g",
            "command -v openclaw",
            'printf \'%s\\n\' "$PATH"',
            'export PATH="$(npm prefix -g)/bin:$PATH"',
            "openclaw doctor",
            "openclaw gateway status",
            "关闭并重新打开终端",
            "https://docs.openclaw.ai/install/node",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

        self.assertIn("Node 22.19+、23.11+ 或 24+", self.text)
        self.assertIn("`<npm-prefix>/bin`", self.text)

    def test_powershell_diagnostics_use_the_windows_global_prefix(self):
        required = (
            "Get-Command openclaw -ErrorAction SilentlyContinue",
            "$env:Path -split ';'",
            "$npmPrefix = npm prefix -g",
            "$env:Path -split ';' -contains $npmPrefix",
            "openclaw gateway status --json",
            "Windows 直接把 `<npm-prefix>` 加入 PATH",
            "重新打开 Windows Terminal 或 PowerShell",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_windows_hub_and_wsl_commands_are_routed_to_the_chosen_environment(self):
        required = (
            "Windows Hub",
            "OpenClawGateway",
            "不会修改你已有的 Ubuntu 发行版",
            "wsl --list --verbose",
            "wsl -d <DistroName> -- openclaw doctor",
            "wsl -d <DistroName> -- openclaw gateway status",
            "https://docs.openclaw.ai/platforms/windows",
            "https://learn.microsoft.com/windows/wsl/networking",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)


if __name__ == "__main__":
    unittest.main()
