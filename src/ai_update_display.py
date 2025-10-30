# AI Environment Module v3.0.28
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30
"""

import os
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

class UpdateDisplay:
    """Handles displaying update information and user interaction for selection"""

    def __init__(self, new_versions_path):
        self.new_versions_path = Path(new_versions_path)

    def display_available_updates(self, zip_files):
        """Display available updates and allow selection"""
        if not zip_files:
            print(f"{Fore.YELLOW}No ZIP files found in new_versions folder.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}To add updates:{Style.RESET_ALL}")
            print(f"  1. Copy ZIP files to: {self.new_versions_path}")
            print(f"  2. Return to this menu to install them")
            return None
        
        print(f"\n{Fore.CYAN}📦 Available Updates:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{\"="*60}{Style.RESET_ALL}")
        
        for i, zip_info in enumerate(zip_files, 1):
            size_mb = zip_info["size"] / (1024 * 1024)
            version_str = f" (v{zip_info[\"version\"]})" if zip_info["version"] else ""
            print(f"{i:2d}. {Fore.WHITE}{zip_info[\"name\"]}{version_str}{Style.RESET_ALL}")
            print(f"     Size: {size_mb:.1f} MB")
            print()
        
        print(f" 0. {Fore.YELLOW}Cancel and return to Version menu{Style.RESET_ALL}")
        print()
        
        try:
            choice = input(f"{Fore.WHITE}Select update to install (0-{len(zip_files)}): {Style.RESET_ALL}").strip()
            
            if choice == "0":
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(zip_files):
                return zip_files[choice_num - 1]
            else:
                print(f"{Fore.RED}Invalid choice. Please select 0-{len(zip_files)}.{Style.RESET_ALL}")
                return None
                
        except (ValueError, KeyboardInterrupt):
            print(f"{Fore.YELLOW}Update cancelled.{Style.RESET_ALL}")
            return None

    def show_update_info(self, zip_files):
        """Show information about the update system"""
        print(f"\n{Fore.CYAN}🔄 AI Environment Update System{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{\"="*60}{Style.RESET_ALL}")
        print()
        print(f"{Fore.WHITE}How to use:{Style.RESET_ALL}")
        print(f"  1. Copy new AI Environment ZIP files to:")
        print(f"     {Fore.CYAN}{self.new_versions_path}{Style.RESET_ALL}")
        print(f"  2. Select this Update option")
        print(f"  3. Choose which ZIP file to install")
        print(f"  4. Confirm installation")
        print()
        print(f"{Fore.WHITE}Safety features:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Automatic backup before update")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Rollback on failure")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Version detection from filenames")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Confirmation before installation")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Safe update for run_ai_env.bat (requires restart){Style.RESET_ALL}")
        print()
        print(f"{Fore.WHITE}Update folder:{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}{self.new_versions_path}{Style.RESET_ALL}")
        
        # Show current contents
        if zip_files:
            print(f"\n{Fore.WHITE}Currently available updates: {len(zip_files)}{Style.RESET_ALL}")
            for zip_info in zip_files:
                version_str = f" (v{zip_info[\"version\"]})" if zip_info["version"] else ""
                print(f"  • {zip_info[\"name\"]}{version_str}")
        else:
            print(f"\n{Fore.YELLOW}No update files found in new_versions folder{Style.RESET_ALL}")




