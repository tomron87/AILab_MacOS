# AI Environment Module v3.0.28
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30
"""

import os
import sys
import zipfile
import shutil
import subprocess
from pathlib import Path
import tempfile
import time
import json
import re

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

def extract_version_from_filename(filename):
    """Extract version number from filename"""
    version_patterns = [
        r"v(\d+\.\d+\.\d+)",
        r"_v(\d+\.\d+\.\d+)",
        r"(\d+\.\d+\.\d+)"
    ]
    
    for pattern in version_patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def create_backup(ai_env_path, backup_path):
    """Create backup of current system"""
    try:
        print(f"{Fore.CYAN}📋 Creating backup...{Style.RESET_ALL}")
        
        # Remove old backup if exists
        if backup_path.exists():
            shutil.rmtree(backup_path)
        
        backup_path.mkdir(exist_ok=True)
        
        # Backup critical files
        critical_files = [
            "src/",
            "config/",
            "version_config.json",
            "run_ai_env.bat",
            "setup_python_env.bat",
            "check_versions.bat",
            "README.md",
            "PACKAGE_INFO.txt",
            "CHECKSUMS.sha256"
        ]
        
        for item in critical_files:
            source = ai_env_path / item
            if source.exists():
                dest = backup_path / item
                if source.is_dir():
                    shutil.copytree(source, dest)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)
        
        print(f"{Fore.GREEN}✅ Backup created successfully{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}Failed to create backup: {e}{Style.RESET_ALL}")
        return False

def extract_and_install(ai_env_path, zip_info):
    """Extract ZIP and install files"""
    try:
        print(f"{Fore.CYAN}📦 Extracting update...{Style.RESET_ALL}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Extract ZIP to temporary directory
            with zipfile.ZipFile(zip_info["path"], "r") as zip_ref:
                zip_ref.extractall(temp_path)
            
            # Find the AI_Environment folder in extracted content
            ai_env_folder = None
            for item in temp_path.iterdir():
                if item.is_dir() and item.name == "AI_Environment":
                    ai_env_folder = item
                    break
            
            if not ai_env_folder:
                print(f"{Fore.RED}Invalid update ZIP: AI_Environment folder not found{Style.RESET_ALL}")
                return False
            
            # Copy files from extracted folder to current location
            print(f"{Fore.CYAN}📁 Installing files...{Style.RESET_ALL}")
            
            for item in ai_env_folder.iterdir():
                if item.name in ["new_versions", "backup"]:
                    continue  # Skip these folders
                
                dest = ai_env_path / item.name
                
                if item.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)
                    print(f"  ✓ Updated folder: {item.name}")
                else:
                    # For run_ai_env.bat, copy to a temp file first
                    if item.name == "run_ai_env.bat":
                        shutil.copy2(item, ai_env_path / "run_ai_env.bat.new")
                        print(f"  ✓ Staged new run_ai_env.bat")
                    else:
                        if dest.exists():
                            dest.unlink()
                        shutil.copy2(item, dest)
                        print(f"  ✓ Updated file: {item.name}")
            
            print(f"{Fore.GREEN}✅ Files installed successfully{Style.RESET_ALL}")
            return True
            
    except Exception as e:
        print(f"{Fore.RED}Failed to extract and install: {e}{Style.RESET_ALL}")
        return False

def restore_backup(ai_env_path, backup_path):
    """Restore from backup if update fails"""
    try:
        if not backup_path.exists():
            return False
        
        print(f"{Fore.CYAN}🔄 Restoring from backup...{Style.RESET_ALL}")
        
        for item in backup_path.iterdir():
            dest = ai_env_path / item.name
            
            if dest.exists():
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
        
        print(f"{Fore.GREEN}✅ System restored from backup{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}Failed to restore backup: {e}{Style.RESET_ALL}")
        return False

def cleanup_backup(backup_path):
    """Clean up backup after successful update"""
    try:
        if backup_path.exists():
            shutil.rmtree(backup_path)
    except Exception:
        pass  # Ignore cleanup errors
        
def update_version_config(ai_env_path, new_version):
    """Update version_config.json with the new version and current date/time"""
    try:
        version_config_path = ai_env_path / "version_config.json"
        if version_config_path.exists():
            with open(version_config_path, "r+") as f:
                config = json.load(f)
                config["config_version"] = new_version
                config["legacy_support"]["metadata_inline"]["system_version"] = new_version
                config["legacy_support"]["metadata_inline"]["created_date"] = time.strftime("%Y-%m-%d")
                config["legacy_support"]["metadata_inline"]["created_time"] = time.strftime("%H:%M")
                f.seek(0)
                json.dump(config, f, indent=2)
                f.truncate()
            print(f"{Fore.GREEN}✅ Updated version_config.json to v{new_version}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Warning: version_config.json not found. Could not update version.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error updating version_config.json: {e}{Style.RESET_ALL}")




