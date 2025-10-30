#!/usr/bin/env python3
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30

AI Environment - Launcher Menu System
Handles display and interaction for application launcher menu
"""

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = ""
    class Style:
        RESET_ALL = ""

class LauncherMenu:
    """Handles application launcher menu display and formatting"""
    
    def __init__(self):
        pass
        
    def show_launch_menu(self):
        """Show application launch menu"""
        print(f"\n{Fore.MAGENTA}🚀 Application Launcher:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW} 1.{Style.RESET_ALL} 💻 VS Code (Enhanced AI Environment Integration)")
        print(f"{Fore.YELLOW} 2.{Style.RESET_ALL} 📊 Jupyter Lab")
        print(f"{Fore.YELLOW} 3.{Style.RESET_ALL} 🌟 Streamlit Demo")
        print(f"{Fore.YELLOW} 4.{Style.RESET_ALL} 🐍 Python REPL")
        print(f"{Fore.YELLOW} 5.{Style.RESET_ALL} 🔧 Conda Prompt")
        print(f"{Fore.YELLOW} 6.{Style.RESET_ALL} 📁 File Explorer")
        print(f"{Fore.YELLOW} 7.{Style.RESET_ALL} 📈 TensorBoard")
        print(f"{Fore.YELLOW} 8.{Style.RESET_ALL} 🔬 MLflow UI")
        print(f"{Fore.YELLOW} 0.{Style.RESET_ALL} ⬅️ Back")
        print()
        
    def show_app_descriptions(self):
        """Show detailed descriptions of each application"""
        print(f"\n{Fore.CYAN}📋 Application Descriptions:{Style.RESET_ALL}")
        print()
        
        descriptions = [
            ("💻 VS Code", "Enhanced integrated development environment with full AI Environment integration"),
            ("📊 Jupyter Lab", "Interactive notebook environment for data science and machine learning"),
            ("🌟 Streamlit", "Web application framework for creating data apps with Python"),
            ("🐍 Python REPL", "Interactive Python interpreter in a new terminal window"),
            ("🔧 Conda Prompt", "Conda environment management terminal with AI2025 environment active"),
            ("📁 File Explorer", "Windows file open opened to AI Environment directory"),
            ("📈 TensorBoard", "Visualization toolkit for TensorFlow and machine learning metrics"),
            ("🔬 MLflow UI", "Machine learning lifecycle management and experiment tracking interface")
        ]
        
        for app, desc in descriptions:
            print(f"{Fore.YELLOW}{app}:{Style.RESET_ALL}")
            print(f"  {desc}")
            print()
            
    def show_vscode_features(self):
        """Show VS Code specific features and integration details"""
        print(f"\n{Fore.GREEN}🎯 VS Code AI Environment Integration Features:{Style.RESET_ALL}")
        print()
        
        features = [
            "✓ AI2025 Python interpreter auto-detection",
            "✓ [AI2025-Terminal] terminal profile matching Option 12",
            "✓ Enhanced workspace configuration with AI Environment paths",
            "✓ Debug configurations for AI Environment system components",
            "✓ Task definitions for running AI Environment commands",
            "✓ Auto-generated main.py with integration examples",
            "✓ Environment variables aligned with AI Environment v3.0.26",
            "✓ Background process tracking integration",
            "✓ Direct access to activate_ai_env.py from VS Code",
            "✓ Recommended extensions for Python development",
            "✓ Jupyter notebook support with AI2025 kernel",
            "✓ Git integration and code formatting setup"
        ]
        
        for feature in features:
            print(f"  {feature}")
        print()
        
        print(f"{Fore.CYAN}🎮 Quick Actions in VS Code:{Style.RESET_ALL}")
        actions = [
            ("Ctrl+`", "Open [AI2025-Terminal] (matches your Option 12)"),
            ("F5", "Debug current file with AI2025 interpreter"),
            ("Ctrl+Shift+P → Tasks", "Access 'AI Environment: Open Main Menu'"),
            ("Ctrl+Shift+P → Python", "Select AI2025 interpreter"),
            ("Terminal command", "python activate_ai_env.py (access main menu)")
        ]
        
        for shortcut, description in actions:
            print(f"  {Fore.YELLOW}{shortcut}:{Style.RESET_ALL} {description}")
        print()

    def show_quick_help(self):
        """Show quick help for application launcher"""
        print(f"\n{Fore.CYAN}💡 Quick Help - Application Launcher:{Style.RESET_ALL}")
        print()
        
        help_items = [
            ("🚀 Getting Started", "Select option 1 to launch VS Code with full AI Environment integration"),
            ("📊 Data Science", "Use Jupyter Lab (option 2) for interactive notebooks and data analysis"),
            ("🌐 Web Apps", "Streamlit (option 3) for creating interactive web applications"),
            ("💻 Development", "Python REPL (option 4) for quick Python experimentation"),
            ("🔧 Environment", "Conda Prompt (option 5) for package management and environment control"),
            ("📁 File Management", "File Explorer (option 6) for browsing AI Environment files"),
            ("📈 ML Monitoring", "TensorBoard (option 7) for visualizing machine learning metrics"),
            ("🔬 Experiment Tracking", "MLflow UI (option 8) for managing ML experiments and models")
        ]
        
        for title, description in help_items:
            print(f"{Fore.GREEN}{title}:{Style.RESET_ALL}")
            print(f"  {description}")
            print()

    def show_troubleshooting(self):
        """Show troubleshooting information"""
        print(f"\n{Fore.YELLOW}🔧 Troubleshooting - Application Launcher:{Style.RESET_ALL}")
        print()
        
        issues = [
            ("VS Code not found", [
                "Install VS Code from https://code.visualstudio.com/",
                "Check VS Code installation paths in ai_app_launcher.py",
                "Consider using portable VS Code in AI Environment directory"
            ]),
            ("Python interpreter issues", [
                "Verify AI2025 conda environment is activated",
                "Check Miniconda installation in AI Environment",
                "Run conda info --envs to list available environments"
            ]),
            ("Application won't launch", [
                "Check background processes (Option 10 in main menu)",
                "Verify port availability (8888 for Jupyter, 8501 for Streamlit)",
                "Restart AI Environment system if needed"
            ]),
            ("Browser not opening", [
                "Manually navigate to the provided URL",
                "Check firewall settings for Python applications",
                "Wait a few seconds for the server to fully start"
            ])
        ]
        
        for issue, solutions in issues:
            print(f"{Fore.RED}❌ {issue}:{Style.RESET_ALL}")
            for solution in solutions:
                print(f"  • {solution}")
            print()

def main():
    """Test launcher menu display"""
    menu = LauncherMenu()
    print("Testing Launcher Menu System...")
    menu.show_launch_menu()
    menu.show_app_descriptions()
    menu.show_vscode_features()
    menu.show_quick_help()
    menu.show_troubleshooting()

if __name__ == "__main__":
    main()
	
	