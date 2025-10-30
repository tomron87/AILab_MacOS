# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.0
Date: 2025-08-12
"""

#!/usr/bin/env python3
"""
AI Environment - PATH Management Module
Handles Windows PATH variable cleanup and restoration
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

class PathManager:
    """Manages Windows PATH variable for AI Environment"""

    def __init__(self, ai_env_path=None):
        """Initialize PATH manager

        Args:
            ai_env_path (str): Path to AI Environment installation (optional)
        """
        self.ai_env_path = Path(ai_env_path).resolve() if ai_env_path else None
        self.essential_paths = [
            "C:\\Windows\\System32",
            "C:\\Windows",
            "C:\\Windows\\System32\\Wbem",
            "C:\\Windows\\System32\\WindowsPowerShell\\v1.0",
            "C:\\Windows\\System32\\OpenSSH",
            "C:\\Program Files\\Common Files\\Microsoft Shared\\Windows Live",
            "C:\\Program Files (x86)\\Common Files\\Microsoft Shared\\Windows Live"
        ]
        
    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")
        
    def print_removed(self, path):
        """Print removed path message"""
        print(f"{Fore.RED}[REMOVED] {path}{Style.RESET_ALL}")
        
    def get_current_path(self):
        """Get current PATH environment variable"""
        return os.environ.get('PATH', '')
        
    def is_ai_environment_path(self, path):
        """Check if path is related to AI Environment"""
        path_upper = path.upper()

        # If we have the actual AI environment path, check against it
        if self.ai_env_path:
            ai_env_str = str(self.ai_env_path).upper()
            if ai_env_str in path_upper:
                return True

        # Check for common AI Environment related patterns
        ai_patterns = [
            "MINICONDA",
            "ANACONDA",
            "OLLAMA",
            "\\AI_ENVIRONMENT",
            "\\AI2025"
        ]

        # Check if path contains any AI-related patterns
        for pattern in ai_patterns:
            if pattern in path_upper:
                # Additional check: verify it's not a system-wide installation
                # Allow system-wide installations in C:\ProgramData or user profile
                if "C:\\PROGRAMDATA" in path_upper or "C:\\USERS" in path_upper:
                    continue
                return True

        return False
        
    def filter_clean_paths(self, current_path):
        """Filter out AI Environment paths, keep essential Windows paths"""
        path_entries = current_path.split(';')
        clean_paths = []
        
        # Start with essential Windows paths
        clean_paths.extend(self.essential_paths)
        
        # Add other system paths (excluding AI Environment paths)
        for path in path_entries:
            path = path.strip()
            if path and not self.is_ai_environment_path(path):
                # Skip if already in essential paths
                if path not in self.essential_paths:
                    clean_paths.append(path)
            elif path and self.is_ai_environment_path(path):
                self.print_removed(path)
                
        return clean_paths
        
    def test_basic_commands(self):
        """Test if basic Windows commands work"""
        commands = ['which', 'dir', 'tasklist']
        results = {}
        
        for cmd in commands:
            try:
                if cmd == 'which':
                    # Test which command with a known Windows executable
                    result = subprocess.run([cmd, 'cmd'], 
                                          capture_output=True, 
                                          timeout=5)
                elif cmd == 'dir':
                    # Test dir command on Windows directory
                    result = subprocess.run([cmd, 'C:\\Windows'], 
                                          capture_output=True, 
                                          timeout=5, shell=True)
                elif cmd == 'tasklist':
                    # Test tasklist command
                    result = subprocess.run([cmd], 
                                          capture_output=True, 
                                          timeout=5)
                else:
                    result = subprocess.run([cmd], 
                                          capture_output=True, 
                                          timeout=5)
                results[cmd] = result.returncode == 0
            except:
                results[cmd] = False
                
        return results
        
    def deactivate_conda_environment(self):
        """Deactivate any active conda environment"""
        conda_env = os.environ.get('CONDA_DEFAULT_ENV', '')
        
        if conda_env:
            self.print_info(f"Deactivating conda environment: {conda_env}")
            try:
                subprocess.run(['conda', 'deactivate'], 
                             capture_output=True, 
                             timeout=10)
                self.print_success("Conda environment deactivated")
            except:
                self.print_info("Could not deactivate conda environment")
                
        # Clear conda environment variables
        conda_vars = ['CONDA_DEFAULT_ENV', 'CONDA_PREFIX', 'CONDA_PROMPT_MODIFIER']
        for var in conda_vars:
            if var in os.environ:
                del os.environ[var]
                
    def restore_original_path(self):
        """Restore original Windows PATH without AI Environment entries"""
        try:
            if self.ai_env_path:
                self.print_info(f"Cleaning AI Environment paths from: {self.ai_env_path}")
            else:
                self.print_info("Cleaning AI Environment related paths from PATH...")

            # Get current PATH
            current_path = self.get_current_path()

            # Count paths before filtering
            original_count = len([p for p in current_path.split(';') if p.strip()])

            # Filter out AI Environment paths
            clean_paths = self.filter_clean_paths(current_path)

            # Count how many were removed
            removed_count = original_count - len(clean_paths)

            # Set cleaned PATH
            new_path = ';'.join(clean_paths)
            os.environ['PATH'] = new_path

            self.print_success("Original Windows PATH restored")
            if removed_count > 0:
                self.print_info(f"Removed {removed_count} AI Environment path(s)")
            else:
                self.print_info("No AI Environment paths found in PATH")
            
            # Test basic Windows commands
            self.print_info("Testing basic Windows commands...")
            test_results = self.test_basic_commands()
            
            for cmd, success in test_results.items():
                if success:
                    self.print_success(f"'{cmd}' command working")
                else:
                    print(f"{Fore.RED}[ERROR] '{cmd}' command not working{Style.RESET_ALL}")
                    
            # Deactivate conda environment
            self.deactivate_conda_environment()
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to restore PATH: {e}{Style.RESET_ALL}")
            return False

def main():
    """Test PATH manager"""
    path_manager = PathManager()
    success = path_manager.restore_original_path()
    
    if success:
        print(f"\n{Fore.GREEN}PATH restoration completed successfully{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}PATH restoration failed{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

