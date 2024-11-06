#!/bin/bash

# Define the installation path
INSTALL_PATH="/usr/local/bin/ollamacommit"

# Copy the commit message generation script to the installation path
cp ollamacommit.sh "$INSTALL_PATH"

# Make the script executable
chmod +x "$INSTALL_PATH"

# Print success message
echo "Installation complete! You can now use 'ollamacommit' as a command."
echo "Ensure that your local Ollama API server is running at http://localhost:11434."

