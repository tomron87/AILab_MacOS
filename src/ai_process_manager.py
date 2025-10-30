# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.17
Date: 2025-08-13
Time: 05:30
"""

#!/usr/bin/env python3
"""
AI Environment - Background Process Manager
Tracks and controls all background processes launched from the menu with enhanced VS Code integration
"""

import subprocess
import time
import json
from pathlib import Path
from datetime import datetime

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
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = ""
    class Style:
        RESET_ALL = ""

class BackgroundProcessManager:
    """Manages all background processes launched from the AI Environment menu"""
    
    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)
        self.processes_file = self.ai_env_path / "background_processes.json"
        self.tracked_processes = {}
        self.load_tracked_processes()
        
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
        
    def load_tracked_processes(self):
        """Load tracked processes from file"""
        try:
            if self.processes_file.exists():
                with open(self.processes_file, 'r') as f:
                    data = json.load(f)
                    self.tracked_processes = data
                    # Clean up dead processes
                    self.cleanup_dead_processes()
        except Exception as e:
            self.print_warning(f"Could not load process tracking file: {e}")
            self.tracked_processes = {}
            
    def save_tracked_processes(self):
        """Save tracked processes to file"""
        try:
            with open(self.processes_file, 'w') as f:
                json.dump(self.tracked_processes, f, indent=2)
        except Exception as e:
            self.print_warning(f"Could not save process tracking file: {e}")
            
    def cleanup_dead_processes(self):
        """Remove dead processes from tracking"""
        dead_processes = []
        for process_id, process_info in self.tracked_processes.items():
            try:
                pid = process_info['pid']
                if not psutil.pid_exists(pid):
                    dead_processes.append(process_id)
            except:
                dead_processes.append(process_id)
                
        for process_id in dead_processes:
            del self.tracked_processes[process_id]
            
        if dead_processes:
            self.save_tracked_processes()
            
    def track_process(self, process_id, name, pid, command, url=None):
        """Track a background process"""
        try:
            from datetime import datetime

            # Verify process exists before tracking
            if PSUTIL_AVAILABLE:
                if not psutil.pid_exists(pid):
                    self.print_error(f"Process {name} (PID: {pid}) is not running")
                    return False

            process_info = {
                'name': name,
                'pid': pid,
                'command': command,
                'started_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'running'
            }

            if url:
                process_info['url'] = url

            self.tracked_processes[process_id] = process_info
            self.save_tracked_processes()
            self.print_success(f"Tracking process: {name} (PID: {pid})")
            return True

        except Exception as e:
            self.print_warning(f"Could not track process {name}: {e}")
            return False
            
    def untrack_process(self, process_id):
        """Stop tracking a background process"""
        try:
            if process_id in self.tracked_processes:
                process_info = self.tracked_processes[process_id]
                del self.tracked_processes[process_id]
                self.save_tracked_processes()
                self.print_success(f"Stopped tracking: {process_info['name']}")
                return True
            else:
                self.print_warning(f"Process {process_id} not found in tracking")
                return False
        except Exception as e:
            self.print_warning(f"Could not untrack process {process_id}: {e}")
            return False
            
    def generate_process_id(self, app_name):
        """Generate unique process ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{app_name}_{timestamp}"
        
    def launch_vscode(self, project_path=None):
        """Launch VS Code in background with proper AI2025 interpreter setup"""
        try:
            vscode_exe = "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
            if not vscode_exe.exists():
                self.print_error(f"VS Code not found at {vscode_exe}")
                return False
            
            # Default to Basic LLM Example project
            if project_path is None:
                project_path = self.ai_env_path / "Projects" / "01_Basic_LLM_Example"
                project_path.mkdir(parents=True, exist_ok=True)
                
                # Create main.py if it doesn't exist
                main_py = project_path / "main.py"
                if not main_py.exists():
                    self._create_basic_main_py(main_py)
            
            # Setup VS Code workspace with AI2025 interpreter
            self._setup_vscode_workspace(project_path)
            
            cmd = [str(vscode_exe)]
            cmd.append(str(project_path))
            
            # Open main.py directly if it exists
            main_py = project_path / "main.py"
            if main_py.exists():
                cmd.append(str(main_py))
                
            self.print_info("Launching VS Code with AI2025 interpreter setup...")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                # macOS: no special creation flags needed
            )
            
            # Track the process
            process_id = self.generate_process_id("vscode")
            self.tracked_processes[process_id] = {
                'pid': process.pid,
                'name': 'VS Code',
                'command': ' '.join(cmd),
                'started_at': datetime.now().isoformat(),
                'type': 'application',
                'project_path': str(project_path)
            }
            
            self.save_tracked_processes()
            self.print_success(f"VS Code launched successfully (PID: {process.pid})")
            self.print_info(f"Project: {project_path}")
            self.print_info("Configured with AI2025 Python interpreter")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to launch VS Code: {e}")
            return False
    
    def _create_basic_main_py(self, main_py_path):
        """Create a basic main.py file for testing Ollama"""
        content = '''"""
Basic LLM Example - Test Ollama Connection
Make sure Ollama is running: ollama serve
"""

import requests
import json

def query_ollama(prompt, model="phi:2.7b", host="127.0.0.1", port=11434):
    """Query Ollama API"""
    url = f"http://{host}:{port}/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "No response received")
        
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    print("Basic LLM Example")
    print("Make sure Ollama is running: ollama serve")
    print()
    
    # Test prompt
    prompt = "Explain artificial intelligence in simple terms"
    print(f"Question: {prompt}")
    print("Thinking...")
    
    # Query Ollama
    response = query_ollama(prompt)
    print(f"AI Response: {response}")

if __name__ == "__main__":
    main()
'''
        
        try:
            with open(main_py_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            self.print_error(f"Failed to create main.py: {e}")
    
    def _setup_vscode_workspace(self, project_path):
        """Setup VS Code workspace with AI2025 interpreter"""
        try:
            # Create .vscode directory
            vscode_dir = project_path / ".vscode"
            vscode_dir.mkdir(exist_ok=True)
            
            # Python interpreter path
            python_path = self.ai_env_path / "Miniconda" / "envs" / "AI2025" / "python"
            
            # Create settings.json
            settings = {
                "python.defaultInterpreterPath": str(python_path).replace("\\", "/"),
                "python.terminal.activateEnvironment": True,
                "python.terminal.activateEnvInCurrentTerminal": True,
                "terminal.integrated.env.windows": {
                    "CONDA_DEFAULT_ENV": "AI2025",
                    "CONDA_PREFIX": str(self.ai_env_path / "Miniconda" / "envs" / "AI2025").replace("\\", "/")
                },
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": False,
                "python.linting.flake8Enabled": True,
                "python.formatting.provider": "black",
                "files.autoSave": "afterDelay",
                "files.autoSaveDelay": 1000
            }
            
            settings_file = vscode_dir / "settings.json"
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
            
            # Create launch.json for debugging
            launch_config = {
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "Python: Current File",
                        "type": "python",
                        "request": "launch",
                        "program": "${file}",
                        "console": "integratedTerminal",
                        "python": str(python_path).replace("\\", "/"),
                        "env": {
                            "CONDA_DEFAULT_ENV": "AI2025"
                        }
                    },
                    {
                        "name": "Python: main.py",
                        "type": "python", 
                        "request": "launch",
                        "program": "${workspaceFolder}/main.py",
                        "console": "integratedTerminal",
                        "python": str(python_path).replace("\\", "/"),
                        "env": {
                            "CONDA_DEFAULT_ENV": "AI2025"
                        }
                    }
                ]
            }
            
            launch_file = vscode_dir / "launch.json"
            with open(launch_file, 'w', encoding='utf-8') as f:
                json.dump(launch_config, f, indent=2)
                
            self.print_success("VS Code workspace configured with AI2025 interpreter")
            
        except Exception as e:
            self.print_error(f"Failed to setup VS Code workspace: {e}")
            
    def launch_jupyter(self):
        """Launch Jupyter Lab in background"""
        try:
            self.print_info("Launching Jupyter Lab in background...")
            
            # Set working directory to Projects folder
            work_dir = self.ai_env_path / "Projects"
            work_dir.mkdir(exist_ok=True)
            
            process = subprocess.Popen(
                ['jupyter', 'lab', '--no-browser', '--port=8888'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=str(work_dir),
                # macOS: no special creation flags needed
            )
            
            # Track the process
            process_id = self.generate_process_id("jupyter")
            self.tracked_processes[process_id] = {
                'pid': process.pid,
                'name': 'Jupyter Lab',
                'command': 'jupyter lab --no-browser --port=8888',
                'started_at': datetime.now().isoformat(),
                'type': 'web_service',
                'url': 'http://localhost:8888'
            }
            
            self.save_tracked_processes()
            self.print_success(f"Jupyter Lab launched successfully (PID: {process.pid})")
            self.print_info("Access Jupyter Lab at: http://localhost:8888")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to launch Jupyter Lab: {e}")
            return False
            
    def launch_streamlit_demo(self):
        """Launch Streamlit demo app in background"""
        try:
            # Check for existing Streamlit processes and kill them
            import psutil
            for proc_id, proc_info in list(self.tracked_processes.items()):
                if 'streamlit' in proc_id.lower() and proc_info.get('type') == 'web_service':
                    try:
                        pid = proc_info.get('pid')
                        if pid and psutil.pid_exists(pid):
                            self.print_info(f"Stopping existing Streamlit process (PID: {pid})...")
                            psutil.Process(pid).terminate()
                            time.sleep(1)  # Give it time to terminate
                        # Remove from tracking
                        del self.tracked_processes[proc_id]
                    except Exception:
                        pass
            self.save_tracked_processes()

            # Create a simple demo app if it doesn't exist
            demo_file = self.ai_env_path / "Projects" / "streamlit_demo.py"
            if not demo_file.exists():
                demo_content = '''import streamlit as st
import pandas as pd
import numpy as np

st.title("AI Environment Demo")
st.write("Welcome to your portable AI development environment!")

# Sample data
data = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100)
})

st.subheader("Sample Chart")
st.line_chart(data)

st.subheader("Sample Data")
st.dataframe(data.head())
'''
                demo_file.parent.mkdir(exist_ok=True)
                with open(demo_file, 'w') as f:
                    f.write(demo_content)
                    
            self.print_info("Launching Streamlit demo in background...")
            
            process = subprocess.Popen(
                ['streamlit', 'run', str(demo_file), '--server.port=8501'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                # macOS: no special creation flags needed
            )
            
            # Track the process
            process_id = self.generate_process_id("streamlit")
            self.tracked_processes[process_id] = {
                'pid': process.pid,
                'name': 'Streamlit Demo',
                'command': f'streamlit run {demo_file} --server.port=8501',
                'started_at': datetime.now().isoformat(),
                'type': 'web_service',
                'url': 'http://localhost:8501'
            }
            
            self.save_tracked_processes()
            self.print_success(f"Streamlit demo launched successfully (PID: {process.pid})")
            self.print_info("Access Streamlit demo at: http://localhost:8501")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to launch Streamlit demo: {e}")
            return False
            
    def launch_custom_command(self, command, name, work_dir=None):
        """Launch custom command in background"""
        try:
            self.print_info(f"Launching {name} in background...")
            
            if work_dir is None:
                work_dir = self.ai_env_path
                
            process = subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=str(work_dir),
                shell=True,
                # macOS: no special creation flags needed
            )
            
            # Track the process
            process_id = self.generate_process_id(name.lower().replace(' ', '_'))
            self.tracked_processes[process_id] = {
                'pid': process.pid,
                'name': name,
                'command': command,
                'started_at': datetime.now().isoformat(),
                'type': 'custom'
            }
            
            self.save_tracked_processes()
            self.print_success(f"{name} launched successfully (PID: {process.pid})")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to launch {name}: {e}")
            return False
            
    def list_background_processes(self):
        """List all tracked background processes"""
        self.cleanup_dead_processes()
        
        if not self.tracked_processes:
            self.print_info("No background processes currently running")
            return
            
        print(f"\n{Fore.CYAN}🔄 Background Processes:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        for process_id, process_info in self.tracked_processes.items():
            try:
                pid = process_info['pid']
                proc = psutil.Process(pid)
                
                status = proc.status()
                cpu_percent = proc.cpu_percent()
                memory_mb = round(proc.memory_info().rss / 1024 / 1024, 1)
                
                print(f"\n{Fore.YELLOW}ID: {process_id}{Style.RESET_ALL}")
                print(f"  Name: {process_info['name']}")
                print(f"  PID: {pid}")
                print(f"  Status: {status}")
                print(f"  CPU: {cpu_percent}%")
                print(f"  Memory: {memory_mb} MB")
                print(f"  Started: {process_info['started_at']}")
                print(f"  Command: {process_info['command']}")
                
                if 'url' in process_info:
                    print(f"  URL: {process_info['url']}")
                    
            except psutil.NoSuchProcess:
                print(f"\n{Fore.RED}ID: {process_id} (DEAD){Style.RESET_ALL}")
                print(f"  Name: {process_info['name']}")
                print(f"  Status: Process no longer exists")
                
    def stop_process(self, process_id):
        """Stop a specific background process"""
        if process_id not in self.tracked_processes:
            self.print_error(f"Process ID '{process_id}' not found")
            return False
            
        process_info = self.tracked_processes[process_id]
        
        try:
            pid = process_info['pid']
            proc = psutil.Process(pid)
            
            self.print_info(f"Stopping {process_info['name']} (PID: {pid})...")
            
            # Try graceful termination first
            proc.terminate()
            
            # Wait for graceful shutdown
            try:
                proc.wait(timeout=5)
                self.print_success(f"{process_info['name']} stopped gracefully")
            except psutil.TimeoutExpired:
                # Force kill if graceful shutdown fails
                self.print_warning("Graceful shutdown failed, force killing...")
                proc.kill()
                proc.wait(timeout=3)
                self.print_success(f"{process_info['name']} force killed")
                
            # Remove from tracking
            del self.tracked_processes[process_id]
            self.save_tracked_processes()
            return True
            
        except psutil.NoSuchProcess:
            self.print_warning(f"Process {process_info['name']} was already dead")
            del self.tracked_processes[process_id]
            self.save_tracked_processes()
            return True
        except Exception as e:
            self.print_error(f"Failed to stop {process_info['name']}: {e}")
            return False
            
    def stop_all_processes(self):
        """Stop all tracked background processes"""
        if not self.tracked_processes:
            self.print_info("No background processes to stop")
            return True
            
        self.print_info("Stopping all background processes...")
        
        success_count = 0
        total_count = len(self.tracked_processes)
        
        # Create a copy of the keys to avoid dictionary size change during iteration
        process_ids = list(self.tracked_processes.keys())
        
        for process_id in process_ids:
            if self.stop_process(process_id):
                success_count += 1
                
        self.print_success(f"Stopped {success_count}/{total_count} processes")
        return success_count == total_count
        
    def get_process_count(self):
        """Get count of running background processes"""
        self.cleanup_dead_processes()
        return len(self.tracked_processes)

def main():
    """Test background process manager"""
    from ai_path_finder import find_ai_environment

    ai_env_path = find_ai_environment(verbose=True)
    if not ai_env_path:
        print(f"{Fore.RED}AI_Environment not found on any drive!{Style.RESET_ALL}")
        return

    process_manager = BackgroundProcessManager(ai_env_path)

    print("Testing Background Process Manager...")
    process_manager.list_background_processes()

if __name__ == "__main__":
    main()

