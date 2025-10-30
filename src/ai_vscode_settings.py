#!/usr/bin/env python3
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30

AI Environment - VS Code Settings Manager
Handles settings.json and launch.json configuration
"""

import json
from pathlib import Path

class VSCodeSettingsManager:
    """Manages VS Code settings.json and launch.json creation"""
    
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

    def _build_terminal_args(self):
        """Build terminal activation arguments"""
        activate_bat = self._normalize_path(self.ai_env_path / "Miniconda" / "bin" / "activate")
        ai2025_env = self._normalize_path(self.ai_env_path / "Miniconda" / "envs" / "AI2025")
        
        return [
            "/k",
            activate_bat,
            ai2025_env,
            "&&",
            "echo [AI2025-Terminal] Environment Active - Type 'python activate_ai_env.py' to access main menu"
        ]

    def create_settings_json(self, vscode_dir):
        """Create enhanced settings.json configuration"""
        # Pre-process paths
        python_path = self._normalize_path(self.ai_env_path / "Miniconda" / "envs" / "AI2025" / "python")
        conda_path = self._normalize_path(self.ai_env_path / "Miniconda" / "bin" / "conda")
        venv_path = self._normalize_path(self.ai_env_path / "Miniconda" / "envs")
        flake8_path = self._normalize_path(self.ai_env_path / "Miniconda" / "envs" / "AI2025" / "Scripts" / "flake8")
        autopep8_path = self._normalize_path(self.ai_env_path / "Miniconda" / "envs" / "AI2025" / "Scripts" / "autopep8")
        
        # Terminal arguments
        terminal_args = self._build_terminal_args()
        
        settings = {
            # Python Configuration - Aligned with AI Environment v3.0.26
            "python.defaultInterpreterPath": python_path,
            "python.condaPath": conda_path,
            "python.venvPath": venv_path,
            "python.terminal.activateEnvironment": True,
            "python.terminal.activateEnvInCurrentTerminal": True,
            
            # Terminal Configuration - Integrated with AI Environment System
            "terminal.integrated.defaultProfile.osx": "AI2025-Terminal",
            "terminal.integrated.profiles.osx": {
                "AI2025-Terminal": {
                    "path": "bash",
                    "args": terminal_args,
                    "icon": "snake",
                    "color": "terminal.ansiGreen"
                },
                "PowerShell": {
                    "source": "PowerShell",
                    "icon": "terminal-powershell"
                },
                "Command Prompt": {
                    "path": [
                        "${env:windir}\\Sysnative\\bash",
                        "${env:windir}\\System32\\bash"
                    ],
                    "args": [],
                    "icon": "terminal-cmd"
                }
            },
            
            # Python Linting and Formatting
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": False,
            "python.linting.flake8Enabled": True,
            "python.linting.flake8Path": flake8_path,
            "python.formatting.provider": "autopep8",
            "python.formatting.autopep8Path": autopep8_path,
            
            # File Associations
            "files.associations": {"*.py": "python"},
            
            # Auto-save and formatting
            "files.autoSave": "onFocusChange",
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {"source.organizeImports": True},
            
            # IntelliSense Configuration
            "python.analysis.typeCheckingMode": "basic",
            "python.analysis.autoImportCompletions": True,
            "python.analysis.completeFunctionParens": True,
            
            # Workspace specific settings
            "python.envFile": "${workspaceFolder}/.env",
            
            # Extension settings
            "extensions.autoUpdate": False,
            "extensions.autoCheckUpdates": False,
            
            # Disable telemetry for privacy
            "telemetry.telemetryLevel": "off",
            
            # Editor settings
            "editor.minimap.enabled": True,
            "editor.lineNumbers": "on",
            "editor.rulers": [80, 120],
            "editor.tabSize": 4,
            "editor.insertSpaces": True,
            
            # Git settings
            "git.enabled": True,
            "git.path": "git",
            
            # Jupyter settings
            "jupyter.askForKernelRestart": False,
            "jupyter.interactiveWindowMode": "single",
            
            # Search settings
            "search.exclude": {
                "**/node_modules": True,
                "**/bower_components": True,
                "**/*.code-search": True,
                "**/__pycache__": True,
                "**/*.pyc": True
            }
        }
        
        settings_file = vscode_dir / "settings.json"
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)

    def create_launch_json(self, vscode_dir):
        """Create enhanced launch.json configuration"""
        # Pre-process paths for launch configurations
        python_path = self._normalize_path(self.ai_env_path / "Miniconda" / "envs" / "AI2025" / "python")
        main_system_program = self._normalize_path(self.ai_env_path / "activate_ai_env.py")
        main_system_cwd = self._normalize_path(self.ai_env_path)
        conda_prefix_norm = self._normalize_path(self.ai_env_path / "Miniconda" / "envs" / "AI2025")
        pythonpath_norm = self._normalize_path(self.ai_env_path / "src")
        ai_env_path_norm = self._normalize_path(self.ai_env_path)
        path_string = self._build_path_string()
        
        launch_config = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "AI Environment: Current File",
                    "type": "python",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}",
                    "python": python_path,
                    "env": {
                        "CONDA_DEFAULT_ENV": "AI2025",
                        "CONDA_PREFIX": conda_prefix_norm,
                        "PATH": path_string,
                        "PYTHONPATH": pythonpath_norm,
                        "AI_ENV_PATH": ai_env_path_norm
                    },
                    "envFile": "${workspaceFolder}/.env",
                    "stopOnEntry": False,
                    "internalConsoleOptions": "neverOpen"
                },
                {
                    "name": "AI Environment: Main System",
                    "type": "python",
                    "request": "launch",
                    "program": main_system_program,
                    "console": "integratedTerminal",
                    "cwd": main_system_cwd,
                    "python": python_path,
                    "env": {
                        "CONDA_DEFAULT_ENV": "AI2025",
                        "CONDA_PREFIX": conda_prefix_norm,
                        "PATH": path_string,
                        "PYTHONPATH": pythonpath_norm
                    },
                    "stopOnEntry": False,
                    "internalConsoleOptions": "neverOpen"
                },
                {
                    "name": "AI Environment: Test Components",
                    "type": "python",
                    "request": "launch",
                    "program": main_system_program,
                    "args": ["test"],
                    "console": "integratedTerminal",
                    "cwd": main_system_cwd,
                    "python": python_path,
                    "env": {
                        "CONDA_DEFAULT_ENV": "AI2025",
                        "CONDA_PREFIX": conda_prefix_norm,
                        "PYTHONPATH": pythonpath_norm
                    }
                }
            ]
        }
        
        launch_file = vscode_dir / "launch.json"
        with open(launch_file, 'w', encoding='utf-8') as f:
            json.dump(launch_config, f, indent=2)
			