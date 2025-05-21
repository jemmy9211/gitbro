#!/bin/bash

# Define the virtual environment path within the project
VENV_PATH="venv"

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# 0. Check if Git is installed
if ! command_exists git; then
    echo "Error: git command not found. Git is required to use this tool."
    exit 1
fi

# 1. Check if Ollama is installed
if ! command_exists ollama; then
    echo "Ollama is not installed. Installing Ollama requires manual setup."
    echo "Please visit https://ollama.com and follow the Linux installation instructions."
    exit 1
else
    echo "Ollama is already installed."
fi

# 2. Check if the llama3.2 model is installed in Ollama
if ! ollama list | grep -q "llama3.2"; then
    echo "Downloading the llama3.2 model for Ollama..."
    if ! ollama pull llama3.2; then
        echo "Failed to download llama3.2 model. Please try again."
        exit 1
    fi
else
    echo "llama3.2 model is already installed in Ollama."
fi

# Check and install python3-venv if not present
if ! dpkg -l | grep -q python3-venv; then
    echo "Python3 venv package is not installed. Attempting to install..."
    if command_exists apt; then
        echo "Installing python3-venv using apt..."
        # Try installation without updating first
        if ! sudo apt install -y python3-venv; then
            echo "Initial installation attempt failed. Trying with update..."
            # If that fails, try updating and installing
            if ! sudo apt update && sudo apt install -y python3-venv; then
                echo "Error: Failed to install python3-venv even after 'apt update'."
                echo "This might be due to issues with your package manager configuration (e.g., broken or outdated sources)."
                echo "Please try to resolve these issues manually. For example, you might need to:"
                echo "  1. Check for and remove problematic source files (e.g., in /etc/apt/sources.list.d/)."
                echo "  2. Run 'sudo apt update' to refresh your package lists."
                echo "  3. Then try 'sudo apt install python3-venv' again."
                exit 1
            fi
        fi
        echo "python3-venv installed successfully."
    else
        echo "Warning: This system doesn't seem to use 'apt' package manager."
        echo "Please ensure python3-venv (or equivalent) is installed manually for your system to proceed."
        exit 1
    fi
fi

# 3. Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating a virtual environment at $VENV_PATH..."
    python3 -m venv "$VENV_PATH"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please ensure Python 3 and venv are installed."
        exit 1
    fi
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# 4. Install required Python packages from requirements.txt
echo "Installing Python packages from requirements.txt in the virtual environment..."
if ! pip install -r requirements.txt; then
    echo "Failed to install packages from requirements.txt. Please check your virtual environment setup and requirements.txt."
    deactivate
    exit 1
fi
echo "Python packages installed successfully from requirements.txt."

# 5. Ensure the ollamacommit script is in bin/ and executable
if [ ! -f "bin/ollamacommit" ]; then
    echo "Error: bin/ollamacommit not found. Please ensure the project structure is intact."
    deactivate
    exit 1
fi

if ! chmod +x "bin/ollamacommit"; then
    echo "Failed to make bin/ollamacommit executable. Please check your permissions."
    deactivate
    exit 1
fi

# Deactivate the virtual environment
deactivate

# Print success message
echo "Installation complete! You can now use './bin/ollamacommit' to generate commit messages."
echo "To run it globally, add the bin directory to your PATH:"
echo "  export PATH=\$PATH:$(pwd)/bin"
echo "Ensure that your local Ollama API server is running at http://localhost:11434."