# AI Environment Python System v3.0.28 - macOS Edition (UV Version)

**A portable, modular AI development environment for macOS with UV-based Python management**

> **Note:** This repository is adapted from the original Windows version: [https://github.com/rmisegal/AILab](https://github.com/rmisegal/AILab)
>
> **Key Difference:** Unlike the original Windows version which uses Conda for environment management, this macOS edition uses **UV** - a modern, blazingly fast Python package installer and environment manager written in Rust. This provides 10-100x faster package installation and significantly smaller environment footprints.
>
> This macOS edition also features native Terminal.app integration, macOS application support, bash-based launcher scripts, and full compatibility with the original system architecture.

---

## 📋 **Overview**

The AI Environment Python System for macOS is a comprehensive, self-contained development environment designed for AI and machine learning work. It provides an interactive menu-driven interface for managing Python environments (via UV), AI models (via Ollama), Jupyter Lab, VS Code, and various development tools - all from a portable installation optimized for macOS.

This is the macOS adaptation of the Windows AI Environment system, featuring:
- Native macOS Terminal.app integration
- Standard macOS application support (Ollama.app, VS Code.app)
- Modern UV environment management for faster, more reliable dependency handling
- Bash-based launcher scripts
- External drive compatibility (works on /Volumes/)
- Support for Apple Silicon and Intel Macs

---

## ⚠️ **Prerequisites**

Before using this system, you **must** install the required components and configure the base environment.

### **Required Software:**

1. **Python 3.11 or higher**
   - Check your installed Python version:
     ```bash
     python3 --version
     ```
   - If you don't have Python installed or need a specific version:
     ```bash
     # Install via Homebrew (recommended)
     brew install python@3.11
     # Or for the latest version
     brew install python@3.13

     # Verify installation
     python3 --version
     ```
   - **Note:** This system requires Python 3.11 or higher. If UV cannot download the requested Python version due to network issues, use any installed Python 3.11+ version by running `uv venv --python 3.13` (or whichever version you have installed)

2. **UV** (Fast Python package installer and environment manager)
   - Install via curl:
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - Or via Homebrew:
     ```bash
     brew install uv
     ```
   - Documentation: https://github.com/astral-sh/uv

2. **Ollama** (Local AI model server)
   - Download from: https://ollama.ai
   - Install the macOS application (installs to `/Applications/Ollama.app`)
   - The system will automatically detect the standard installation
   - Alternative: Install portable version in `AI_Environment/Ollama` (advanced users)

3. **VS Code** (Code editor - optional but recommended)
   - Download from: https://code.visualstudio.com/
   - Install to `/Applications/Visual Studio Code.app`
   - Install the `code` command in PATH: Open VS Code → Command Palette (⌘⇧P) → "Shell Command: Install 'code' command in PATH"

---

## 🚀 **Quick Start Installation**

### **Step 1: Clone or Download AILab-Mac**

```bash
cd ~/Developer
git clone <repository-url> AILab-Mac
cd AILab-Mac
```

### **Step 2: Make Scripts Executable**

**IMPORTANT:** After cloning from GitHub, you must make the shell scripts executable:

```bash
chmod +x run_ai_env.sh setup_python_env.sh
```

### **Step 3: Check Python and Install UV**

First, verify you have Python 3.11 or higher installed:

```bash
# Check Python version
python3 --version

# If you don't have Python or need a newer version:
brew install python@3.13  # or python@3.11
```

Then install UV (the fast Python package installer):

```bash
# Via curl (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew
brew install uv

# Verify installation
uv --version
```

### **Step 4: Create UV Virtual Environment**

The virtual environment will be created automatically when you first run the system, or you can create it manually:

```bash
cd ~/Developer/AILab-Mac

# Check which Python versions you have installed
python3 --version
ls /usr/local/bin/python* 2>/dev/null | grep python3

# Create virtual environment with Python 3.11 or higher
# Use whichever version you have installed (3.11, 3.12, 3.13, etc.)
uv venv --python 3.13  # or --python 3.11, --python 3.12, etc.

# Install dependencies
uv pip install -e .
```

**Note:** If you encounter download timeouts when UV tries to fetch Python, use a Python version already installed on your system (see Step 3 for how to check installed versions).

### **Step 5: Install Ollama**

Download and install Ollama from https://ollama.ai

The application will install to `/Applications/Ollama.app` automatically.

### **Step 6: Launch AILab-Mac**

```bash
cd ~/Developer/AILab-Mac
./run_ai_env.sh
```

You should see the interactive menu system!

---

## 📦 **Installation for External Hard Drives**

This section is for users who want to run the AI Environment from an external hard drive (USB drive, external SSD, etc.) or want maximum portability across different Macs.

### **External Drive Setup**

The AI Environment uses a two-part setup:

1. **AILab-Mac** (this repository) - Contains the UV virtual environment, management interface, and tools
2. **AI_Environment** (optional) - Contains Ollama (portable) and AI models

---

### **Step 1: Prepare Your External Drive**

```bash
# Identify your external drive (it will be under /Volumes/)
ls /Volumes/

# Example: Your drive is named "MyDrive"
cd /Volumes/MyDrive

# Clone AILab-Mac
git clone <repository-url> AILab-Mac
cd AILab-Mac

# Make scripts executable
chmod +x run_ai_env.sh setup_python_env.sh
```

### **Step 2: Install UV (if not already installed)**

```bash
# Install UV globally (only needs to be done once per Mac)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### **Step 3: Create Virtual Environment on External Drive**

```bash
cd /Volumes/MyDrive/AILab-Mac

# Check which Python versions are available
python3 --version

# Create UV virtual environment with Python 3.11 or higher
# Use whichever version you have installed (3.11, 3.12, 3.13, etc.)
uv venv --python 3.13  # or --python 3.11, --python 3.12, etc.

# Install dependencies
uv pip install -e .
```

### **Step 4: Launch from External Drive**

```bash
cd /Volumes/MyDrive/AILab-Mac
./run_ai_env.sh
```

**Benefits of External Drive Setup:**
- ✅ Fully portable - move between different Macs
- ✅ Fast setup with UV (minutes instead of hours)
- ✅ Automatic detection via relative paths
- ✅ Easy backup - just copy the entire folder
- ✅ Consistent environment across machines
- ✅ No large conda installation needed

---

## 🎯 **Core Features**

### **1. Interactive Menu System**
The system provides a Python-based interactive menu (`activate_ai_env.py`) that serves as the central hub for all operations:

- **Full color-coded interface** - Easy-to-read menus with status indicators
- **Real-time status updates** - Shows running processes and environment state
- **Context-aware options** - Menu items adapt based on current system state
- **Keyboard navigation** - Simple number-based selection system
- **Native macOS Terminal integration** - Works with Terminal.app and iTerm2

### **2. Environment Management**
Manages UV virtual environments and Python installations:

- **Automatic UV detection** - Uses UV for fast Python environment management
- **Virtual environment activation** - Pre-configured Python environment with AI packages
- **PATH management** - Safe PATH manipulation with backup/restore capabilities
- **Environment validation** - Comprehensive checks for packages and dependencies
- **Fast dependency installation** - UV provides significantly faster package installation than conda

### **3. AI Model Management (Ollama)**
Complete integration with Ollama for local AI model hosting:

- **Model download** - Interactive selection from popular models or custom URLs
- **Model loading** - Automatic loading with Python usage examples
- **Model status checking** - View loaded and available models
- **Model deletion** - Storage space management
- **Help documentation** - Detailed guides for each model (phi, llama2, mistral, codellama)

### **4. Application Launchers**
One-click launching of development tools (macOS native):

- **Jupyter Lab** - Full sub-menu with server management (start, stop, status, custom ports)
- **VS Code** - Automatic workspace configuration with AI2025 environment
- **AI2025 Terminal** - Enhanced Terminal.app window with pre-activated environment
- **Finder** - Open Finder in project directory
- **Custom applications** - Extensible launcher system

### **5. Process Management**
Background process tracking and control:

- **Automatic tracking** - Monitors Ollama, Jupyter Lab, VS Code
- **Status display** - View all running processes with PIDs
- **Clean shutdown** - Stop all tracked processes on exit
- **Process persistence** - JSON-based storage for session recovery

### **6. Component Testing**
Comprehensive validation system with 9 different tests:

- **Directory structure** - Verifies AI Environment layout
- **UV installation** - Checks UV executable and version
- **Virtual environment** - Validates Python environment
- **Python packages** - Tests psutil, colorama, requests, numpy, pandas
- **Ollama server** - Optional AI server availability check
- **System integration** - PATH, environment variables, macOS commands
- **AI model system** - Model management functionality
- **Jupyter Lab system** - Server management functionality
- **Help documentation** - Model help files availability

---

## 🏗️ **Architecture**

### **Modular Design**
The system is split into focused, maintainable modules (all under 250 lines):

```
AILab-Mac/
├── run_ai_env.sh               # Main launcher script (bash)
├── setup_python_env.sh         # Environment setup script (bash)
├── src/
│   ├── activate_ai_env.py      # Main entry point and orchestration
│   ├── ai_menu_system.py       # Interactive menu display and navigation
│   ├── ai_action_handlers.py   # Menu action implementations
│   ├── ai_component_tester.py  # Comprehensive testing system
│   ├── ai_path_manager.py      # PATH and environment variable management
│   ├── ai_conda_manager.py     # Conda environment operations (macOS)
│   ├── ai_path_finder.py       # macOS-specific path detection
│   ├── ai_component_setup.py   # Component initialization
│   ├── ai_ollama_manager.py    # Ollama server management (macOS)
│   ├── ai_process_manager.py   # Background process tracking
│   ├── ai_jupyter_manager.py   # Jupyter Lab management
│   ├── ai_model_manager.py     # AI model management hub
│   ├── ai_model_downloader.py  # Model download operations
│   ├── ai_model_loader.py      # Model loading and usage instructions
│   ├── ai_document_viewer.py   # Markdown document viewer
│   ├── ai_update_manager.py    # System update functionality
│   ├── ai_vscode_config.py     # VS Code workspace configuration (macOS)
│   ├── ai_terminal_launcher.py # Terminal.app launcher (macOS)
│   ├── ai_app_launchers.py     # Application launchers (macOS)
│   └── ai_status_display.py    # Status information display
├── config/
│   ├── metadata.json           # System information and features
│   ├── expected_versions.json  # File version tracking
│   ├── install_config.json     # Package requirements
│   └── version_history.json    # Complete changelog
├── help/
│   ├── phi_2_7b.txt           # Phi 2.7B model documentation
│   ├── llama2_7b.txt          # Llama2 model documentation
│   ├── mistral_7b.txt         # Mistral model documentation
│   ├── codellama_7b.txt       # CodeLlama model documentation
│   └── gpt_oss_20b.txt        # GPT-OSS model documentation
└── version_config.json         # Main configuration with references
```

---

## 🔧 **macOS-Specific Features**

### **Path Detection**
- Automatically finds Ollama at `/Applications/Ollama.app/Contents/MacOS/ollama`
- Detects VS Code at `/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code`
- Searches for UV virtual environment:
  - `~/Developer/AILab-Mac/.venv` (standard location)
  - External drives: `/Volumes/*/AILab-Mac/.venv`
- Detects UV installation in system PATH

### **Terminal Integration**
- Launches new Terminal.app windows with custom profiles
- Pre-activates UV virtual environment in launched terminals
- Custom prompt: `[AILab-Terminal] directory $`
- Return-to-menu command available from spawned terminals

### **Application Support**
- **Ollama**: Uses standard macOS app installation
- **VS Code**: Integrates with macOS app bundle
- **Finder**: Opens directories in native Finder
- **Jupyter**: Launches in default web browser

---

## 📚 **Usage**

### **Starting the System**

```bash
cd ~/Developer/AILab-Mac
./run_ai_env.sh
```

### **Main Menu Options**

1. **Full Activation** - Activates UV virtual environment, starts Ollama, optionally loads AI model
2. **Restore Original PATH** - Deactivates virtual environment, restores system PATH
3. **Activate Virtual Environment** - Activates UV environment only
4. **Test All Components** - Runs comprehensive 9-test validation suite
5. **Setup Flask** - Installs Flask for web development
6. **Setup Ollama Server** - Starts Ollama AI model server
7. **Download AI Models** - Interactive model management sub-menu
8. **Run Environment Validation** - Checks for missing packages
9. **Launch Applications** - Opens Jupyter Lab, VS Code, or Terminal
10. **Background Processes** - Manage running processes
11. **Advanced Options** - Version info, updates, utilities
12. **Quit** - Exit menu (keeps processes running)
13. **Exit and Close All** - Stop all processes and clean shutdown

---

## 🆘 **Troubleshooting**

### **Common Issues**

**"Permission denied" when running ./run_ai_env.sh:**
```bash
# Make scripts executable
chmod +x run_ai_env.sh setup_python_env.sh
```

**"UV not found" errors:**
```bash
# Verify UV installation
which uv

# If not found, install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew
brew install uv
```

**"Virtual environment not found":**
```bash
# First check which Python versions you have installed
python3 --version
ls /usr/local/bin/python* 2>/dev/null | grep python3

# Create the virtual environment with an available Python version
cd ~/Developer/AILab-Mac
uv venv --python 3.13  # Use the version you have installed

# Install dependencies
uv pip install -e .
```

**"UV timeout when downloading Python" or "error sending request":**
```bash
# This happens when UV tries to download a Python version from GitHub
# Solution: Use a Python version already installed on your Mac

# Check installed Python versions
python3 --version
which python3.11 python3.12 python3.13

# Use an installed version instead
cd ~/Developer/AILab-Mac
uv venv --python 3.13  # or whichever version is installed

# If you need Python 3.11 specifically, install it first:
brew install python@3.11
uv venv --python 3.11
```

**"Ollama not found" errors:**
```bash
# Check if Ollama is installed
ls /Applications/Ollama.app

# If not found, download from https://ollama.ai
```

**"VS Code 'code' command not found":**
```bash
# Install code command from VS Code
# 1. Open VS Code
# 2. Press Cmd+Shift+P (Command Palette)
# 3. Type "Shell Command: Install 'code' command in PATH"
# 4. Press Enter

# Verify installation
which code
```

**External drive not detected:**
```bash
# Check if drive is mounted
ls /Volumes/

# Verify AI_Environment folder structure
ls /Volumes/YourDrive/AILab-Mac/AI_Environment/

# Run with verbose mode for debugging
./run_ai_env.sh --verbose
```

**Python packages missing:**
```bash
# Activate virtual environment
cd ~/Developer/AILab-Mac
source .venv/bin/activate

# Install missing packages
uv pip install psutil colorama requests numpy pandas jupyter jupyterlab

# Or reinstall all dependencies
uv pip install -e .

# Verify installation
python -c "import psutil, colorama, requests, numpy, pandas"
```

### **Apple Silicon vs Intel Macs**

The system works on both Apple Silicon (M1/M2/M3) and Intel Macs. UV automatically detects your architecture and downloads the appropriate Python version and packages.

Ollama and VS Code have universal binaries that work on both architectures.

### **Permissions Issues**

If you encounter permissions issues with Ollama or other applications:

```bash
# Grant necessary permissions in System Settings
# System Settings → Privacy & Security → Full Disk Access
# Add Terminal.app and/or the applications

# Or run with sudo (not recommended for regular use)
sudo ./run_ai_env.sh
```

---

## 🔄 **Updating the System**

### **Update from GitHub**

```bash
cd ~/Developer/AILab-Mac
git pull origin main

# Re-make scripts executable if needed
chmod +x run_ai_env.sh setup_python_env.sh
```

### **Update Python Packages**

```bash
cd ~/Developer/AILab-Mac
source .venv/bin/activate
uv pip install --upgrade psutil colorama requests numpy pandas jupyter jupyterlab
# Or update all dependencies
uv pip install -e . --upgrade
deactivate
```

### **Update Ollama Models**

From within the AILab menu system:
- Select "Download AI Models"
- Download newer versions of models
- Delete old versions to free space

---

## 📞 **Version Checking**

To verify your installation version:

```bash
# Cross-platform Python version checker
python check_versions.py
```

Expected output:
```
[SUCCESS] All files have correct versions (100%)
[INFO] Your AI Environment system is up to date!
```

---

## 🚀 **Portable Design**

The system is fully portable and uses **relative paths** throughout:

- **No hard-coded absolute paths**: All scripts detect their location dynamically
- **Auto-detection**: Finds Miniconda and applications wherever installed
- **External drive friendly**: Works from /Volumes/ with automatic detection
- **Multi-Mac usage**: Copy entire folder to different Macs
- **No system modifications**: Everything self-contained

This makes it ideal for:
- USB-based portable development environments
- Multi-Mac workflows
- Testing and demonstration
- Offline AI development
- Backup and migration

---

## 📋 **Manual Setup Checklist**

After cloning from GitHub, users must:

- [ ] Install Python 3.11 or higher: `brew install python@3.13` (or check if already installed with `python3 --version`)
- [ ] Make shell scripts executable: `chmod +x *.sh`
- [ ] Install UV (via curl or Homebrew)
- [ ] Create UV virtual environment: `uv venv --python 3.13` (or use any installed Python 3.11+)
- [ ] Install required Python packages: `uv pip install -e .`
- [ ] Install Ollama from https://ollama.ai
- [ ] (Optional) Install VS Code and the `code` command
- [ ] (Optional) Download AI models via Ollama

---

## 🔗 **Resources**

- **UV**: https://github.com/astral-sh/uv
- **Ollama**: https://ollama.ai
- **VS Code**: https://code.visualstudio.com/
- **Jupyter**: https://jupyter.org/

---

**AI Environment Python System v3.0.28 - macOS Edition**
**Advanced and Modular AI Development Environment Management System** 🚀
