# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.28 - macOS Version with UV
Date: 2025-08-14
"""

#!/usr/bin/env python3
"""
AI Environment - UV Environment Management Module (macOS)
Handles UV virtual environment activation and verification
"""

import os
import subprocess
from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = ""
    class Style:
        RESET_ALL = ""

class UVManager:
    """Manages UV virtual environment activation for AI Environment on macOS"""

    def __init__(self, venv_path):
        self.venv_path = Path(venv_path)
        self.python_exe = self.venv_path / "bin" / "python"
        self.ai_env_path = self.venv_path.parent

    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")

    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")

    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")

    def setup_venv_paths(self):
        """Setup UV virtual environment paths in environment variables for macOS"""

        # Verify the virtual environment actually exists
        if not self.venv_path.exists():
            self.print_error(f"Virtual environment not found at: {self.venv_path}")
            self.print_info("Please create the virtual environment first using 'uv venv'")
            return False

        # Build new PATH with venv paths first
        venv_paths = [
            str(self.venv_path / "bin"),
        ]

        # Get current PATH and prepend venv paths
        current_path = os.environ.get('PATH', '')
        new_path = ':'.join(venv_paths + [current_path])

        # Set environment variables
        os.environ['PATH'] = new_path
        os.environ['VIRTUAL_ENV'] = str(self.venv_path)

        # Remove PYTHONHOME if set (can interfere with venv)
        if 'PYTHONHOME' in os.environ:
            del os.environ['PYTHONHOME']

        self.print_info("UV virtual environment paths configured")
        return True

    def verify_python_location(self):
        """Verify Python is accessible"""
        try:
            # First try to get Python executable path directly
            result = subprocess.run(['python', '-c', 'import sys; print(sys.executable)'],
                                  capture_output=True,
                                  text=True,
                                  timeout=10)

            if result.returncode == 0:
                python_path = result.stdout.strip()
                # Normalize paths for comparison
                normalized_python_path = str(Path(python_path).resolve())
                normalized_venv_path = str(self.venv_path.resolve())

                # Check if Python is from our virtual environment
                if normalized_venv_path in normalized_python_path:
                    self.print_success(f"Using Python from UV virtual environment: {python_path}")
                    return True
                else:
                    self.print_error(f"Python is not from virtual environment: {python_path}")
                    self.print_info(f"Expected Python from: {self.venv_path}")
                    return False
            else:
                self.print_error("Could not locate Python executable")
                return False

        except Exception as e:
            self.print_error(f"Failed to verify Python location: {e}")
            return False

    def get_python_version(self):
        """Get Python version from activated environment"""
        try:
            result = subprocess.run(['python', '--version'],
                                  capture_output=True,
                                  text=True,
                                  timeout=10)

            if result.returncode == 0:
                version = result.stdout.strip()
                self.print_info(f"Python version: {version}")
                return version
            else:
                self.print_error("Could not get Python version")
                return None

        except Exception as e:
            self.print_error(f"Failed to get Python version: {e}")
            return None

    def test_venv_environment(self):
        """Test if virtual environment is working"""
        try:
            # Test pip list command
            result = subprocess.run(['python', '-m', 'pip', 'list'],
                                  capture_output=True,
                                  text=True,
                                  timeout=15)

            if result.returncode == 0:
                self.print_success("Virtual environment is functional")
                return True
            else:
                self.print_error("Virtual environment test failed")
                if result.stderr:
                    self.print_error(f"Error output: {result.stderr.strip()}")
                if result.stdout:
                    self.print_info(f"Standard output: {result.stdout.strip()}")
                return False

        except Exception as e:
            self.print_error(f"Virtual environment test error: {e}")
            return False

    def activate_environment(self):
        """Activate UV virtual environment"""
        try:
            self.print_info(f"Activating UV virtual environment")

            # Setup venv paths - verify environment exists first
            if not self.setup_venv_paths():
                return False

            # Verify Python location
            if not self.verify_python_location():
                return False

            # Get Python version
            self.get_python_version()

            # Test virtual environment
            if not self.test_venv_environment():
                return False

            self.print_success(f"UV virtual environment activated successfully")
            return True

        except Exception as e:
            self.print_error(f"Failed to activate virtual environment: {e}")
            return False

def main():
    """Test UV manager"""
    from ai_path_finder import find_uv_venv

    venv_path = find_uv_venv()
    if not venv_path:
        print(f"{Fore.RED}UV virtual environment not found!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Run 'uv venv' to create one first{Style.RESET_ALL}")
        return

    uv_manager = UVManager(venv_path)

    success = uv_manager.activate_environment()

    if success:
        print(f"\n{Fore.GREEN}UV environment activation successful{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}UV environment activation failed{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
