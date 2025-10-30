# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.0 - macOS Version
Date: 2025-08-12
"""

#!/usr/bin/env python3
"""
AI Environment - Conda Management Module (macOS)
Handles conda environment activation and verification
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

class CondaManager:
    """Manages conda environment activation for AI Environment on macOS"""

    def __init__(self, conda_path):
        self.conda_path = Path(conda_path)
        self.conda_exe = self.conda_path / "bin" / "conda"
        self.ai_env_path = self.conda_path.parent

    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")

    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")

    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")

    def setup_conda_paths(self, env_name):
        """Setup conda paths in environment variables for macOS"""
        env_path = self.conda_path / "envs" / env_name

        # Verify the conda environment actually exists
        if not env_path.exists():
            self.print_error(f"Conda environment not found at: {env_path}")
            self.print_info(f"Please create the '{env_name}' environment first")
            return False

        # Build new PATH with conda paths first (macOS structure)
        conda_paths = [
            str(env_path / "bin"),
            str(self.conda_path / "bin"),
            str(self.conda_path / "condabin"),
        ]

        # Get current PATH and prepend conda paths
        current_path = os.environ.get('PATH', '')
        new_path = ':'.join(conda_paths + [current_path])

        # Set environment variables
        os.environ['PATH'] = new_path
        os.environ['CONDA_DEFAULT_ENV'] = env_name
        os.environ['CONDA_PREFIX'] = str(env_path)

        self.print_info("Conda paths configured")
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
                normalized_ai_env_path = str(self.ai_env_path.resolve())

                # Check if Python is from our AI Environment (preferred) or external installation (acceptable)
                if normalized_ai_env_path in normalized_python_path:
                    self.print_success(f"Using portable Python from AI Environment: {python_path}")
                    return True
                else:
                    # Allow external Python installations (like system-wide Miniconda)
                    self.print_info(f"Using external Python installation: {python_path}")
                    self.print_info(f"Note: For full portability, install Miniconda in {self.ai_env_path}")
                    return True
            else:
                # Fallback: try which command if available
                try:
                    result = subprocess.run(['which', 'python'],
                                          capture_output=True,
                                          text=True,
                                          timeout=10)

                    if result.returncode == 0:
                        python_path = result.stdout.strip()
                        # Normalize paths for comparison
                        normalized_python_path = str(Path(python_path).resolve())
                        normalized_ai_env_path = str(self.ai_env_path.resolve())

                        # Check if Python is from our AI Environment (preferred) or external installation (acceptable)
                        if normalized_ai_env_path in normalized_python_path:
                            self.print_success(f"Using portable Python from AI Environment: {python_path}")
                            return True
                        else:
                            # Allow external Python installations (like system-wide Miniconda)
                            self.print_info(f"Using external Python installation: {python_path}")
                            self.print_info(f"Note: For full portability, install Miniconda in {self.ai_env_path}")
                            return True
                    else:
                        self.print_error("Could not locate Python executable")
                        return False
                except:
                    self.print_error("Could not verify Python location")
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

    def test_conda_environment(self, env_name):
        """Test if conda environment is working"""
        try:
            # Test conda list command
            result = subprocess.run(['conda', 'list'],
                                  capture_output=True,
                                  text=True,
                                  timeout=15)

            if result.returncode == 0:
                self.print_success("Conda environment is functional")
                return True
            else:
                self.print_error("Conda environment test failed")
                if result.stderr:
                    self.print_error(f"Error output: {result.stderr.strip()}")
                if result.stdout:
                    self.print_info(f"Standard output: {result.stdout.strip()}")
                return False

        except Exception as e:
            self.print_error(f"Conda environment test error: {e}")
            return False

    def activate_environment(self, env_name):
        """Activate conda environment"""
        try:
            self.print_info(f"Activating conda environment: {env_name}")

            # Setup conda paths - verify environment exists first
            if not self.setup_conda_paths(env_name):
                return False

            # Verify Python location
            if not self.verify_python_location():
                return False

            # Get Python version
            self.get_python_version()

            # Test conda environment
            if not self.test_conda_environment(env_name):
                return False

            self.print_success(f"Conda environment '{env_name}' activated successfully")
            return True

        except Exception as e:
            self.print_error(f"Failed to activate conda environment: {e}")
            return False

def main():
    """Test conda manager"""
    from ai_path_finder import find_miniconda

    conda_path = find_miniconda()
    if not conda_path:
        print(f"{Fore.RED}Miniconda not found!{Style.RESET_ALL}")
        return

    conda_manager = CondaManager(conda_path)

    success = conda_manager.activate_environment("AI2025")

    if success:
        print(f"\n{Fore.GREEN}Conda environment activation successful{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Conda environment activation failed{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
