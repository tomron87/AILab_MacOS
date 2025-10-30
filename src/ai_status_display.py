# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.0
Date: 2025-08-12
"""

#!/usr/bin/env python3
"""
AI Environment - Status Display Module
Handles status reporting and completion messages
"""

import os
from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = ""
    class Style:
        RESET_ALL = ""

class StatusDisplay:
    """Displays AI Environment status and completion information"""
    
    def __init__(self):
        # Get the script's directory (src/) and go up one level to AI_Environment root
        script_dir = Path(__file__).resolve().parent
        self.ai_env_path = script_dir.parent
        
    def show_completion_status(self):
        """Show environment completion status"""
        print(f"\n{Fore.GREEN}🎉 AI Environment is Ready!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}📍 Environment Location:{Style.RESET_ALL}")
        print(f"   {self.ai_env_path}")
        
        print(f"\n{Fore.CYAN}🐍 Python Environment:{Style.RESET_ALL}")
        conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not activated')
        print(f"   Environment: {conda_env}")
        
        print(f"\n{Fore.CYAN}🚀 Available Commands:{Style.RESET_ALL}")
        print(f"   {Fore.YELLOW}python{Style.RESET_ALL}           - Start Python interpreter")
        print(f"   {Fore.YELLOW}pip install <pkg>{Style.RESET_ALL} - Install Python packages")
        print(f"   {Fore.YELLOW}conda list{Style.RESET_ALL}       - Show installed packages")
        print(f"   {Fore.YELLOW}jupyter lab{Style.RESET_ALL}      - Start Jupyter Lab")
        print(f"   {Fore.YELLOW}code .{Style.RESET_ALL}           - Open VS Code")
        print(f"   {Fore.YELLOW}ollama list{Style.RESET_ALL}      - Show AI models")
        print(f"   {Fore.YELLOW}ollama run <model>{Style.RESET_ALL} - Chat with AI model")
        
        print(f"\n{Fore.CYAN}🔧 Management:{Style.RESET_ALL}")
        print(f"   Use Advanced Options (option 10) for detailed control")
        print(f"   Start/Stop/Restart Ollama server")
        print(f"   Monitor system status and processes")

def main():
    """Test status display"""
    status_display = StatusDisplay()
    status_display.show_completion_status()

if __name__ == "__main__":
    main()

