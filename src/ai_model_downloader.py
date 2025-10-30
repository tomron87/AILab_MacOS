"""
AI Model Downloader
Handles downloading of AI models from various sources

Version: 3.0.28
Author: AI Environment Team
Date: 2025-08-14
Time: 10:30
"""

import subprocess
import requests
from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = WHITE = LIGHTBLACK_EX = ""
    class Style:
        RESET_ALL = ""

class ModelDownloader:
    """Handles AI model downloading"""
    
    def __init__(self, ollama_path):
        """Initialize Model Downloader
        
        Args:
            ollama_path (Path): Path to Ollama executable
        """
        self.ollama_path = Path(ollama_path)
        
        # Popular models for quick download
        self.popular_models = {
            "1": {
                "name": "phi:2.7b",
                "display_name": "Phi 2.7B (Recommended)",
                "size": "1.6 GB",
                "description": "Fast and efficient small model by Microsoft"
            },
            "2": {
                "name": "llama2:7b", 
                "display_name": "Llama2 7B",
                "size": "3.8 GB",
                "description": "Meta's powerful general-purpose model"
            },
            "3": {
                "name": "mistral:7b",
                "display_name": "Mistral 7B",
                "size": "4.4 GB",
                "description": "High-quality French AI model"
            },
            "4": {
                "name": "codellama:7b",
                "display_name": "CodeLlama 7B", 
                "size": "3.8 GB",
                "description": "Specialized for code generation"
            },
            "5": {
                "name": "llama3.2:3b",
                "display_name": "Llama 3.2 3B",
                "size": "2.0 GB", 
                "description": "Latest Llama model, compact version"
            },
            "6": {
                "name": "qwen2:7b",
                "display_name": "Qwen2 7B",
                "size": "4.4 GB",
                "description": "Alibaba's multilingual model"
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

    def show_download_menu(self):
        """Show download options menu"""
        print(f"\n{Fore.GREEN}🔥 Download AI Model:{Style.RESET_ALL}")
        print(f" 1. {Fore.CYAN}📋 Popular Models (Quick Download){Style.RESET_ALL}")
        print(f" 2. {Fore.YELLOW}🔗 Custom Model (Enter URL/Name){Style.RESET_ALL}")
        print(f" 3. {Fore.BLUE}🌐 Browse Ollama Library{Style.RESET_ALL}")
        print(f" 0. {Fore.WHITE}⬅️ Back{Style.RESET_ALL}")
        
        try:
            choice = input(f"\n{Fore.YELLOW}Enter your choice (0-3): {Style.RESET_ALL}")
            choice = int(choice)
            
            if choice == 0:
                return
            elif choice == 1:
                self.download_popular_model()
            elif choice == 2:
                self.download_custom_model()
            elif choice == 3:
                self.browse_ollama_library()
            else:
                self.print_error("Invalid choice")
        except ValueError:
            self.print_error("Invalid input")

    def download_popular_model(self):
        """Download from popular models list"""
        print(f"\n{Fore.CYAN}📋 Popular AI Models:{Style.RESET_ALL}")
        
        for key, model in self.popular_models.items():
            print(f" {key}. {model['display_name']} ({model['size']})")
            print(f"    {Fore.LIGHTBLACK_EX}{model['description']}{Style.RESET_ALL}")
        
        try:
            choice = input(f"\n{Fore.YELLOW}Select model (1-{len(self.popular_models)}) or 0 to cancel: {Style.RESET_ALL}")
            
            if choice == "0":
                self.print_info("Download cancelled")
                return
            
            if choice in self.popular_models:
                model = self.popular_models[choice]
                self.download_model(model['name'], model['display_name'])
            else:
                self.print_error("Invalid choice")
        except Exception as e:
            self.print_error(f"Error: {e}")

    def download_custom_model(self):
        """Download custom model by name or URL"""
        print(f"\n{Fore.YELLOW}🔗 Custom Model Download:{Style.RESET_ALL}")
        print("You can enter:")
        print("• Model name (e.g., 'llama2:7b', 'phi:2.7b')")
        print("• Hugging Face model (e.g., 'microsoft/DialoGPT-medium')")
        print("• Custom URL to model file")
        
        model_input = input(f"\n{Fore.YELLOW}Enter model name or URL: {Style.RESET_ALL}").strip()
        
        if not model_input:
            self.print_error("No input provided")
            return
        
        # Check if it's a URL
        if model_input.startswith(('http://', 'https://')):
            self.print_info("URL downloads require manual setup")
            self.print_info("Please use Ollama's import functionality:")
            print(f"{Fore.CYAN}ollama create mymodel -f Modelfile{Style.RESET_ALL}")
            return
        
        self.download_model(model_input, model_input)

    def browse_ollama_library(self):
        """Show information about browsing Ollama library"""
        print(f"\n{Fore.BLUE}🌐 Ollama Model Library:{Style.RESET_ALL}")
        print("Visit: https://ollama.ai/library")
        print("\nPopular categories:")
        print("• 🧠 General Purpose: llama2, mistral, phi")
        print("• 💻 Code Generation: codellama, starcoder")
        print("• 🌐 Multilingual: qwen2, gemma")
        print("• 🎨 Creative: nous-hermes, dolphin")
        
        self.print_info("Copy model name from the website and use option 2 (Custom Model)")

    def download_model(self, model_name, display_name=None):
        """Download a specific model
        
        Args:
            model_name (str): Name of the model to download
            display_name (str, optional): Display name for user feedback
        """
        if display_name is None:
            display_name = model_name
        
        print(f"\n{Fore.BLUE}🔥 Downloading {display_name}...{Style.RESET_ALL}")
        self.print_info("This may take several minutes depending on model size")
        self.print_warning("Do not close this window during download")
        
        try:
            # Check if Ollama is available
            if not self.ollama_path.exists():
                self.print_error(f"Ollama not found at: {self.ollama_path}")
                return False
            
            # Start download
            process = subprocess.Popen(
                [str(self.ollama_path), "pull", model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            # Show progress
            print(f"{Fore.YELLOW}Progress:{Style.RESET_ALL}")
            for line in process.stdout:
                if line.strip():
                    # Clean up the progress line
                    if "pulling" in line.lower() or "%" in line:
                        print(f"  {line.strip()}")
                    elif "success" in line.lower():
                        print(f"  {Fore.GREEN}{line.strip()}{Style.RESET_ALL}")
            
            # Wait for completion
            return_code = process.wait()
            
            if return_code == 0:
                self.print_success(f"Successfully downloaded {display_name}")
                self.print_info(f"Model '{model_name}' is now available")
                self.show_usage_example(model_name)
                return True
            else:
                self.print_error(f"Failed to download {display_name}")
                return False
                
        except FileNotFoundError:
            self.print_error("Ollama executable not found")
            self.print_info("Make sure Ollama is properly installed")
            return False
        except Exception as e:
            self.print_error(f"Download failed: {e}")
            return False

    def show_usage_example(self, model_name):
        """Show usage example for downloaded model
        
        Args:
            model_name (str): Name of the downloaded model
        """
        print(f"\n{Fore.GREEN}🐍 Python Usage Example:{Style.RESET_ALL}")
        print("Update your Python code to use this model:")
        print(f"{Fore.CYAN}")
        print("# In your main.py or other Python files:")
        example_code = f'response = query_ollama(prompt, model="{model_name}")'
        print(example_code)
        print(f"{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}💡 Remember to update your code!{Style.RESET_ALL}")
        print("Change the model parameter in your Python scripts to use the new model.")

    def check_available_space(self):
        """Check available disk space (Windows specific)"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(str(self.ollama_path.parent))
            free_gb = free // (1024**3)
            return free_gb
        except:
            return None

    def estimate_download_time(self, size_gb, speed_mbps=10):
        """Estimate download time
        
        Args:
            size_gb (float): Size in GB
            speed_mbps (float): Internet speed in Mbps
            
        Returns:
            str: Estimated time string
        """
        size_mb = size_gb * 1024
        time_seconds = (size_mb * 8) / speed_mbps
        
        if time_seconds < 60:
            return f"{int(time_seconds)} seconds"
        elif time_seconds < 3600:
            return f"{int(time_seconds / 60)} minutes"
        else:
            return f"{int(time_seconds / 3600)} hours"
			