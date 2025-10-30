#!/usr/bin/env python3
"""
AI Path Finder - Finds AI_Environment on macOS
Shared utility for all AI Environment modules
"""

import os
from pathlib import Path
from typing import Optional


def find_ai_environment(verbose: bool = False) -> Optional[Path]:
    """
    Find AI_Environment installation on macOS.
    Searches for AI_Environment in standard Mac locations and external drives.

    Args:
        verbose: If True, print debug messages

    Returns:
        Path to AI_Environment or None if not found
    """
    # Get the current script's directory
    current_dir = Path(__file__).resolve().parent.parent

    # Check if AI_Environment exists relative to current location
    relative_paths = [
        current_dir / "AI_Environment",           # AILab-Mac/AI_Environment
        current_dir.parent / "AI_Environment",    # Parent directory
    ]

    for path in relative_paths:
        if path.exists() and path.is_dir():
            if (path / "Ollama").exists() or (path / "Miniconda").exists():
                if verbose:
                    print(f"[VERBOSE] Found AI_Environment at: {path}")
                return path

    # Check external drives (mounted under /Volumes/)
    volumes_path = Path("/Volumes")
    if volumes_path.exists():
        for volume in volumes_path.iterdir():
            if not volume.is_dir():
                continue

            # Skip system volumes
            if volume.name in ["Macintosh HD", "Preboot", "Recovery", "VM"]:
                continue

            # Check AILab-Mac/AI_Environment on external drive
            ai_lab_path = volume / "AILab-Mac" / "AI_Environment"
            if ai_lab_path.exists() and ai_lab_path.is_dir():
                if (ai_lab_path / "Ollama").exists() or (ai_lab_path / "Miniconda").exists():
                    if verbose:
                        print(f"[VERBOSE] Found AI_Environment at: {ai_lab_path}")
                    return ai_lab_path

            # Check AI_Environment directly on external drive
            ai_env_path = volume / "AI_Environment"
            if ai_env_path.exists() and ai_env_path.is_dir():
                if (ai_env_path / "Ollama").exists() or (ai_env_path / "Miniconda").exists():
                    if verbose:
                        print(f"[VERBOSE] Found AI_Environment at: {ai_env_path}")
                    return ai_env_path

    # Check standard Mac locations
    standard_paths = [
        Path.home() / "AI_Environment",
        Path.home() / "Developer" / "AILab-Mac" / "AI_Environment",
        Path("/opt/AI_Environment"),
    ]

    for path in standard_paths:
        if path.exists() and path.is_dir():
            if (path / "Ollama").exists() or (path / "Miniconda").exists():
                if verbose:
                    print(f"[VERBOSE] Found AI_Environment at: {path}")
                return path

    if verbose:
        print("[VERBOSE] AI_Environment not found")
    return None


def find_ollama() -> Optional[Path]:
    """
    Find Ollama installation on macOS.

    Returns:
        Path to ollama binary or None if not found
    """
    # Check standard Mac application
    mac_app = Path("/Applications/Ollama.app/Contents/MacOS/ollama")
    if mac_app.exists():
        return mac_app

    # Check if ollama is in PATH
    import shutil
    ollama_in_path = shutil.which("ollama")
    if ollama_in_path:
        return Path(ollama_in_path)

    # Check portable installation
    ai_env = find_ai_environment()
    if ai_env:
        portable_ollama = ai_env / "Ollama" / "ollama"
        if portable_ollama.exists():
            return portable_ollama

    return None


def find_vscode() -> Optional[Path]:
    """
    Find VS Code installation on macOS.

    Returns:
        Path to 'code' command or None if not found
    """
    # Check standard Mac application
    mac_app = Path("/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code")
    if mac_app.exists():
        return mac_app

    # Check if code is in PATH
    import shutil
    code_in_path = shutil.which("code")
    if code_in_path:
        return Path(code_in_path)

    # Check user Applications folder
    user_app = Path.home() / "Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
    if user_app.exists():
        return user_app

    return None


def find_miniconda() -> Optional[Path]:
    """
    Find Miniconda installation on macOS.

    Returns:
        Path to miniconda root directory or None if not found
    """
    # Check portable installation first
    ai_env = find_ai_environment()
    if ai_env:
        portable_conda = ai_env / "Miniconda"
        if (portable_conda / "bin" / "conda").exists():
            return portable_conda

    # Check standard Mac locations
    conda_locations = [
        Path.home() / "miniconda3",
        Path.home() / "opt" / "miniconda3",
        Path("/opt/miniconda3"),
        Path.home() / "anaconda3",
        Path.home() / "opt" / "anaconda3",
        Path("/opt/anaconda3"),
    ]

    for location in conda_locations:
        if (location / "bin" / "conda").exists():
            return location

    # Check if conda is in PATH
    import shutil
    conda_in_path = shutil.which("conda")
    if conda_in_path:
        # Get conda root by going up from bin/conda
        conda_path = Path(conda_in_path).parent.parent
        return conda_path

    return None


def main():
    """Test path finder"""
    print("=== macOS Path Finder Test ===\n")

    print("Searching for AI_Environment...")
    ai_env_path = find_ai_environment(verbose=True)
    if ai_env_path:
        print(f"✅ Found: {ai_env_path}")
    else:
        print("❌ Not found")

    print("\nSearching for Ollama...")
    ollama_path = find_ollama()
    if ollama_path:
        print(f"✅ Found: {ollama_path}")
    else:
        print("❌ Not found")

    print("\nSearching for VS Code...")
    vscode_path = find_vscode()
    if vscode_path:
        print(f"✅ Found: {vscode_path}")
    else:
        print("❌ Not found")

    print("\nSearching for Miniconda...")
    conda_path = find_miniconda()
    if conda_path:
        print(f"✅ Found: {conda_path}")
    else:
        print("❌ Not found")


if __name__ == "__main__":
    main()
