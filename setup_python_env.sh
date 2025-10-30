#!/bin/bash
# Setup Python Environment for AI Environment Manager v3.0.28 - macOS Version with UV
# This script prepares the UV environment before running Python code

SCRIPT_VERSION="3.0.28"
SCRIPT_DATE="2025-08-14"
VERBOSE_MODE=0

# Check for --verbose parameter
if [[ "$1" == "--verbose" ]] || [[ "$2" == "--verbose" ]]; then
    VERBOSE_MODE=1
fi

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] setup_python_env.sh v${SCRIPT_VERSION} (${SCRIPT_DATE}) starting"
fi

echo "================================================================"
echo "                  Python Environment Setup"
echo "                   Version ${SCRIPT_VERSION} (${SCRIPT_DATE})"
echo "                   Preparing for AI Manager (UV)"
echo "================================================================"
echo ""

# Define paths - use current script location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
AI_ENV_PATH="${SCRIPT_DIR}"

# UV virtual environment path
VENV_PATH="${AI_ENV_PATH}/.venv"
PYTHON_EXE="${VENV_PATH}/bin/python"

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] AI_ENV_PATH=${AI_ENV_PATH}"
    echo "[VERBOSE] VENV_PATH=${VENV_PATH}"
    echo "[VERBOSE] PYTHON_EXE=${PYTHON_EXE}"
fi

echo "[*] Step 1: Checking AI Environment structure"
echo "----------------------------------------------------------------"

# Check if AI Environment exists
if [ ! -d "${AI_ENV_PATH}" ]; then
    echo "[ERROR] AI Environment not found at ${AI_ENV_PATH}"
    echo "Please ensure the AI Environment is installed correctly"
    return 1 2>/dev/null || exit 1
fi
echo "[OK] AI Environment directory found"

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "[ERROR] UV is not installed"
    echo "Please install UV first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "Or on macOS with Homebrew:"
    echo "  brew install uv"
    return 1 2>/dev/null || exit 1
fi
echo "[OK] UV is installed"

if [ "$VERBOSE_MODE" -eq 1 ]; then
    UV_VERSION=$(uv --version 2>&1)
    echo "[VERBOSE] UV version: ${UV_VERSION}"
fi

echo ""
echo "[*] Step 2: Setting up Python virtual environment"
echo "----------------------------------------------------------------"

# Check if virtual environment exists, create if not
if [ ! -d "${VENV_PATH}" ]; then
    echo "[INFO] Creating UV virtual environment"
    cd "${AI_ENV_PATH}"
    uv venv --python 3.11
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create UV virtual environment"
        return 1 2>/dev/null || exit 1
    fi
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

# Check if Python executable exists
if [ ! -f "${PYTHON_EXE}" ]; then
    echo "[ERROR] Python executable not found at ${PYTHON_EXE}"
    echo "Please ensure the virtual environment was created correctly"
    return 1 2>/dev/null || exit 1
fi
echo "[OK] Python executable found"

echo ""
echo "[*] Step 3: Installing dependencies"
echo "----------------------------------------------------------------"

# Install dependencies using UV
cd "${AI_ENV_PATH}"
if [ -f "pyproject.toml" ]; then
    echo "[INFO] Installing dependencies from pyproject.toml"
    uv pip install -e .
    if [ $? -ne 0 ]; then
        echo "[WARNING] Failed to install some dependencies"
    else
        echo "[OK] Dependencies installed"
    fi
else
    echo "[WARNING] pyproject.toml not found, installing core packages"
    uv pip install psutil colorama requests numpy pandas jupyter jupyterlab
    if [ $? -ne 0 ]; then
        echo "[WARNING] Failed to install some packages"
    else
        echo "[OK] Core packages installed"
    fi
fi

echo ""
echo "[*] Step 4: Activating virtual environment"
echo "----------------------------------------------------------------"

# Activate virtual environment
source "${VENV_PATH}/bin/activate"
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    return 1 2>/dev/null || exit 1
fi
echo "[OK] Virtual environment activated"

echo ""
echo "[*] Step 5: Verifying Python setup"
echo "----------------------------------------------------------------"

# Test Python executable
if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Testing Python executable: ${PYTHON_EXE}"
fi

"${PYTHON_EXE}" --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[ERROR] Python executable test failed"
    return 1 2>/dev/null || exit 1
fi

# Get Python version
PYTHON_VERSION=$("${PYTHON_EXE}" --version 2>&1 | awk '{print $2}')
echo "[OK] Python ${PYTHON_VERSION} ready"

echo ""
echo "[*] Step 6: Checking required Python packages"
echo "----------------------------------------------------------------"

# Check for required packages
if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Checking psutil package"
fi

"${PYTHON_EXE}" -c "import psutil" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[INFO] Installing psutil package"
    uv pip install psutil >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "[WARNING] Failed to install psutil"
    else
        echo "[OK] psutil package installed"
    fi
else
    echo "[OK] psutil package available"
fi

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Checking colorama package"
fi

"${PYTHON_EXE}" -c "import colorama" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[INFO] Installing colorama package"
    uv pip install colorama >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "[WARNING] Failed to install colorama"
    else
        echo "[OK] colorama package installed"
    fi
else
    echo "[OK] colorama package available"
fi

echo ""
echo "================================================================"
echo "                 PYTHON ENVIRONMENT READY"
echo "================================================================"
echo ""
echo "Environment: UV Virtual Environment"
echo "Python: ${PYTHON_VERSION}"
echo "Location: ${AI_ENV_PATH}"
echo ""
echo "[*] Python environment is now configured and ready"
echo "[*] You can now run Python scripts with full AI Environment support"
echo ""

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Exporting environment variables"
    echo "[VERBOSE] AI_PYTHON_EXE=${PYTHON_EXE}"
    echo "[VERBOSE] AI_ENV_READY=1"
fi

# Export environment variables for calling script
export AI_PYTHON_EXE="${PYTHON_EXE}"
export AI_ENV_READY="1"
export AI_ENV_PATH="${AI_ENV_PATH}"
export VIRTUAL_ENV="${VENV_PATH}"

return 0 2>/dev/null || exit 0
