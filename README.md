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
   - The script generates a commit message based on staged changes.
   - You will then be presented with the generated message and options:
     1. Accept and commit: Uses the generated message to make the commit.
     2. Regenerate with more creativity: Increases the 'temperature' setting for the language model and generates a new message. This can result in more diverse and imaginative suggestions. The temperature resets after each commit or cancellation.
     3. Cancel and exit: Aborts the commit process.

## How It Works

1. The tool extracts the Git diff of staged changes using `git diff --cached`.
2. It sends this diff to a locally running llama3.2 model via Ollama's API.
3. The model is prompted to generate a concise, relevant commit message based on the code changes.
4. The user is then prompted to accept the message, regenerate it with increased creativity (temperature), or cancel.
5. If accepted, the generated message is used to create a Git commit.

## Notes

- **Python Requirements:** Ensure `python3` and `pip` are installed on your system. Use `pip3` if necessary.
- **Dependencies:** The installation script handles Python package installation within the project's virtual environment.
- **Model Download:** The `llama3.2` model is downloaded automatically if not present.
- **Troubleshooting:** If the tool fails, ensure Ollama is running and accessible at `http://localhost:11434`, and that changes are staged with `git add`.  

This setup provides an efficient way to generate commit messages with minimal setup on Linux, offering user control over the final message.

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

This project is licensed under the MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to report a bug, please feel free to open an issue or submit a pull request.

### Development
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

Please ensure your code adheres to good coding practices and include tests if applicable.

