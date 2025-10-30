#!/bin/bash
# Setup Python Environment for AI Environment Manager v3.0.28 - macOS Version

# Setup Python Environment for AI Environment Manager v3.0.28
# This script prepares the environment before running Python code

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
echo "                   Preparing for AI Manager"
echo "================================================================"
echo ""

# Define paths - use current script location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
AI_ENV_PATH="${SCRIPT_DIR}"

# Search for Miniconda installation
CONDA_PATH=""

# 1. Check relative path (./Miniconda)
if [ -f "${AI_ENV_PATH}/Miniconda/bin/conda" ]; then
    CONDA_PATH="${AI_ENV_PATH}/Miniconda"
    if [ "$VERBOSE_MODE" -eq 1 ]; then
        echo "[VERBOSE] Found Miniconda at: ${AI_ENV_PATH}/Miniconda"
    fi
fi

# 2. Check AI_Environment subfolder
if [ -z "$CONDA_PATH" ] && [ -f "${AI_ENV_PATH}/AI_Environment/Miniconda/bin/conda" ]; then
    CONDA_PATH="${AI_ENV_PATH}/AI_Environment/Miniconda"
    if [ "$VERBOSE_MODE" -eq 1 ]; then
        echo "[VERBOSE] Found Miniconda at: ${AI_ENV_PATH}/AI_Environment/Miniconda"
    fi
fi

# 3. Try to detect from PATH environment variable
if [ -z "$CONDA_PATH" ]; then
    CONDA_EXE_PATH=$(which conda 2>/dev/null)
    if [ -n "$CONDA_EXE_PATH" ]; then
        # Extract conda root directory (go up 2 levels from bin/conda)
        EXTRACTED_PATH=$(cd "$(dirname "$CONDA_EXE_PATH")/.." && pwd)
        if [ -f "${EXTRACTED_PATH}/bin/conda" ]; then
            CONDA_PATH="${EXTRACTED_PATH}"
            if [ "$VERBOSE_MODE" -eq 1 ]; then
                echo "[VERBOSE] Detected Miniconda in PATH at: ${EXTRACTED_PATH}"
            fi
        fi
    fi
fi

# 4. Check common system-wide installation locations as fallback
if [ -z "$CONDA_PATH" ]; then
    POSSIBLE_PATHS=(
        "$HOME/miniconda3"
        "$HOME/opt/miniconda3"
        "/opt/miniconda3"
        "$HOME/anaconda3"
        "$HOME/opt/anaconda3"
        "/opt/anaconda3"
    )

    for path in "${POSSIBLE_PATHS[@]}"; do
        if [ -f "${path}/bin/conda" ]; then
            CONDA_PATH="${path}"
            if [ "$VERBOSE_MODE" -eq 1 ]; then
                echo "[VERBOSE] Found Miniconda at: ${path}"
            fi
            break
        fi
    done
fi

CONDA_ENV_PATH="${CONDA_PATH}/envs/AI2025"
PYTHON_EXE="${CONDA_ENV_PATH}/bin/python"

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] AI_ENV_PATH=${AI_ENV_PATH}"
    echo "[VERBOSE] CONDA_PATH=${CONDA_PATH}"
    echo "[VERBOSE] CONDA_ENV_PATH=${CONDA_ENV_PATH}"
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

# Check if Miniconda exists
if [ ! -d "${CONDA_PATH}" ]; then
    echo "[ERROR] Miniconda not found at ${CONDA_PATH}"
    echo "Please ensure Miniconda is installed in the AI Environment"
    echo ""
    echo "To install Miniconda on macOS:"
    echo "  1. Download from: https://docs.conda.io/en/latest/miniconda.html"
    echo "  2. Install to: ${AI_ENV_PATH}/Miniconda (for portability)"
    echo "     OR install system-wide to ~/miniconda3"
    return 1 2>/dev/null || exit 1
fi
echo "[OK] Miniconda installation found"

# Check if AI2025 environment exists
if [ ! -d "${CONDA_ENV_PATH}" ]; then
    echo "[ERROR] AI2025 conda environment not found at ${CONDA_ENV_PATH}"
    echo "Please ensure the AI2025 environment is created"
    echo ""
    echo "To create the AI2025 environment:"
    echo "  conda create -n AI2025 python=3.11 -y"
    echo "  conda activate AI2025"
    echo "  pip install psutil colorama requests numpy pandas"
    return 1 2>/dev/null || exit 1
fi
echo "[OK] AI2025 conda environment found"

# Check if Python executable exists
if [ ! -f "${PYTHON_EXE}" ]; then
    echo "[ERROR] Python executable not found at ${PYTHON_EXE}"
    echo "Please ensure Python is installed in the AI2025 environment"
    return 1 2>/dev/null || exit 1
fi
echo "[OK] Python executable found"

echo ""
echo "[*] Step 2: Setting up Python environment paths"
echo "----------------------------------------------------------------"

# Set conda and Python paths (macOS structure uses bin instead of Scripts)
CONDA_PATHS="${CONDA_ENV_PATH}/bin:${CONDA_PATH}/bin:${CONDA_PATH}/condabin"

# Get current PATH and prepend conda paths
export PATH="${CONDA_PATHS}:${PATH}"

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] CONDA_PATHS=${CONDA_PATHS}"
    echo "[VERBOSE] Updated PATH (first 100 chars): ${PATH:0:100}..."
fi

echo "[OK] Python environment paths configured"

echo ""
echo "[*] Step 3: Activating conda environment"
echo "----------------------------------------------------------------"

# Initialize conda for current shell session
if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Initializing conda for current session"
fi

# Source conda.sh to enable conda command in this shell
if [ -f "${CONDA_PATH}/etc/profile.d/conda.sh" ]; then
    source "${CONDA_PATH}/etc/profile.d/conda.sh"
else
    echo "[WARNING] conda.sh not found, trying alternative initialization"
    # Alternative: add conda to PATH and set up basic conda functionality
    export CONDA_EXE="${CONDA_PATH}/bin/conda"
    export CONDA_PYTHON_EXE="${CONDA_PATH}/bin/python"
fi

# Activate AI2025 environment
if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Activating AI2025 environment"
fi

conda activate AI2025 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] Standard activation failed, using manual setup"
    export CONDA_DEFAULT_ENV="AI2025"
    export CONDA_PREFIX="${CONDA_ENV_PATH}"
    export PATH="${CONDA_ENV_PATH}/bin:${PATH}"
else
    echo "[OK] AI2025 environment activated"
fi

echo ""
echo "[*] Step 4: Verifying Python setup"
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

# Test conda command
if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Testing conda command"
fi

conda --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[WARNING] Conda command not available"
else
    CONDA_VERSION=$(conda --version 2>&1 | awk '{print $2}')
    echo "[OK] Conda ${CONDA_VERSION} ready"
fi

echo ""
echo "[*] Step 5: Checking required Python packages"
echo "----------------------------------------------------------------"

# Check for required packages
if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Checking psutil package"
fi

"${PYTHON_EXE}" -c "import psutil" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[INFO] Installing psutil package"
    "${PYTHON_EXE}" -m pip install psutil >/dev/null 2>&1
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
    "${PYTHON_EXE}" -m pip install colorama >/dev/null 2>&1
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
echo "Environment: AI2025 (Conda)"
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
export CONDA_DEFAULT_ENV="AI2025"
export CONDA_PREFIX="${CONDA_ENV_PATH}"

return 0 2>/dev/null || exit 0
