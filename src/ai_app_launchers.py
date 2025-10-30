#!/usr/bin/env python3
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30

AI Environment - Individual Application Launchers (macOS Version)
Handles launching of specific applications (Jupyter, Streamlit, etc.)
"""

import webbrowser
import time
from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = ""
    class Style:
        RESET_ALL = ""

class AppLaunchers:
    """Handles launching of individual applications on macOS"""

    def __init__(self, ai_env_path, process_manager):
        self.ai_env_path = Path(ai_env_path)
        self.process_manager = process_manager

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

    def launch_jupyter(self):
        """Launch Jupyter Lab"""
        print(f"\n{Fore.BLUE}📊 Launching Jupyter Lab...{Style.RESET_ALL}")

        success = self.process_manager.launch_jupyter()
        if success:
            self.print_info("Jupyter Lab is now running in background")
            self.print_info("Use 'Background Processes' menu to manage it")

            # Ask if user wants to open browser
            try:
                open_browser = input(f"\n{Fore.CYAN}Open Jupyter Lab in browser? (y/n): {Style.RESET_ALL}").lower()
                if open_browser in ['y', 'yes']:
                    time.sleep(3)  # Wait for server to start
                    webbrowser.open('http://localhost:8888')
                    self.print_success("Jupyter Lab opened in browser")
            except:
                pass

        return success

    def launch_streamlit_demo(self):
        """Launch Streamlit demo application"""
        print(f"\n{Fore.BLUE}🌟 Launching Streamlit Demo...{Style.RESET_ALL}")

        success = self.process_manager.launch_streamlit_demo()
        if success:
            self.print_info("Streamlit demo is now running in background")
            self.print_info("Use 'Background Processes' menu to manage it")

            # Ask if user wants to open browser
            try:
                open_browser = input(f"\n{Fore.CYAN}Open Streamlit demo in browser? (y/n): {Style.RESET_ALL}").lower().strip()
                if open_browser in ['y', 'yes']:
                    self.print_info("Waiting for Streamlit server to initialize...")
                    # Wait longer for Streamlit to start (it's slower than Jupyter)
                    max_wait = 15
                    port_found = False
                    for i in range(max_wait):
                        time.sleep(1)
                        if self._is_port_in_use(8501):
                            port_found = True
                            # Give it 2 more seconds after port opens for app to fully initialize
                            self.print_info("Server responding, finalizing startup...")
                            time.sleep(2)
                            break
                        if i % 2 == 0:
                            print(f"{Fore.YELLOW}.{Style.RESET_ALL}", end="", flush=True)
                    print()  # New line after dots

                    if not port_found:
                        self.print_warning("Server took longer than expected to start")
                        self.print_info("Opening browser anyway - you may need to refresh")

                    webbrowser.open('http://localhost:8501')
                    self.print_success("Streamlit demo opened in browser")
            except KeyboardInterrupt:
                self.print_info("Browser launch cancelled")
            except Exception as e:
                self.print_warning(f"Could not open browser: {e}")

        return success

    def _is_port_in_use(self, port):
        """Check if a port is in use"""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def launch_python_repl(self):
        """Launch Python REPL in new terminal on macOS"""
        print(f"\n{Fore.BLUE}🐍 Launching Python REPL...{Style.RESET_ALL}")

        try:
            # Launch Python in a new Terminal window using osascript
            osascript_cmd = f'''
tell application "Terminal"
    do script "cd '{self.ai_env_path}' && source '{self.ai_env_path}/Miniconda/bin/activate' AI2025 && python"
    activate
end tell
'''

            import subprocess
            process = subprocess.Popen(
                ['osascript', '-e', osascript_cmd],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            if process:
                self.print_success("Python REPL launched in new terminal window")
                self.print_info("Use 'Background Processes' menu to manage it")
                return True

            return False

        except Exception as e:
            self.print_error(f"Failed to launch Python REPL: {e}")
            return False

    def launch_conda_prompt(self):
        """Launch Conda prompt in new terminal on macOS"""
        print(f"\n{Fore.BLUE}🔧 Launching Conda Prompt...{Style.RESET_ALL}")

        try:
            # Find conda executable - check multiple locations for macOS
            from ai_path_finder import find_conda
            conda_exe = find_conda()

            if not conda_exe:
                conda_locations = [
                    self.ai_env_path / "Miniconda" / "bin" / "conda",
                    Path.home() / "miniconda3" / "bin" / "conda",
                    Path.home() / "anaconda3" / "bin" / "conda",
                    Path("/opt/miniconda3/bin/conda"),
                ]

                for location in conda_locations:
                    if location.exists():
                        conda_exe = location
                        break

            if not conda_exe:
                self.print_error("Conda executable not found!")
                self.print_info("Checked locations:")
                for loc in [
                    self.ai_env_path / "Miniconda" / "bin" / "conda",
                    Path.home() / "miniconda3" / "bin" / "conda",
                    Path.home() / "anaconda3" / "bin" / "conda",
                ]:
                    self.print_info(f"  - {loc}")
                return False

            # Activate conda environment and open prompt using Terminal.app
            osascript_cmd = f'''
tell application "Terminal"
    do script "cd '{self.ai_env_path}' && source '{conda_exe.parent.parent}/bin/activate' AI2025"
    activate
end tell
'''

            import subprocess
            process = subprocess.Popen(
                ['osascript', '-e', osascript_cmd],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            if process:
                self.print_success("Conda prompt launched in new terminal window")
                self.print_info("Use 'Background Processes' menu to manage it")
                return True

            return False

        except Exception as e:
            self.print_error(f"Failed to launch Conda prompt: {e}")
            return False

    def launch_file_explorer(self):
        """Launch Finder in AI Environment directory on macOS"""
        print(f"\n{Fore.BLUE}📁 Opening Finder...{Style.RESET_ALL}")

        try:
            import subprocess
            cmd = ['open', str(self.ai_env_path)]

            success = self.process_manager.launch_custom_command(
                ' '.join(cmd),
                "Finder",
                self.ai_env_path
            )

            if success:
                self.print_success("Finder opened")
                self.print_info("Use 'Background Processes' menu to manage it")
            return success

        except Exception as e:
            self.print_error(f"Failed to open Finder: {e}")
            return False

    def launch_tensorboard(self, log_dir=None):
        """Launch TensorBoard"""
        print(f"\n{Fore.BLUE}📈 Launching TensorBoard...{Style.RESET_ALL}")

        if log_dir is None:
            log_dir = self.ai_env_path / "Projects" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)

        try:
            cmd = f'tensorboard --logdir="{log_dir}" --port=6006'

            success = self.process_manager.launch_custom_command(
                cmd,
                "TensorBoard",
                self.ai_env_path
            )

            if success:
                self.print_success("TensorBoard launched successfully")
                self.print_info("Access TensorBoard at: http://localhost:6006")
                self.print_info("Use 'Background Processes' menu to manage it")

                # Ask if user wants to open browser
                try:
                    open_browser = input(f"\n{Fore.CYAN}Open TensorBoard in browser? (y/n): {Style.RESET_ALL}").lower()
                    if open_browser in ['y', 'yes']:
                        time.sleep(3)  # Wait for server to start
                        webbrowser.open('http://localhost:6006')
                        self.print_success("TensorBoard opened in browser")
                except:
                    pass

            return success

        except Exception as e:
            self.print_error(f"Failed to launch TensorBoard: {e}")
            return False

    def launch_mlflow_ui(self):
        """Launch MLflow UI"""
        print(f"\n{Fore.BLUE}🔬 Launching MLflow UI...{Style.RESET_ALL}")

        try:
            # Set MLflow tracking directory
            mlflow_dir = self.ai_env_path / "Projects" / "mlruns"
            mlflow_dir.mkdir(parents=True, exist_ok=True)

            cmd = f'mlflow ui --backend-store-uri "file:///{mlflow_dir}" --port=5000'

            success = self.process_manager.launch_custom_command(
                cmd,
                "MLflow UI",
                self.ai_env_path
            )

            if success:
                self.print_success("MLflow UI launched successfully")
                self.print_info("Access MLflow UI at: http://localhost:5000")
                self.print_info("Use 'Background Processes' menu to manage it")

                # Ask if user wants to open browser
                try:
                    open_browser = input(f"\n{Fore.CYAN}Open MLflow UI in browser? (y/n): {Style.RESET_ALL}").lower()
                    if open_browser in ['y', 'yes']:
                        time.sleep(3)  # Wait for server to start
                        webbrowser.open('http://localhost:5000')
                        self.print_success("MLflow UI opened in browser")
                except:
                    pass

            return success

        except Exception as e:
            self.print_error(f"Failed to launch MLflow UI: {e}")
            return False
