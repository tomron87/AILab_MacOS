# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.18
Date: 2025-08-13
"""

#!/usr/bin/env python3
"""
AI Environment - Ollama Management Module (macOS Version)
Handles Ollama server lifecycle and control
"""

import subprocess
import time
from pathlib import Path

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("[WARNING] psutil not available - some process management features will be limited")

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = ""
    class Style:
        RESET_ALL = ""

class OllamaManager:
    """Manages Ollama server lifecycle and operations on macOS"""

    def __init__(self, ai_env_path, ollama_path=None):
        self.ai_env_path = Path(ai_env_path)
        # Use provided ollama_path or find using ai_path_finder
        if ollama_path is None:
            try:
                from ai_path_finder import find_ollama
                ollama_path = find_ollama()
                if not ollama_path:
                    # Fallback to common macOS locations
                    ollama_path = Path("/Applications/Ollama.app/Contents/MacOS/ollama")
            except ImportError:
                # Fallback to common macOS locations
                ollama_path = Path("/Applications/Ollama.app/Contents/MacOS/ollama")

        self.ollama_exe = Path(ollama_path)
        self.process = None

    def find_models_directory(self):
        """Find Ollama models directory using multiple detection methods

        Returns:
            Path: Path to models directory, or None if not found
        """
        # Check multiple possible locations in priority order
        possible_paths = [
            self.ai_env_path / "AI_Environment" / "Models",        # Inside AI_Environment subfolder (check first)
            self.ai_env_path / "Models",                           # Direct in AI_Lab
            self.ai_env_path.parent / "AI_Environment" / "Models", # Sibling directory
            Path.home() / ".ollama" / "models",                    # Default macOS location
        ]

        for path in possible_paths:
            if path.exists() and path.is_dir():
                # Verify this directory actually contains models by checking for blobs
                blobs_dir = path / "blobs"
                if blobs_dir.exists() and any(blobs_dir.iterdir()):
                    return path

        # If no existing directory with models found, check for any existing empty directories
        for path in possible_paths:
            if path.exists() and path.is_dir():
                return path

        # If no existing directory found, create in AI_Environment subfolder
        default_path = self.ai_env_path / "AI_Environment" / "Models"
        default_path.mkdir(parents=True, exist_ok=True)
        return default_path

    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")

    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")

    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")

    def print_warning(self, message):
        """Print warning message"""
        print(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")

    def check_ollama_exists(self):
        """Check if Ollama executable exists"""
        if not self.ollama_exe.exists():
            self.print_error(f"Ollama not found at {self.ollama_exe}")
            return False
        return True

    def get_ollama_processes(self):
        """Get all running Ollama processes"""
        if not PSUTIL_AVAILABLE:
            return []

        ollama_processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if proc.info['name'] and 'ollama' in proc.info['name'].lower():
                    ollama_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        return ollama_processes

    def is_ollama_running(self):
        """Check if Ollama server is running"""
        processes = self.get_ollama_processes()
        return len(processes) > 0

    def get_ollama_status(self):
        """Get detailed Ollama server status"""
        processes = self.get_ollama_processes()

        if not processes:
            return {
                'running': False,
                'process_count': 0,
                'processes': []
            }

        process_info = []
        for proc in processes:
            try:
                info = {
                    'pid': proc.pid,
                    'name': proc.name(),
                    'status': proc.status(),
                    'cpu_percent': proc.cpu_percent(),
                    'memory_mb': round(proc.memory_info().rss / 1024 / 1024, 1),
                    'create_time': time.strftime('%H:%M:%S', time.localtime(proc.create_time()))
                }
                process_info.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return {
            'running': True,
            'process_count': len(processes),
            'processes': process_info
        }

    def start_ollama_server(self):
        """Start Ollama server in background"""
        try:
            if not self.check_ollama_exists():
                return False

            if self.is_ollama_running():
                self.print_warning("Ollama server is already running")
                return True

            self.print_info("Starting Ollama server in background...")

            # Find and set models directory
            models_path = self.find_models_directory()
            self.print_info(f"Using models directory: {models_path}")

            # Prepare environment with OLLAMA_MODELS variable
            import os
            env = os.environ.copy()
            env['OLLAMA_MODELS'] = str(models_path)

            # Start Ollama server as background process
            self.process = subprocess.Popen(
                [str(self.ollama_exe), 'serve'],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Wait for server to start
            self.print_info("Waiting for server to initialize...")
            for i in range(10):  # Wait up to 10 seconds
                time.sleep(1)
                if self.is_ollama_running():
                    status = self.get_ollama_status()
                    pid = status['processes'][0]['pid']
                    self.print_success(f"Ollama server started successfully (PID: {pid})")

                    # Track the process
                    try:
                        from ai_process_manager import BackgroundProcessManager
                        process_manager = BackgroundProcessManager(self.ai_env_path)
                        process_manager.track_process(
                            process_id="ollama_server",
                            name="Ollama Server",
                            pid=pid,
                            command=f"{self.ollama_exe} serve",
                            url="http://127.0.0.1:11434"
                        )
                    except Exception as e:
                        self.print_warning(f"Could not track Ollama process: {e}")

                    return True

            self.print_error("Ollama server failed to start within timeout")
            return False

        except Exception as e:
            self.print_error(f"Failed to start Ollama server: {e}")
            return False

    def stop_ollama_server(self):
        """Stop Ollama server"""
        try:
            processes = self.get_ollama_processes()

            if not processes:
                self.print_warning("Ollama server is not running")
                return True

            self.print_info(f"Stopping {len(processes)} Ollama process(es)...")

            # Try graceful shutdown first
            for proc in processes:
                try:
                    proc.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Wait for graceful shutdown
            time.sleep(3)

            # Force kill if still running
            remaining_processes = self.get_ollama_processes()
            if remaining_processes:
                self.print_warning("Force killing remaining Ollama processes...")
                for proc in remaining_processes:
                    try:
                        proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                time.sleep(1)

            # Verify shutdown
            if not self.is_ollama_running():
                self.print_success("Ollama server stopped successfully")
                return True
            else:
                self.print_error("Failed to stop all Ollama processes")
                return False

        except Exception as e:
            self.print_error(f"Failed to stop Ollama server: {e}")
            return False

    def restart_ollama_server(self):
        """Restart Ollama server"""
        self.print_info("Restarting Ollama server...")

        if not self.stop_ollama_server():
            return False

        time.sleep(2)  # Brief pause between stop and start

        return self.start_ollama_server()

    def show_ollama_status(self):
        """Display detailed Ollama status"""
        status = self.get_ollama_status()

        print(f"\n{Fore.CYAN}🦙 Ollama Server Status:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}")

        if not status['running']:
            print(f"{Fore.RED}Status: Not Running{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Use option 6 to start Ollama server{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Status: Running{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Process Count: {status['process_count']}{Style.RESET_ALL}")

            for i, proc in enumerate(status['processes'], 1):
                print(f"\n{Fore.CYAN}Process {i}:{Style.RESET_ALL}")
                print(f"  PID: {proc['pid']}")
                print(f"  Name: {proc['name']}")
                print(f"  Status: {proc['status']}")
                print(f"  CPU: {proc['cpu_percent']}%")
                print(f"  Memory: {proc['memory_mb']} MB")
                print(f"  Started: {proc['create_time']}")

        return status['running']

    def list_available_models(self):
        """List available AI models"""
        try:
            if not self.is_ollama_running():
                self.print_error("Ollama server is not running")
                return False

            self.print_info("Fetching available models...")

            result = subprocess.run(
                [str(self.ollama_exe), 'list'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    print(f"\n{Fore.CYAN}🤖 Available AI Models:{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
                    print(output)
                else:
                    self.print_warning("No models are currently installed")
                    self.print_info("Use option 7 to download AI models")
                return True
            else:
                self.print_error(f"Failed to list models: {result.stderr}")
                return False

        except Exception as e:
            self.print_error(f"Failed to list models: {e}")
            return False

    def test_ollama_connection(self):
        """Test Ollama server connection"""
        try:
            if not self.is_ollama_running():
                self.print_error("Ollama server is not running")
                return False

            self.print_info("Testing Ollama server connection...")

            # Try to get version info
            result = subprocess.run(
                [str(self.ollama_exe), '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                self.print_success(f"Ollama server is responsive - {version}")
                return True
            else:
                self.print_error("Ollama server is not responding")
                return False

        except Exception as e:
            self.print_error(f"Connection test failed: {e}")
            return False

def main():
    """Test Ollama manager"""
    from ai_path_finder import find_ai_environment

    ai_env_path = find_ai_environment(verbose=True)
    if not ai_env_path:
        print("AI_Environment not found on any drive!")
        return

    ollama_manager = OllamaManager(ai_env_path)

    print("Testing Ollama Manager...")
    ollama_manager.show_ollama_status()

if __name__ == "__main__":
    main()
