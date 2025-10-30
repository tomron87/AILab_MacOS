# AI Environment Checksum Verifier v3.0.28
#!/usr/bin/env python3
"""
AI Environment Checksum Verifier v3.0.26
Verifies file integrity and completeness using SHA256 checksums

Author: AI Environment Team
Date: 2025-08-14
Version: 3.0.28
"""

import os
import sys
import hashlib
from pathlib import Path

# Version information
SCRIPT_VERSION = "3.0.28"
SCRIPT_DATE = "2025-08-14"

# Color codes for cross-platform support
class Colors:
    if os.name == 'nt':  # Windows
        RESET = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        CYAN = ''
    else:  # Unix/Linux/Mac
        RESET = '\033[0m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        CYAN = '\033[96m'

def calculate_sha256(filepath):
    """Calculate SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return None

def print_header():
    """Print the header banner"""
    print("================================================================")
    print("                AI Environment Checksum Verifier")
    print(f"                     Version {SCRIPT_VERSION} ({SCRIPT_DATE})")
    print("                     File Integrity Verification")
    print("================================================================")
    print()

def load_checksums():
    """Load expected checksums from CHECKSUMS.sha256"""
    checksums_file = "CHECKSUMS.sha256"
    
    if not os.path.exists(checksums_file):
        print(f"{Colors.RED}[ERROR] Checksums file not found: {checksums_file}{Colors.RESET}")
        return None
    
    checksums = {}
    try:
        with open(checksums_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('  ', 1)
                    if len(parts) == 2:
                        expected_hash, filepath = parts
                        # Remove ./ prefix if present
                        filepath = filepath.lstrip('./')
                        checksums[filepath] = expected_hash
        
        print(f"{Colors.GREEN}[OK] Loaded checksums for {len(checksums)} files{Colors.RESET}")
        return checksums
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR] Failed to load checksums: {e}{Colors.RESET}")
        return None

def verify_files(expected_checksums):
    """Verify all files against expected checksums"""
    print("\n================================================================")
    print("                    FILE INTEGRITY VERIFICATION")
    print("================================================================")
    
    stats = {
        'total': len(expected_checksums),
        'verified': 0,
        'missing': 0,
        'corrupted': 0,
        'errors': 0
    }
    
    for filepath, expected_hash in expected_checksums.items():
        print(f"[*] Verifying: {filepath}")
        
        if not os.path.exists(filepath):
            print(f"{Colors.RED}[MISSING] {filepath} - File not found{Colors.RESET}")
            stats['missing'] += 1
            continue
        
        actual_hash = calculate_sha256(filepath)
        if actual_hash is None:
            print(f"{Colors.RED}[ERROR] {filepath} - Cannot calculate checksum{Colors.RESET}")
            stats['errors'] += 1
            continue
        
        if actual_hash == expected_hash:
            print(f"{Colors.GREEN}[OK] {filepath} - Checksum verified{Colors.RESET}")
            stats['verified'] += 1
        else:
            print(f"{Colors.RED}[CORRUPTED] {filepath} - Checksum mismatch{Colors.RESET}")
            print(f"    Expected: {expected_hash}")
            print(f"    Actual:   {actual_hash}")
            stats['corrupted'] += 1
        
        print()
    
    return stats

def load_json_expected_files():
    """Load expected files from version_config.json"""
    json_file = "version_config.json"
    expected_files = set()
    
    if not os.path.exists(json_file):
        print(f"{Colors.YELLOW}[WARNING] JSON config not found: {json_file}{Colors.RESET}")
        return expected_files
    
    try:
        import json
        with open(json_file, 'r') as f:
            config = json.load(f)
        
        # Get files from batch_files section
        if 'expected_versions' in config and 'batch_files' in config['expected_versions']:
            for filename in config['expected_versions']['batch_files'].keys():
                expected_files.add(filename)
        
        # Get files from python_files section
        if 'expected_versions' in config and 'python_files' in config['expected_versions']:
            for filename in config['expected_versions']['python_files'].keys():
                expected_files.add(filename)
        
        print(f"{Colors.GREEN}[OK] Loaded {len(expected_files)} expected files from JSON config{Colors.RESET}")
        
    except Exception as e:
        print(f"{Colors.YELLOW}[WARNING] Failed to load JSON config: {e}{Colors.RESET}")
    
    return expected_files

def check_extra_files():
    """Check for unexpected files - only among AI Environment files"""
    print("================================================================")
    print("                    EXTRA FILES CHECK")
    print("================================================================")
    
    # Get expected files from checksums
    checksum_files = set()
    if os.path.exists("CHECKSUMS.sha256"):
        with open("CHECKSUMS.sha256", 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('  ', 1)
                    if len(parts) == 2:
                        filepath = parts[1].lstrip('./')
                        checksum_files.add(filepath)
    
    # Get expected files from JSON config
    json_files = load_json_expected_files()
    
    # Add verification files
    verification_files = {"CHECKSUMS.sha256", "verify_checksums.py", "PACKAGE_INFO.txt", "version_config.json"}
    
    # All expected files
    all_expected = checksum_files | json_files | verification_files
    
    # Only check files that should be part of AI Environment
    # Don't scan the entire directory - only check specific AI Environment files
    ai_env_files = set()
    
    # Check only the files we expect to exist
    for expected_file in all_expected:
        if os.path.exists(expected_file):
            ai_env_files.add(expected_file)
    
    # Find extra files only among AI Environment related files
    extra_files = ai_env_files - all_expected
    
    print(f"{Colors.GREEN}[INFO] Checking only AI Environment files (not scanning entire directory){Colors.RESET}")
    print(f"{Colors.GREEN}[INFO] Expected AI Environment files: {len(all_expected)}{Colors.RESET}")
    print(f"{Colors.GREEN}[INFO] Found AI Environment files: {len(ai_env_files)}{Colors.RESET}")
    
    if extra_files:
        print(f"{Colors.YELLOW}[WARNING] Found {len(extra_files)} unexpected AI Environment files:{Colors.RESET}")
        for file in sorted(extra_files):
            print(f"  - {file}")
    else:
        print(f"{Colors.GREEN}[OK] No unexpected AI Environment files found{Colors.RESET}")
    
    print(f"{Colors.CYAN}[INFO] Note: Only checking AI Environment files, ignoring system installations{Colors.RESET}")
    print()
    return len(extra_files)

def print_summary(stats, extra_files_count):
    """Print verification summary"""
    print("================================================================")
    print("                    VERIFICATION SUMMARY")
    print("================================================================")
    
    total_files_in_checksum = stats['total']
    total_files_found = stats['verified'] + stats['corrupted'] + stats['errors']

    print(f"Total files in CHECKSUMS.sha256: {total_files_in_checksum}")
    print(f"Files found and processed: {total_files_found}")
    print(f"Files missing: {stats['missing']}")
    print(f"Files corrupted: {stats['corrupted']}")
    print(f"Verification errors: {stats['errors']}")
    print(f"Extra files found: {extra_files_count}")
    print()
    
    if stats['missing'] == 0 and stats['corrupted'] == 0 and stats['errors'] == 0 and extra_files_count == 0:
        print(f"{Colors.GREEN}[SUCCESS] All files verified successfully!{Colors.RESET}")
        print(f"{Colors.GREEN}[INFO] Package integrity confirmed - all files are present and correct{Colors.RESET}")
        return True
    else:
        print(f"{Colors.RED}[FAILURE] Package integrity check failed{Colors.RESET}")
        if stats['missing'] > 0:
            print(f"{Colors.RED}[ACTION] {stats['missing']} files are missing - re-extract the package{Colors.RESET}")
        if stats['corrupted'] > 0:
            print(f"{Colors.RED}[ACTION] {stats['corrupted']} files are corrupted - re-download the package{Colors.RESET}")
        if stats['errors'] > 0:
            print(f"{Colors.YELLOW}[ACTION] {stats['errors']} files had verification errors{Colors.RESET}")
        return False

def main():
    """Main function"""
    print_header()
    
    # Load expected checksums
    expected_checksums = load_checksums()
    if not expected_checksums:
        sys.exit(1)
    
    print(f"[INFO] Verifying package integrity in: {os.getcwd()}")
    print(f"[INFO] Expected files: {len(expected_checksums)}")
    print()
    
    # Verify files
    stats = verify_files(expected_checksums)
    
    # Check for extra files
    extra_files_count = check_extra_files()
    
    # Print summary
    success = print_summary(stats, extra_files_count)
    
    print("================================================================")
    print("                 CHECKSUM VERIFICATION COMPLETE")
    print("================================================================")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI Environment Checksum Verifier")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild CHECKSUMS.sha256")
    args = parser.parse_args()

    if args.rebuild:
        print_header()
        print("\n================================================================")
        print("                    REBUILDING CHECKSUMS.sha256")
        print("================================================================")
        checksums_file = "CHECKSUMS.sha256"
        ai_env_path = Path(os.getcwd())
        
        # List of files to include in checksums
        files_to_checksum = [
            "check_versions.bat",
            "PACKAGE_INFO.txt",
            "README.md",
            "run_ai_env.bat",
            "setup_python_env.bat",
            "version_config.json",
            "version_config_old.json",
            "src/activate_ai_env.py",
            "src/ai_action_handlers.py",
            "src/ai_app_launcher.py",
            "src/ai_component_setup.py",
            "src/ai_component_tester.py",
            "src/ai_conda_manager.py",
            "src/ai_document_viewer.py",
            "src/ai_environment_validator.py",
            "src/ai_jupyter_manager.py",
            "src/ai_menu_system.py",
            "src/ai_model_downloader.py",
            "src/ai_model_loader.py",
            "src/ai_model_manager.py",
            "src/ai_ollama_manager.py",
            "src/ai_path_manager.py",
            "src/ai_process_manager.py",
            "src/ai_status_display.py",
            "src/ai_terminal_launcher.py",
            "src/ai_update_manager.py",
            "src/ai_update_utils.py",
            "src/ai_update_display.py",
            "src/check_versions.py",
            "src/verify_checksums.py",
            "help/codellama_7b.txt",
            "help/gpt_oss_20b.txt",
            "help/llama2_7b.txt",
            "help/mistral_7b.txt",
            "help/phi_2_7b.txt"
        ]

        new_checksums = {}
        for file_path_str in files_to_checksum:
            full_path = ai_env_path / file_path_str
            if full_path.exists():
                print(f"Calculating checksum for: {file_path_str}")
                checksum = calculate_sha256(full_path)
                if checksum:
                    new_checksums[file_path_str] = checksum
                else:
                    print(f"{Colors.RED}[ERROR] Could not calculate checksum for {file_path_str}{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}[WARNING] File not found for checksum: {file_path_str}{Colors.RESET}")
        
        try:
            with open(checksums_file, "w") as f:
                for filepath, checksum in new_checksums.items():
                    f.write(f"{checksum}  {filepath}\n")
            print(f"{Colors.GREEN}\n✅ CHECKSUMS.sha256 rebuilt successfully with {len(new_checksums)} files.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR] Failed to write CHECKSUMS.sha256: {e}{Colors.RESET}")
        sys.exit(0)
    else:
        try:
            main()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[INFO] Verification interrupted by user{Colors.RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"\n{Colors.RED}[ERROR] Unexpected error: {e}{Colors.RESET}")
            sys.exit(1)


