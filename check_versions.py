#!/usr/bin/env python3
"""
AI Environment Version Checker v3.0.0
Cross-platform Python version of check_versions.bat
Dynamically reads all files from version_config.json

Author: AI Environment Team
Date: 2025-08-17
Version: 3.0.28
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime

# Version information
SCRIPT_VERSION = "3.0.28"
SCRIPT_DATE = "2025-08-17"

# Color codes for cross-platform support
class Colors:
    if os.name == 'nt':  # Windows
        # Windows color codes
        RESET = ''
        CYAN = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        BLUE = ''
        MAGENTA = ''
    else:  # Unix/Linux/Mac
        RESET = '\033[0m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'

def print_header():
    """Print the header banner"""
    print("================================================================")
    print("                   AI Environment Version Checker")
    print(f"                     Version {SCRIPT_VERSION} ({SCRIPT_DATE})")
    print("                     Python Cross-Platform Mode")
    print("================================================================")
    print()

def load_config():
    """Load the version configuration from JSON"""
    config_file = "version_config.json"
    
    print(f"[INFO] Checking file versions in: {os.getcwd()}")
    print(f"[INFO] Using configuration: {config_file}")
    print()
    
    try:
        if not os.path.exists(config_file):
            print(f"{Colors.RED}[ERROR] Configuration file not found: {config_file}{Colors.RESET}")
            return None
            
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        print(f"{Colors.GREEN}[OK] Configuration file found: {config_file}{Colors.RESET}")
        print()
        
        return config
        
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}[ERROR] Invalid JSON in {config_file}: {e}{Colors.RESET}")
        return None
    except Exception as e:
        print(f"{Colors.RED}[ERROR] Failed to load {config_file}: {e}{Colors.RESET}")
        return None

def check_file_version(filepath, expected_version, search_pattern, description=""):
    """Check if a file contains the expected version"""
    try:
        if not os.path.exists(filepath):
            return False, "FILE NOT FOUND", "missing"
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # If there's a specific search pattern, use it
        if search_pattern:
            if search_pattern in content:
                return True, f"Version {expected_version} found", "correct"
            else:
                return False, f"Version {expected_version} NOT found", "wrong"
        else:
            # Default search patterns based on file type
            file_ext = os.path.splitext(filepath)[1].lower()
            
            if file_ext == '.bat':
                patterns = [
                    f'SCRIPT_VERSION={expected_version}',
                    f'SCRIPT_VERSION="{expected_version}"',
                    f'v{expected_version}'
                ]
            elif file_ext == '.py':
                patterns = [
                    f'SCRIPT_VERSION = "{expected_version}"',
                    f'AI Environment Module v{expected_version}',
                    f'Version: {expected_version}',
                    f'Version {expected_version}'
                ]
            else:
                patterns = [
                    f'v{expected_version}',
                    f'Version {expected_version}',
                    expected_version
                ]
            
            for pattern in patterns:
                if pattern in content:
                    return True, f"Version {expected_version} found", "correct"
            
            return False, f"Version {expected_version} NOT found", "wrong"
    
    except Exception as e:
        return False, f"ERROR: {e}", "error"

def check_files_category(category_name, files_dict, stats):
    """Check a category of files (batch or python)"""
    print("================================================================")
    print(f"                       {category_name.upper()}")
    print("================================================================")
    print(f"[*] Checking {category_name.lower()} files from JSON configuration...")
    print()
    
    for filename, info in files_dict.items():
        stats['total'] += 1
        expected_version = info['version']
        search_pattern = info.get('search_pattern', '')
        description = info.get('description', '')
        
        print(f"[*] Checking: {filename} (expected: {expected_version})")
        
        success, message, status = check_file_version(filename, expected_version, search_pattern, description)
        
        if success:
            print(f"{Colors.GREEN}[OK] {filename} - {message}{Colors.RESET}")
            stats['correct'] += 1
        else:
            if status == "missing":
                print(f"{Colors.RED}[ERROR] {filename} - {message}{Colors.RESET}")
                stats['missing'] += 1
            else:
                print(f"{Colors.YELLOW}[WARNING] {filename} - {message}{Colors.RESET}")
                stats['wrong'] += 1
        print()

def print_summary(stats):
    """Print the summary statistics"""
    print("================================================================")
    print("                       VERSION SUMMARY")
    print("================================================================")
    print()
    print(f"Total files checked: {stats['total']}")
    print(f"Files with correct version: {stats['correct']}")
    print(f"Files with wrong version: {stats['wrong']}")
    print(f"Files missing: {stats['missing']}")
    print()
    
    if stats['correct'] == stats['total'] and stats['total'] > 0:
        percentage = 100.0
        print(f"{Colors.GREEN}[SUCCESS] All files have correct versions ({percentage:.0f}%){Colors.RESET}")
        print(f"{Colors.GREEN}[INFO] Your AI Environment system is up to date!{Colors.RESET}")
        return True
    else:
        percentage = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"{Colors.YELLOW}[WARNING] Only {stats['correct']}/{stats['total']} files have correct versions ({percentage:.0f}%){Colors.RESET}")
        print()
        
        if stats['wrong'] > 0:
            print(f"{Colors.YELLOW}[ACTION REQUIRED] {stats['wrong']} files have wrong versions{Colors.RESET}")
        if stats['missing'] > 0:
            print(f"{Colors.RED}[ACTION REQUIRED] {stats['missing']} files are missing{Colors.RESET}")
        
        print(f"{Colors.CYAN}[SOLUTION] Check version_config.json for expected versions{Colors.RESET}")
        print(f"{Colors.CYAN}[SOLUTION] Update files as needed or download latest package{Colors.RESET}")
        return False

def print_footer(success):
    """Print the footer information"""
    print()
    print("================================================================")
    print("                   JSON CONFIGURATION INFO")
    print("================================================================")
    print()
    print(f"[INFO] Configuration file: version_config.json")
    print(f"[INFO] Script version: {SCRIPT_VERSION}")
    print(f"[INFO] To view detailed version requirements:")
    if os.name == 'nt':  # Windows
        print("  type version_config.json")
    else:  # Unix/Linux/Mac
        print("  cat version_config.json")
    print()
    print(f"[INFO] To update expected versions:")
    print("  Edit version_config.json with your preferred text editor")
    print()
    print("================================================================")
    print("                   VERSION CHECK COMPLETE")
    print("================================================================")

def main():
    """Main function"""
    print_header()
    
    # Load configuration
    config = load_config()
    if not config:
        sys.exit(1)
    
    expected_versions = config.get('expected_versions', {})
    
    # Initialize statistics
    stats = {
        'total': 0,
        'correct': 0,
        'wrong': 0,
        'missing': 0
    }
    
    # Count total files
    batch_files = expected_versions.get('batch_files', {})
    python_files = expected_versions.get('python_files', {})
    total_expected = len(batch_files) + len(python_files)
    
    print(f"[INFO] Found configuration for {total_expected} files")
    print()
    
    # Check batch files
    if batch_files:
        check_files_category("BATCH FILES", batch_files, stats)
    
    # Check Python files
    if python_files:
        check_files_category("PYTHON FILES", python_files, stats)
    
    # Print summary
    success = print_summary(stats)
    
    # Print footer
    print_footer(success)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INFO] Version check interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)

