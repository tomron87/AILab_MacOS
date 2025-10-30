#!/bin/bash
# AI Environment Python Launcher v3.0.28 - macOS Version

# AI Environment Python Launcher v3.0.28
# First sets up the Python environment, then launches the Python system

SCRIPT_VERSION="3.0.28"
SCRIPT_DATE="2025-08-14"
VERBOSE_MODE=0

# Check for --verbose parameter
if [[ "$1" == "--verbose" ]] || [[ "$2" == "--verbose" ]]; then
    VERBOSE_MODE=1
fi

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] run_ai_env.sh v${SCRIPT_VERSION} (${SCRIPT_DATE}) starting"
fi

echo "================================================================"
echo "                AI Environment Python Launcher"
echo "                      Version ${SCRIPT_VERSION} (${SCRIPT_DATE})"
echo "================================================================"
echo ""

# Determine current directory (AI Environment directory)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
AI_ENV_PATH="${SCRIPT_DIR}"

# Navigate to AI Environment directory
cd "${AI_ENV_PATH}"

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Current directory: $(pwd)"
    echo "[VERBOSE] Checking for setup_python_env.sh"
fi

# Check if setup script exists
if [ ! -f "setup_python_env.sh" ]; then
    echo "[ERROR] setup_python_env.sh not found in ${AI_ENV_PATH}"
    echo "[ERROR] Please ensure all files are extracted correctly"
    echo "[INFO] Expected files:"
    echo "  - setup_python_env.sh"
    echo "  - src/activate_ai_env.py"
    echo "  - src/ai_*.py"
    exit 1
fi

# Step 1: Setup Python environment
echo "[INFO] Setting up Python environment"
if [ "$VERBOSE_MODE" -eq 1 ]; then
    source ./setup_python_env.sh --verbose
else
    source ./setup_python_env.sh
fi

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to setup Python environment"
    echo "[ERROR] Please check the error messages above"
    exit 1
fi

# Step 2: Check if Python environment is ready
if [ "$AI_ENV_READY" != "1" ]; then
    echo "[ERROR] Python environment setup incomplete"
    echo "[ERROR] AI_ENV_READY flag not set"
    if [ "$VERBOSE_MODE" -eq 1 ]; then
        echo "[VERBOSE] Environment variables:"
        echo "[VERBOSE] AI_ENV_READY=${AI_ENV_READY}"
        echo "[VERBOSE] AI_PYTHON_EXE=${AI_PYTHON_EXE}"
    fi
    exit 1
fi

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Python environment ready"
    echo "[VERBOSE] AI_PYTHON_EXE=${AI_PYTHON_EXE}"
fi

# Step 3: Check if activation script exists
if [ ! -f "src/activate_ai_env.py" ]; then
    echo "[ERROR] src/activate_ai_env.py not found"
    echo "Please ensure all Python files are in ${AI_ENV_PATH}/src"
    if [ "$VERBOSE_MODE" -eq 1 ]; then
        echo "[VERBOSE] Current directory contents:"
        ls -la
        echo "[VERBOSE] src directory contents:"
        ls -la src/
    fi
    exit 1
fi

# Step 4: Verify Python executable exists
if [ ! -f "${AI_PYTHON_EXE}" ]; then
    echo "[ERROR] Python executable not found at: ${AI_PYTHON_EXE}"
    echo "[ERROR] Please check your AI Environment installation"
    exit 1
fi

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Testing Python executable"
    "${AI_PYTHON_EXE}" --version
    if [ $? -ne 0 ]; then
        echo "[VERBOSE] Python test failed"
    else
        echo "[VERBOSE] Python test successful"
    fi
fi

# Step 5: Launch the Python activation system using the configured Python
echo "[INFO] Starting AI Environment Manager"
echo ""

if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] Launching: ${AI_PYTHON_EXE} src/activate_ai_env.py --verbose"
    "${AI_PYTHON_EXE}" src/activate_ai_env.py
else
    "${AI_PYTHON_EXE}" src/activate_ai_env.py
fi

# Step 6: Cleanup and exit
echo ""
echo "[INFO] AI Environment Manager closed"
if [ "$VERBOSE_MODE" -eq 1 ]; then
    echo "[VERBOSE] run_ai_env.sh v${SCRIPT_VERSION} completed"
fi
