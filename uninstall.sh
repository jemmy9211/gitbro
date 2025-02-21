#!/bin/bash

# Define the virtual environment path
VENV_PATH="venv"

echo "Starting uninstallation process..."

# Remove virtual environment if it exists
if [ -d "$VENV_PATH" ]; then
    echo "Removing virtual environment..."
    rm -rf "$VENV_PATH"
    echo "Virtual environment removed successfully."
else
    echo "Virtual environment not found."
fi

# Ask if user wants to remove the llama3.2 model
read -p "Do you want to remove the llama3.2 model from Ollama? (y/N): " remove_model
if [[ $remove_model =~ ^[Yy]$ ]]; then
    if command -v ollama &> /dev/null; then
        echo "Removing llama3.2 model..."
        ollama rm llama3.2
        echo "llama3.2 model removed successfully."
    else
        echo "Ollama is not installed or not in PATH."
    fi
fi

# Ask if user wants to remove Ollama completely
read -p "Do you want to completely remove Ollama? (y/N): " remove_ollama
if [[ $remove_ollama =~ ^[Yy]$ ]]; then
    if command -v ollama &> /dev/null; then
        echo "Removing Ollama..."
        sudo systemctl stop ollama
        sudo rm -rf /usr/local/bin/ollama
        sudo rm -rf ~/.ollama
        echo "Ollama removed successfully."
    else
        echo "Ollama is not installed or not in PATH."
    fi
fi

echo "Uninstallation complete!"
