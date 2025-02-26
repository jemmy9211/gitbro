# Ollama Git Commit Message Generator for Linux

A command-line tool that generates commit messages from Git diffs using Ollama's llama3.2 model running locally on `http://localhost:11434`. The script automates dependency installation, model setup, and commit message generation, making it seamless for Linux users.

## Installation

1. **Clone or Download the Project:**
   ```bash
   git clone https://github.com/yourusername/ollamacommit.git
   cd ollamacommit
   ```

2. **Ensure Ollama is Installed:**
   - Visit [Ollama's website](https://ollama.com) and follow the Linux installation instructions if Ollama is not already installed.

3. **Run the Installation Script:**
   ```bash
   ./install.sh
   ```
   - This script checks for Ollama, pulls the `llama3.2` model, sets up a virtual environment in `venv/`, and installs required Python packages (`requests`, `langchain`, `langchain_ollama`).

4. **(Optional) Add to PATH:**
   - To run `ollamacommit` globally without specifying the path, add the `bin/` directory to your PATH:
     ```bash
     export PATH=$PATH:/path/to/ollamacommit/bin
     ```
   - Add this line to your `~/.bashrc` or `~/.zshrc` for persistence.

## Usage

1. **Ensure Ollama is Running:**
   Start your local Ollama server:
   ```bash
   ollama serve
   ```
   Verify it's running at `http://localhost:11434`.

2. **Stage Changes:**
   ```bash
   git add .
   ```

3. **Generate and Commit:**
   Run the tool:
   ```bash
   ./bin/ollamacommit
   ```
   - Or, if added to PATH:
     ```bash
     ollamacommit
     ```
   - The script generates a commit message based on staged changes and commits them automatically.

## How It Works

1. The tool extracts the Git diff of staged changes using `git diff --cached`.
2. It sends this diff to a locally running llama3.2 model via Ollama's API.
3. The model is prompted to generate a concise, relevant commit message based on the code changes.
4. Users can adjust the "creativity" level by increasing the temperature parameter if they want more varied suggestions.
5. Once satisfied, the generated message is used to create a Git commit automatically.

## Notes

- **Python Requirements:** Ensure `python3` and `pip` are installed on your system. Use `pip3` if necessary.
- **Dependencies:** The installation script handles Python package installation within the project's virtual environment.
- **Model Download:** The `llama3.2` model is downloaded automatically if not present.
- **Troubleshooting:** If the tool fails, ensure Ollama is running and accessible at `http://localhost:11434`, and that changes are staged with `git add`.  
- **Creativity Control:** The tool allows incrementally increasing the "temperature" parameter (from 0.7 up to 1.0) to generate more creative commit messages when regenerating.

This setup provides an efficient way to automate commit message generation with minimal setup on Linux.

## Uninstallation

To remove the tool and its components:

1. Run the uninstallation script:
   ```bash
   ./uninstall.sh
   ```

2. The script will:
   - Remove the virtual environment
   - Optionally remove the llama3.2 model
   - Optionally remove Ollama completely

3. If you added the bin directory to PATH, remember to remove it from your `~/.bashrc` or `~/.zshrc`.

## Project Structure

- `install.sh`: Installation script that sets up dependencies and environment.
- `uninstall.sh`: Script to clean up installed components.
- `bin/ollamacommit`: Main executable script for generating and managing commit messages.
- `src/generate_message.py`: Python module that handles LLM integration and message generation.
- `venv/`: Virtual environment directory (created during installation).

## License

{{ Add license information here if applicable }}

