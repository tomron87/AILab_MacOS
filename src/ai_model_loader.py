# AI Environment Module v3.0.28
"""
AI Environment Module v3.0.17
Date: 2025-08-13
Time: 05:30

Handles loading and managing AI models with help system
"""

import subprocess
import time
from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = WHITE = ""
    class Style:
        RESET_ALL = ""

class ModelLoader:
    """Handles AI model loading and help system"""
    
    def __init__(self, ollama_path, help_path):
        """Initialize Model Loader
        
        Args:
            ollama_path (Path): Path to Ollama executable
            help_path (Path): Path to help directory containing model documentation
        """
        self.ollama_path = Path(ollama_path)
        self.help_path = Path(help_path)
        
        # Model help file mapping
        self.help_files = {
            "phi:2.7b": "phi_2_7b.txt",
            "llama2:7b": "llama2_7b.txt", 
            "mistral:7b": "mistral_7b.txt",
            "codellama:7b": "codellama_7b.txt",
            "gpt-oss:20b": "gpt_oss_20b.txt"
        }

    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

    def print_warning(self, message):
        """Print warning message"""
        print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")

    def get_installed_models(self):
        """Get list of installed models"""
        try:
            result = subprocess.run(
                [str(self.ollama_path), "list"],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8',
                errors='replace'
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
                check=True,
                encoding='utf-8',
                errors='replace'
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

    def show_load_menu(self):
        """Show model loading menu"""
        installed = self.get_installed_models()
        if not installed:
            self.print_warning("No models installed")
            self.print_info("Use option 1 to download models first")
            return
        
        loaded = self.get_loaded_models()
        loaded_names = [m['name'] for m in loaded]
        
        print(f"\n{Fore.BLUE}🚀 Load AI Model:{Style.RESET_ALL}")
        print("Available models:")
        
        for i, model in enumerate(installed, 1):
            status = "✅ LOADED" if model['name'] in loaded_names else "⭕ Available"
            print(f" {i}. {model['name']} ({model['size']}) - {status}")
        
        try:
            choice = input(f"\n{Fore.YELLOW}Select model to load (1-{len(installed)}) or 0 to cancel: {Style.RESET_ALL}")
            choice = int(choice)
            
            if choice == 0:
                self.print_info("Loading cancelled")
                return
            
            if 1 <= choice <= len(installed):
                model = installed[choice - 1]
                self.load_model(model['name'])
            else:
                self.print_error("Invalid choice")
        except ValueError:
            self.print_error("Invalid input")

    def load_model(self, model_name):
        """Load a specific model
        
        Args:
            model_name (str): Name of the model to load
        """
        # Check if already loaded
        loaded = self.get_loaded_models()
        if model_name in [m['name'] for m in loaded]:
            self.print_info(f"Model '{model_name}' is already loaded")
            self.show_usage_instructions(model_name)
            return True
        
        print(f"\n{Fore.BLUE}🚀 Loading {model_name}...{Style.RESET_ALL}")
        self.print_info("This may take 30 seconds to 5 minutes depending on model size")
        
        try:
            # Start loading process with proper encoding
            process = subprocess.Popen(
                [str(self.ollama_path), "run", model_name, "Hello"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            # Send a simple prompt to load the model with extended timeout
            try:
                stdout, stderr = process.communicate(input="\n", timeout=300)  # 5 minutes for large models
                
                # Check if model is now loaded
                time.sleep(3)  # Give more time for large models
                loaded = self.get_loaded_models()
                if model_name in [m['name'] for m in loaded]:
                    self.print_success(f"Successfully loaded {model_name}")
                    self.show_usage_instructions(model_name)
                    return True
                else:
                    self.print_error(f"Failed to load {model_name}")
                    if stderr:
                        self.print_error(f"Error: {stderr}")
                    return False
                    
            except subprocess.TimeoutExpired:
                process.kill()
                self.print_error("Loading timed out (5 minutes) - model may be too large")
                self.print_info("Try using a smaller model like phi:2.7b or mistral:7b")
                return False
                
        except Exception as e:
            self.print_error(f"Error loading model: {e}")
            return False

    def show_usage_instructions(self, model_name):
        """Show usage instructions for loaded model
        
        Args:
            model_name (str): Name of the loaded model
        """
        print(f"\n{Fore.GREEN}🐍 Python Usage Instructions:{Style.RESET_ALL}")
        print("Update your Python code to use this model:")
        print(f"{Fore.CYAN}")
        print("# In your main.py or other Python files:")
        print(f'response = query_ollama(prompt, model="{model_name}")')
        print(f"{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}💡 Important Reminders:{Style.RESET_ALL}")
        print("1. Update the model parameter in your Python scripts")
        print("2. Make sure Ollama server is running")
        print("3. Adjust timeout if needed for larger models")
        
        # Show model-specific tips
        if model_name == "phi:2.7b":
            print(f"\n{Fore.MAGENTA}📝 Phi 2.7B Tips:{Style.RESET_ALL}")
            print("• Fast responses, great for learning")
            print("• Use timeout=30 in requests")
            print("• Perfect for simple tasks and prototyping")
        elif model_name == "llama2:7b":
            print(f"\n{Fore.MAGENTA}📝 Llama2 7B Tips:{Style.RESET_ALL}")
            print("• Excellent general-purpose model")
            print("• Use timeout=120 in requests")
            print("• Great for complex reasoning and writing")
        elif model_name == "mistral:7b":
            print(f"\n{Fore.MAGENTA}📝 Mistral 7B Tips:{Style.RESET_ALL}")
            print("• Excellent efficiency and multilingual support")
            print("• Use timeout=120 in requests")
            print("• Great for European languages")
        elif model_name == "codellama:7b":
            print(f"\n{Fore.MAGENTA}📝 CodeLlama 7B Tips:{Style.RESET_ALL}")
            print("• Specialized for programming tasks")
            print("• Use timeout=120 in requests")
            print("• Specify programming language in prompts")
        elif model_name == "gpt-oss:20b":
            print(f"\n{Fore.MAGENTA}📝 GPT-OSS 20B Tips:{Style.RESET_ALL}")
            print("• Large model, slower but very capable")
            print("• Use timeout=300 in requests")
            print("• Consider streaming for long responses")

    def show_model_help_menu(self):
        """Show model help menu"""
        print(f"\n{Fore.MAGENTA}📚 Model Help & Documentation:{Style.RESET_ALL}")
        
        available_help = []
        for model_name, help_file in self.help_files.items():
            help_path = self.help_path / help_file
            if help_path.exists():
                available_help.append((model_name, help_file))
        
        if not available_help:
            self.print_warning("No help files found")
            return
        
        print("Available model documentation:")
        for i, (model_name, help_file) in enumerate(available_help, 1):
            print(f" {i}. {model_name} - Complete guide and examples")
        
        try:
            choice = input(f"\n{Fore.YELLOW}Select model for help (1-{len(available_help)}) or 0 to cancel: {Style.RESET_ALL}")
            choice = int(choice)
            
            if choice == 0:
                return
            
            if 1 <= choice <= len(available_help):
                model_name, help_file = available_help[choice - 1]
                self.show_model_help(model_name, help_file)
            else:
                self.print_error("Invalid choice")
        except ValueError:
            self.print_error("Invalid input")

    def show_model_help(self, model_name, help_file):
        """Show help for specific model
        
        Args:
            model_name (str): Name of the model
            help_file (str): Help file name
        """
        help_path = self.help_path / help_file
        
        if not help_path.exists():
            self.print_error(f"Help file not found: {help_file}")
            return
        
        try:
            with open(help_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"📚 {model_name.upper()} - Complete Guide")
            print(f"{'='*60}{Style.RESET_ALL}")
            print(content)
            
        except Exception as e:
            self.print_error(f"Error reading help file: {e}")

    def select_model_for_activation(self, default_model="phi:2.7b"):
        """Select model for Full Activation
        
        Args:
            default_model (str): Default model to suggest
            
        Returns:
            str: Selected model name or None if cancelled
        """
        installed = self.get_installed_models()
        if not installed:
            self.print_warning("No models installed")
            self.print_info("Proceeding without model loading")
            return None
        
        print(f"\n{Fore.MAGENTA}🤖 Select AI Model for Activation:{Style.RESET_ALL}")
        print("Available models:")
        
        default_index = None
        for i, model in enumerate(installed, 1):
            marker = "⭐ RECOMMENDED" if model['name'] == default_model else ""
            print(f" {i}. {model['name']} ({model['size']}) {marker}")
            if model['name'] == default_model:
                default_index = i
        
        print(f" 0. Skip model loading")
        
        try:
            if default_index:
                prompt = f"Select model (1-{len(installed)}, Enter for default #{default_index}): "
            else:
                prompt = f"Select model (1-{len(installed)}) or 0 to skip: "
            
            choice = input(f"\n{Fore.YELLOW}{prompt}{Style.RESET_ALL}")
            
            if choice == "":
                if default_index:
                    choice = default_index
                else:
                    return None
            else:
                choice = int(choice)
            
            if choice == 0:
                self.print_info("Skipping model loading")
                return None
            
            if 1 <= choice <= len(installed):
                model = installed[choice - 1]
                return model['name']
            else:
                self.print_error("Invalid choice")
                return None
                
        except ValueError:
            self.print_error("Invalid input")
            return None

