#!/bin/bash

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
if ! ollama list | grep -q "phi3.5"; then
    echo "Downloading the phi3.5 model for Ollama..."
    ollama pull phi3.5 || { echo "Failed to download phi3.5 model. Please try again."; exit 1; }
else
    echo "phi3.5 model is already installed in Ollama."
fi

# 3. Check and install required Python packages
REQUIRED_PACKAGES=("requests" "langchain_community" "langchain_core")

echo "Checking for required Python packages..."
for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import ${package}" &> /dev/null; then
        echo "Installing missing package: ${package}"
        pip install "$package" || { echo "Failed to install $package. Exiting."; exit 1; }
    else
        echo "Package ${package} is already installed."
    fi
done

# 4. Run Python script to generate the commit message and automatically commit
commit_message=$(python3 - <<END
import subprocess
import requests
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Configure LLM with local Ollama instance
llm = Ollama(model="phi3.5", base_url="http://localhost:11434")
prompt = ChatPromptTemplate.from_messages([
    ("system", "Your task is to write a concise commit message\
        according to a given code diff. Your output should only be\
        the commit message with no other information."),
    ("user", "Code Diff: {query_diff} Commit Message:")
])
chain = prompt | llm

def get_git_diff():
    # Get the Git diff of staged changes
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return result.stdout

def generate_commit_message(diff):
    # Get response from LLM
    rsp = chain.invoke({
        "query_diff": diff
    })
    return rsp

if __name__ == "__main__":
    git_diff = get_git_diff()
    if not git_diff:
        print("No changes staged for commit.")
        exit(1)  # Exit with an error code if there are no staged changes
    else:
        commit_message = generate_commit_message(git_diff)
        print(commit_message)  # Print the commit message to be captured by the shell
END
)

# Check if the commit message was successfully generated
if [ -z "$commit_message" ]; then
    echo "Failed to generate a commit message. Please try again."
    exit 1
fi

# Automatically commit the changes with the generated message
git commit -m "$commit_message"
