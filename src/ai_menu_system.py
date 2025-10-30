# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30
"""

"""
AI Environment - Menu System Module
Interactive menu interfaces for AI Environment management
"""

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = WHITE = MAGENTA = ""
    class Style:
        RESET_ALL = ""

class MenuSystem:
    """Interactive menu system for AI Environment"""
    
    def __init__(self, script_version, script_date):
        self.script_version = script_version
        self.script_date = script_date
        
    def print_header(self):
        """Print application header"""
        print(f"\n{Fore.CYAN}{'='*64}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}                AI Environment Manager{Style.RESET_ALL}")
        print(f"{Fore.CYAN}               Version {self.script_version} ({self.script_date}){Style.RESET_ALL}")
        print(f"{Fore.CYAN}               Portable AI Development{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*64}{Style.RESET_ALL}")
        
    def print_interactive_menu(self):
        """Print main interactive menu with fixed colors for black terminal backgrounds"""
        print(f"\n{Fore.CYAN}📋 Available Actions:{Style.RESET_ALL}")
        print(f" 1. {Fore.GREEN}🚀 Full Activation{Style.RESET_ALL} (Complete Setup)")
        print(f" 2. {Fore.YELLOW}🧹 Restore Original PATH{Style.RESET_ALL}")
        print(f" 3. {Fore.WHITE}🐍 Activate Conda Environment Only{Style.RESET_ALL}")
        print(f" 4. {Fore.CYAN}🧪 Test All Components{Style.RESET_ALL}")
        print(f" 5. {Fore.GREEN}🌶️ Setup Flask{Style.RESET_ALL}")
        print(f" 6. {Fore.WHITE}🦙 Setup Ollama Server{Style.RESET_ALL}")
        print(f" 7. {Fore.MAGENTA}🔥 Download AI Models{Style.RESET_ALL}")
        print(f" 8. {Fore.GREEN}✅ Run Environment Validation{Style.RESET_ALL}")
        print(f" 9. {Fore.GREEN}🚀 Launch Applications{Style.RESET_ALL}")
        
        # Show background processes count
        try:
            from ai_process_manager import ProcessManager
            process_manager = ProcessManager()
            active_count = len(process_manager.get_active_processes())
            if active_count > 0:
                print(f"10. {Fore.YELLOW}🔄 Background Processes{Style.RESET_ALL} ({active_count})")
            else:
                print(f"10. {Fore.YELLOW}🔄 Background Processes{Style.RESET_ALL} (none)")
        except:
            print(f"10. {Fore.YELLOW}🔄 Background Processes{Style.RESET_ALL}")
            
        print(f"11. {Fore.CYAN}🔧 Advanced Options{Style.RESET_ALL}")
        print(f"12. {Fore.WHITE}💻 Open AI2025 Terminal{Style.RESET_ALL} (Enhanced terminal with return function)")
        print(f"13. {Fore.WHITE}📋 Version & Documentation{Style.RESET_ALL} (README, Package Info, About)")
        print(f"14. {Fore.YELLOW}🚪 Quit{Style.RESET_ALL} (Leave processes running)")
        print(f"15. {Fore.RED}🛑 Exit and Close All{Style.RESET_ALL} (Stop all background processes)")
        
    def print_advanced_menu(self):
        """Print advanced options menu with fixed colors"""
        print(f"\n{Fore.CYAN}🔧 Advanced Options:{Style.RESET_ALL}")
        print(f" 1. {Fore.YELLOW}📊 Show System Status{Style.RESET_ALL}")
        print(f" 2. {Fore.WHITE}🔄 Restart Ollama Server{Style.RESET_ALL}")
        print(f" 3. {Fore.RED}🛑 Stop All Background Processes{Style.RESET_ALL}")
        print(f" 4. {Fore.CYAN}🧹 Clean Temporary Files{Style.RESET_ALL}")
        print(f" 5. {Fore.GREEN}📋 Export Environment Info{Style.RESET_ALL}")
        print(f" 0. {Fore.YELLOW}⬅️ Back to Main Menu{Style.RESET_ALL}")
        
    def print_help_menu(self):
        """Print version and documentation menu"""
        print(f"\n{Fore.WHITE}📋 Version & Documentation:{Style.RESET_ALL}")
        print(f" 1. {Fore.GREEN}📖 View README.md{Style.RESET_ALL} (System documentation and features)")
        print(f" 2. {Fore.CYAN}📦 View PACKAGE_INFO.txt{Style.RESET_ALL} (Package contents and version info)")
        print(f" 3. {Fore.YELLOW}ℹ️ About AI Environment{Style.RESET_ALL} (Version, date, and system info)")
        print(f" 4. {Fore.WHITE}🔍 Verify Checksums{Style.RESET_ALL} (Check file integrity)")
        print(f" 5. {Fore.WHITE}📋 Check Versions{Style.RESET_ALL} (Verify component versions)")
        print(f" 6. {Fore.GREEN}🔄 Update System{Style.RESET_ALL} (Install updates from new_versions folder)")
        print(f" 0. {Fore.YELLOW}⬅️ Back to Main Menu{Style.RESET_ALL}")
        
    def print_about_info(self):
        """Print About AI Environment information"""
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}ℹ️ About AI Environment{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print()
        print(f"{Fore.WHITE}System Information:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Name:{Style.RESET_ALL} AI Environment Python System")
        print(f"  {Fore.GREEN}Version:{Style.RESET_ALL} {self.script_version}")
        print(f"  {Fore.GREEN}Release Date:{Style.RESET_ALL} {self.script_date}")
        print(f"  {Fore.GREEN}Current Time:{Style.RESET_ALL} {current_time}")
        print()
        print(f"{Fore.WHITE}Description:{Style.RESET_ALL}")
        print(f"  Complete AI development environment management system")
        print(f"  with interactive interface and advanced model management")
        print()
        print(f"{Fore.WHITE}Key Features:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Environment validation with install_config.json")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} AI2025 terminal launcher with return functionality")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Background process management")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Jupyter Lab integration")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Ollama server management")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} VS Code integration")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Comprehensive component testing")
        print()
        print(f"{Fore.WHITE}Components:{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}•{Style.RESET_ALL} Conda Environment (AI2025)")
        print(f"  {Fore.CYAN}•{Style.RESET_ALL} Python 3.10+ with AI packages")
        print(f"  {Fore.CYAN}•{Style.RESET_ALL} Ollama for local AI models")
        print(f"  {Fore.CYAN}•{Style.RESET_ALL} Jupyter Lab for development")
        print(f"  {Fore.CYAN}•{Style.RESET_ALL} VS Code integration")
        print(f"  {Fore.CYAN}•{Style.RESET_ALL} Model management system")
        print()
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
    def print_launch_menu(self):
        """Print application launcher menu with fixed colors"""
        print(f"\n{Fore.GREEN}🚀 Application Launcher:{Style.RESET_ALL}")
        print(f" 1. {Fore.WHITE}💻 VS Code{Style.RESET_ALL} (Full IDE)")
        print(f" 2. {Fore.YELLOW}📓 Jupyter Lab{Style.RESET_ALL} (Port 8888)")
        print(f" 3. {Fore.GREEN}🐍 Python REPL{Style.RESET_ALL} (Interactive)")
        print(f" 4. {Fore.CYAN}📦 Conda Prompt{Style.RESET_ALL} (Package Management)")
        print(f" 5. {Fore.RED}🌐 Streamlit Demo{Style.RESET_ALL} (Port 8501)")
        print(f" 6. {Fore.MAGENTA}📊 TensorBoard{Style.RESET_ALL} (Port 6006)")
        print(f" 7. {Fore.WHITE}🔬 MLflow UI{Style.RESET_ALL} (Port 5000)")
        print(f" 8. {Fore.YELLOW}📁 File Explorer{Style.RESET_ALL} (AI Environment)")
        print(f" 0. {Fore.YELLOW}⬅️ Back to Main Menu{Style.RESET_ALL}")
        
    def print_background_menu(self):
        """Print background processes menu with fixed colors"""
        print(f"\n{Fore.YELLOW}🔄 Background Process Management:{Style.RESET_ALL}")
        print(f" 1. {Fore.CYAN}📋 List All Processes{Style.RESET_ALL}")
        print(f" 2. {Fore.RED}🛑 Stop Specific Process{Style.RESET_ALL}")
        print(f" 3. {Fore.RED}⚠️ Stop All Background Processes{Style.RESET_ALL}")
        print(f" 4. {Fore.GREEN}🔄 Refresh Process List{Style.RESET_ALL}")
        print(f" 0. {Fore.YELLOW}⬅️ Back to Main Menu{Style.RESET_ALL}")
        
    def print_validation_menu(self):
        """Print environment validation menu"""
        print(f"\n{Fore.GREEN}✅ Environment Validation:{Style.RESET_ALL}")
        print(f" 1. {Fore.CYAN}🔍 Quick Package Check{Style.RESET_ALL}")
        print(f" 2. {Fore.YELLOW}📋 Full Validation Report{Style.RESET_ALL}")
        print(f" 3. {Fore.GREEN}📦 Install Missing Packages{Style.RESET_ALL}")
        print(f" 4. {Fore.WHITE}🔄 View Configuration{Style.RESET_ALL}")
        print(f" 0. {Fore.YELLOW}⬅️ Back to Main Menu{Style.RESET_ALL}")
        
    def get_user_choice(self, max_option):
        """Get user menu choice with validation"""
        while True:
            try:
                print(f"\n{Fore.WHITE}Enter your choice (0-{max_option}): {Style.RESET_ALL}", end="")
                choice = input().strip()
                
                if choice == "":
                    continue
                    
                choice_num = int(choice)
                if 0 <= choice_num <= max_option:
                    return choice_num
                else:
                    print(f"{Fore.RED}❌ Invalid choice. Please enter a number between 0 and {max_option}.{Style.RESET_ALL}")
                    
            except ValueError:
                print(f"{Fore.RED}❌ Invalid input. Please enter a number.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}⚠️ Operation cancelled by user.{Style.RESET_ALL}")
                return 0
                
    def print_exit_options_explanation(self):
        """Explain the difference between exit options"""
        print(f"\n{Fore.CYAN}ℹ️ Exit Options Explained:{Style.RESET_ALL}")
        print(f"   {Fore.YELLOW}🚪 Quit (13):{Style.RESET_ALL} Exits menu but leaves background processes running")
        print(f"      - Ollama server stays active")
        print(f"      - Jupyter Lab stays active") 
        print(f"      - VS Code instances stay open")
        print(f"      - You can return later and processes will still be running")
        print()
        print(f"   {Fore.RED}🛑 Exit and Close All (14):{Style.RESET_ALL} Stops all processes and exits")
        print(f"      - Stops Ollama server")
        print(f"      - Stops Jupyter Lab")
        print(f"      - Closes VS Code instances")
        print(f"      - Clean shutdown of all AI Environment processes")
        print()
        
    def print_terminal_info(self):
        """Print information about the AI2025 terminal option"""
        print(f"\n{Fore.CYAN}💻 AI2025 Terminal Features:{Style.RESET_ALL}")
        print(f"   {Fore.GREEN}✓{Style.RESET_ALL} AI2025 conda environment pre-activated")
        print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Custom prompt: [AI2025-Terminal]")
        print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Enhanced commands available:")
        print(f"     - {Fore.WHITE}return_to_menu{Style.RESET_ALL} : Return to this main menu")
        print(f"     - {Fore.WHITE}python{Style.RESET_ALL} : Python with AI packages")
        print(f"     - {Fore.WHITE}jupyter lab{Style.RESET_ALL} : Launch Jupyter Lab")
        print(f"     - {Fore.WHITE}code .{Style.RESET_ALL} : Open VS Code")
        print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Working directory: AI Environment root")
        print()
        
    def confirm_action(self, action_description):
        """Get user confirmation for important actions"""
        print(f"\n{Fore.YELLOW}⚠️ Confirm Action:{Style.RESET_ALL}")
        print(f"   {action_description}")
        print(f"\n{Fore.WHITE}Are you sure? (y/N): {Style.RESET_ALL}", end="")
        
        try:
            response = input().strip().lower()
            return response in ["y", "yes"]
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️ Action cancelled by user.{Style.RESET_ALL}")
            return False
			