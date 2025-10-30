#!/bin/bash
# AI Environment Prerequisites Checker for macOS
# This script checks if all required components are installed

echo "================================================================"
echo "        AI Environment Prerequisites Checker - macOS"
echo "================================================================"
echo ""

ISSUES_FOUND=0

# Check 1: Python 3
echo "[1/6] Checking Python 3..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "  ✅ Python 3 found: ${PYTHON_VERSION}"
else
    echo "  ❌ Python 3 not found"
    echo "     Install with: brew install python3"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi
echo ""

# Check 2: Conda/Miniconda
echo "[2/6] Checking Conda/Miniconda..."
if command -v conda &> /dev/null; then
    CONDA_VERSION=$(conda --version 2>&1 | awk '{print $2}')
    CONDA_PATH=$(which conda)
    echo "  ✅ Conda found: ${CONDA_VERSION}"
    echo "     Location: ${CONDA_PATH}"

    # Check for AI2025 environment
    if conda env list | grep -q "AI2025"; then
        echo "  ✅ AI2025 environment found"
    else
        echo "  ⚠️  AI2025 environment not found"
        echo "     Create with: conda create -n AI2025 python=3.11 -y"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo "  ❌ Conda/Miniconda not found"
    echo "     Download from: https://docs.conda.io/en/latest/miniconda.html"
    echo "     Recommended install location: ~/miniconda3"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi
echo ""

# Check 3: Ollama
echo "[3/6] Checking Ollama..."
if [ -d "/Applications/Ollama.app" ]; then
    echo "  ✅ Ollama.app found in /Applications"

    # Check if ollama command is available
    if command -v ollama &> /dev/null; then
        echo "  ✅ ollama command available in PATH"
    else
        echo "  ⚠️  ollama command not in PATH"
        echo "     Run Ollama.app once to install CLI tools"
    fi
else
    echo "  ❌ Ollama not found"
    echo "     Download from: https://ollama.ai"
    echo "     Install to: /Applications/Ollama.app"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi
echo ""

# Check 4: VS Code
echo "[4/6] Checking VS Code..."
if [ -d "/Applications/Visual Studio Code.app" ]; then
    echo "  ✅ VS Code found in /Applications"

    # Check if code command is available
    if command -v code &> /dev/null; then
        echo "  ✅ 'code' command available in PATH"
    else
        echo "  ⚠️  'code' command not in PATH"
        echo "     Install via: VS Code → Command Palette (⌘⇧P) → 'Shell Command: Install code command in PATH'"
    fi
else
    echo "  ⚠️  VS Code not found (optional)"
    echo "     Download from: https://code.visualstudio.com/"
fi
echo ""

# Check 5: Script Permissions
echo "[5/6] Checking script permissions..."
if [ -x "run_ai_env.sh" ] && [ -x "setup_python_env.sh" ]; then
    echo "  ✅ Shell scripts are executable"
else
    echo "  ❌ Shell scripts are not executable"
    echo "     Fix with: chmod +x run_ai_env.sh setup_python_env.sh"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi
echo ""

# Check 6: Required Python packages (if conda is available)
echo "[6/6] Checking Python packages..."
if command -v conda &> /dev/null && conda env list | grep -q "AI2025"; then
    # Activate AI2025 and check packages
    eval "$(conda shell.bash hook)"
    conda activate AI2025 2>/dev/null

    PACKAGES=("psutil" "colorama" "requests" "numpy" "pandas")
    ALL_PACKAGES_FOUND=true

    for package in "${PACKAGES[@]}"; do
        if python3 -c "import ${package}" 2>/dev/null; then
            echo "  ✅ ${package} installed"
        else
            echo "  ❌ ${package} not installed"
            ALL_PACKAGES_FOUND=false
        fi
    done

    if [ "$ALL_PACKAGES_FOUND" = false ]; then
        echo ""
        echo "  Install missing packages with:"
        echo "     conda activate AI2025"
        echo "     pip install psutil colorama requests numpy pandas jupyter jupyterlab"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    conda deactivate 2>/dev/null
else
    echo "  ⚠️  Cannot check packages (AI2025 environment not found)"
fi
echo ""

# Summary
echo "================================================================"
if [ $ISSUES_FOUND -eq 0 ]; then
    echo "  ✅ All prerequisites are satisfied!"
    echo "  You can now run: ./run_ai_env.sh"
else
    echo "  ⚠️  ${ISSUES_FOUND} issue(s) found"
    echo "  Please resolve the issues above before running AILab-Mac"
fi
echo "================================================================"
echo ""

exit $ISSUES_FOUND
