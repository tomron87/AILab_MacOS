# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30
"""

"""
AI Environment - Update Manager Module
Handles system updates from ZIP files in new_versions folder
"""

import os
import sys
import shutil
from pathlib import Path
import time

# Import utility functions
from src.ai_update_utils import (
    extract_version_from_filename,
    create_backup,
    extract_and_install,
    restore_backup,
    cleanup_backup,
    update_version_config
)
from src.ai_update_display import UpdateDisplay

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

class UpdateManager:
    """Manages system updates from ZIP files"""
    
    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)
        self.new_versions_path = self.ai_env_path / "new_versions"
        self.backup_path = self.ai_env_path / "backup"
        self.temp_update_script = self.ai_env_path / "temp_update_script.bat"
        self.display = UpdateDisplay(self.new_versions_path)
        
        # Ensure directories exist
        self.new_versions_path.mkdir(exist_ok=True)
        
    def scan_for_updates(self):
        """Scan new_versions folder for ZIP files"""
        try:
            if not self.new_versions_path.exists():
                return []
            
            zip_files = []
            for file_path in self.new_versions_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() == ".zip":
                    # Extract version info from filename if possible
                    filename = file_path.name
                    version = extract_version_from_filename(filename)
                    
                    zip_files.append({
                        "path": file_path,
                        "name": filename,
                        "version": version,
                        "size": file_path.stat().st_size
                    })
            
            # Sort by version if available, otherwise by name
            zip_files.sort(key=lambda x: (x["version"] or "", x["name"]))
            return zip_files
            
        except Exception as e:
            print(f"{Fore.RED}Error scanning for updates: {e}{Style.RESET_ALL}")
            return []
    
    def display_available_updates(self):
        """Display available updates and allow selection"""
        zip_files = self.scan_for_updates()
        return self.display.display_available_updates(zip_files)
    
    def install_update(self, zip_info):
        """Install selected update"""
        try:
            print(f"\n{Fore.CYAN}🔄 Installing Update: {zip_info["name"]}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{"="*60}{Style.RESET_ALL}")
            
            # Confirm installation
            print(f"{Fore.YELLOW}⚠️  This will update your AI Environment system.{Style.RESET_ALL}")
            print(f"Current location: {self.ai_env_path}")
            print(f"Update file: {zip_info["name"]}")
            if zip_info["version"]:
                print(f"Version: {zip_info["version"]}")
            print()
            
            confirm = input(f"{Fore.WHITE}Continue with installation? (y/N): {Style.RESET_ALL}").strip().lower()
            if confirm not in ["y", "yes"]:
                print(f"{Fore.YELLOW}Update cancelled by user.{Style.RESET_ALL}")
                return False
            
            # Create backup
            if not create_backup(self.ai_env_path, self.backup_path):
                print(f"{Fore.RED}Failed to create backup. Update cancelled.{Style.RESET_ALL}")
                return False
            
            # Extract and install
            if not extract_and_install(self.ai_env_path, zip_info):
                print(f"{Fore.RED}Update installation failed.{Style.RESET_ALL}")
                restore_backup(self.ai_env_path, self.backup_path)
                return False
            
            # Handle run_ai_env.bat update if needed
            self._handle_batch_file_update()
            
            print(f"\n{Fore.GREEN}✅ Update installed successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Changes will take effect on next restart.{Style.RESET_ALL}")
            
            # Clean up
            cleanup_backup(self.backup_path)
            
            # Update version_config.json
            update_version_config(self.ai_env_path, zip_info["version"])
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error during update installation: {e}{Style.RESET_ALL}")
            restore_backup(self.ai_env_path, self.backup_path)
            return False
    
    def _handle_batch_file_update(self):
        """Handle updating batch files while system is running"""
        try:
            print(f"{Fore.CYAN}🔄 Checking batch file updates...{Style.RESET_ALL}")
            
            new_run_ai_env = self.ai_env_path / "run_ai_env.bat.new"
            if new_run_ai_env.exists():
                print(f"{Fore.YELLOW}ℹ️  New run_ai_env.bat detected. Scheduling update...{Style.RESET_ALL}")
                
                # Create a temporary batch script to replace run_ai_env.bat after exit
                script_content = f"""
@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:WAIT_FOR_PROCESS
TASKLIST /FI "IMAGENAME eq bash" /FI "WINDOWTITLE eq AI_Environment" | FINDSTR /I "bash" >NUL
IF %ERRORLEVEL% EQU 0 (
    ECHO Waiting for AI_Environment to close...
    TIMEOUT /T 1 /NOBREAK >NUL
    GOTO :WAIT_FOR_PROCESS
)

ECHO AI_Environment closed. Proceeding with update...

REM Delete old run_ai_env.bat
IF EXIST "{self.ai_env_path / 'run_ai_env.bat'}" (
    DEL "{self.ai_env_path / 'run_ai_env.bat'}"
)

REM Rename new run_ai_env.bat
IF EXIST "{new_run_ai_env}" (
    REN "{new_run_ai_env}" "run_ai_env.bat"
)

ECHO Update complete. You can now restart AI_Environment.
DEL "%~f0"
"""
                
                with open(self.temp_update_script, "w") as f:
                    f.write(script_content)
                
                print(f"{Fore.GREEN}✅ Update script created: {self.temp_update_script}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Please close the current AI Environment window to complete the update.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}The system will automatically apply the new run_ai_env.bat on exit.{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}No run_ai_env.bat update needed.{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not handle batch file updates: {e}{Style.RESET_ALL}")
    
    def show_update_info(self):
        """Show information about the update system"""
        zip_files = self.scan_for_updates()
        self.display.show_update_info(zip_files)

def main():
    """Main function for standalone execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Environment Update Manager")
    parser.add_argument("--ai-env-path", default=".", 
                       help="Path to AI Environment directory")
    parser.add_argument("--scan", action="store_true",
                       help="Scan for available updates")
    parser.add_argument("--info", action="store_true",
                       help="Show update system information")
    
    args = parser.parse_args()
    
    manager = UpdateManager(args.ai_env_path)
    
    if args.scan:
        zip_files = manager.scan_for_updates()
        print(f"Found {len(zip_files)} update files")
        for zip_info in zip_files:
            print(f"  {zip_info["name"]}")
    elif args.info:
        manager.show_update_info()
    else:
        # Interactive mode
        selected = manager.display_available_updates()
        if selected:
            manager.install_update(selected)

if __name__ == "__main__":
    main()


