# Quick Start Guide - AILab-Mac

Get up and running with AILab-Mac in 5 minutes!

> **Note:** This is the macOS version adapted from [https://github.com/rmisegal/AILab](https://github.com/rmisegal/AILab)

## Prerequisites

Before you begin, make sure you have:
- macOS 10.15 (Catalina) or later
- At least 5GB of free disk space
- Internet connection (for downloading components)

## Step 1: Clone the Repository

```bash
cd ~/Developer
git clone <repository-url> AILab-Mac
cd AILab-Mac
```

## Step 2: Make Scripts Executable

```bash
chmod +x run_ai_env.sh setup_python_env.sh check_prerequisites.sh
```

## Step 3: Check Prerequisites

Run the prerequisites checker to see what you need to install:

```bash
./check_prerequisites.sh
```

This will tell you exactly what's missing and how to install it.

## Step 4: Install Miniconda

If you don't have Miniconda installed:

```bash
# Download installer (choose your Mac type)
# For Apple Silicon (M1/M2/M3):
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh

# For Intel Macs:
# curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

# Install
bash Miniconda3-latest-MacOSX-arm64.sh

# Follow the prompts, accept license, choose install location
# Default location: ~/miniconda3 (recommended)
```

After installation, **restart your terminal** or run:

```bash
source ~/.bash_profile  # if using bash
# or
source ~/.zshrc        # if using zsh
```

## Step 5: Create AI2025 Environment

```bash
# Create environment
conda create -n AI2025 python=3.11 -y

# Activate environment
conda activate AI2025

# Install required packages
pip install psutil colorama requests numpy pandas jupyter jupyterlab

# Deactivate
conda deactivate
```

## Step 6: Install Ollama

1. Download Ollama from: https://ollama.ai
2. Open the downloaded .dmg file
3. Drag Ollama to Applications folder
4. Launch Ollama.app once (this installs CLI tools)
5. Close Ollama

## Step 7: (Optional) Install VS Code

1. Download from: https://code.visualstudio.com/
2. Install to Applications folder
3. Open VS Code
4. Press `Cmd+Shift+P` (Command Palette)
5. Type: "Shell Command: Install 'code' command in PATH"
6. Press Enter

## Step 8: Run AILab-Mac!

```bash
cd ~/Developer/AILab-Mac
./run_ai_env.sh
```

You should see the interactive menu!

## First-Time Menu Options

When you first run AILab-Mac, try these options in order:

1. **Option 4: Test All Components** - Verify everything is working
2. **Option 6: Setup Ollama Server** - Start the AI model server
3. **Option 7: Download AI Models** - Download your first AI model (try phi:2.7b for fastest download)
4. **Option 9: Launch Applications** - Try launching Jupyter Lab

## Common First-Run Issues

### "Permission denied" error
```bash
chmod +x run_ai_env.sh setup_python_env.sh
```

### "Miniconda not found"
Make sure you restarted your terminal after installing Miniconda

### "AI2025 environment not found"
Run: `conda create -n AI2025 python=3.11 -y`

### "Ollama not found"
Make sure you launched Ollama.app at least once after installing

## Need Help?

- Run: `./check_prerequisites.sh` to diagnose issues
- Check the full readme.md for detailed troubleshooting
- Make sure all prerequisites are installed correctly

## External Drive Setup

Want to run from an external drive? See the **Installation for External Hard Drives** section in readme.md

## Next Steps

Once everything is running:

1. Download AI models via the menu (Option 7)
2. Launch Jupyter Lab (Option 9 → 1)
3. Start coding in the AI2025 environment
4. Use the menu to manage background processes

Happy coding! 🚀
