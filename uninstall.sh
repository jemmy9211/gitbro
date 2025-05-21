#!/bin/bash

# Define the virtual environment path
VENV_PATH="venv"

echo "Starting Ollamacommit uninstallation process..."
echo "Note: Removing the Ollama application itself, if chosen, will likely require sudo privileges for some operations."

# Remove virtual environment if it exists
if [ -d "$VENV_PATH" ]; then
    echo -e "\nRemoving project virtual environment ($VENV_PATH)..."
    rm -rf "$VENV_PATH"
    echo "Project virtual environment removed successfully."
else
    echo -e "\nProject virtual environment ($VENV_PATH) not found. Skipping."
fi

# Ask if user wants to remove the llama3.2 model
read -p "Do you want to attempt to remove the llama3.2 model from Ollama? (y/N): " remove_model
if [[ $remove_model =~ ^[Yy]$ ]]; then
    echo -e "\nAttempting to remove llama3.2 model from Ollama..."
    if command -v ollama &> /dev/null; then
        if ollama rm llama3.2 &> /dev/null; then
            echo "Successfully initiated removal of llama3.2 model. Check 'ollama list' to confirm."
        else
            echo "Failed to remove llama3.2 model using 'ollama rm llama3.2'."
            echo "The model may not have been installed, or Ollama encountered an error."
            echo "You can check with 'ollama list' and attempt manual removal if needed."
        fi
    else
        echo "Ollama command not found. Cannot remove model."
        echo "Please ensure Ollama is installed and in your PATH if you wish to manage its models manually."
    fi
fi

# Ask if user wants to remove Ollama completely
read -p "Do you want to attempt to completely remove the Ollama application from your system? (This is a system-wide change) (y/N): " remove_ollama
if [[ $remove_ollama =~ ^[Yy]$ ]]; then
    echo -e "\nAttempting to remove the Ollama application (may require sudo for some commands)..."
    if command -v ollama &> /dev/null; then
        echo "Attempting to stop Ollama service (sudo may be required)..."
        if sudo systemctl stop ollama; then
            echo "Ollama service stopped."
        else
            echo "Warning: Failed to stop Ollama service. It might not have been running or you may lack sudo privileges."
        fi
        
        echo "Attempting to remove Ollama binary (sudo may be required)..."
        if sudo rm -f /usr/local/bin/ollama; then # -f to suppress error if not found
            echo "Ollama binary (/usr/local/bin/ollama) removed (if it existed)."
        else
            echo "Warning: Failed to remove Ollama binary. It might not be in /usr/local/bin or you may lack sudo privileges."
        fi
        
        echo "Attempting to remove Ollama user data (typically ~/.ollama)..."
        # This path is usually user-specific. If Ollama was run as root or installed system-wide, this path might differ or require sudo.
        if rm -rf ~/.ollama; then 
            echo "Ollama user data directory (~/.ollama) removed."
        else
            echo "Warning: Failed to remove Ollama user data directory (~/.ollama). Check permissions or if it exists."
            echo "If Ollama was run by root or installed for all users, you might need to manually remove /root/.ollama or other system paths."
        fi
        echo "Ollama application removal process attempted. Please verify manually, especially if you encountered warnings."
    else
        echo "Ollama command not found. Cannot perform automated Ollama application removal."
        echo "If Ollama is installed, you may need to follow official Ollama uninstallation instructions manually."
    fi
fi

echo -e "\nOllamacommit uninstallation process complete!"
