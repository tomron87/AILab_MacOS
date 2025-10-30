#!/usr/bin/env python3
"""
AI Environment Validator
Validates installed packages against install_config.json requirements

Version: 3.0.28
Author: AI Environment Team
Date: 2025-08-13
Time: 12:45
"""

import os
import sys
import json
import subprocess
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

class EnvironmentValidator:
    """Validates AI Environment against configuration requirements"""
    
    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)
        self.config_path = self.ai_env_path / "config" / "install_config.json"
        self.config = None
        self.missing_packages = []
        self.installed_packages = []
        
    def load_config(self):
        """Load install configuration"""
        try:
            if not self.config_path.exists():
                print(f"{Fore.RED}[ERROR] Configuration file not found: {self.config_path}")
                return False
                
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to load config: {e}")
            return False
    
    def check_python_packages(self):
        """Check installed Python packages against requirements"""
        if not self.config:
            return False
            
        required_packages = self.config.get('python_packages', [])
        print(f"{Fore.CYAN}[INFO] Checking {len(required_packages)} required packages...")
        
        self.missing_packages = []
        self.installed_packages = []
        
        for package in required_packages:
            # Extract package name (remove version constraints)
            package_name = package.split('>=')[0].split('==')[0].split('<')[0].split('>')[0]
            
            try:
                # Try to import the package
                result = subprocess.run([
                    sys.executable, '-c', f'import {package_name}; print("OK")'
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    self.installed_packages.append(package)
                    print(f"{Fore.GREEN}[OK]   ✓ {package_name}")
                else:
                    self.missing_packages.append(package)
                    print(f"{Fore.RED}[MISSING] ✗ {package_name}")
                    
            except subprocess.TimeoutExpired:
                print(f"{Fore.YELLOW}[TIMEOUT] ? {package_name} (import timeout)")
                self.missing_packages.append(package)
            except Exception as e:
                print(f"{Fore.RED}[ERROR] ✗ {package_name}: {e}")
                self.missing_packages.append(package)
        
        return len(self.missing_packages) == 0
    
    def generate_summary_report(self):
        """Generate validation summary report"""
        if not self.config:
            return "Configuration not loaded"
            
        total_packages = len(self.config.get('python_packages', []))
        installed_count = len(self.installed_packages)
        missing_count = len(self.missing_packages)
        
        report = []
        report.append("=" * 60)
        report.append("         ENVIRONMENT VALIDATION SUMMARY")
        report.append("=" * 60)
        report.append("")
        report.append(f"Total packages checked: {total_packages}")
        report.append(f"Packages installed: {installed_count}")
        report.append(f"Packages missing: {missing_count}")
        report.append(f"Success rate: {(installed_count/total_packages)*100:.1f}%")
        report.append("")
        
        if self.missing_packages:
            report.append("MISSING PACKAGES:")
            report.append("-" * 20)
            for package in self.missing_packages:
                report.append(f"  - {package}")
            report.append("")
        
        if missing_count == 0:
            report.append(f"{Fore.GREEN}✅ ALL PACKAGES INSTALLED - Environment is complete!")
        elif missing_count <= 3:
            report.append(f"{Fore.YELLOW}⚠️  MOSTLY COMPLETE - {missing_count} packages missing")
        else:
            report.append(f"{Fore.RED}❌ INCOMPLETE - {missing_count} packages missing")
        
        report.append("=" * 60)
        return "\n".join(report)
    
    def offer_installation(self):
        """Offer to install missing packages"""
        if not self.missing_packages:
            return True
            
        print(f"\n{Fore.YELLOW}Would you like to install the missing packages? (y/N): ", end="")
        try:
            choice = input().strip().lower()
            if choice in ['y', 'yes']:
                return self.install_missing_packages()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Installation cancelled by user")
        
        return False
    
    def install_missing_packages(self):
        """Install missing packages using pip"""
        if not self.missing_packages:
            return True
            
        print(f"\n{Fore.CYAN}[INFO] Installing {len(self.missing_packages)} missing packages...")
        
        success_count = 0
        for package in self.missing_packages:
            try:
                print(f"{Fore.CYAN}[INFO] Installing {package}...")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"{Fore.GREEN}[OK] ✓ {package} installed successfully")
                    success_count += 1
                else:
                    print(f"{Fore.RED}[ERROR] ✗ Failed to install {package}")
                    print(f"       {result.stderr.strip()}")
                    
            except subprocess.TimeoutExpired:
                print(f"{Fore.RED}[ERROR] ✗ {package} installation timeout")
            except Exception as e:
                print(f"{Fore.RED}[ERROR] ✗ {package}: {e}")
        
        print(f"\n{Fore.CYAN}[INFO] Installation complete: {success_count}/{len(self.missing_packages)} packages installed")
        return success_count == len(self.missing_packages)
    
    def run_validation(self):
        """Run complete environment validation"""
        print(f"{Fore.CYAN}🔍 Running Environment Validation...")
        print("=" * 60)
        
        # Load configuration
        if not self.load_config():
            return False
        
        print(f"{Fore.GREEN}[OK] Configuration loaded from: {self.config_path}")
        
        # Check Python packages
        packages_ok = self.check_python_packages()
        
        # Generate and display summary
        print("\n" + self.generate_summary_report())
        
        # Offer installation if needed
        if not packages_ok:
            self.offer_installation()
        
        return packages_ok

def main():
    """Main function for standalone execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Environment Validator')
    parser.add_argument('--ai-env-path', default='.', 
                       help='Path to AI Environment directory')
    
    args = parser.parse_args()
    
    validator = EnvironmentValidator(args.ai_env_path)
    success = validator.run_validation()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

