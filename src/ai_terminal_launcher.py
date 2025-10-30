#!/usr/bin/env python3
"""
AI Terminal Launcher (macOS Version)
Launches AI2025 terminal with unique prompt and return functionality

Version: 3.0.28
Author: AI Environment Team
Date: 2025-08-13
Time: 12:45
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    class Fore:
        GREEN = YELLOW = CYAN = WHITE = RED = MAGENTA = ""
    class Style:
        RESET_ALL = ""
    COLORAMA_AVAILABLE = False

class TerminalLauncher:
    """Launches AI2025 terminal with enhanced functionality on macOS"""

    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)

        # Find conda installation - check multiple locations for macOS
        conda_locations = [
            self.ai_env_path / "Miniconda",
            Path.home() / "miniconda3",
            Path.home() / "anaconda3",
            Path("/opt/miniconda3"),
            Path("/opt/anaconda3"),
        ]

        self.conda_path = None
        for location in conda_locations:
            if (location / "bin" / "activate").exists():
                self.conda_path = location
                break

        if not self.conda_path:
            # Fallback to first location (will show error later)
            self.conda_path = self.ai_env_path / "Miniconda"

        self.activate_script = self.conda_path / "bin" / "activate"

    def create_terminal_script(self):
        """Create enhanced terminal script with return functionality for macOS"""
        script_content = f'''#!/bin/bash

# AI Environment Terminal Launcher v3.0.20
# Enhanced terminal with return functionality (macOS)

export AI_ENV_PATH="{self.ai_env_path}"
export CONDA_PATH="{self.conda_path}"

# Set terminal title
echo -ne "\\033]0;AI Environment Terminal (AI2025 Active)\\007"

# Display welcome banner
echo ""
echo "{Fore.CYAN}================================================================"
echo "                   AI Environment Terminal"
echo "                    AI2025 Environment Active"
echo "                      Version 3.0.28"
echo "================================================================{Style.RESET_ALL}"
echo ""
echo "{Fore.GREEN}✅ AI2025 conda environment is now active{Style.RESET_ALL}"
echo "{Fore.YELLOW}📁 Working directory: $AI_ENV_PATH{Style.RESET_ALL}"
echo "{Fore.CYAN}🐍 Python environment: AI2025{Style.RESET_ALL}"
echo ""
echo "{Fore.WHITE}Available commands:{Style.RESET_ALL}"
echo "   {Fore.GREEN}python{Style.RESET_ALL}          - Run Python in AI2025 environment"
echo "   {Fore.GREEN}pip{Style.RESET_ALL}             - Install packages in AI2025 environment"
echo "   {Fore.GREEN}jupyter lab{Style.RESET_ALL}     - Launch Jupyter Lab"
echo "   {Fore.GREEN}code .{Style.RESET_ALL}          - Open VS Code in current directory"
echo "   {Fore.GREEN}return_to_menu{Style.RESET_ALL}  - Return to AI Environment main menu"
echo "   {Fore.GREEN}exit{Style.RESET_ALL}            - Close this terminal"
echo ""

# Source conda
source "$CONDA_PATH/bin/activate" AI2025

# Set custom prompt
export PS1="[AI2025-Terminal] \\W $ "

# Create return_to_menu command
cat > /tmp/return_to_menu.sh << 'EOF'
#!/bin/bash
echo ""
echo "{Fore.CYAN}🔄 Returning to AI Environment main menu...{Style.RESET_ALL}"
echo ""
cd "$AI_ENV_PATH"
python activate_ai_env.py
EOF

chmod +x /tmp/return_to_menu.sh

# Create alias for return_to_menu
alias return_to_menu='/tmp/return_to_menu.sh'

# Change to AI Environment directory
cd "$AI_ENV_PATH"

# Start interactive bash shell
exec bash --noprofile --norc
'''

        # Write script to temporary file
        script_path = Path(tempfile.mktemp(suffix=".sh"))
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

        # Make script executable
        os.chmod(script_path, 0o755)

        return script_path

    def launch_terminal(self):
        """Launch enhanced AI2025 terminal on macOS"""
        try:
            # Verify conda was found
            if not self.activate_script.exists():
                print(f"{Fore.RED}[ERROR] Conda activation script not found!")
                print(f"{Fore.YELLOW}[INFO] Searched locations:")
                conda_locations = [
                    self.ai_env_path / "Miniconda",
                    Path.home() / "miniconda3",
                    Path.home() / "anaconda3",
                    Path("/opt/miniconda3"),
                    Path("/opt/anaconda3"),
                ]
                for loc in conda_locations:
                    print(f"{Fore.YELLOW}  - {loc / 'bin' / 'activate'}")
                return False

            print(f"{Fore.CYAN}🚀 Launching AI2025 Terminal...")
            print(f"{Fore.YELLOW}   - Custom prompt: [AI2025-Terminal]")
            print(f"{Fore.YELLOW}   - Return command: return_to_menu")
            print(f"{Fore.YELLOW}   - Working directory: {self.ai_env_path}")
            print(f"{Fore.GREEN}   - Conda found at: {self.conda_path}")

            # Create terminal script
            script_path = self.create_terminal_script()

            # Launch Terminal.app with the script using osascript
            # This opens a new Terminal window and runs the script
            osascript_command = f'''
tell application "Terminal"
    do script "bash '{script_path}'"
    activate
end tell
'''

            subprocess.run(
                ['osascript', '-e', osascript_command],
                check=False
            )

            # Note: We don't clean up the script immediately because Terminal needs it
            # The script will be cleaned up on next system temp cleanup

            return True

        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to launch terminal: {e}")
            return False

    def create_python_return_function(self):
        """Create Python function for returning to menu from Python scripts"""
        return_function = '''
def return_to_menu():
    """Return to AI Environment main menu from Python"""
    import os
    import subprocess

    print("\\n🔄 Returning to AI Environment main menu...")
    ai_env_path = os.environ.get('AI_ENV_PATH', '.')
    subprocess.run(['python', os.path.join(ai_env_path, 'activate_ai_env.py')])

# Auto-import return function
print("📋 AI Environment functions loaded:")
print("   - return_to_menu() : Return to main menu")
'''

        # Create startup script for Python
        startup_path = self.ai_env_path / "ai_python_startup.py"
        with open(startup_path, 'w', encoding='utf-8') as f:
            f.write(return_function)

        return startup_path

def main():
    """Main function for standalone execution"""
    import argparse

    parser = argparse.ArgumentParser(description='AI Terminal Launcher')
    parser.add_argument('--ai-env-path', default='.',
                       help='Path to AI Environment directory')

    args = parser.parse_args()

    launcher = TerminalLauncher(args.ai_env_path)
    success = launcher.launch_terminal()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
