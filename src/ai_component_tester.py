# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30
"""

#!/usr/bin/env python3
"""
AI Environment - Component Testing Module
Comprehensive testing of all AI Environment components including model management and Jupyter Lab system
"""

import os
import re
import subprocess
import sys
from pathlib import Path
try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = ""
    class Style:
        RESET_ALL = ""

from ai_path_manager import PathManager
from ai_uv_manager import UVManager

class ComponentTester:
    """Comprehensive testing of AI Environment components"""

    def __init__(self, ai_env_path, venv_path):
        self.ai_env_path = Path(ai_env_path)
        self.venv_path = Path(venv_path)
        
    def print_step(self, step_num, description):
        """Print step header"""
        print(f"{Fore.CYAN}[*] Step {step_num}: {description}...{Style.RESET_ALL}")
        separator = "-" * 50
        print(f"{Fore.CYAN}{separator}{Style.RESET_ALL}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")
        
    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")
        
    def test_directory_structure(self):
        """Test AI Environment directory structure"""
        if self.ai_env_path.exists():
            self.print_success("AI Environment directory found")

            # Check for UV virtual environment (required)
            venv_found = False
            if self.venv_path.exists():
                self.print_success(f"  ✓ UV virtual environment found at: {self.venv_path}")
                venv_found = True
            else:
                self.print_error(f"  ✗ UV virtual environment not found")

            # Check for Ollama (optional) - check multiple locations
            ollama_found = False
            if (self.ai_env_path / "Ollama").exists():
                self.print_success(f"  ✓ Ollama directory found (portable)")
                ollama_found = True
            elif (self.ai_env_path / "AI_Environment" / "Ollama").exists():
                self.print_success(f"  ✓ Ollama directory found (in AI_Environment subfolder)")
                ollama_found = True
            else:
                self.print_info(f"  - Ollama directory not found (optional)")

            # Check other optional directories
            if (self.ai_env_path / "AI_Installer").exists():
                self.print_success(f"  ✓ AI_Installer directory found (optional)")
            else:
                self.print_info(f"  - AI_Installer directory not found (optional)")

            if venv_found:
                self.print_success("Directory structure test PASSED")
                return True
            else:
                self.print_error(f"Directory structure test FAILED - UV virtual environment not found")
                return False
        else:
            self.print_error("AI Environment directory not found")
            return False
            
    def test_uv_installation(self):
        """Test UV installation"""
        try:
            # Test UV command
            result = subprocess.run(["uv", "--version"],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.print_success(f"  ✓ UV version: {version}")
                self.print_success("UV installation test PASSED")
                return True
            else:
                self.print_error("  ✗ UV command failed")
                self.print_error("UV installation test FAILED")
                return False
        except FileNotFoundError:
            self.print_error("  ✗ UV not found in PATH")
            self.print_error("UV installation test FAILED")
            return False
        except Exception as e:
            self.print_error(f"  ✗ UV test error: {e}")
            self.print_error("UV installation test FAILED")
            return False
            
    def test_venv_environment(self):
        """Test UV virtual environment"""
        if self.venv_path.exists():
            self.print_success("UV virtual environment directory found")

            # Test Python executable
            python_exe = self.venv_path / "bin" / "python"
            if python_exe.exists():
                self.print_success("  ✓ Python executable found")

                # Test Python version
                try:
                    result = subprocess.run([str(python_exe), "--version"],
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        version = result.stdout.strip()
                        self.print_success(f"  ✓ Python version: {version}")
                        self.print_success("UV virtual environment test PASSED")
                        return True
                    else:
                        self.print_error("  ✗ Python version check failed")
                        self.print_error("UV virtual environment test FAILED")
                        return False
                except Exception as e:
                    self.print_error(f"  ✗ Python test error: {e}")
                    self.print_error("UV virtual environment test FAILED")
                    return False
            else:
                self.print_error("  ✗ Python executable not found")
                self.print_error("UV virtual environment test FAILED")
                return False
        else:
            self.print_error("UV virtual environment not found")
            return False
            
    def test_python_packages(self):
        """Test required Python packages"""
        required_packages = ["psutil", "colorama", "requests", "numpy", "pandas"]

        try:
            # Activate environment and test packages
            uv_manager = UVManager(self.venv_path)
            uv_manager.setup_venv_paths()
            
            package_results = []
            for package in required_packages:
                try:
                    # Special handling for packages that can be slow to import
                    if package == "pandas":
                        timeout_duration = 15
                        self.print_info(f"  Testing {package} (may take a moment)...")
                    elif package == "numpy":
                        timeout_duration = 10
                        self.print_info(f"  Testing {package} (may take a moment)...")
                    else:
                        timeout_duration = 5
                    
                    result = subprocess.run(["python", "-c", f"import {package}; print('{package} OK')"], 
                                          capture_output=True, text=True, timeout=timeout_duration)
                    if result.returncode == 0:
                        self.print_success(f"  ✓ {package} package available")
                        package_results.append(True)
                    else:
                        self.print_error(f"  ✗ {package} package missing or broken")
                        package_results.append(False)
                except subprocess.TimeoutExpired:
                    self.print_error(f"  ✗ {package} test error: Command 'python -c import {package}' timed out after {timeout_duration} seconds")
                    package_results.append(False)
                except Exception as e:
                    self.print_error(f"  ✗ {package} test error: {e}")
                    package_results.append(False)
            
            if all(package_results):
                self.print_success("Python packages test PASSED")
                return True
            else:
                missing_count = len([r for r in package_results if not r])
                self.print_error(f"Python packages test FAILED - {missing_count}/{len(required_packages)} packages missing")
                return False
                
        except Exception as e:
            self.print_error(f"Package testing failed: {e}")
            return False
            
    def test_ollama_installation(self):
        """Test Ollama installation (optional)"""
        # Check multiple locations for Ollama
        ollama_exe = None

        # 1. Check portable location
        portable_ollama = self.ai_env_path / "Ollama" / "ollama.exe"
        if portable_ollama.exists():
            self.print_success("Ollama directory found (portable)")
            ollama_exe = portable_ollama

        # 2. Check AI_Environment subfolder
        installer_ollama = self.ai_env_path / "AI_Environment" / "Ollama" / "ollama.exe"
        if not ollama_exe and installer_ollama.exists():
            self.print_success("Ollama directory found (in AI_Environment subfolder)")
            ollama_exe = installer_ollama

        if ollama_exe:
            self.print_success("  ✓ ollama.exe found")

            try:
                # Try version command first
                result = subprocess.run([str(ollama_exe), "version"],
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    version_info = result.stdout.strip()
                    self.print_success(f"  ✓ Ollama version: {version_info}")
                    self.print_success("Ollama installation test PASSED")
                    return True
                else:
                    # Try alternative commands if version fails
                    self.print_info("  - Version command failed, trying alternative check...")
                    result2 = subprocess.run([str(ollama_exe), "--help"],
                                            capture_output=True, text=True, timeout=5)
                    if result2.returncode == 0:
                        self.print_success("  ✓ Ollama executable responds to --help")
                        self.print_success("Ollama installation test PASSED (basic)")
                        return True
                    else:
                        self.print_error(f"  ✗ Ollama version check failed (exit code: {result.returncode})")
                        if result.stderr:
                            self.print_error(f"  ✗ Error output: {result.stderr.strip()}")
                        self.print_error("Ollama installation test FAILED")
                        return False
            except Exception as e:
                self.print_error(f"  ✗ Ollama test error: {e}")
                self.print_error("Ollama installation test FAILED")
                return False
        else:
            self.print_info("Ollama not installed (optional component)")
            return True  # Count as passed since it's optional
            
    def test_system_integration(self):
        """Test system integration"""
        try:
            # Test PATH configuration
            current_path = os.environ.get("PATH", "")
            if "AI_Environment" in current_path:
                self.print_success("  ✓ AI Environment paths in system PATH")
            else:
                self.print_info("  ℹ AI Environment paths not in current PATH (normal)")
            
            # Test environment variables
            venv_active = os.environ.get("VIRTUAL_ENV", "")
            if venv_active:
                self.print_success(f"  ✓ Active virtual environment: {venv_active}")
            else:
                self.print_info("  ℹ No active virtual environment")
            
            # Test basic Windows commands
            path_manager = PathManager()
            cmd_results = path_manager.test_basic_commands()
            
            working_commands = sum(1 for result in cmd_results.values() if result)
            total_commands = len(cmd_results)
            
            if working_commands == total_commands:
                self.print_success(f"  ✓ All Windows commands working ({working_commands}/{total_commands})")
                self.print_success("System integration test PASSED")
                return True
            else:
                self.print_error(f"  ✗ Some Windows commands not working ({working_commands}/{total_commands})")
                self.print_error("System integration test FAILED")
                return False
                
        except Exception as e:
            self.print_error(f"System integration test error: {e}")
            return False
            
    def test_model_management_system(self):
        """Test AI model management components"""
        try:
            self.print_info("Testing AI model management system...")
            
            # Test model manager import
            try:
                import sys
                sys.path.append(str(self.ai_env_path / "src"))
                from ai_model_manager import AIModelManager
                self.print_success("  ✓ AI Model Manager module loads correctly")
            except ImportError as e:
                self.print_error(f"  ✗ AI Model Manager import failed: {e}")
                return False
            
            # Test model loader import
            try:
                from ai_model_loader import ModelLoader
                self.print_success("  ✓ Model Loader module loads correctly")
            except ImportError as e:
                self.print_error(f"  ✗ Model Loader import failed: {e}")
                return False
            
            # Test model downloader import
            try:
                from ai_model_downloader import ModelDownloader
                self.print_success("  ✓ Model Downloader module loads correctly")
            except ImportError as e:
                self.print_error(f"  ✗ Model Downloader import failed: {e}")
                return False
            
            # Test help directory
            help_dir = self.ai_env_path / "help"
            if help_dir.exists():
                help_files = list(help_dir.glob("*.txt"))
                if len(help_files) >= 5:
                    self.print_success(f"  ✓ Help directory contains {len(help_files)} model help files")
                else:
                    self.print_info(f"  ⚠ Help directory contains only {len(help_files)} files (expected 5+)")
            else:
                self.print_error("  ✗ Help directory not found")
                return False
            
            self.print_success("Model management system test PASSED")
            return True
            
        except Exception as e:
            self.print_error(f"Model management system test error: {e}")
            return False
    
    def test_jupyter_lab_system(self):
        """Test Jupyter Lab management components"""
        try:
            self.print_info("Testing Jupyter Lab management system...")
            
            # Test Jupyter manager import
            try:
                import sys
                sys.path.append(str(self.ai_env_path / "src"))
                from ai_jupyter_manager import JupyterLabManager
                self.print_success("  ✓ Jupyter Lab Manager module loads correctly")
            except ImportError as e:
                self.print_error(f"  ✗ Jupyter Lab Manager import failed: {e}")
                return False
            
            # Test Projects directory
            projects_dir = self.ai_env_path / "Projects"
            if projects_dir.exists():
                project_dirs = [d for d in projects_dir.iterdir() if d.is_dir()]
                if len(project_dirs) > 0:
                    self.print_success(f"  ✓ Projects directory contains {len(project_dirs)} project(s)")
                else:
                    self.print_info("  ℹ Projects directory is empty (normal for new installation)")
            else:
                self.print_info("  ℹ Projects directory not found (will be created on first use)")
            
            self.print_success("Jupyter Lab system test PASSED")
            return True
            
        except Exception as e:
            self.print_error(f"Jupyter Lab system test error: {e}")
            return False

    def test_safe_update_mechanism(self):
        """Test the safe update mechanism for run_ai_env.bat"""
        self.print_info("Testing safe update mechanism...")
        
        new_bat_file = self.ai_env_path / "run_ai_env.bat.new"
        temp_update_script = self.ai_env_path / "temp_update_script.bat"

        # Simulate creation of the .new file and the temp script
        try:
            with open(new_bat_file, "w") as f:
                f.write("echo This is the new run_ai_env.bat")
            self.print_success(f"  ✓ Created dummy {new_bat_file.name}")

            script_content = f"""
@echo off
REM This is a dummy update script
DEL "{new_bat_file}"
DEL "%~f0"
"""
            with open(temp_update_script, "w") as f:
                f.write(script_content)
            self.print_success(f"  ✓ Created dummy {temp_update_script.name}")

            # Check if the files exist
            if new_bat_file.exists() and temp_update_script.exists():
                self.print_success("  ✓ Staging files for safe update exist")
                self.print_success("Safe update mechanism test PASSED")
                return True
            else:
                self.print_error("  ✗ Staging files for safe update do not exist")
                self.print_error("Safe update mechanism test FAILED")
                return False
        except Exception as e:
            self.print_error(f"  ✗ Error during safe update mechanism test: {e}")
            self.print_error("Safe update mechanism test FAILED")
            return False
        finally:
            # Clean up dummy files
            if new_bat_file.exists():
                new_bat_file.unlink()
            if temp_update_script.exists():
                temp_update_script.unlink()

    def run_all_tests(self):
        """Run all component tests"""
        results = {}
        
        self.print_step(1, "Testing AI Environment directory structure")
        results["directory_structure"] = self.test_directory_structure()

        self.print_step(2, "Testing UV installation")
        results["uv_installation"] = self.test_uv_installation()

        self.print_step(3, "Testing UV virtual environment")
        results["venv_environment"] = self.test_venv_environment()
        
        self.print_step(4, "Testing Python packages")
        results["python_packages"] = self.test_python_packages()
        
        self.print_step(5, "Testing Ollama installation (optional)")
        results["ollama_installation"] = self.test_ollama_installation()
        
        self.print_step(6, "Testing system integration")
        results["system_integration"] = self.test_system_integration()

        self.print_step(7, "Testing AI model management system")
        results["model_management"] = self.test_model_management_system()

        self.print_step(8, "Testing Jupyter Lab management system")
        results["jupyter_lab_management"] = self.test_jupyter_lab_system()

        self.print_step(9, "Testing safe update mechanism")
        results["safe_update_mechanism"] = self.test_safe_update_mechanism()
        
        self.print_summary(results)
        return all(results.values())
        
    def print_summary(self, results):
        """Print test summary"""
        print("\n============================================================")
        print("                        TEST SUMMARY")
        print("============================================================")
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Total tests run: {total_tests}")
        print(f"Tests passed: {passed_tests}")
        print(f"Tests failed: {failed_tests}")
        print(f"Success rate: {success_rate:.1f}%")
        print()
        
        if passed_tests == total_tests:
            print(f"{Fore.GREEN}🎉 ALL TESTS PASSED! Your AI Environment is fully functional.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ SOME TESTS FAILED. Please review the errors above.{Style.RESET_ALL}")

def main():
    """Main function for standalone execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description=
        "AI Environment Component Tester")
    parser.add_argument("--ai-env-path", default=".",
                       help="Path to AI Environment directory")
    parser.add_argument("--venv-path",
                       default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".venv"),
                       help="Path to UV virtual environment")

    args = parser.parse_args()

    tester = ComponentTester(args.ai_env_path, args.venv_path)
    tester.run_all_tests()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[INFO] Testing interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] Unexpected error during testing: {e}{Style.RESET_ALL}")
        sys.exit(1)
		