"""
AI Model Manager
Comprehensive model management for Ollama AI models

Version: 3.0.28
Author: AI Environment Team
Date: 2025-08-14
Time: 10:30
"""

import os
import subprocess
import json
from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = WHITE = ""
    class Style:
        RESET_ALL = ""

from ai_model_downloader import ModelDownloader
from ai_model_loader import ModelLoader

class AIModelManager:
    """Comprehensive AI model management system"""
    
    def __init__(self, ai_env_path, ollama_path=None):
        """Initialize AI Model Manager
        
        Args:
            ai_env_path (Path): Path to AI Environment
            ollama_path (Path, optional): Path to Ollama executable
        """
        self.ai_env_path = Path(ai_env_path)
        self.ollama_path = ollama_path or self.ai_env_path / "Ollama" / "ollama.exe"
        self.models_help_path = self.ai_env_path / "models"
        
        # Initialize components
        self.downloader = ModelDownloader(self.ollama_path)
        self.loader = ModelLoader(self.ollama_path, self.models_help_path)
        
        # Ensure models help directory exists
        self.models_help_path.mkdir(exist_ok=True)
        
        # Popular models configuration
        self.popular_models = {
            "phi:2.7b": {
                "name": "Phi 2.7B",
                "size": "1.6 GB",
                "description": "Fast and efficient small model by Microsoft",
                "recommended": True
            },
            "llama2:7b": {
                "name": "Llama2 7B", 
                "size": "3.8 GB",
                "description": "Meta's powerful general-purpose model",
                "recommended": True
            },
            "mistral:7b": {
                "name": "Mistral 7B",
                "size": "4.4 GB", 
                "description": "High-quality French AI model",
                "recommended": False
            },
            "codellama:7b": {
                "name": "CodeLlama 7B",
                "size": "3.8 GB",
                "description": "Specialized for code generation",
                "recommended": False
            }
        }

    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.CYAN}ℹ️ {message}{Style.RESET_ALL}")

    def print_warning(self, message):
        """Print warning message"""
        print(f"{Fore.YELLOW}⚠️ {message}{Style.RESET_ALL}")

    def show_menu(self):
        """Display AI model management menu"""
        separator = "=" * 60
        print(f"\n{Fore.MAGENTA}{separator}")
        print(f"🤖 AI Model Management")
        print(f"{separator}{Style.RESET_ALL}")
        print(f" 1. {Fore.GREEN}🔥 Download Model{Style.RESET_ALL}")
        print(f" 2. {Fore.BLUE}🚀 Load Model{Style.RESET_ALL}")
        print(f" 3. {Fore.CYAN}📋 Show Available Models{Style.RESET_ALL}")
        print(f" 4. {Fore.YELLOW}📊 Model Status{Style.RESET_ALL}")
        print(f" 5. {Fore.RED}🗑️ Delete Model{Style.RESET_ALL}")
        print(f" 6. {Fore.MAGENTA}📚 Model Help{Style.RESET_ALL}")
        print(f" 0. {Fore.WHITE}⬅️ Back to Main Menu{Style.RESET_ALL}")

    def get_installed_models(self):
        """Get list of installed models"""
        try:
            result = subprocess.run(
                [str(self.ollama_path), "list"],
                capture_output=True,
                text=True,
                check=True
            )
            
            models = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        models.append({
                            'name': parts[0],
                            'id': parts[1],
                            'size': parts[2],
                            'modified': ' '.join(parts[3:]) if len(parts) > 3 else 'Unknown'
                        })
            return models
        except Exception as e:
            self.print_error(f"Failed to get installed models: {e}")
            return []

    def get_loaded_models(self):
        """Get list of currently loaded models"""
        try:
            result = subprocess.run(
                [str(self.ollama_path), "ps"],
                capture_output=True,
                text=True,
                check=True
            )
            
            models = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        models.append({
                            'name': parts[0],
                            'id': parts[1],
                            'size': parts[2] if len(parts) > 2 else 'Unknown',
                            'processor': parts[3] if len(parts) > 3 else 'Unknown'
                        })
            return models
        except Exception as e:
            self.print_error(f"Failed to get loaded models: {e}")
            return []

    def handle_download_model(self):
        """Handle model download"""
        self.downloader.show_download_menu()

    def handle_load_model(self):
        """Handle model loading"""
        self.loader.show_load_menu()

    def handle_show_available(self):
        """Handle showing available models"""
        print(f"\n{Fore.CYAN}📋 Available Models:{Style.RESET_ALL}")
        
        installed = self.get_installed_models()
        if not installed:
            self.print_warning("No models installed")
            self.print_info("Use option 1 to download models")
            return
        
        print(f"\n{Fore.GREEN}Installed Models:{Style.RESET_ALL}")
        for i, model in enumerate(installed, 1):
            status = "✅" if model['name'] in [m['name'] for m in self.get_loaded_models()] else "⭕"
            print(f" {i}. {status} {model['name']} ({model['size']}) - {model['modified']}")
        
        print(f"\n{Fore.YELLOW}Popular Models Available for Download:{Style.RESET_ALL}")
        for model_id, info in self.popular_models.items():
            installed_names = [m['name'] for m in installed]
            if model_id not in installed_names:
                rec = "⭐" if info['recommended'] else "  "
                print(f" {rec} {info['name']} ({info['size']}) - {info['description']}")

    def handle_model_status(self):
        """Handle model status display"""
        print(f"\n{Fore.CYAN}📊 Model Status:{Style.RESET_ALL}")
        
        loaded = self.get_loaded_models()
        if loaded:
            print(f"\n{Fore.GREEN}Currently Loaded Models:{Style.RESET_ALL}")
            for model in loaded:
                print(f" ✅ {model['name']} (ID: {model['id']}) - {model['processor']}")
        else:
            self.print_info("No models currently loaded")
        
        installed = self.get_installed_models()
        if installed:
            unloaded = [m for m in installed if m['name'] not in [l['name'] for l in loaded]]
            if unloaded:
                print(f"\n{Fore.YELLOW}Available but Not Loaded:{Style.RESET_ALL}")
                for model in unloaded:
                    print(f" ⭕ {model['name']} ({model['size']})")

    def handle_delete_model(self):
        """Handle model deletion"""
        installed = self.get_installed_models()
        if not installed:
            self.print_warning("No models installed to delete")
            return
        
        print(f"\n{Fore.RED}🗑️ Delete Model:{Style.RESET_ALL}")
        print("Select model to delete:")
        
        for i, model in enumerate(installed, 1):
            print(f" {i}. {model['name']} ({model['size']})")
        
        try:
            choice = input(f"\n{Fore.YELLOW}Enter choice (1-{len(installed)}) or 0 to cancel: {Style.RESET_ALL}")
            choice = int(choice)
            
            if choice == 0:
                self.print_info("Deletion cancelled")
                return
            
            if 1 <= choice <= len(installed):
                model = installed[choice - 1]
                confirm = input(f"{Fore.RED}Are you sure you want to delete '{model['name']}'? (y/N): {Style.RESET_ALL}")
                
                if confirm.lower() == 'y':
                    try:
                        subprocess.run(
                            [str(self.ollama_path), "rm", model['name']],
                            check=True
                        )
                        self.print_success(f"Deleted model: {model['name']}")
                    except subprocess.CalledProcessError as e:
                        self.print_error(f"Failed to delete model: {e}")
                else:
                    self.print_info("Deletion cancelled")
            else:
                self.print_error("Invalid choice")
        except ValueError:
            self.print_error("Invalid input")

    def handle_model_help(self):
        """Handle model help display"""
        self.loader.show_model_help_menu()

    def run_interactive_menu(self):
        """Run interactive model management menu"""
        while True:
            self.show_menu()
            
            try:
                choice = input(f"\n{Fore.YELLOW}Enter your choice (0-6): {Style.RESET_ALL}")
                choice = int(choice)
                
                if choice == 0:
                    break
                elif choice == 1:
                    self.handle_download_model()
                elif choice == 2:
                    self.handle_load_model()
                elif choice == 3:
                    self.handle_show_available()
                elif choice == 4:
                    self.handle_model_status()
                elif choice == 5:
                    self.handle_delete_model()
                elif choice == 6:
                    self.handle_model_help()
                else:
                    self.print_error("Invalid choice. Please try again.")
                    
                if choice != 0:
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    
            except ValueError:
                self.print_error("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Exiting model management...{Style.RESET_ALL}")
                break
				