# AI Environment Module v3.0.28
# Version: 3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30

AI Environment - Application Launcher Module (Main Class)
Handles launching various applications in background mode with enhanced VS Code integration
"""

import subprocess
import time
import os
from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = ""
    class Style:
        RESET_ALL = ""

from ai_process_manager import BackgroundProcessManager
from ai_vscode_config import VSCodeConfigManager
from ai_app_launchers import AppLaunchers
from ai_launcher_menu import LauncherMenu

# Universal path detection - works regardless of installation location
def get_ai_environment_path():
    """
    Dynamically detect AI_Environment path based on script location.
    This module is in src/ subdirectory, so go up one level to get AI_Environment root.

    Returns:
        Path: The absolute path to AI_Environment directory
    """
    # This script is in src/ folder, so parent's parent is AI_Environment
    script_path = Path(__file__).resolve()
    ai_env_path = script_path.parent.parent

    # Verify this is actually the AI_Environment directory
    expected_items = ['src', 'Projects', 'activate_ai_env.py']
    if all((ai_env_path / item).exists() for item in expected_items):
        return ai_env_path

    # Fallback: search for AI_Environment folder in path
    if 'AI_Environment' in str(ai_env_path):
        parts = ai_env_path.parts
        for i, part in enumerate(parts):
            if part == 'AI_Environment':
                return Path(*parts[:i+1])

    # Last resort: return calculated path
    return ai_env_path

class ApplicationLauncher:
    """Launches and manages various AI development applications"""
    
    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)
        self.process_manager = BackgroundProcessManager(ai_env_path)
        self.vscode_config = VSCodeConfigManager(ai_env_path)
        self.app_launchers = AppLaunchers(ai_env_path, self.process_manager)
        self.launcher_menu = LauncherMenu()
        
    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")
        
    def print_warning(self, message):
        """Print warning message"""
        print(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")

    def launch_vscode(self, project_path=None):
        """Enhanced VS Code launcher with AI Environment v3.0.26 integration"""
        print(f"\n{Fore.BLUE}💻 Launching VS Code with AI Environment Integration...{Style.RESET_ALL}")
        
        if project_path is None:
            # Show enhanced project selection menu
            projects_dir = self.ai_env_path / "Projects"
            projects_dir.mkdir(exist_ok=True)
            
            print(f"\n{Fore.CYAN}📁 Available Projects:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW} 1.{Style.RESET_ALL} Open Projects workspace (AI Environment standard)")
            print(f"{Fore.YELLOW} 2.{Style.RESET_ALL} Create new AI project")
            print(f"{Fore.YELLOW} 3.{Style.RESET_ALL} Open AI Environment root (system development)")
            print(f"{Fore.YELLOW} 4.{Style.RESET_ALL} Open current directory")
            print(f"{Fore.YELLOW} 0.{Style.RESET_ALL} Cancel")
            
            try:
                choice = int(input(f"\n{Fore.CYAN}Select option (0-4): {Style.RESET_ALL}"))
                
                if choice == 0:
                    return False
                elif choice == 1:
                    project_path = projects_dir
                elif choice == 2:
                    project_name = input(f"{Fore.CYAN}Enter project name: {Style.RESET_ALL}").strip()
                    if project_name:
                        project_path = projects_dir / project_name
                        project_path.mkdir(exist_ok=True)
                        self.print_success(f"Created project: {project_path}")
                    else:
                        self.print_error("Invalid project name")
                        return False
                elif choice == 3:
                    project_path = self.ai_env_path
                elif choice == 4:
                    project_path = Path.cwd()
                else:
                    self.print_error("Invalid choice")
                    return False
                    
            except ValueError:
                self.print_error("Invalid input")
                return False

        # Check for VS Code executable (try multiple locations)
        vscode_paths = [
            "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code",  # Portable in AI Environment
            "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code".format(os.environ.get('USERNAME', '')),
            "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code",
            "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
        ]
        
        vscode_exe = None
        for path in vscode_paths:
            if Path(path).exists():
                vscode_exe = Path(path)
                break
        
        if not vscode_exe:
            self.print_error("VS Code not found! Please install VS Code or update the path")
            self.print_info("Checked locations:")
            for path in vscode_paths:
                self.print_info(f"  - {path}")
            return False

        # Setup enhanced workspace configuration
        self.vscode_config.create_enhanced_vscode_config(project_path)
        
        # Create enhanced main.py if it doesn't exist
        main_py = project_path / "main.py"
        if not main_py.exists():
            self.vscode_config.create_enhanced_main_py(main_py)
        
        # Prepare VS Code command with AI Environment integration
        cmd = [str(vscode_exe)]
        cmd.append(str(project_path))
        
        # Add additional arguments for better integration
        cmd.extend([
            "--disable-telemetry",  # Privacy
            "--new-window"          # Always open in new window
        ])
        
        # Open main.py directly if it exists
        if main_py.exists():
            cmd.append(str(main_py))
            
        self.print_info("Launching VS Code with enhanced AI Environment integration...")
        self.print_info(f"✓ Project workspace: {project_path}")
        self.print_info(f"✓ VS Code executable: {vscode_exe}")
        self.print_info("✓ AI2025 interpreter configured")
        self.print_info("✓ [AI2025-Terminal] profile ready")
        self.print_info("✓ AI Environment system integration enabled")
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                # macOS: no special creation flags needed
            )
            
            # Track the process with enhanced information
            success = self.process_manager.track_process(
                process_id=f"vscode_ai_env_{int(time.time())}",
                name="VS Code (AI Environment)",
                pid=process.pid,
                command=' '.join(cmd),
                url=None
            )
            
            if success:
                self.print_success(f"VS Code launched successfully (PID: {process.pid})")
                self.print_info("🎯 Quick Start Guide:")
                self.print_info("  1. Press Ctrl+` to open [AI2025-Terminal]")
                self.print_info("  2. Press F5 to debug with AI2025 interpreter")
                self.print_info("  3. Use Ctrl+Shift+P → 'Tasks: Run Task' for AI Environment tasks")
                self.print_info("  4. Run 'python activate_ai_env.py' to access main menu")
                self.print_success("🚀 VS Code is ready with full AI Environment v3.0.26 integration!")
                return True
            else:
                self.print_error("Failed to track VS Code process")
                return False
            
        except Exception as e:
            self.print_error(f"Failed to launch VS Code: {e}")
            return False

    # Delegate other launcher methods to AppLaunchers
    def launch_jupyter(self):
        """Launch Jupyter Lab"""
        return self.app_launchers.launch_jupyter()
        
    def launch_streamlit_demo(self):
        """Launch Streamlit demo application"""
        return self.app_launchers.launch_streamlit_demo()
        
    def launch_python_repl(self):
        """Launch Python REPL in new terminal"""
        return self.app_launchers.launch_python_repl()
            
    def launch_conda_prompt(self):
        """Launch Conda prompt in new terminal"""
        return self.app_launchers.launch_conda_prompt()
            
    def launch_file_explorer(self):
        """Launch File Explorer in AI Environment directory"""
        return self.app_launchers.launch_file_explorer()
            
    def launch_tensorboard(self, log_dir=None):
        """Launch TensorBoard"""
        return self.app_launchers.launch_tensorboard(log_dir)
            
    def launch_mlflow_ui(self):
        """Launch MLflow UI"""
        return self.app_launchers.launch_mlflow_ui()
            
    def show_launch_menu(self):
        """Show application launch menu"""
        return self.launcher_menu.show_launch_menu()
        
    def handle_launch_choice(self, choice):
        """Handle application launch choice"""
        if choice == 1:
            return self.launch_vscode()
        elif choice == 2:
            return self.launch_jupyter()
        elif choice == 3:
            return self.launch_streamlit_demo()
        elif choice == 4:
            return self.launch_python_repl()
        elif choice == 5:
            return self.launch_conda_prompt()
        elif choice == 6:
            return self.launch_file_explorer()
        elif choice == 7:
            return self.launch_tensorboard()
        elif choice == 8:
            return self.launch_mlflow_ui()
        else:
            return False

def main():
    """Test application launcher"""
    # Use dynamic path detection instead of hardcoded path
    ai_env_path = get_ai_environment_path()
    app_launcher = ApplicationLauncher(ai_env_path)
    
    print("Testing Enhanced Application Launcher with AI Environment v3.0.26 integration...")
    app_launcher.show_launch_menu()

if __name__ == "__main__":
    main()
	