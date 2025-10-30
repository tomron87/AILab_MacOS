"""
AI Jupyter Lab Manager
Handles Jupyter Lab server management with full control

Version: 3.0.28
Author: AI Environment Team
Date: 2025-08-14 10:30
"""

import os
import socket
import subprocess
import time
import webbrowser
from pathlib import Path

# Try to import optional dependencies
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Try to import colorama, fallback if not available
try:
    from colorama import Fore, Style, init
    # Initialize colorama for Windows compatibility
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    # Fallback if colorama is not available
    class MockColor:
        GREEN = BLUE = MAGENTA = YELLOW = CYAN = RED = WHITE = ""
        RESET_ALL = ""
    
    Fore = MockColor()
    Style = MockColor()
    COLORAMA_AVAILABLE = False

class JupyterLabManager:
    """Manages Jupyter Lab server operations in AI2025 environment"""
    
    def __init__(self, ai_env_path, conda_path):
        """Initialize Jupyter Lab manager

        Args:
            ai_env_path (Path): Path to AI Environment directory
            conda_path (Path): Path to Miniconda installation
        """
        self.ai_env_path = Path(ai_env_path)
        self.conda_path = Path(conda_path)
        self.default_port = 8888
        self.server_tokens = {}  # Store tokens for each port
        
    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")
        
    def print_warning(self, message):
        """Print warning message"""
        print(f"{Fore.YELLOW}⚠️ {message}{Style.RESET_ALL}")
        
    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.CYAN}ℹ️ {message}{Style.RESET_ALL}")

    def extract_token_from_output(self, output, port):
        """Extract Jupyter token from server output

        Args:
            output (str): Server output text
            port (int): Port number to match

        Returns:
            str: Token string or None if not found
        """
        import re
        # Look for token in URLs like http://localhost:8888/?token=abc123 or http://localhost:8888/lab?token=abc123
        pattern = rf"http://[^:]+:{port}/?\S*\?token=([a-f0-9]+)"
        match = re.search(pattern, output)
        if match:
            return match.group(1)
        return None

    def show_menu(self):
        """Display Jupyter Lab management menu"""
        separator = "=" * 60
        print(f"\n{Fore.CYAN}{separator}")
        print(f"{Fore.CYAN}🔬 Jupyter Lab Management")
        print(f"{Fore.CYAN}{separator}{Style.RESET_ALL}")
        print(f" 1. {Fore.GREEN}🚀 Start Server Only{Style.RESET_ALL}")
        print(f" 2. {Fore.BLUE}🌐 Start Client Only{Style.RESET_ALL}")
        print(f" 3. {Fore.MAGENTA}⚡ Start Server + Client{Style.RESET_ALL}")
        print(f" 4. {Fore.YELLOW}🔧 Choose Custom Port{Style.RESET_ALL}")
        print(f" 5. {Fore.CYAN}📊 Check Server Status{Style.RESET_ALL}")
        print(f" 6. {Fore.RED}🛑 Stop Server{Style.RESET_ALL}")
        print(f" 0. {Fore.WHITE}⬅️ Back to Applications Menu{Style.RESET_ALL}")

    def start_server_only(self, port=None):
        """Start Jupyter Lab server only in AI2025 environment
        
        Args:
            port (int, optional): Port number to use. Defaults to 8888.
        """
        if port is None:
            port = self.default_port
            
        print(f"\n{Fore.BLUE}🚀 Starting Jupyter Lab Server on port {port}...{Style.RESET_ALL}")
        
        # Check if server is already running
        if self.is_server_running(port):
            self.print_success(f"Jupyter Lab server is already running on port {port}")
            self.print_info(f"Access at: http://localhost:{port}")
            return True
        
        # Set working directory to Projects folder
        projects_dir = self.ai_env_path / "Projects" / "01_Basic_LLM_Example"
        if not projects_dir.exists():
            # Create the directory if it doesn't exist
            projects_dir.mkdir(parents=True, exist_ok=True)
            self.print_info(f"Created projects directory: {projects_dir}")
        
        # Start server in AI2025 environment
        try:
            # Prepare command to run in AI2025 environment
            if os.name == "posix":  # macOS/Linux
                conda_path = self.conda_path / "bin" / "conda"
                if not conda_path.exists():
                    self.print_error(f"Conda not found at: {conda_path}")
                    return False
                    
                cmd = [
                    str(conda_path), "run", "-n", "AI2025",
                    "jupyter", "lab", "--no-browser", f"--port={port}",
                    "--allow-root", "--ip=0.0.0.0",
                    "--IdentityProvider.token=''"
                ]
            else:  # Linux/Mac
                cmd = [
                    "conda", "run", "-n", "AI2025",
                    "jupyter", "lab", "--no-browser", f"--port={port}",
                    "--allow-root", "--ip=0.0.0.0",
                    "--IdentityProvider.token=''"
                ]
            
            self.print_info(f"Starting Jupyter Lab with command: {' '.join(cmd[:3])}...")
            
            # Start process in background (non-blocking)
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(projects_dir),  # Start in projects directory
                # macOS: no special creation flags needed,
                stdin=subprocess.DEVNULL  # Prevent stdin interference
            )
            
            # Track the process immediately
            try:
                from ai_process_manager import BackgroundProcessManager
                process_manager = BackgroundProcessManager(self.ai_env_path)
                process_manager.track_process(
                    process_id=f"jupyter_lab_server_{port}",
                    name=f"Jupyter Lab Server (Port {port})",
                    pid=process.pid,
                    command=" ".join(cmd),
                    url=f"http://localhost:{port}"
                )
                self.print_info(f"Tracking Jupyter Lab server (PID: {process.pid})")
            except Exception as e:
                self.print_warning(f"Could not track Jupyter process: {e}")

            # Wait for server to start with retry mechanism
            self.print_info("Waiting for server to start...")
            max_wait_time = 15  # Maximum 15 seconds
            check_interval = 1  # Check every 1 second
            checks_performed = 0

            for attempt in range(max_wait_time):
                time.sleep(check_interval)
                checks_performed += 1

                if self.is_server_running(port):
                    self.print_success(f"Jupyter Lab server started successfully on port {port} (after {checks_performed} seconds)")
                    self.print_info(f"Working directory: {projects_dir}")
                    self.print_info(f"Access at: http://localhost:{port}/lab")

                    # Update tracked process URL
                    try:
                        process_manager.tracked_processes[f"jupyter_lab_server_{port}"]['url'] = f"http://localhost:{port}/lab"
                        process_manager.save_tracked_processes()
                    except Exception:
                        pass

                    return True

                # Show progress dots
                if attempt % 3 == 0:
                    print(f"{Fore.YELLOW}.{Style.RESET_ALL}", end="", flush=True)

            print()  # New line after dots
            
            # Final check - server might be starting but not ready yet
            self.print_warning(f"Server not accessible on port {port} after {max_wait_time} seconds")
            
            # Try to get error output from the process
            try:
                stdout, stderr = process.communicate(timeout=2)
                if stderr:
                    error_msg = stderr.decode().strip()
                    if error_msg:
                        self.print_error(f"Error details: {error_msg}")
                if stdout:
                    output_msg = stdout.decode().strip()
                    if output_msg:
                        self.print_info(f"Output: {output_msg}")
            except subprocess.TimeoutExpired:
                self.print_info("Server process is still running, but port not accessible")
                self.print_info("The server might still be initializing - try checking status in a moment")
            except Exception as comm_error:
                self.print_warning(f"Could not get process output: {comm_error}")
            
            return False
                
        except FileNotFoundError as e:
            self.print_error(f"Command not found: {e}")
            self.print_info("Make sure conda and AI2025 environment are properly installed")
            return False
        except Exception as e:
            self.print_error(f"Error starting Jupyter Lab server: {e}")
            return False

    def start_client_only(self, port=None):
        """Start Jupyter Lab client only (open browser)

        Args:
            port (int, optional): Port number to connect to. Defaults to 8888.
        """
        if port is None:
            port = self.default_port

        print(f"\n{Fore.BLUE}🌐 Opening Jupyter Lab Client...{Style.RESET_ALL}")

        # Check if server is running
        if not self.is_server_running(port):
            self.print_warning(f"Jupyter Lab server is not running on port {port}!")
            self.print_info("Please start the server first (option 1 or 3)")
            return False

        # Open browser to Jupyter Lab (no authentication required)
        try:
            url = f"http://localhost:{port}/lab"
            webbrowser.open(url)
            self.print_success("Jupyter Lab client opened in browser")
            self.print_info(f"URL: {url}")
            return True
        except Exception as e:
            self.print_error(f"Failed to open browser: {e}")
            self.print_info(f"Please manually open: http://localhost:{port}/lab")
            return False

    def start_server_and_client(self, port=None):
        """Start both Jupyter Lab server and client
        
        Args:
            port (int, optional): Port number to use. Defaults to 8888.
        """
        if port is None:
            port = self.default_port
            
        print(f"\n{Fore.MAGENTA}⚡ Starting Jupyter Lab Server + Client...{Style.RESET_ALL}")
        
        # Check if server is already running
        if self.is_server_running(port):
            self.print_info(f"Server already running on port {port}, opening client...")
            return self.start_client_only(port)
        
        # Start server first
        server_started = self.start_server_only(port)
        
        if server_started:
            # Wait for server to fully start with timeout
            self.print_info("Waiting for server to fully initialize...")
            max_wait = 10  # Maximum 10 seconds
            wait_time = 0
            
            while wait_time < max_wait:
                time.sleep(1)
                wait_time += 1
                if self.is_server_running(port):
                    self.print_success("Server is ready!")
                    break
                print(f"{Fore.YELLOW}.{Style.RESET_ALL}", end="", flush=True)
            
            print()  # New line after dots
            
            # Check if server is actually running
            if self.is_server_running(port):
                # Then start client
                return self.start_client_only(port)
            else:
                self.print_error("Server failed to start properly")
                return False
        else:
            self.print_error("Failed to start server")
            return False

    def choose_custom_port(self):
        """Allow user to choose custom port for Jupyter Lab"""
        print(f"\n{Fore.YELLOW}🔧 Choose Custom Port for Jupyter Lab{Style.RESET_ALL}")
        
        try:
            port_input = input(f"\n{Fore.CYAN}Enter port number (default 8888): {Style.RESET_ALL}").strip()
            if not port_input:
                port = 8888
            else:
                port = int(port_input)
            
            if port < 1024 or port > 65535:
                self.print_error("Port must be between 1024 and 65535")
                return
            
            # Check if port is in use
            if self.is_port_in_use(port):
                self.print_warning(f"Port {port} is already in use")
                return
            
            # Start server on custom port
            server_started = self.start_server_only(port)
            
            if server_started:
                # Ask if user wants to open browser
                open_browser = input(f"\n{Fore.CYAN}Open in browser? (y/n): {Style.RESET_ALL}").lower()
                if open_browser == "y":
                    self.start_client_only(port)
            
        except ValueError:
            self.print_error("Invalid port number")
        except Exception as e:
            self.print_error(f"Error with custom port: {e}")

    def check_server_status(self):
        """Check Jupyter Lab server status"""
        print(f"\n{Fore.CYAN}📊 Checking Jupyter Lab Server Status...{Style.RESET_ALL}")
        
        # Check if server is running on default port
        if self.is_server_running(self.default_port):
            self.print_success(f"Jupyter Lab server is running on port {self.default_port}")
            self.print_info(f"Access at: http://localhost:{self.default_port}")
        else:
            self.print_info(f"Jupyter Lab server is not running on port {self.default_port}")
        
        # Check for servers on other common ports
        common_ports = [8889, 8890, 8891, 8892]
        running_ports = []
        
        for port in common_ports:
            if self.is_server_running(port):
                running_ports.append(port)
        
        if running_ports:
            self.print_info(f"Found Jupyter servers on ports: {', '.join(map(str, running_ports))}")
            for port in running_ports:
                self.print_info(f"  - http://localhost:{port}")
        
        if not self.is_server_running(self.default_port) and not running_ports:
            self.print_info("No Jupyter Lab servers found running")

    def stop_server(self):
        """Stop Jupyter Lab server"""
        print(f"\n{Fore.RED}🛑 Stopping Jupyter Lab Server...{Style.RESET_ALL}")
        
        stopped_any = False
        
        # Try to stop servers on common ports
        common_ports = [8888, 8889, 8890, 8891, 8892]
        
        for port in common_ports:
            if self.is_server_running(port):
                self.print_info(f"Found server running on port {port}, stopping...")
                if self._stop_server_on_port(port):
                    stopped_any = True
                    
                    # Wait a moment and verify it stopped
                    time.sleep(2)
                    if not self.is_server_running(port):
                        self.print_success(f"Successfully stopped server on port {port}")
                    else:
                        self.print_warning(f"Server on port {port} may still be running")
        
        if not stopped_any:
            self.print_info("No running Jupyter Lab servers found")
        else:
            self.print_success("Server shutdown process completed")

    def is_server_running(self, port=None):
        """Check if Jupyter Lab is running on specified port
        
        Args:
            port (int, optional): Port to check. Defaults to default_port.
            
        Returns:
            bool: True if server is running, False otherwise
        """
        if port is None:
            port = self.default_port
            
        return self.is_port_in_use(port)

    def is_port_in_use(self, port):
        """Check if a port is in use
        
        Args:
            port (int): Port number to check
            
        Returns:
            bool: True if port is in use, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except:
            return False

    def _stop_server_on_port(self, port):
        """Stop Jupyter server on specific port
        
        Args:
            port (int): Port number
            
        Returns:
            bool: True if stopped successfully, False otherwise
        """
        try:
            # Try graceful shutdown first if requests is available
            if REQUESTS_AVAILABLE:
                try:
                    import requests
                    response = requests.post(
                        f"http://localhost:{port}/api/shutdown",
                        timeout=5
                    )
                    if response.status_code == 200:
                        self.print_success(f"Gracefully shut down server on port {port}")
                        return True
                except:
                    pass  # Fall back to process killing
            
            # Fall back to killing processes on the port
            if PSUTIL_AVAILABLE:
                import psutil
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        connections = proc.connections()
                        if connections:
                            for conn in connections:
                                if conn.laddr.port == port:
                                    proc.terminate()
                                    proc.wait(timeout=3)
                                    self.print_success(f"Terminated process {proc.info['name']} (PID: {proc.info['pid']}) on port {port}")
                                    return True
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
            else:
                # Windows fallback using netstat and taskkill
                if os.name == "nt":
                    try:
                        # Find PID using netstat
                        result = subprocess.run(
                            ["netstat", "-ano", "-p", "TCP"],
                            capture_output=True,
                            text=True
                        )
                        lines = result.stdout.split('\n')
                        for line in lines:
                            if f":{port}" in line and "LISTENING" in line:
                                parts = line.split()
                                if len(parts) >= 5:
                                    pid = parts[-1]
                                    try:
                                        subprocess.run(
                                            ["kill", "/F", "/PID", pid],
                                            check=True,
                                            capture_output=True
                                        )
                                        self.print_success(f"Killed process {pid} on port {port}")
                                        return True
                                    except subprocess.CalledProcessError:
                                        continue
                    except Exception:
                        pass
            
            self.print_error(f"Could not stop server on port {port}")
            return False
            
        except Exception as e:
            self.print_error(f"Error stopping server on port {port}: {e}")
            return False