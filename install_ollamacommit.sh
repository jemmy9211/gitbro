#!/bin/bash

# Define the installation path
INSTALL_PATH="/usr/local/bin/ollamacommit"

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# 1. Check if Ollama is installed
if ! command_exists ollama; then
    echo "Ollama is not installed. Installing Ollama..."
    # For Linux, direct users to install Ollama manually if there's no automated installer
    echo "Please install Ollama manually by visiting https://ollama.com and follow the Linux installation instructions."
    exit 1
else
    echo "Ollama is already installed."
fi

# 2. Check if the phi3.5 model is installed in Ollama
if ! ollama list | grep -q "llama3.2"; then
    echo "Downloading the llama3.2 model for Ollama..."
    ollama pull llama3.2 || { echo "Failed to download llama3.2 model. Please try again."; exit 1; }
else
    echo "llama3.2 model is already installed in Ollama."
fi

# 3. Check and install required Python packages
REQUIRED_PACKAGES=("requests" "langchain" "langchain_ollama")

echo "Checking for required Python packages..."
pip install requests
pip install langchain
pip install langchain_ollama


# 4. Copy the commit message generation script to the installation path
echo "Copying the ollamacommit script to $INSTALL_PATH..."
cp ollamacommit.sh "$INSTALL_PATH"

# 5. Make the script executable
chmod +x "$INSTALL_PATH"

# Print success message
echo "Installation complete! You can now use 'ollamacommit' as a command."
echo "Ensure that your local Ollama API server is running at http://localhost:11434."
