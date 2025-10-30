#!/bin/bash
# AI Environment Prerequisites Checker for macOS (UV Version)
# This script checks if all required components are installed

echo "================================================================"
echo "   AI Environment Prerequisites Checker - macOS (UV Version)"
echo "================================================================"
echo ""

ISSUES_FOUND=0

# Check 1: UV
echo "[1/6] Checking UV..."
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version 2>&1)
    echo "  ✅ UV found: ${UV_VERSION}"
else
    echo "  ❌ UV not found"
    echo "     Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "     Or via Homebrew: brew install uv"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi
echo ""

# Check 2: UV Virtual Environment
echo "[2/6] Checking UV Virtual Environment..."
if [ -d ".venv" ]; then
    echo "  ✅ UV virtual environment found at .venv"

    # Check if Python executable exists in venv
    if [ -f ".venv/bin/python" ]; then
        VENV_PYTHON_VERSION=$(.venv/bin/python --version 2>&1 | awk '{print $2}')
        echo "  ✅ Python ${VENV_PYTHON_VERSION} in virtual environment"
    else
        echo "  ⚠️  Python executable not found in virtual environment"
        echo "     Recreate with: uv venv --python 3.11"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo "  ❌ UV virtual environment not found"
    echo "     Create with: uv venv --python 3.11"
    echo "     Then install dependencies: uv pip install -e ."
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

# Check 6: Required Python packages (if venv is available)
echo "[6/6] Checking Python packages..."
if [ -f ".venv/bin/python" ]; then
    PACKAGES=("psutil" "colorama" "requests" "numpy" "pandas")
    ALL_PACKAGES_FOUND=true

    for package in "${PACKAGES[@]}"; do
        if .venv/bin/python -c "import ${package}" 2>/dev/null; then
            echo "  ✅ ${package} installed"
        else
            echo "  ❌ ${package} not installed"
            ALL_PACKAGES_FOUND=false
        fi
    done

    if [ "$ALL_PACKAGES_FOUND" = false ]; then
        echo ""
        echo "  Install missing packages with:"
        echo "     source .venv/bin/activate"
        echo "     uv pip install -e ."
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo "  ⚠️  Cannot check packages (virtual environment not found)"
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
