# Ollama Git Commit Message Generator for Linux

A command-line tool that generates commit messages from Git diffs using Ollama’s `phi3.5` model running locally on `localhost:11434`. The script automatically handles dependency installation, model setup, and commit message generation.

---

## Installation

Since `brew` isn’t typically available on Linux, you’ll need to install Ollama manually. Follow these steps:

1. **Install Ollama**: Visit the [Ollama website](https://ollama.com) and follow the instructions for Linux installation.

2. **Download the `phi3.5` Model**: Once Ollama is installed and running, the script will automatically pull the `phi3.5` model if it’s not already available.

3. **Place the Script in Your `PATH`**: Move `ollamacommit` to a directory in your `PATH`, such as `/usr/local/bin`, to use it as a command.

---

## Usage

1. **Ensure Ollama is Running**: Start your local Ollama server on `localhost:11434`.
2. **Make the Script Executable**:
   ```bash
   chmod +x ollamacommit
   ```
3. **Stage Changes**:
   ```bash
   git add .
   ```
4. **Run the Script**:
   ```bash
   ./ollamacommit
   ```

---

## Notes

- **Python Requirements**: Ensure `pip` and `python3` are correctly set up on your Linux system. Use `pip3` if necessary.
- **Dependencies**: The script will install any missing Python packages (`requests`, `langchain_community`, `langchain_core`) automatically.
- **Model Download**: The script checks for the `phi3.5` model and will download it if not present.

This setup provides a seamless way to automate commit message generation with minimal setup on Linux.
