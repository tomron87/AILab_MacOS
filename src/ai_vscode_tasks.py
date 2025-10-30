#!/usr/bin/env python3
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30

AI Environment - VS Code Tasks Manager
Handles tasks.json and extensions.json configuration
"""

import json
from pathlib import Path

class VSCodeTasksManager:
    """Manages VS Code tasks.json and extensions.json creation"""
    
    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)

    def _normalize_path(self, path):
        """Convert Windows path to forward slashes for configuration files"""
        return str(path).replace('\\', '/')

    def _build_path_string(self):
        """Build PATH environment variable string"""
        ai2025_path = self._normalize_path(self.ai_env_path / 'Miniconda' / 'envs' / 'AI2025')
        ai2025_scripts = self._normalize_path(self.ai_env_path / 'Miniconda' / 'envs' / 'AI2025' / 'Scripts')
        src_path = self._normalize_path(self.ai_env_path / 'src')
        return f"{ai2025_path}:{ai2025_scripts}:{src_path}:${{env:PATH}}"

    def create_tasks_json(self, vscode_dir):
        """Create enhanced tasks.json configuration"""
        # Pre-process paths for tasks
        python_path = self._normalize_path(self.ai_env_path / "Miniconda" / "envs" / "AI2025" / "python")
        main_system_program = self._normalize_path(self.ai_env_path / "activate_ai_env.py")
        main_system_cwd = self._normalize_path(self.ai_env_path)
        conda_prefix_norm = self._normalize_path(self.ai_env_path / "Miniconda" / "envs" / "AI2025")
        pythonpath_norm = self._normalize_path(self.ai_env_path / "src")
        path_string = self._build_path_string()
        
        tasks_config = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "AI Environment: Run Current File",
                    "type": "shell",
                    "command": python_path,
                    "args": ["${file}"],
                    "group": {
                        "kind": "build",
                        "isDefault": True
                    },
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "options": {
                        "cwd": "${workspaceFolder}",
                        "env": {
                            "CONDA_DEFAULT_ENV": "AI2025",
                            "CONDA_PREFIX": conda_prefix_norm,
                            "PATH": path_string,
                            "PYTHONPATH": pythonpath_norm
                        }
                    },
                    "problemMatcher": []
                },
                {
                    "label": "AI Environment: Open Main Menu",
                    "type": "shell",
                    "command": python_path,
                    "args": [main_system_program],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": True,
                        "panel": "new"
                    },
                    "options": {
                        "cwd": main_system_cwd,
                        "env": {
                            "CONDA_DEFAULT_ENV": "AI2025",
                            "CONDA_PREFIX": conda_prefix_norm
                        }
                    },
                    "problemMatcher": []
                },
                {
                    "label": "AI Environment: Test All Components",
                    "type": "shell",
                    "command": python_path,
                    "args": [main_system_program, "test"],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": True,
                        "panel": "new"
                    },
                    "options": {
                        "cwd": main_system_cwd
                    },
                    "problemMatcher": []
                }
            ]
        }
        
        tasks_file = vscode_dir / "tasks.json"
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(tasks_config, f, indent=2)

    def create_extensions_json(self, vscode_dir):
        """Create extensions.json configuration"""
        extensions_config = {
            "recommendations": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.flake8",
                "ms-python.autopep8",
                "ms-toolsai.jupyter",
                "ms-toolsai.jupyter-keymap",
                "ms-toolsai.jupyter-renderers",
                "ms-vscode.vscode-json",
                "streetsidesoftware.code-spell-checker",
                "visualstudioexptteam.vscodeintellicode",
                "ms-vscode.powershell"
            ],
            "unwantedRecommendations": [
                "ms-python.pylint"
            ]
        }
        
        extensions_file = vscode_dir / "extensions.json"
        with open(extensions_file, 'w', encoding='utf-8') as f:
            json.dump(extensions_config, f, indent=2)
			