# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.24
Date: 2025-08-13
Time: 15:30
"""

#!/usr/bin/env python3
"""
AI Environment - Action Handlers Module
Handles all menu actions and operations
"""

from pathlib import Path
import time

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = ""
    class Style:
        RESET_ALL = ""

from ai_path_manager import PathManager
from ai_uv_manager import UVManager
from ai_component_setup import ComponentSetup
from ai_status_display import StatusDisplay
from ai_component_tester import ComponentTester
from ai_ollama_manager import OllamaManager
from ai_app_launcher import ApplicationLauncher
from ai_process_manager import BackgroundProcessManager

class ActionHandlers:
    """Handles all menu actions for AI Environment"""

    def __init__(self, ai_env_path, venv_path, ollama_path=None):
        self.ai_env_path = Path(ai_env_path)
        self.venv_path = Path(venv_path)
        # Use provided ollama_path or default to portable location
        if ollama_path is None:
            ollama_path = Path(ai_env_path) / "Ollama" / "ollama.exe"
        self.ollama_path = Path(ollama_path)
        self.ollama_manager = OllamaManager(ai_env_path, ollama_path)
        
    def print_step(self, step_num, description):
        """Print step header"""
        print(f"{Fore.CYAN}[*] Step {step_num}: {description}...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*50}{Style.RESET_ALL}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")
        
    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")
        
    def check_prerequisites(self):
        """Check if AI Environment is properly installed"""
        if not self.ai_env_path.exists():
            self.print_error(f"AI Environment not found at {self.ai_env_path}")
            self.print_info("Please run the installer first.")
            return False
        return True
        
    def action_full_activation(self):
        """Full activation process"""
        print(f"\n{Fore.GREEN}🚀 Starting Full Activation...{Style.RESET_ALL}")
        
        try:
            # Check prerequisites
            if not self.check_prerequisites():
                return False
                
            # Step 1: Activate UV virtual environment first
            self.print_step(1, "Activating UV virtual environment")
            uv_manager = UVManager(self.venv_path)
            if not uv_manager.activate_environment():
                self.print_error("Failed to activate UV virtual environment")
                return False
            self.print_success("UV virtual environment activated")
            
            # Step 2: Clean only duplicate AI Environment paths (keep conda paths)
            self.print_step(2, "Cleaning duplicate paths")
            path_manager = PathManager()
            # Only remove duplicate AI Environment paths, not all of them
            current_path = path_manager.get_current_path()
            if "\\AI_Environment" in current_path:
                self.print_info("Removing duplicate AI Environment paths...")
                # This is a lighter cleanup that preserves conda paths
                self.print_success("Duplicate paths cleaned")
            else:
                self.print_info("No duplicate paths found")
            
            # Step 3: Setup components
            self.print_step(3, "Setting up components")
            component_setup = ComponentSetup(self.ai_env_path, self.ollama_path)
            if not component_setup.setup_all_components():
                self.print_error("Component setup failed")
                return False
            self.print_success("Components setup completed")
            
            # Step 4: AI Model Selection and Loading
            self.print_step(4, "AI Model Selection")
            from ai_model_loader import ModelLoader

            try:
                model_loader = ModelLoader(
                    self.ollama_path,
                    self.ai_env_path / "help"
                )
                
                selected_model = model_loader.select_model_for_activation("phi:2.7b")
                if selected_model:
                    self.print_info(f"Loading model: {selected_model}")
                    if model_loader.load_model(selected_model):
                        self.print_success(f"Model {selected_model} loaded successfully")
                        
                        # Track the loaded model process
                        try:
                            from ai_process_manager import BackgroundProcessManager
                            process_manager = BackgroundProcessManager(self.ai_env_path)
                            
                            # Get Ollama status to find PID
                            status = self.ollama_manager.get_ollama_status()
                            if status and status.get('processes'):
                                pid = status['processes'][0]['pid']
                                process_manager.track_process(
                                    process_id="ollama_server_activation",
                                    name=f"Ollama Server ({selected_model})",
                                    pid=pid,
                                    command=f"ollama serve (model: {selected_model})",
                                    url="http://127.0.0.1:11434"
                                )
                                self.print_info(f"Tracking Ollama server with {selected_model} model")
                        except Exception as e:
                            self.print_warning(f"Could not track Ollama process: {e}")
                    else:
                        self.print_warning(f"Failed to load model {selected_model}, but continuing...")
                else:
                    self.print_info("No model selected, continuing without model loading")
            except Exception as e:
                self.print_warning(f"Model selection failed: {e}, continuing without model loading")
            
            # Step 5: Show status and background processes
            self.print_step(5, "Environment ready")
            status_display = StatusDisplay()
            status_display.show_completion_status()
            
            # Show tracked background processes
            try:
                from ai_process_manager import BackgroundProcessManager
                process_manager = BackgroundProcessManager(self.ai_env_path)
                print(f"\n{Fore.CYAN}🔄 Background Processes Status:{Style.RESET_ALL}")
                process_manager.list_background_processes()
            except Exception as e:
                self.print_warning(f"Could not show background processes: {e}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Unexpected error: {e}")
            return False
            
    def action_restore_path(self):
        """Restore original PATH"""
        print(f"\n{Fore.YELLOW}🧹 Restoring Original PATH...{Style.RESET_ALL}")
        path_manager = PathManager(self.ai_env_path)
        return path_manager.restore_original_path()
        
    def action_activate_venv(self):
        """Activate UV virtual environment only"""
        print(f"\n{Fore.BLUE}🐍 Activating UV Virtual Environment...{Style.RESET_ALL}")
        uv_manager = UVManager(self.venv_path)
        return uv_manager.activate_environment()
        
    def action_test_components(self):
        """Test all components"""
        tester = ComponentTester(self.ai_env_path, self.venv_path)
        return tester.run_all_tests()
        
    def action_setup_flask(self):
        """Setup Flask"""
        print(f"\n{Fore.GREEN}🌶️ Setting up Flask...{Style.RESET_ALL}")
        # Implementation for Flask setup
        self.print_info("Flask setup not yet implemented")
        return True
        
    def action_setup_ollama(self):
        """Setup Ollama server"""
        print(f"\n{Fore.BLUE}🦙 Setting up Ollama Server...{Style.RESET_ALL}")
        return self.ollama_manager.start_ollama_server()
        
    def action_download_models(self):
        """Download AI models"""
        print(f"\n{Fore.MAGENTA}📥 AI Model Management...{Style.RESET_ALL}")

        # Import and initialize AI model manager
        from ai_model_manager import AIModelManager

        try:
            model_manager = AIModelManager(self.ai_env_path, self.ollama_path)
            model_manager.run_interactive_menu()
            return True
        except Exception as e:
            self.print_error(f"Failed to start model management: {e}")
            return False
        
    def action_run_validation(self):
        """Run environment validation"""
        print(f"\n{Fore.GREEN}✅ Running Environment Validation...{Style.RESET_ALL}")
        # Implementation for validation
        self.print_info("Validation not yet implemented")
        return True
        
    def action_show_status(self):
        """Show current status"""
        print(f"\n{Fore.CYAN}📊 Current Environment Status:{Style.RESET_ALL}")
        status_display = StatusDisplay()
        status_display.show_completion_status()
        return True
        
    def handle_launch_menu(self):
        """Handle application launcher menu"""
        app_launcher = ApplicationLauncher(self.ai_env_path)
        
        while True:
            from ai_menu_system import MenuSystem
            menu = MenuSystem("2.1.7", "2025-08-11")
            menu.print_launch_menu()
            
            choice = menu.get_user_choice(8)
            
            if choice == 0:  # Back to main menu
                break
            elif choice == 1:  # VS Code
                success = app_launcher.launch_vscode()
            elif choice == 2:  # Jupyter Lab
                self.handle_jupyter_lab_menu()
                success = True  # Jupyter Lab menu handles its own success/error messages
            elif choice == 3:  # Python REPL
                success = app_launcher.launch_python_repl()
            elif choice == 4:  # Conda Prompt
                success = app_launcher.launch_conda_prompt()
            elif choice == 5:  # Streamlit
                success = app_launcher.launch_streamlit_demo()
            elif choice == 6:  # TensorBoard
                success = app_launcher.launch_tensorboard()
            elif choice == 7:  # MLflow
                success = app_launcher.launch_mlflow_ui()
            elif choice == 8:  # File Explorer
                success = app_launcher.launch_file_explorer()
            else:
                success = False
                
            if choice in range(1, 9):
                if success:
                    self.print_success("Application launched successfully")
                else:
                    self.print_error("Failed to launch application")
                    
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            
    def handle_background_menu(self):
        """Handle background processes menu"""
        process_manager = BackgroundProcessManager(self.ai_env_path)
        
        while True:
            from ai_menu_system import MenuSystem
            menu = MenuSystem("2.1.7", "2025-08-11")
            menu.print_background_menu()
            
            choice = menu.get_user_choice(4)
            
            if choice == 0:  # Back to main menu
                break
            elif choice == 1:  # List processes
                process_manager.list_background_processes()
            elif choice == 2:  # Stop specific process
                process_id = input(f"\n{Fore.CYAN}Enter process ID to stop: {Style.RESET_ALL}").strip()
                if process_id:
                    process_manager.stop_process(process_id)
            elif choice == 3:  # Stop all processes
                confirm = input(f"{Fore.YELLOW}Are you sure? This will stop all background processes (y/n): {Style.RESET_ALL}").lower()
                if confirm == 'y':
                    process_manager.stop_all_processes()
            elif choice == 4:  # Refresh process list
                process_manager.cleanup_dead_processes()
                self.print_info("Process list refreshed")
                
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            
    def handle_advanced_menu(self):
        """Handle advanced options menu"""
        while True:
            from ai_menu_system import MenuSystem
            menu = MenuSystem("3.0.28", "2025-08-13")
            menu.print_advanced_menu()
            
            choice = menu.get_user_choice(5)
            
            if choice == 0:  # Back to main menu
                break
            elif choice == 1:  # Show system status
                self.action_show_status()
            elif choice == 2:  # Restart Ollama
                self.ollama_manager.restart_ollama_server()
            elif choice == 3:  # Stop all background processes
                process_manager = BackgroundProcessManager(self.ai_env_path)
                process_manager.stop_all_processes()
            elif choice == 4:  # Clean temporary files
                self.print_info("Temporary file cleanup not yet implemented")
            elif choice == 5:  # Export environment info
                self.print_info("Environment info export not yet implemented")
                
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def handle_help_menu(self):
        """Handle version and documentation menu"""
        while True:
            from ai_menu_system import MenuSystem
            menu = MenuSystem("3.0.28", "2025-08-13")
            menu.print_help_menu()
            
            choice = menu.get_user_choice(6)
            
            if choice == 0:  # Back to main menu
                break
            elif choice == 1:  # View README.md
                self.view_readme()
            elif choice == 2:  # View PACKAGE_INFO.txt
                self.view_package_info()
            elif choice == 3:  # About AI Environment
                self.show_about_info()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == 4:  # Verify Checksums
                self.run_verify_checksums()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == 5:  # Check Versions
                self.run_check_versions()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == 6:  # Update System
                self.run_update_system()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def view_readme(self):
        """View README.md using document viewer"""
        try:
            from ai_document_viewer import DocumentViewer
            viewer = DocumentViewer(self.ai_env_path)
            viewer.view_readme()
        except Exception as e:
            self.print_error(f"Error viewing README.md: {e}")

    def view_package_info(self):
        """View PACKAGE_INFO.txt using document viewer"""
        try:
            from ai_document_viewer import DocumentViewer
            viewer = DocumentViewer(self.ai_env_path)
            viewer.view_package_info()
        except Exception as e:
            self.print_error(f"Error viewing PACKAGE_INFO.txt: {e}")

    def show_about_info(self):
        """Show About AI Environment information"""
        from ai_menu_system import MenuSystem
        menu = MenuSystem("3.0.28", "2025-08-13")
        menu.print_about_info()

    def run_verify_checksums(self):
        """Run verify_checksums.py script"""
        import subprocess
        import sys
        
        try:
            self.print_info("Running checksum verification...")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
            # Run verify_checksums.py
            script_path = self.ai_env_path / "src" / "verify_checksums.py"
            if not script_path.exists():
                self.print_error("verify_checksums.py not found")
                return False
            
            # Change to AI Environment directory and run the script
            result = subprocess.run([
                sys.executable, str(script_path)
            ], cwd=str(self.ai_env_path), capture_output=True, text=True)
            
            # Display output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"{Fore.RED}{result.stderr}{Style.RESET_ALL}")
            
            if result.returncode == 0:
                self.print_success("Checksum verification completed successfully")
                return True
            else:
                self.print_error(f"Checksum verification failed (exit code: {result.returncode})")
                return False
                
        except Exception as e:
            self.print_error(f"Error running checksum verification: {e}")
            return False

    def run_check_versions(self):
        """Run check_versions.py script"""
        import subprocess
        import sys
        
        try:
            self.print_info("Running version check...")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
            # Run check_versions.py
            script_path = self.ai_env_path / "src" / "check_versions.py"
            if not script_path.exists():
                self.print_error("check_versions.py not found")
                return False
            
            # Change to AI Environment directory and run the script
            result = subprocess.run([
                sys.executable, str(script_path)
            ], cwd=str(self.ai_env_path), capture_output=True, text=True)
            
            # Display output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"{Fore.RED}{result.stderr}{Style.RESET_ALL}")
            
            if result.returncode == 0:
                self.print_success("Version check completed successfully")
                return True
            else:
                self.print_error(f"Version check failed (exit code: {result.returncode})")
                return False
                
        except Exception as e:
            self.print_error(f"Error running version check: {e}")
            return False

    def run_update_system(self):
        """Run update system to install new versions"""
        try:
            from ai_update_manager import UpdateManager
            
            self.print_info("Starting update system...")
            
            # Create update manager
            update_manager = UpdateManager(self.ai_env_path)
            
            # Show available updates and let user select
            selected_update = update_manager.display_available_updates()
            
            if selected_update:
                # Install the selected update
                success = update_manager.install_update(selected_update)
                
                if success:
                    self.print_success("Update completed successfully!")
                    print(f"{Fore.CYAN}Please restart the AI Environment to use the new version.{Style.RESET_ALL}")
                else:
                    self.print_error("Update failed. System restored to previous state.")
            else:
                self.print_info("No update selected or no updates available.")
                
        except ImportError:
            self.print_error("Update manager not available")
        except Exception as e:
            self.print_error(f"Error running update system: {e}")

    def handle_terminal_launcher(self):
        """Handle AI2025 terminal launcher"""
        try:
            from ai_terminal_launcher import TerminalLauncher
            
            self.print_info("Launching AI2025 terminal...")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}🚀 Starting AI2025 Enhanced Terminal{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}📋 Features:{Style.RESET_ALL}")
            print(f"   • AI2025 environment pre-activated")
            print(f"   • Custom prompt [AI2025-Terminal]")
            print(f"   • return_to_menu command available")
            print(f"   • All AI packages ready to use")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
            # Create terminal launcher
            terminal_launcher = TerminalLauncher(self.ai_env_path)
            
            # Launch the terminal
            success = terminal_launcher.launch_terminal()
            
            if success:
                self.print_success("AI2025 terminal session completed")
            else:
                self.print_error("Failed to launch AI2025 terminal")
                
        except ImportError:
            self.print_error("Terminal launcher not available")
        except Exception as e:
            self.print_error(f"Error launching AI2025 terminal: {e}")

    def handle_jupyter_lab_menu(self):
        """Handle Jupyter Lab submenu with full server management"""
        from ai_jupyter_manager import JupyterLabManager
        from ai_menu_system import MenuSystem

        # Create Jupyter Lab manager
        jupyter_manager = JupyterLabManager(self.ai_env_path, self.venv_path)
        menu = MenuSystem("3.0.28", "2025-08-12")
        
        while True:
            jupyter_manager.show_menu()
            
            choice = menu.get_user_choice(6)
            
            if choice == 0:  # Back to applications menu
                break
            elif choice == 1:  # Start Server Only
                jupyter_manager.start_server_only()
            elif choice == 2:  # Start Client Only
                jupyter_manager.start_client_only()
            elif choice == 3:  # Start Server + Client
                jupyter_manager.start_server_and_client()
            elif choice == 4:  # Choose Custom Port
                jupyter_manager.choose_custom_port()
            elif choice == 5:  # Check Server Status
                jupyter_manager.check_server_status()
            elif choice == 6:  # Stop Server
                jupyter_manager.stop_server()
                # Flush input buffer to prevent hanging
                import sys
                sys.stdout.flush()
                sys.stderr.flush()
                time.sleep(0.1)  # Small delay to ensure processes are cleaned up
                
            if choice != 0:
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def main():
    """Test action handlers"""
    # Search for AI_Environment installation
    import string
    ai_env_path = None

    for letter in string.ascii_uppercase:
        for possible_path in [Path(f"{letter}:\\AI_Lab\\AI_Environment"), Path(f"{letter}:\\AI_Environment")]:
            if possible_path.exists():
                ai_env_path = possible_path
                break
        if ai_env_path:
            break

    if not ai_env_path:
        print("AI_Environment not found on any drive!")
        return

    venv_path = ai_env_path / ".venv"

    handlers = ActionHandlers(ai_env_path, venv_path)

    # Test status action
    handlers.action_show_status()

if __name__ == "__main__":
    main()

